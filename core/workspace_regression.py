"""One deterministic manifest for workspace store/fan/tether/self promotion gates."""

from __future__ import annotations

try:
    from .cognitive_workspace import Fact
    from .workspace_mouth import certify_divergence
    from .workspace_runtime import TypedFactStore, grounded_answer, identity_control
except ImportError:
    from cognitive_workspace import Fact
    from workspace_mouth import certify_divergence
    from workspace_runtime import TypedFactStore, grounded_answer, identity_control


def run_workspace_regression() -> dict[str, object]:
    store = TypedFactStore([
        Fact("library", "opens_at", "09:00", ("sign",)),
        Fact("anima", "has_identity_anchor", "anchor-a", ("self",)),
    ])
    conflicting = TypedFactStore([
        Fact("library", "opens_at", "09:00", ("sign",)),
        Fact("library", "opens_at", "10:00", ("conflict",)),
    ])
    store_checks = {
        "live": grounded_answer(store, "library", "opens_at") == "09:00",
        "store_off": grounded_answer(TypedFactStore(), "library", "opens_at") == "UNGROUNDED",
        "key_shuffle": grounded_answer(store, "other", "opens_at") == "UNGROUNDED",
        "relation_shuffle": grounded_answer(store, "library", "closes_at") == "UNGROUNDED",
        "conflict_abstain": grounded_answer(conflicting, "library", "opens_at") == "UNGROUNDED",
    }
    tether_checks = {
        "supported_answer": grounded_answer(store, "library", "opens_at") == "09:00",
        "unsupported_abstain": grounded_answer(store, "library", "owner") == "UNGROUNDED",
        "ambiguous_abstain": grounded_answer(conflicting, "library", "opens_at") == "UNGROUNDED",
    }
    en = certify_divergence("if copper conducts heat, then water drives turbines")
    ko = certify_divergence("만약 비가 오지 않으면, 그러면 도로는 젖지 않는다")
    fan_checks = {
        "english": bool(en["ok"]), "korean": bool(ko["ok"]),
        "english_missing_collapse": en["missing_admit"] == 0,
        "english_shuffle_collapse": en["shuffle_admit"] == 0,
        "korean_missing_collapse": ko["missing_admit"] == 0,
        "korean_shuffle_collapse": ko["shuffle_admit"] == 0,
    }
    self_result = identity_control(store, "anima", "anchor-a", "other")
    self_checks = {
        "anchor_on": self_result["on"],
        "anchor_off_collapse": not self_result["off"],
        "anchor_shuffle_collapse": not self_result["shuffle"],
    }
    groups = {"store": store_checks, "fan": fan_checks,
              "tether": tether_checks, "self": self_checks}
    system_pass = all(all(checks.values()) for checks in groups.values())
    # Promotion includes external canonical-mouth evidence. These remain false until a
    # measured model run changes them; system fixtures cannot silently overwrite them.
    blockers = {
        "bare_store": False,
        "bare_fan": False,
        "bare_tether": False,
        "bare_self": False,
        "model_realizer_semantic_accept": False,
    }
    return {
        "schema": "anima.workspace.regression/1",
        "groups": groups,
        "system_pass": system_pass,
        "promotion_blockers": blockers,
        "default_promotable": system_pass and all(blockers.values()),
    }


def format_workspace_regression(report: dict[str, object]) -> str:
    lines = ["=== anima workspace regression manifest ==="]
    for group, checks in report["groups"].items():
        lines.append("%s: %s" % (group, "PASS" if all(checks.values()) else "FAIL"))
        lines.extend("  %s=%s" % (name, value) for name, value in checks.items())
    lines.append("system_pass=%s" % report["system_pass"])
    lines.append("promotion_blockers=" + ",".join(
        name for name, passed in report["promotion_blockers"].items() if not passed))
    lines.append("default_promotable=%s" % report["default_promotable"])
    return "\n".join(lines)
