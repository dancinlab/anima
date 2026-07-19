# H_9763 — R8-3 · 지속-lane CONTENT TRANSPLANT (kosmos file-swap) — content-∀ 봉인 + H_9762 positive control 겸용

**status:** 🔵 PROPOSED (lab full Fable 5 심화 · R8 · pool · 직렬화 API 불요 — 파일 스왑 · H_9761 이 (b)-lane 확정 후 발사)
**lane:** theta-alive-sigma-rebase (interior-부재 SUFFICIENT · cross-session 채널 봉인)
**related:** [[H_9738]] · [[H_9749]] · [[H_9761]] · [[H_9762]]

## ① 한 줄 주장 (반증가능)

cross-session persistence 의 유일 carrier = 디스크 표면(`.kosmos` dir · `core/kosmos_io.py` — H_9761 (b)-lane 목록으로 확정).
donor 데몬의 지속-lane **내용 전체를 스왑**(file copy — opaque hexa 핸들 직렬화 불요)한 뒤 고정 public future 로 재구동하면
own==donor 궤적이 t≤N−W 에 exact relock = 그 lane 의 private capacity 0. **content-∀ ⊇ history-∀**: 임의 내용은
어떤 history 로 도달가능한 내용의 상위집합 — H_9762 가 못 닫는 "미검정 prefix 의 latch" 꼬리를 lane 단위로 전수 봉인.

## ② H_9762 와의 겸용 (positive-control arm)

swap 이 공통 phase 초기창에서 **발산 자체를 못 만들면**: 정적 read-path 추적으로 이중확인 →
kosmos 가 mouth/emit 경로에서 **read 되지 않으면**(write-only) = efficacious interior carrier 아님 (같은 결론 · 다른 경로 · 그 자체 판정).
read-path 살아있는데 발산 0 = INSTRUMENT-DEAD (스왑 내용 대비 강화 재발사).

## ③ 조작 (engine-native)

동일 ckpt 데몬 2개를 상이 history 로 구동해 상이 `.kosmos` dir 생성(사전 file-diff 로 상이함 증명) →
- **swap**: A 에 B 의 dir 이식(파일 복사)
- **sham**: A 에 A 자신의 dir 재복사 (copy-artifact 통제 · mtime/inode confound 제거)
- **no-swap**: 원본 그대로 (C0 baseline)
- **scramble**: B 내용을 구조보존 셔플 (내용 vs 형식 분리 통제)
→ 4 arm 전부 동일 `--percept-script` N tick → `ANIMA_DECISION_TRACE` diff. kosmos dir 경로는 기존 config/flag 재사용, 부재 시 `--kosmos-dir` 플래그 1개 신설(a_experiment_engine_native).

## ④ 사전등록 판정식 (상수 L·W·N = H_9761 유도 · H_9762 와 동일 metric)

- **washout(주장 지지)**: swap∧scramble 이 sham 대비 초기창 TIER-1 발산 생성 **후** t≤N−W exact relock ∧ sham≡no-swap d≡0.
- **INTERIOR-CANDIDATE**: swap 발산이 지평 N 유지 — kosmos = 후보 carrier(프런티어 재개봉 · 다음 H = 어떤 내용 성분이 잔류를 나르나).
- **carrier 아님(read-dead 경로)**: 발산 0 ∧ 정적 read-path dead 확증.
- sham 이 no-swap 과 불일치 = copy-artifact — INSTRUMENT 결함, 판정 금지.

## ⑤ falsify
지속 발산 = 반증(= 발견). tune-to-green 불가 — bar exact0 · arm 구조 사전등록 · 상수 코드유도.

## kill-list 구분 (H_9738 재생성 아님)
죽은 각 = **상상 텍스트→저장**(certificate 0 byte)·**상상 조성→미래**(own==donor). 본 카드의 객체는 상상이 아니라
**persistence lane 의 저장 내용 자체** — H_9738 이 W_S 에서 연 transplant 방법론의 다른-객체 확장이지 동일각 재생성이 아님.
