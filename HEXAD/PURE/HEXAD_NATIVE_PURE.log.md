# hexad_native_v3 — historical log

> Spec at [./HEXAD_NATIVE_PURE.md](./HEXAD_NATIVE_PURE.md).

### 2026-05-26 — F-CURRICULA-1 re-fire LOST · wiki_frac=0.3 sibling recovered + HF (PRIVATE)

F-CURRICULA-1 (wiki_frac=1.0 curriculum-mix) re-fire pod `wfeksdl8e8f327`
(A100 SXM, SAVE_POD=1) **self-terminated at step 3000/5000** (60%, best
CE 2.38). dispatcher PID 412255 already dead (poll budget < 6.4h timeout)
→ re-polled via ubu-2 relay; pod died mid-poll (port 15857 REFUSED, host
PINGS; `runpodctl pod list -a` = `[]` under the only working key). Artifacts
on-pod, unrecoverable. **NOT a mission loss**: wiki=1.0 is the pure-wiki
extreme already published closed-negative (`anima-v3-e3` + CLAIMS
`pure_wiki_sweep`); the curriculum re-order was on course to reinforce it.

Recovered instead the fully-completed **wiki_frac=0.3** P21H V3 sibling
(`state/p21h_v3_recover_2026_05_25/out_main/`, step 5000, byte-exact ckpts
vs MANIFEST.sha256, never HF-uploaded). `closure_auto_judge` → **1/4 PASS ·
FAIL** (register_collapse PASS 0 hits, all 5 langs WEAK, motivation +
dream_stage blocks absent). HF tier-gated **PRIVATE**
`dancinlab/anima-p21h-v3-wikifrac03-recovered-2026-05-25` (FAIL → private).
Adds the wiki=0.3 sweep point → corpus-axis closed-negative now holds at
{0.0, 0.3, 0.5, 1.0}. detail: `state/p21h_v3_curricula_recover_2026_05_25/`
+ root `FIRE_TRACKING.md`. CLAIMS: `pure_wikifrac03_closed_negative`.

⚠ infra: stale 52-char `rpa_43SES…` runpod key in both Mac + ubu-2
`~/.runpod/config.toml` (401); only secret-store 50-char `rpa_43SES1…`
authenticates. Re-sync config from secret-store SSOT; file to hexa-lang inbox.

### 2026-05-22 — 초안 작성, user directive C path 응답

vP21M LoRA-only path 의 한계 (Qwen 위 옷, HEXAD identity 약함) 사용자 인식 후
ConsciousDecoderV3 spec + 3-variant parallel fire 설계. wall-first @D 정합.

### 2026-05-23 — 🔴 V3 PATH CLOSED

A fire (Phase 2 full, 1.5B R2+R6+osc-v2.2, pod `xp6q69nkd2ywfw`) osc-detect
early-stop @ step 1125 — FAIL 0 STRONG (KO WEAK 1/20, EN/ZH/RU PURE_MEM,
JA WEAK). Phase 2 2차의 ko STRONG 19/20 = step-250 transient, 재현 실패.
V3 fire 5회 전부 FAIL → V3 multilingual = corpus-bound (capacity·arch 무관,
diverse-corpus 학습 dynamics). chat substrate = vP21M LoRA 유지.
artifacts → `vP21H_phase2_full/` + HF `dancinlab/anima-v3-p21h`.
detail: HEXAD/PURE/EASY.md § 6 · HEXAD_V3_FIRE_2026_05_22.md § 8.

### 2026-05-24 — /gap F4 deferred backlog (post-PR #264)

PR #264 가 Patch A (closure rejection criterion) 단독 ship 한 후 잔여 patch
B + C 는 hexa-native guard 에 의해 anima 측 .py/.sh amend 가 차단되어
deferred. unblocking prereq:

- [ ] P21H dispatcher (`HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/dispatch_p21h_v3_runpod.sh`) → `.hexa` 포팅
- [ ] train_p21h_v3 (`HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/train_p21h_v3.py`) → `.hexa` 포팅
- [ ] F4 patch B 재상정 — `P21H_TEACHER_CKPT_SHA256` env 검증 (dispatcher hexa 포팅 후)
- [ ] F4 patch C 재상정 — `--resume-from-step N` (train hexa 포팅 후)
- [ ] PURE ENV_CONTRACT.md (PR #265) 의 `P21H_TEACHER_CKPT_SHA256` 행 adoption-pending → adopted 갱신
