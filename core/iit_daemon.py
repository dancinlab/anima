"""Persistent IIT-daemon causal core.

This module is a state boundary around the existing three-node recurrent TPM and
``engine_cli.big_phi_bounded`` instrument.  It is deliberately not a language
model, persona, evaluator, or consciousness claim.  Events can perturb the
candidate state, after which the autonomous TPM owns the next transition.
"""

from dataclasses import asdict, dataclass
import hashlib
import json
import math
import os
import tempfile

import recurrent_lane as RL


SNAPSHOT_SCHEMA = "anima-iit-daemon-snapshot/1"
CORE_SCHEMA = "anima-iit-daemon-core/1"
MAX_SNAPSHOT_BYTES = 1 << 20
DELAYED_PROTOCOL_SCHEMA = "anima-iit-daemon-delayed-protocol/1"
CLMS_LATCH_PROTOCOL_SCHEMA = "anima-iit-daemon-clms-protocol/1"
CONTENT_PROTOCOL_SCHEMA = "anima-iit-daemon-content-protocol/1"
COMPOSITION_PROTOCOL_SCHEMA = "anima-iit-daemon-composition-protocol/1"
COMPOSITION_PANEL_SCHEMA = "anima-iit-daemon-composition-panel/1"
WORKSPACE_SNAPSHOT_SCHEMA = "anima-iit-content-workspace-snapshot/1"
SEMANTIC_BRIDGE_PROTOCOL_SCHEMA = "anima-iit-daemon-semantic-bridge-protocol/1"
SEMANTIC_BRIDGE_PANEL_SCHEMA = "anima-iit-daemon-semantic-bridge-panel/1"
SEMANTIC_BRIDGE_MODEL_SCHEMA = "anima-iit-semantic-bridge-model/1"
SEMANTIC_BRIDGE_MAX_MODEL_BYTES = 4 << 20
SEMANTIC_EVENT_MAX_BYTES = 256
CONTENT_RECORD_FIELDS = ("entity", "relation", "value")


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
        return _core_from_snapshot_document(document)


