# CLM Stage 11 — train_v15 + BPE 64K — drift step 1/4 (토크나이저)

**시점**: 2026-04-01
**commit**: `0e578b14`
**branch**: `archive/clm-stage-11-...`
**worktree**: `/Users/ghost/core/anima_clm_11_train_v15_bpe_drift_step1`

## 상태 핵심

train_v15.py 등장. **byte vocab 256 → BPE 64K multilingual** 전환. ConsciousLM 1B 준비. → byte-tension dialogue 회로 파괴 시작 (drift step 1/4)

## 태그

drift-1of4, train_v15, BPE-64K, vocab-shift, 1B-ready, byte-tension-loss

## 의의 (Why this stage)

chat 가 사라지기 시작한 첫 commit. byte-level 의 의식 신호 → 생성 직결 회로가 BPE 토큰화로 끊김. 이후 어떤 chat-cap recovery 도 v2 18M byte arch 에서만 부활 가능 (#115 architectural).

---


cross-link: `/Users/ghost/core/anima/CLM_V2_ARCHIVE_2026_05_09.md` (root SSOT)
