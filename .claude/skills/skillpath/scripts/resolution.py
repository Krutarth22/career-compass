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


def _normalize(text: str) -> str:
    return text.strip().lower()


def resolve_skill(text: str, taxonomy: list[dict]) -> dict:
    """Resolve free-text skill mention `text` against `taxonomy` (already
    loaded list of {id, display_name, synonyms} dicts from Task 2's
    skill-taxonomy.yaml).

    Returns {"id": str, "unmapped": bool}. Matching is case-insensitive
    exact or substring against each entry's id and synonyms — no fuzzy
    scoring. On no match, returns a provisional id (normalized text with
    non-alphanumeric runs collapsed to single hyphens) and unmapped=True.
    """
    normalized = _normalize(text)

    for entry in taxonomy:
        candidates = [entry["id"]] + list(entry.get("synonyms") or [])
        for candidate in candidates:
            candidate_norm = _normalize(str(candidate))
            if not candidate_norm:
                continue
            if candidate_norm == normalized:
                return {"id": entry["id"], "unmapped": False}
            if candidate_norm in normalized or normalized in candidate_norm:
                return {"id": entry["id"], "unmapped": False}

    provisional = _NON_ALNUM_RE.sub("-", normalized).strip("-")
    return {"id": provisional, "unmapped": True}


def resolve_track(target_role: str, track_aliases: dict) -> str | None:
    """Resolve free-text `target_role` against `track_aliases` (already
    loaded dict of track_id -> {aliases: [...]} from Task 2's
    track-aliases.yaml).

    Standalone level words (junior/mid/senior/lead/principal/staff) are
    stripped as whole words before matching. Returns the track key or None.
    """
    normalized = _normalize(target_role)
    stripped = _LEVEL_WORD_RE.sub("", normalized)
    stripped = re.sub(r"\s+", " ", stripped).strip()

    for track_id, config in track_aliases.items():
        aliases = (config or {}).get("aliases") or []
        for alias in aliases:
            alias_norm = _normalize(str(alias))
            if not alias_norm:
                continue
            if alias_norm == stripped:
                return track_id
            if alias_norm in stripped or stripped in alias_norm:
                return track_id

    return None


def _default_taxonomy_path() -> Path:
    return Path(__file__).parent.parent / "reference" / "skill-taxonomy.yaml"


def _default_track_aliases_path() -> Path:
    return Path(__file__).parent.parent / "reference" / "track-aliases.yaml"


def _load_yaml(path) -> object:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="skillpath resolution utility")
    sub = parser.add_subparsers(dest="command", required=True)

    skill_p = sub.add_parser("resolve-skill", help="Resolve a free-text skill mention")
    skill_p.add_argument("text")
    skill_p.add_argument(
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
