"""Persistent IIT-daemon causal core.

This module is a state boundary around the existing three-node recurrent TPM and
``engine_cli.big_phi_bounded`` instrument.  It is deliberately not a language
model, persona, evaluator, or consciousness claim.  Events can perturb the
candidate state, after which the autonomous TPM owns the next transition.
"""

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import tempfile

import recurrent_lane as RL


SNAPSHOT_SCHEMA = "anima-iit-daemon-snapshot/1"
CORE_SCHEMA = "anima-iit-daemon-core/1"
MAX_SNAPSHOT_BYTES = 1 << 20
DELAYED_PROTOCOL_SCHEMA = "anima-iit-daemon-delayed-protocol/1"
CLMS_LATCH_PROTOCOL_SCHEMA = "anima-iit-daemon-clms-protocol/1"
CONTENT_PROTOCOL_SCHEMA = "anima-iit-daemon-content-protocol/1"


def _canonical_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def _sha256(value):
    return hashlib.sha256(_canonical_json(value)).hexdigest()


def _state(value, name="state"):
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("%s must be an integer" % name)
    if value < 0 or value >= (1 << RL.N_CELL):
        raise ValueError("%s must be in [0,%d]" % (name, (1 << RL.N_CELL) - 1))
    return value


def _permutation(value):
    if not isinstance(value, (list, tuple)) or len(value) != RL.N_CELL:
        raise ValueError("permutation must contain exactly three node indexes")
    p = tuple(value)
    if any(isinstance(x, bool) or not isinstance(x, int) for x in p):
        raise TypeError("permutation indexes must be integers")
    if sorted(p) != list(range(RL.N_CELL)):
        raise ValueError("permutation must be a bijection over the three nodes")
    return p


def permute_bits(value, permutation):
    """Return bits where destination i reads source ``permutation[i]``."""
    source = _state(value, "intervention")
    p = _permutation(permutation)
    out = 0
    for destination, source_index in enumerate(p):
        out |= ((source >> source_index) & 1) << destination
    return out


@dataclass(frozen=True)
class IITDaemonConfig:
    schema: str = CORE_SCHEMA
    nodes: int = RL.N_CELL
    transition: str = "xor-other-two-ring"
    purview_cap: int = RL.N_CELL

    def validate(self):
        if self.schema != CORE_SCHEMA:
            raise ValueError("unsupported IIT daemon core schema")
        if self.nodes != RL.N_CELL:
            raise ValueError("R0 requires exactly three intrinsic nodes")
        if self.transition != "xor-other-two-ring":
            raise ValueError("R0 transition is frozen to xor-other-two-ring")
        if self.purview_cap != RL.N_CELL:
            raise ValueError("R0 requires full three-node purviews")
        return self

    @property
    def checksum(self):
        self.validate()
        return _sha256(asdict(self))


