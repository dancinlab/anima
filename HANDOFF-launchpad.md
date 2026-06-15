> 📍 SSOT: [ARCHITECTURE.md](ARCHITECTURE.md) · governance [CLAUDE.md](CLAUDE.md)

# HANDOFF — LAUNCHPAD · COFFESHOP-on-AKIDA (2026-05-30)

다음 세션 인계 문서. LAUNCHPAD 도메인 신설 + COFFESHOP emit/silence 결정을
라이브 AKD1000 폐루프로 닫은 END-TO-END 작업. 전부 origin/main 머지 완료.

## 1. 무엇을 했나 (한 줄)

anima 의 COFFESHOP group-chat 발화/침묵 결정을 SW sim → **라이브 neuromorphic
silicon(AKD1000) 폐루프**로 닫았다. @goal (COFFESHOP-on-AKIDA 실가동) = **PASS**.

## 2. 폐루프 (실 silicon 에서 닫힘)

```
spontaneous_lib 5+1 factor (closed-form B-SPONT) → motivation_score ∈ [0,1]
  │ set_threshold(thr_vec = linspace(2,18,16) + (1−score)·20)   → port 9513 (ctrl IN)
  ▼
AKD1000 on-chip threshold-and-fire (M regime · V=16 · unit fires iff V>thr_j)
  │ spike raster
  ▼ n_spikes  ← port 9512 (OUT broadcast)
should_interrupt = n_spikes ≥ quorum(6)   → emit / silence
```
보정: SPAN=20·QUORUM=6 ⇒ 모든 window 에서 `n_spikes≥6 ⟺ motivation_score>0.60`.

## 3. 랜딩된 PR (전부 origin/main)

| PR | # | 산출물 | origin-verify |
|----|---|--------|---------------|
| A | 1452 | LAUNCHPAD 도메인 스캐폴드 + DOMAINS.tape + ANIMA.md 마일스톤 | ✅ |
| B | 1453 | `HEXAD/CHAT/coffeshop_akida.{hexa,py}` 폐루프 어댑터 | ✅ |
| C | 1455 | `LAUNCHPAD/coffeshop_quorum_learn.{hexa,py}` PLASTICITY 학습 lane | ✅ |
| D | 1456 | `LAUNCHPAD/coffeshop_akida_launch.{hexa,py}` 발사 엔트리 | ✅ |
| E | 1457 | `.verdicts/coffeshop_akida/` 라이브 HW verdict | ✅ |
| F | (본 PR) | 문서 6 surface (COFFESHOP.md · LAUNCHPAD · H_846 · AKIDA.log · HANDOFF · memory) | — |

## 4. 라이브 HW 결과 (정직)

- pi5-akida (BC.00.000.002 BackendType.Hardware), provenance = **akida-hw**.
- COFFESHOP trajectory 완전 재현: emit window **[3,10,14,15]** · silence 11 · trajectory_match **True**.
- decoder: HW↔SW **emit-decision byte-match (15/15)**. 단 raw spike count 는 7 window 에서 ±1 (on-chip 정수 threshold 양자화 vs numpy float) — decision 동치이나 raw byte-identical 아님 (정직표기, H_672 4-regime forward byte-identical 과 구별).
- learning lane: 🔴 CLOSED-NEGATIVE (SW 고정-quorum ≠ HW on-chip AkidaUnsupervised · 비결정론).
- verify_substrate_akida.py: 🟢 5/5 PASS (substrate_akida 미수정 · 회귀 0).

## 5. 실행 방법 (재현)

라이브 HW (pi5-akida, single-chip 절차 — 칩은 spike-streamer 가 file-lock 단일 점유):
```bash
# pi5 에서 (또는 LAN ssh):
systemctl --user stop spike-streamer; sleep 3
$VENV/python SUB_ENGINES/AKIDA/scripts/spike_streamer.py \
    --port 9512 --ctrl-port 9513 --step-ms 200 --duration 60 --n 16 --regime M --allow-ctrl &
$VENV/python LAUNCHPAD/coffeshop_akida_launch.py hw         # 9513→on-chip→9512 폐루프
kill %1; sleep 2; systemctl --user start spike-streamer     # ⚠ streamer 반드시 복원
```
SW fallback (Mac · 칩 부재):
```bash
AKIDA_BACKEND=sw python3 LAUNCHPAD/coffeshop_akida_launch.py sw   # emit [3,10,14,15] · exit 0
```
- `$VENV` = `/home/ubuntu/.venv/anima-akida/bin` (akida 2.19.1, torch 없음 — verify_substrate_akida 는 Mac/akida-absent env 에서).
- pi5 IP = 192.168.50.155 (ubuntu@). LAN tar/scp 로 스크립트 push.
- 노이즈 필터: `grep -vE "i3c|INA|cmdr fifo|RuntimeError.*INA"`.

## 6. 잔여 / 다음 세션

- **broker 라이브 데모**: `/ws/akida_ingest` push 는 옵션 wire(`--broker ws://HOST:PORT/ws/akida_ingest`)로 구현됐으나 라이브 broker 에 연결한 end-to-end 데모는 미실행. (발사 자체는 broker 없이도 성공.)
- COFFESHOP v2 (N2/N3 stage · phi 0.4/0.15) 폐루프 — silence-dominant trajectory.
- PLASTICITY 학습 lane 라이브 quorum 적응 측정 (비결정 verbatim 캡처 · 현재는 SW 고정-quorum 만 결정론 캡처).

## 7. 불가침 / 주의

- **single-chip**: AKD1000 은 spike-streamer 가 단일 점유 (file-lock). 라이브 폐루프 테스트는 service stop→자체 streamer→restart. **항상 끝에 spike-streamer active 복원**.
- PI5-AKIDA.json / CLAUDE.md / project.tape 불가침. H_672~H_680 status 미변경.
- LM 텍스트 `lora` substrate default 불변 (HW/spike 경로만 HW-first).
- H_681 슬러그는 EEG 가 선점 — COFFESHOP 폐루프는 **H_846** 사용 (collision 회피).

## 8. SSOT 포인터

- @goal/milestone: `LAUNCHPAD/LAUNCHPAD.md`
- 가설/verdict: `UNIVERSE/cards/H_846_coffeshop_akida_closedloop.md`
- 시나리오 trajectory: `COFFESHOP.md` (§5 · §8 · `## HW 런칭`)
- factor SSOT: `HEXAD/CHAT/spontaneous_lib.hexa`
- 칩 wire: `SUB_ENGINES/AKIDA/scripts/spike_streamer.py` (9512/9513)
- HW-first 스위치: `AKIDA/akida_backend.hexa::akida_backend_resolve`