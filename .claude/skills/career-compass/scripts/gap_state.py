"""gap_state.py — deterministic gap-lifecycle reconciliation.

`reconcile_assessments` is a PURE function: it does not import tracker_io.py
or report_state.py, and performs no I/O. Callers load profile.yaml, the
prior report's `gap_assessments`, and tracker CSV rows themselves (via
profile_io / report_state / tracker_io) and pass the already-loaded plain
dicts/lists in here.

PROFILE CONTRACT: `profile["current_skills"]` entries are matched by their
`skill_id` key, which must already hold a canonical taxonomy id. The `skill`
key in profile.yaml is free text a human typed ("CAD Design", "Python") and
is NEVER compared here. The caller is responsible for running
`resolution.resolve_profile_skills(current_skills, taxonomy)` (which returns
the same entries with `skill_id` added) before handing the profile to this
module. gap_state.py deliberately does not import resolution.py, so it
cannot do this itself; an entry with no `skill_id` simply never covers
anything.

Lifecycle: open -> practiced -> confirmed-closed, where a `skill_confirmed`
tracker event only closes a gap when it was recorded against the CURRENT
run's target_role/target_level; a confirmation recorded for a different
target is a real historical event but does not affect status here (the
report layer is responsible for surfacing "confirmed previously for
<old target>" using the raw tracker row).
"""

from __future__ import annotations

from datetime import datetime, timezone

COMPLETION_EVENT_TYPES = {"project_completed", "course_completed"}
CONFIRMED_PROFICIENCIES = {"practiced", "proficient"}


def _find_prior_assessment(prior_assessments: list[dict], skill_id: str) -> dict | None:
    """Step 1 helper: find the prior assessment entry for `skill_id`, if any."""
    for entry in prior_assessments:
        if entry.get("skill_id") == skill_id:
            return entry
    return None


def _resolve_first_seen(
    prior: dict | None,
    now_iso: str,
    this_report_id: str,
) -> tuple[str, str]:
    """Step 1: carry forward first_seen_at/first_seen_report_id from a prior
    assessment unchanged, or stamp them fresh for a newly-seen skill.
    """
    if prior is not None:
        first_seen_at = prior.get("first_seen_at")
        first_seen_report_id = prior.get("first_seen_report_id")
        if (
            isinstance(first_seen_at, str)
            and first_seen_at
            and isinstance(first_seen_report_id, str)
            and first_seen_report_id
        ):
            try:
                _parse_timestamp(first_seen_at)
            except ValueError:
                pass
            else:
                return first_seen_at, first_seen_report_id
    return now_iso, this_report_id


def _parse_timestamp(value: str) -> datetime:
    """Parse ISO 8601 text and normalize it for chronological comparison."""
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _pass1_covered(skill_id: str, profile: dict) -> bool:
    """Step 2: does profile["current_skills"] show this skill_id at
    practiced/proficient proficiency?

    Matches against each entry's `skill_id` (the canonical taxonomy id),
    NOT its free-text `skill` field — the caller must have already resolved
    profile skill text to ids via resolution.resolve_profile_skills (see the
    module docstring's PROFILE CONTRACT).
    """
    current_skills = (profile or {}).get("current_skills") or []
    for entry in current_skills:
        if entry.get("skill_id") == skill_id and entry.get("proficiency") in CONFIRMED_PROFICIENCIES:
            return True
    return False


def _events_for_skill(
    tracker_events: list[dict],
    skill_id: str,
    first_seen_at: str,
) -> list[dict]:
    """Step 3 helper: tracker events relevant to this skill, filtered to
    occurred_at >= first_seen_at for this skill.
    """
    relevant = []
    first_seen_timestamp = _parse_timestamp(first_seen_at)
    for event in tracker_events:
        related = event.get("related_skill_ids") or []
        if skill_id not in related:
            continue
        occurred_at = event.get("occurred_at") or ""
        try:
            occurred_timestamp = _parse_timestamp(occurred_at)
        except (TypeError, ValueError):
            continue
        if occurred_timestamp < first_seen_timestamp:
            continue
        relevant.append(event)
    return relevant


def _has_completion_event(events: list[dict]) -> bool:
    """Step 3: any project_completed/course_completed event for this skill."""
    return any(event.get("event_type") in COMPLETION_EVENT_TYPES for event in events)


def _is_confirmed_closed(
    events: list[dict],
    target_role: str,
    target_level: str,
) -> bool:
    """Step 3: closes the gap when the most recent skill_confirmed event
    *for this exact target* (confirmed_for_target_role/
    confirmed_for_target_level matching the current run's target) exists.
    Confirmations recorded for a different target are real historical
    events but are filtered out before picking "most recent" — otherwise a
    newer confirmation for another target would hide an older, still-valid
    confirmation for the current one (e.g. confirm for senior, later
    confirm for junior, then return to senior: the senior confirmation
    must still count).
    """
    confirmations = [
        e
        for e in events
        if e.get("event_type") == "skill_confirmed"
        and e.get("confirmed_for_target_role") == target_role
        and e.get("confirmed_for_target_level") == target_level
    ]
    return bool(confirmations)


def _compute_status(
    skill_id: str,
    profile: dict,
    events: list[dict],
    target_role: str,
    target_level: str,
) -> str:
    """Steps 2-4: combine Pass-1 coverage and tracker events into a status,
    defaulting to "open" when nothing else applies. confirmed-closed takes
    precedence over practiced when the most recent skill_confirmed event
    matches the current target.
    """
    if _is_confirmed_closed(events, target_role, target_level):
        return "confirmed-closed"
    if _pass1_covered(skill_id, profile) or _has_completion_event(events):
        return "practiced"
    return "open"


def reconcile_assessments(
    requirements: list[dict],
    profile: dict,
    prior_assessments: list[dict],
    tracker_events: list[dict],
    target_role: str,
    target_level: str,
    this_report_id: str,
    now: datetime | None = None,
) -> list[dict]:
    """Reconcile this run's gap_assessments from scratch.

    `profile` must already carry resolved canonical ids on its
    `current_skills` entries' `skill_id` key — see the module docstring's
    PROFILE CONTRACT.

    Returns a list of {skill_id, tier, status, first_seen_at,
    first_seen_report_id} dicts, one per input requirement, in the same
    order as `requirements`.
    """
    if now is None:
        now = datetime.now(timezone.utc)
    now_iso = now.isoformat()

    results: list[dict] = []
    for requirement in requirements:
        skill_id = requirement["skill_id"]
        tier = requirement["tier"]

        # Step 1: carry forward or freshly stamp first_seen_at/report_id.
        prior = _find_prior_assessment(prior_assessments, skill_id)
        first_seen_at, first_seen_report_id = _resolve_first_seen(
            prior, now_iso, this_report_id
        )

        # Steps 2-4: compute status from Pass-1 coverage + tracker events.
        events = _events_for_skill(tracker_events, skill_id, first_seen_at)
        status = _compute_status(skill_id, profile, events, target_role, target_level)

        # Step 5: tier is copied through, not computed here.
        results.append(
            {
                "skill_id": skill_id,
                "tier": tier,
                "status": status,
                "first_seen_at": first_seen_at,
                "first_seen_report_id": first_seen_report_id,
            }
        )

    return results
