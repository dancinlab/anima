# IIT daemon R3.6 support-identifiability microaudit (2026-08-15)

Status: COMPLETE — `SUPPORT-GAP-IDENTIFIED`.

Two local batteries are now exhausted: 24 representation×classifier arms produced three frozen
passers and zero robust passers; 18 contrastive-support arms improved shortcut rejection but still
produced zero robust passers. This final microaudit asks whether another shallow local encoder is
information-supported, or whether unseen semantics require a new provenance-bearing language
support source.

## Fixed audit

The audit reuses the checksum-pinned original 702 support rows, 47 frozen rows, eight shortcut
stress rows and eight independent confirmation rows. It performs no fitting and changes no labels.
For token unigram, token bigram and positional token representations it records:

- support vocabulary and evaluation token/bigram coverage;
- OOV tokens by event kind and panel;
- exact feature-vector invariance after each OOV token is replaced by a different unseen sentinel;
- prediction invariance for the three frozen-passing ridge arms under the same replacement;
- query-trigger coverage, relation-surface coverage and atom coverage separately;
- projected-feature collisions and nearest supported label sets after OOV removal.

The audit is valid only if it reproduces both prior result checksums, all fixture counts and every
original-arm prediction checksum. `SUPPORT-GAP-IDENTIFIED` requires at least one failed confirmation
case containing one of the preregistered semantic probe tokens (`fetch`, `tell`, `never`, `not`,
`untouched`, `only`) where that token is OOV and the prediction is invariant to replacing it with a
different unseen token. Otherwise the result is `SUPPORT-GAP-NOT-IDENTIFIED`; malformed custody or
mismatch is `INVALID-SUPPORT-AUDIT`.

This does not prove that every possible neural architecture must fail. It establishes the narrower
claim that the exhausted support-vocabulary shallow family cannot learn distinctions absent from
its data. If identified, no further post-result templates, n-gram widths, classifier constants or
local shallow arms are authorized. The next step must be separately scoped data/sequence-semantic
work. 303M, IIT-mouth coupling, participant deployment and production remain blocked.

## Result

The audit reproduced both prior artifact hashes, all `702/47` fixture counts and all three original
ridge prediction hashes. The original support contains 54 token types. Token coverage is `75.81%`
on shortcut stress and `60.00%` on independent confirmation. Replacing every OOV token with a new
unseen sentinel left every prediction unchanged for all three representations.

Sixteen failed cases meet the preregistered support-gap criterion. Examples include `not` and
`only` in shortcut negatives and `fetch`, `never`, `tell`, `untouched` in confirmation. The model
continues to classify them as query or memory after the decisive word is replaced, because that
word has no learned support feature. The canonical result records `identified_case_count=16` and
ends shallow local experimentation at `BLOCKED-R36-MICRO-EXHAUSTED`.

Focused IIT/CHAT Python QA passed `91/91`. A clean isolated `anima_python-0.20.245` wheel reproduced
all three result JSON files byte-for-byte; wheel SHA-256 is `6db9ea67…366c3ca`. The same wheel was
installed into the local canonical `anima-py`, whose audit result again matched byte-for-byte. The
CHAT path was not restarted because no broker/participant code changed. Read-only verification
reports LaunchAgent `loaded=true healthy=true`, local/public HTTP `200`, and local/public WebSocket
`hello`. The existing step-45000 participant still reports `anima_alive=true`; these microstudies
neither changed nor certified it. No GPU, Vast.ai lease, model checkpoint or HF dataset was created.