def _core_from_snapshot_document(document):
    """Validate an in-memory core snapshot through the canonical snapshot contract."""
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
    return IITDaemonCore(payload["state"], config=config, tick=payload["tick"],
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


def _content_atom(value, name):
    """Validate one bounded symbolic atom without accepting prompt-like payloads."""
    if not isinstance(value, str) or not value or len(value.encode("utf-8")) > 32:
        raise ValueError("%s must be a non-empty atom of at most 32 bytes" % name)
    if not value.isascii() or not value[0].islower() or any(
            not (char.islower() or char.isdigit() or char == "-") for char in value):
        raise ValueError("%s must use canonical lowercase ASCII atom syntax" % name)
    return value


def validate_content_records(records, addresses=None):
    """Return a detached, canonical copy of bounded entity/relation/value slots."""
    if not isinstance(records, dict) or not records:
        raise ValueError("content records must be a non-empty address object")
    expected_addresses = None
    if addresses is not None:
        if not isinstance(addresses, (list, tuple)) or not addresses:
            raise ValueError("content addresses must be a non-empty sequence")
        expected_addresses = {_content_atom(value, "content address") for value in addresses}
        if len(expected_addresses) != len(addresses):
            raise ValueError("content addresses must be unique")
        if set(records) != expected_addresses:
            raise ValueError("content records must exactly cover registered addresses")
    normalized = {}
    for address, record in records.items():
        address = _content_atom(address, "content address")
        if not isinstance(record, dict) or set(record) != set(CONTENT_RECORD_FIELDS):
            raise ValueError("content record fields must be entity, relation and value")
        normalized[address] = {
            field: _content_atom(record[field], "content record %s" % field)
            for field in CONTENT_RECORD_FIELDS
        }
    if len(normalized) != len(records):
        raise ValueError("content record addresses must be unique")
    return normalized


def _semantic_event_text(text):
    """Validate one bounded English event without accepting transcript/control payloads."""
    if not isinstance(text, str) or not text:
        raise ValueError("semantic bridge event must be a non-empty string")
    raw = text.encode("utf-8")
    if len(raw) > SEMANTIC_EVENT_MAX_BYTES:
        raise ValueError("semantic bridge event exceeds the bounded byte budget")
    if not text.isascii() or any(ord(char) < 32 or ord(char) == 127 for char in text):
        raise ValueError("semantic bridge event must be single-line printable ASCII")
    return text


def _semantic_bridge_example(example):
    if not isinstance(example, dict) or set(example) != {"text", "labels"}:
        raise ValueError("semantic bridge example fields must be text and labels")
    text = _semantic_event_text(example["text"])
    labels = example["labels"]
    if not isinstance(labels, dict) or "kind" not in labels:
        raise ValueError("semantic bridge example labels are incomplete")
    kind = labels["kind"]
    expected = {
        "memory": {"kind", "address", "entity", "relation", "value"},
        "query": {"kind", "address"},
        "other": {"kind"},
    }
    if kind not in expected or set(labels) != expected[kind]:
        raise ValueError("semantic bridge labels do not match the event kind")
    checked = {"kind": kind}
    for field, value in labels.items():
        if field != "kind":
            checked[field] = _content_atom(value, "semantic bridge " + field)
    return {"text": text, "labels": checked}


def _semantic_bridge_model(model):
    """Fail-closed validation for a detached learned bridge model document."""
    if not isinstance(model, dict) or set(model) != {"schema", "payload", "sha256"} or \
            model.get("schema") != SEMANTIC_BRIDGE_MODEL_SCHEMA:
        raise ValueError("unsupported semantic bridge model schema")
    payload = model["payload"]
    if not isinstance(payload, dict) or model["sha256"] != _sha256(payload):
        raise ValueError("semantic bridge model checksum mismatch")
    if set(payload) != {"feature", "training_sha256", "classifiers"}:
        raise ValueError("semantic bridge model payload fields mismatch")
    feature = payload["feature"]
    if not isinstance(feature, dict) or feature != {
            "name": "core.mi_compress.hashed_ngram_features",
            "dim": feature.get("dim"), "ngram_sizes": [1, 2, 3], "log_weight": True}:
        raise ValueError("semantic bridge feature contract mismatch")
    dim = feature["dim"]
    if isinstance(dim, bool) or not isinstance(dim, int) or dim < 64 or dim > 8192:
        raise ValueError("semantic bridge feature dimension is invalid")
    training_sha = payload["training_sha256"]
    if not isinstance(training_sha, str) or len(training_sha) != 64 or any(
            char not in "0123456789abcdef" for char in training_sha):
        raise ValueError("semantic bridge training checksum is invalid")
    classifiers = payload["classifiers"]
    required = {"kind", "address", "entity", "relation", "value"}
    if not isinstance(classifiers, dict) or set(classifiers) != required:
        raise ValueError("semantic bridge classifiers are incomplete")
    detached = {}
    for field in sorted(required):
        classifier = classifiers[field]
        if not isinstance(classifier, dict) or set(classifier) != {
                "classes", "centroids", "examples"}:
            raise ValueError("semantic bridge classifier fields mismatch")
        classes = classifier["classes"]
        if not isinstance(classes, list) or len(classes) < 2 or classes != sorted(set(classes)):
            raise ValueError("semantic bridge classifier classes are invalid")
        examples = classifier["examples"]
        if isinstance(examples, bool) or not isinstance(examples, int) or examples < len(classes):
            raise ValueError("semantic bridge classifier example count is invalid")
        centroids = classifier["centroids"]
        if not isinstance(centroids, dict) or set(centroids) != set(classes):
            raise ValueError("semantic bridge classifier centroid classes mismatch")
        checked_centroids = {}
        for label in classes:
            _content_atom(label, "semantic bridge class")
            vector = centroids[label]
            if not isinstance(vector, list) or len(vector) != dim or any(
                    isinstance(value, bool) or not isinstance(value, (int, float)) or
                    not math.isfinite(value) for value in vector):
                raise ValueError("semantic bridge centroid is invalid")
            norm = math.sqrt(math.fsum(float(value) ** 2 for value in vector))
            if abs(norm - 1.0) > 1.0e-9:
                raise ValueError("semantic bridge centroid must be unit-normalized")
            checked_centroids[label] = [float(value) for value in vector]
        detached[field] = {"classes": list(classes), "centroids": checked_centroids,
                           "examples": examples}
    clean_payload = {"feature": dict(feature), "training_sha256": training_sha,
                     "classifiers": detached}
    return {"schema": SEMANTIC_BRIDGE_MODEL_SCHEMA, "payload": clean_payload,
            "sha256": _sha256(clean_payload)}


def train_semantic_bridge(examples, feature_dim=2048):
    """Fit deterministic factorised centroids over the canonical byte n-gram features."""
    import mi_compress as MI

    if isinstance(feature_dim, bool) or not isinstance(feature_dim, int) or \
            feature_dim < 64 or feature_dim > 8192:
        raise ValueError("semantic bridge feature dimension is invalid")
    if not isinstance(examples, list) or not examples:
        raise ValueError("semantic bridge needs a non-empty example list")
    checked = [_semantic_bridge_example(example) for example in examples]
    texts = [example["text"] for example in checked]
    if len(texts) != len(set(texts)):
        raise ValueError("semantic bridge training texts must be unique")
    features = [MI.hashed_ngram_features(text.encode("utf-8"), dim=feature_dim)
                for text in texts]
    classifiers = {}
    for field in ("kind", "address", "entity", "relation", "value"):
        rows = [(vector, example["labels"][field])
                for vector, example in zip(features, checked)
                if field in example["labels"]]
        classes = sorted({label for _, label in rows})
        if len(classes) < 2:
            raise ValueError("semantic bridge field lacks multiple classes: " + field)
        centroids = {}
        for label in classes:
            selected = [vector for vector, actual in rows if actual == label]
            mean = [math.fsum(vector[index] for vector in selected) / len(selected)
                    for index in range(feature_dim)]
            norm = math.sqrt(math.fsum(value * value for value in mean))
            if norm <= 0.0:
                raise ValueError("semantic bridge learned an empty centroid")
            centroids[label] = [value / norm for value in mean]
        classifiers[field] = {"classes": classes, "centroids": centroids,
                              "examples": len(rows)}
    payload = {
        "feature": {"name": "core.mi_compress.hashed_ngram_features",
                    "dim": feature_dim, "ngram_sizes": [1, 2, 3], "log_weight": True},
        "training_sha256": _sha256(checked),
        "classifiers": classifiers,
    }
    return _semantic_bridge_model({"schema": SEMANTIC_BRIDGE_MODEL_SCHEMA,
                                   "payload": payload, "sha256": _sha256(payload)})


def semantic_bridge_encode(model, text):
    """Map one bounded byte event to a learned event kind, address and optional record."""
    import mi_compress as MI

    checked = _semantic_bridge_model(model)
    text = _semantic_event_text(text)
    payload = checked["payload"]
    vector = MI.hashed_ngram_features(text.encode("utf-8"),
                                      dim=payload["feature"]["dim"])

    def predict(field):
        classifier = payload["classifiers"][field]
        scored = [(math.fsum(a * b for a, b in zip(
            vector, classifier["centroids"][label])), label)
                  for label in classifier["classes"]]
        scored.sort(key=lambda row: (-row[0], row[1]))
        margin = scored[0][0] - scored[1][0]
        return scored[0][1], margin

    kind, kind_margin = predict("kind")
    result = {"kind": kind, "address": None, "record": None,
              "margins": {"kind": kind_margin}, "model_sha256": checked["sha256"]}
    if kind in ("memory", "query"):
        address, margin = predict("address")
        result["address"] = address
        result["margins"]["address"] = margin
    if kind == "memory":
        record = {}
        for field in CONTENT_RECORD_FIELDS:
            record[field], result["margins"][field] = predict(field)
        result["record"] = validate_content_records({"event": record})["event"]
    return result


def save_semantic_bridge_model(path, model):
    """Atomically persist a checksum-validated learned bridge with mode 0600."""
    checked = _semantic_bridge_model(model)
    target = os.path.abspath(os.fspath(path))
    parent = os.path.dirname(target)
    if not os.path.isdir(parent):
        raise FileNotFoundError("semantic bridge model parent directory does not exist")
    body = _canonical_json(checked) + b"\n"
    if len(body) > SEMANTIC_BRIDGE_MAX_MODEL_BYTES:
        raise ValueError("semantic bridge model exceeds the bounded size")
    fd, temporary = tempfile.mkstemp(prefix=".iit-semantic-bridge-", suffix=".json", dir=parent)
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


def load_semantic_bridge_model(path):
    """Load a bounded learned bridge and fail closed on schema or checksum drift."""
    target = os.path.abspath(os.fspath(path))
    size = os.path.getsize(target)
    if size <= 0 or size > SEMANTIC_BRIDGE_MAX_MODEL_BYTES:
        raise ValueError("semantic bridge model size is invalid")
    with open(target, "rb") as handle:
        raw = handle.read(SEMANTIC_BRIDGE_MAX_MODEL_BYTES + 1)
    try:
        document = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("semantic bridge model is not valid canonical JSON") from exc
    return _semantic_bridge_model(document)


def content_workspace_codebook(address_to_cue):
    """Derive the final-state -> content-address map from the frozen intrinsic core."""
    if not isinstance(address_to_cue, dict) or len(address_to_cue) != RL.N_CELL:
        raise ValueError("content workspace requires one address per intrinsic node")
    cue_to_address = {}
    for address, raw_cue in address_to_cue.items():
        address = _content_atom(address, "content address")
        cue = _state(raw_cue, "content address cue")
        if cue == 0 or cue & (cue - 1):
            raise ValueError("each content address cue must intervene on exactly one node")
        if cue in cue_to_address:
            raise ValueError("content address cues must be distinct")
        cue_to_address[cue] = address
    state_to_cue = delayed_codebook(list(cue_to_address))
    return {state: cue_to_address[cue] for state, cue in state_to_cue.items()}


def permute_content_records(records, destination_sources):
    """Permute slot addresses while preserving every registered record exactly once."""
    normalized = validate_content_records(records)
    addresses = sorted(normalized)
    if not isinstance(destination_sources, (list, tuple)) or \
            len(destination_sources) != len(addresses):
        raise ValueError("workspace permutation must contain one source per address")
    sources = [_content_atom(value, "workspace permutation source")
               for value in destination_sources]
    if sorted(sources) != addresses:
        raise ValueError("workspace permutation must be a bijection over addresses")
    return {destination: dict(normalized[source])
            for destination, source in zip(addresses, sources)}


def replace_content_record(records, address, record):
    """Return a detached store with one validated slot replaced."""
    normalized = validate_content_records(records)
    address = _content_atom(address, "content address")
    if address not in normalized:
        raise ValueError("content replacement address is not registered")
    replacement = validate_content_records({address: record})[address]
    normalized[address] = replacement
    return normalized


def content_workspace_trial(active_address, records, address_to_cue, *, delay=1,
                            permutation=(0, 1, 2), reset_before_delay=False,
                            lesion_mask=0):
    """Latch one address and select a later record from final intrinsic state only."""
    state_to_address = content_workspace_codebook(address_to_cue)
    addresses = sorted(address_to_cue)
    normalized = validate_content_records(records, addresses)
    active_address = _content_atom(active_address, "active content address")
    if active_address not in address_to_cue:
        raise ValueError("active content address is not registered")
    if isinstance(delay, bool) or not isinstance(delay, int) or delay < 1:
        raise ValueError("content workspace delay must be a positive integer")
    if not isinstance(reset_before_delay, bool):
        raise TypeError("reset_before_delay must be bool")
    p = _permutation(permutation)
    lesion_mask = _state(lesion_mask, "lesion_mask")
    core = IITDaemonCore(0)
    encoding = core.step(address_to_cue[active_address], permutation=p,
                         lesion_mask=lesion_mask)
    reset_count = 0
    if reset_before_delay:
        core = IITDaemonCore(0)
        reset_count = 1
    delay_receipts = [core.step(0, lesion_mask=lesion_mask) for _ in range(delay)]
    selected_address = state_to_address.get(core.state)
    selected_record = (dict(normalized[selected_address])
                       if selected_address is not None else None)
    return {
        "active_address": active_address,
        "encoding": encoding,
        "encoded_state": encoding["after"],
        "delay": delay,
        "delay_receipts": delay_receipts,
        "permutation": list(p),
        "reset_before_delay": reset_before_delay,
        "reset_count": reset_count,
        "lesion_mask": lesion_mask,
        "final_state": core.state,
        "state_to_address": dict(state_to_address),
        "selected_address": selected_address,
        "selected_record": selected_record,
        "tick": core.tick,
        "audit_head": core.audit_head,
        "core": core,
    }


def content_workspace_snapshot(core, records, address_to_cue):
    """Build a checksummed snapshot of intrinsic state plus addressed external content."""
    if not isinstance(core, IITDaemonCore):
        raise TypeError("content workspace snapshot needs IITDaemonCore")
    codebook = content_workspace_codebook(address_to_cue)
    normalized = validate_content_records(records, sorted(address_to_cue))
    payload = {
        "core": core.snapshot(),
        "records": normalized,
        "address_to_cue": dict(address_to_cue),
        "state_to_address": {str(state): address for state, address in codebook.items()},
    }
    return {"schema": WORKSPACE_SNAPSHOT_SCHEMA, "payload": payload,
            "sha256": _sha256(payload)}


def save_content_workspace_snapshot(path, core, records, address_to_cue):
    """Atomically persist the complete bounded workspace with mode 0600."""
    target = os.path.abspath(os.fspath(path))
    parent = os.path.dirname(target)
    if not os.path.isdir(parent):
        raise FileNotFoundError("workspace snapshot parent directory does not exist")
    body = _canonical_json(content_workspace_snapshot(
        core, records, address_to_cue)) + b"\n"
    fd, temporary = tempfile.mkstemp(prefix=".iit-workspace-", suffix=".json", dir=parent)
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


def load_content_workspace_snapshot(path):
    """Load and fail-closed validate a complete core+content workspace snapshot."""
    target = os.path.abspath(os.fspath(path))
    size = os.path.getsize(target)
    if size <= 0 or size > MAX_SNAPSHOT_BYTES:
        raise ValueError("workspace snapshot size is invalid")
    with open(target, "rb") as handle:
        raw = handle.read(MAX_SNAPSHOT_BYTES + 1)
    try:
        document = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("workspace snapshot is not valid canonical JSON") from exc
    if not isinstance(document, dict) or document.get("schema") != WORKSPACE_SNAPSHOT_SCHEMA:
        raise ValueError("unsupported workspace snapshot schema")
    payload = document.get("payload")
    if not isinstance(payload, dict) or document.get("sha256") != _sha256(payload):
        raise ValueError("workspace snapshot checksum mismatch")
    if set(payload) != {"core", "records", "address_to_cue", "state_to_address"}:
        raise ValueError("workspace snapshot payload fields mismatch")
    core = _core_from_snapshot_document(payload["core"])
    address_to_cue = payload["address_to_cue"]
    expected_codebook = content_workspace_codebook(address_to_cue)
    actual_codebook = payload["state_to_address"]
    if actual_codebook != {str(state): address
                           for state, address in expected_codebook.items()}:
        raise ValueError("workspace snapshot state/address codebook mismatch")
    records = validate_content_records(payload["records"], sorted(address_to_cue))
    return core, records, dict(address_to_cue)