class IITDaemonCore:
    """A deterministic session-persistent intrinsic state with hash-chained steps."""

    def __init__(self, state=0, *, config=None, tick=0, audit_head=None):
        self.config = (config or IITDaemonConfig()).validate()
        self.state = _state(state)
        if isinstance(tick, bool) or not isinstance(tick, int) or tick < 0:
            raise ValueError("tick must be a non-negative integer")
        self.tick = tick
        self.tpm = RL.validate_tpm(RL.xor_ring_tpm(), self.config.nodes)
        genesis = {
            "schema": SNAPSHOT_SCHEMA,
            "config_checksum": self.config.checksum,
            "initial_state": self.state,
        }
        self.audit_head = str(audit_head) if audit_head is not None else _sha256(genesis)
        if len(self.audit_head) != 64 or any(c not in "0123456789abcdef" for c in self.audit_head):
            raise ValueError("audit_head must be a lowercase SHA-256 hex digest")

    def _transition(self, state, tpm):
        next_state = 0
        for unit in range(self.config.nodes):
            probability = tpm[state * self.config.nodes + unit]
            if probability not in (0.0, 1.0):
                raise ValueError("runtime R0 transition must be deterministic")
            next_state |= int(probability) << unit
        return next_state

    def step(self, intervention=0, *, permutation=(0, 1, 2), lesion_mask=0):
        intervention = _state(intervention, "intervention")
        p = _permutation(permutation)
        lesion_mask = _state(lesion_mask, "lesion_mask")
        shuffled = permute_bits(intervention, p)
        before = self.state
        perturbed = (before ^ shuffled) & ~lesion_mask
        active_tpm = self.tpm if lesion_mask == 0 else RL.lesion_tpm(
            self.tpm, lesion_mask, self.config.nodes)
        after = self._transition(perturbed, active_tpm)
        receipt = {
            "tick": self.tick + 1,
            "before": before,
            "intervention": intervention,
            "permutation": list(p),
            "shuffled_intervention": shuffled,
            "perturbed": perturbed,
            "lesion_mask": lesion_mask,
            "after": after,
        }
        self.audit_head = hashlib.sha256(
            bytes.fromhex(self.audit_head) + _canonical_json(receipt)).hexdigest()
        self.tick += 1
        self.state = after
        return dict(receipt, audit_head=self.audit_head)

    def measure(self):
        states = RL.all_state_big_phi(self.tpm, self.config.nodes, self.config.purview_cap)
        current = states[self.state]
        return {
            "instrument": "core.engine_cli.big_phi_bounded",
            "scope": "fixed-candidate-bounded-structure-loss",
            "state": self.state,
            "state_phi": current,
            "all_state_phi": states,
            "mean_phi": sum(states) / len(states),
            "min_phi": min(states),
            "max_phi": max(states),
            "causal_edges": [list(edge) for edge in RL.causal_edges(self.tpm)],
        }

    def snapshot(self):
        payload = {
            "config": asdict(self.config),
            "config_checksum": self.config.checksum,
            "state": self.state,
            "tick": self.tick,
            "audit_head": self.audit_head,
        }
        return {"schema": SNAPSHOT_SCHEMA, "payload": payload, "sha256": _sha256(payload)}

    def save_snapshot(self, path):
        target = os.path.abspath(os.fspath(path))
        parent = os.path.dirname(target)
        if not os.path.isdir(parent):
            raise FileNotFoundError("snapshot parent directory does not exist")
        body = _canonical_json(self.snapshot()) + b"\n"
        fd, temporary = tempfile.mkstemp(prefix=".iit-daemon-", suffix=".json", dir=parent)
        try:
            os.fchmod(fd, 0o600)
            with os.fdopen(fd, "wb") as handle:
                handle.write(body)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, target)
            directory_fd = os.open(parent, os.O_RDONLY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
        except BaseException:
            try:
                os.unlink(temporary)
            except FileNotFoundError:
                pass
            raise
        return target

    @classmethod
    def load_snapshot(cls, path):
        target = os.path.abspath(os.fspath(path))
        size = os.path.getsize(target)
        if size <= 0 or size > MAX_SNAPSHOT_BYTES:
            raise ValueError("snapshot size is invalid")
        with open(target, "rb") as handle:
            raw = handle.read(MAX_SNAPSHOT_BYTES + 1)
        try:
            document = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("snapshot is not valid canonical JSON") from exc
        if not isinstance(document, dict) or document.get("schema") != SNAPSHOT_SCHEMA:
            raise ValueError("unsupported snapshot schema")
        payload = document.get("payload")
        if not isinstance(payload, dict) or document.get("sha256") != _sha256(payload):
            raise ValueError("snapshot checksum mismatch")
        expected = {"config", "config_checksum", "state", "tick", "audit_head"}
        if set(payload) != expected:
            raise ValueError("snapshot payload fields mismatch")
        try:
            config = IITDaemonConfig(**payload["config"]).validate()
        except (TypeError, ValueError) as exc:
            raise ValueError("snapshot config is invalid") from exc
        if payload["config_checksum"] != config.checksum:
            raise ValueError("snapshot config checksum mismatch")
        return cls(payload["state"], config=config, tick=payload["tick"],
                   audit_head=payload["audit_head"])


def delayed_codebook(cues):
    """Derive the delayed-task state->cue readout from the frozen core transition.

    The readout is intentionally prescribed rather than learned.  Every cue must
    encode to a distinct fixed point so the later action is wholly determined by
    persistent intrinsic state, not by an evaluator-side copy of the cue.
    """
    if not isinstance(cues, (list, tuple)) or not cues:
        raise ValueError("delayed cues must be a non-empty sequence")
    if len(set(cues)) != len(cues):
        raise ValueError("delayed cues must be unique")
    codebook = {}
    for cue in cues:
        cue = _state(cue, "cue")
        core = IITDaemonCore(0)
        encoded = core.step(cue)["after"]
        settled = core.step(0)["after"]
        if settled != encoded:
            raise ValueError("each delayed cue must encode to a stable intrinsic state")
        if encoded in codebook:
            raise ValueError("delayed cues must encode bijectively")
        codebook[encoded] = cue
    return codebook


def delayed_task_trial(cue, delay, cues, *, permutation=(0, 1, 2),
                       reset_every_turn=False):
    """Encode one cue, advance autonomous turns, and read the persistent action.

    Reset is an explicit negative-control intervention: a fresh state-zero core
    replaces the prior core before every delayed turn.  The returned action is
    decoded only from final intrinsic state through ``delayed_codebook``.
    """
    cue = _state(cue, "cue")
    codebook = delayed_codebook(cues)
    if cue not in codebook.values():
        raise ValueError("cue is not registered in the delayed task")
    if isinstance(delay, bool) or not isinstance(delay, int) or delay < 1:
        raise ValueError("delay must be a positive integer")
    p = _permutation(permutation)
    core = IITDaemonCore(0)
    encoding = core.step(cue, permutation=p)
    encoded_state = core.state
    receipts = []
    resets = 0
    for _ in range(delay):
        if reset_every_turn:
            core = IITDaemonCore(0)
            resets += 1
        receipts.append(core.step(0))
    action = codebook.get(core.state)
    return {
        "cue": cue,
        "delay": delay,
        "permutation": list(p),
        "reset_every_turn": bool(reset_every_turn),
        "reset_count": resets,
        "encoding": encoding,
        "encoded_state": encoded_state,
        "delay_receipts": receipts,
        "final_state": core.state,
        "action": action,
        "gold": cue,
        "correct": action == cue,
        "tick": core.tick,
        "audit_head": core.audit_head,
    }


def clms_latch_codebook(class_to_cue):
    """Derive the bounded CLMS-class readout from the frozen core transition.

    R2 supplies only a class prediction to this boundary.  Each class must own a
    distinct one-node cue; the store, addresses, target slots, prompt and gold do
    not cross the boundary.  The returned mapping decodes intrinsic state back to
    the original class after the autonomous transition.
    """
    if not isinstance(class_to_cue, dict) or set(class_to_cue) != {"good", "bad"}:
        raise ValueError("CLMS latch needs exactly the 'good' and 'bad' classes")
    cues = []
    cue_to_class = {}
    for label in ("good", "bad"):
        cue = _state(class_to_cue[label], "class cue")
        if cue == 0 or cue & (cue - 1):
            raise ValueError("each CLMS class cue must intervene on exactly one node")
        if cue in cue_to_class:
            raise ValueError("CLMS class cues must be distinct")
        cues.append(cue)
        cue_to_class[cue] = label
    state_to_cue = delayed_codebook(cues)
    return {state: cue_to_class[cue] for state, cue in state_to_cue.items()}


def clms_latch_trial(prediction, gold, class_to_cue, *, delay=1,
                     permutation=(0, 1, 2), reset_every_turn=False):
    """Latch one CLMS class into persistent state and read a later action.

    ``gold`` is used only after action production to score the trial.  It never
    enters the core or the class-to-cue mapping.
    """
    codebook = clms_latch_codebook(class_to_cue)
    if prediction not in class_to_cue:
        raise ValueError("CLMS latch prediction is not registered")
    if gold not in class_to_cue:
        raise ValueError("CLMS latch gold is not registered")
    if isinstance(delay, bool) or not isinstance(delay, int) or delay < 1:
        raise ValueError("CLMS latch delay must be a positive integer")
    p = _permutation(permutation)
    if not isinstance(reset_every_turn, bool):
        raise TypeError("reset_every_turn must be bool")
    cue = class_to_cue[prediction]
    core = IITDaemonCore(0)
    encoding = core.step(cue, permutation=p)
    receipts = []
    resets = 0
    for _ in range(delay):
        if reset_every_turn:
            core = IITDaemonCore(0)
            resets += 1
        receipts.append(core.step(0))
    action = codebook.get(core.state)
    result = {
        "prediction": prediction,
        "gold": gold,
        "latch_cue": cue,
        "encoding": encoding,
        "encoded_state": encoding["after"],
        "delay": delay,
        "delay_receipts": receipts,
        "final_state": core.state,
        "action": action,
        "correct": action == gold,
        "mirrors_prediction": action == prediction,
        "tick": core.tick,
        "audit_head": core.audit_head,
    }
    if p != (0, 1, 2) or reset_every_turn:
        result.update({
            "permutation": list(p),
            "reset_every_turn": reset_every_turn,
            "reset_count": resets,
        })
    return result
