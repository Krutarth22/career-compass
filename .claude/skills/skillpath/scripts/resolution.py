"""resolution.py — resolve free-text skill/role mentions against the
reference taxonomy (Task 2's skill-taxonomy.yaml / track-aliases.yaml).

Pure-function library first, CLI wrapper second.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

_LEVEL_WORD_RE = re.compile(
    r"\b(junior|mid|senior|lead|principal|staff)\b", flags=re.IGNORECASE
)
_NON_ALNUM_RE = re.compile(r"[^a-z0-9]+")
_SEPARATOR_RE = re.compile(r"[\s_-]+")

#: Minimum length for a SINGLE-token id/synonym/input to be eligible for
#: whole-word phrase matching. Below this, only an exact match counts.
#: This is what stops the 3-letter synonym "rag" from matching inside
#: "storage" / "average" / "leverage", and "ml" from matching inside
#: unrelated phrases.
MIN_PHRASE_TOKEN_LEN = 5


def _normalize(text: str) -> str:
    return text.strip().lower()


def _normalize_key(text: str) -> str:
    """Canonical comparison key: lowercase, with runs of whitespace,
    underscores and hyphens collapsed to a single hyphen. "Python 3",
    "python_3" and "python-3" all become "python-3".
    """
    return _SEPARATOR_RE.sub("-", _normalize(text)).strip("-")


def _is_phrase_eligible(key: str) -> bool:
    """A key may be used as a whole-word containment pattern only if it is
    multi-token (contains a separator after normalization) or long enough
    that an incidental letter-run collision is implausible.
    """
    return "-" in key or len(key) >= MIN_PHRASE_TOKEN_LEN


def _phrase_contains(pattern_key: str, haystack_key: str) -> bool:
    """Whole-word containment of `pattern_key` inside `haystack_key`.

    Boundaries are enforced with alphanumeric lookarounds rather than plain
    substring containment, so "rag" never matches inside "sto-rag-e".
    """
    return (
        re.search(
            r"(?<![a-z0-9])" + re.escape(pattern_key) + r"(?![a-z0-9])",
            haystack_key,
        )
        is not None
    )


def _match_by_phrase(input_key: str, candidate_keys: list[tuple[str, str]]) -> str | None:
    """Rule 3 (see resolve_skill): whole-word phrase match in either
    direction, restricted to phrase-eligible keys. `candidate_keys` is a
    list of (candidate_key, owner_id). Returns the owner id only when the
    match is unambiguous (all matches point at the same owner).
    """
    owners: list[str] = []
    for candidate_key, owner_id in candidate_keys:
        matched = False
        if _is_phrase_eligible(candidate_key) and _phrase_contains(
            candidate_key, input_key
        ):
            matched = True
        elif _is_phrase_eligible(input_key) and _phrase_contains(
            input_key, candidate_key
        ):
            matched = True
        if matched and owner_id not in owners:
            owners.append(owner_id)

    if len(owners) == 1:
        return owners[0]
    return None


def resolve_skill(text: str, taxonomy: list[dict]) -> dict:
    """Resolve free-text skill mention `text` against `taxonomy` (already
    loaded list of {id, display_name, synonyms} dicts from Task 2's
    skill-taxonomy.yaml).

    Returns {"id": str, "unmapped": bool}. Matching is deliberately strict
    — raw bidirectional substring containment used to produce nonsense
    matches ("storage"/"average"/"leverage" all hitting the 3-letter
    synonym "rag"), which matters more now that every profile skill is
    routed through here. The rules, in order:

    1. Exact match (case-insensitive, whitespace/underscore/hyphen
       normalized to a single form) against an entry's `id`.
    2. Exact match, same normalization, against an entry's `synonyms` —
       accepted only when exactly one entry matches.
    3. Whole-word phrase containment in either direction (input inside a
       candidate, or a candidate inside the input), restricted to keys that
       are multi-token or at least MIN_PHRASE_TOKEN_LEN characters long,
       and accepted only when all matches point at a single entry. Short
       single-token ids/synonyms (e.g. "rag", "ml", "sql") can therefore
       ONLY be reached by rules 1-2.
    4. No match: return a provisional id (normalized text with
       non-alphanumeric runs collapsed to single hyphens) and
       unmapped=True. Never guess.
    """
    input_key = _normalize_key(text)
    if not input_key:
        return {"id": "", "unmapped": True}

    # Rule 1: exact id match.
    for entry in taxonomy:
        if _normalize_key(str(entry["id"])) == input_key:
            return {"id": entry["id"], "unmapped": False}

    # Rule 2: exact synonym match, unambiguous.
    synonym_owners: list[str] = []
    candidate_keys: list[tuple[str, str]] = []
    for entry in taxonomy:
        entry_id = entry["id"]
        for candidate in [entry_id] + list(entry.get("synonyms") or []):
            candidate_key = _normalize_key(str(candidate))
            if not candidate_key:
                continue
            candidate_keys.append((candidate_key, entry_id))
            if candidate_key == input_key and entry_id not in synonym_owners:
                synonym_owners.append(entry_id)
    if len(synonym_owners) == 1:
        return {"id": synonym_owners[0], "unmapped": False}

    # Rule 3: bounded whole-word phrase match, unambiguous.
    phrase_owner = _match_by_phrase(input_key, candidate_keys)
    if phrase_owner is not None:
        return {"id": phrase_owner, "unmapped": False}

    # Rule 4: provisional / unmapped.
    provisional = _NON_ALNUM_RE.sub("-", _normalize(text)).strip("-")
    return {"id": provisional, "unmapped": True}


def resolve_profile_skills(current_skills: list[dict], taxonomy: list[dict]) -> list[dict]:
    """Resolve a profile's free-text `current_skills` entries to canonical
    skill ids.

    `profile.yaml`'s `current_skills[].skill` is free text a human typed
    ("CAD Design", "Python", "Excel"). Downstream consumers — gap_state's
    Pass-1 coverage check and project_planner's prerequisite-satisfaction
    check — compare against canonical taxonomy ids, so the text must be
    resolved first or a user's real skills silently cover nothing.

    Returns a NEW list of new dicts, each a copy of the input entry with an
    added `skill_id` key holding the resolved canonical id (or the
    provisional slug when unmapped). The original `skill` text is kept
    intact for display. Input dicts are not mutated.

    This lives here, in the caller-side resolution layer, deliberately:
    gap_state.py must never import resolution.py (architecture constraint),
    so resolution happens before the profile is handed to it.
    """
    resolved: list[dict] = []
    for entry in current_skills or []:
        new_entry = dict(entry)
        new_entry["skill_id"] = resolve_skill(str(entry.get("skill") or ""), taxonomy)["id"]
        resolved.append(new_entry)
    return resolved


def resolve_track(target_role: str, track_aliases: dict) -> str | None:
    """Resolve free-text `target_role` against `track_aliases` (already
    loaded dict of track_id -> {aliases: [...]} from Task 2's
    track-aliases.yaml).

    Standalone level words (junior/mid/senior/lead/principal/staff) are
    stripped as whole words before matching. Matching uses the same
    tightened rules as resolve_skill (exact normalized match first, then
    bounded whole-word phrase containment for phrase-eligible keys only) so
    a short alias like "mle" can never match inside an unrelated word.
    Returns the track key or None.
    """
    normalized = _normalize(target_role)
    stripped = _LEVEL_WORD_RE.sub("", normalized)
    stripped = re.sub(r"\s+", " ", stripped).strip()
    input_key = _normalize_key(stripped)
    if not input_key:
        return None

    candidate_keys: list[tuple[str, str]] = []
    for track_id, config in track_aliases.items():
        aliases = (config or {}).get("aliases") or []
        for alias in aliases:
            alias_key = _normalize_key(str(alias))
            if not alias_key:
                continue
            if alias_key == input_key:
                return track_id
            candidate_keys.append((alias_key, track_id))

    return _match_by_phrase(input_key, candidate_keys)


def _default_taxonomy_path() -> Path:
    return Path(__file__).parent.parent / "reference" / "skill-taxonomy.yaml"


def _default_track_aliases_path() -> Path:
    return Path(__file__).parent.parent / "reference" / "track-aliases.yaml"


def _load_yaml(path) -> object:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _load_json(path) -> object:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="skillpath resolution utility")
    sub = parser.add_subparsers(dest="command", required=True)

    skill_p = sub.add_parser("resolve-skill", help="Resolve a free-text skill mention")
    skill_p.add_argument("text")
    skill_p.add_argument(
        "--taxonomy", default=None, help="Path to skill-taxonomy.yaml"
    )

    profile_p = sub.add_parser(
        "resolve-profile-skills",
        help="Resolve a profile's current_skills free text to canonical skill_ids",
    )
    profile_p.add_argument(
        "--current-skills",
        required=True,
        help="Path to a JSON file containing the profile's current_skills list",
    )
    profile_p.add_argument(
        "--taxonomy", default=None, help="Path to skill-taxonomy.yaml"
    )

    track_p = sub.add_parser("resolve-track", help="Resolve a free-text target role")
    track_p.add_argument("target_role")
    track_p.add_argument(
        "--track-aliases", default=None, help="Path to track-aliases.yaml"
    )

    return parser


def main(argv=None) -> int:
    parser = _build_arg_parser()
    ns = parser.parse_args(argv)

    try:
        if ns.command == "resolve-skill":
            taxonomy_path = ns.taxonomy or _default_taxonomy_path()
            taxonomy = _load_yaml(taxonomy_path)
            result = resolve_skill(ns.text, taxonomy)
            print(json.dumps(result))
            return 0
        if ns.command == "resolve-profile-skills":
            taxonomy_path = ns.taxonomy or _default_taxonomy_path()
            taxonomy = _load_yaml(taxonomy_path)
            current_skills = _load_json(ns.current_skills)
            result = resolve_profile_skills(current_skills, taxonomy)
            print(json.dumps(result, default=str))
            return 0
        if ns.command == "resolve-track":
            track_aliases_path = ns.track_aliases or _default_track_aliases_path()
            track_aliases = _load_yaml(track_aliases_path)
            result = resolve_track(ns.target_role, track_aliases)
            print(json.dumps(result))
            return 0
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        return 1

    parser.print_help(sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
