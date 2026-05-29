# HANDOFF — akida-hw-first-plasticity (2026-05-30)

> 다음 세션 인계. AKIDA HW/SW 백엔드 스위치 **HW-first** 배선 + 학습 lane
> **PLASTICITY** 도메인 신설을 ANIMA 트리에 end-to-end land 한 결과 요약.
> 상세 SSOT = [`AKIDA/HW_FIRST_INTEGRATION_2026_05_30.md`](./AKIDA/HW_FIRST_INTEGRATION_2026_05_30.md).

## 한 줄 요약

AKIDA 칩 추론/학습을 **하나의 HW-first 스위치 SSOT** 위에서 두 형제 lane 으로 가름:
**DECODER(추론·결정론·🟢 byte-identical)** ⊥ **PLASTICITY(학습·비결정론·🔴 SW≠HW 정직)**.

## land 된 PR (전부 origin/main 반영 confirmed)

| PR | # | 내용 |
|---|---|---|
| A | 1446 | PLASTICITY 도메인 신설 (PLASTICITY.md/log + DOMAINS.tape 33 domains + sibling) |
| B | 1447 | HW-first 스위치 SSOT — akida_backend_resolve_graceful + akida_provenance |
| C | 1448 | DECODER lane 배선 (AKIDA HW-first lane section + 양방향 sibling) |
| D | 1449 | PLASTICITY lane 배선 + SW 근사 learner + 🔴 비동치 verdict |
| E | 1450 | 5도메인 백링크 (MITOSIS/CHANNEL/WAKE/EEG/HW-CORE) + AKIDA boost |
| F | — | 문서 SSOT + H_679 + H_680 + AKIDA.log (this PR) |

## 핵심 결정 (6 locked, user-confirmed B + PLASTICITY)

1. **HW-first**: resolver default "hw" → 칩 도달 시 HW, 미도달 시 graceful SW (panic 아님).
2. **scope**: AKIDA/spike 경로만 HW-first. LM 텍스트 default `lora` **불변** (blast-radius 억제).
3. **2-lane**: DECODER = HW forward / SW akida_sw_lif (🟢 byte-identical 입증됨).
   PLASTICITY = HW edge-learn / SW numpy 근사 (🔴 CLOSED-NEGATIVE — 위조 동치 금지).
4. **도메인**: PLASTICITY 신설 (학습 lane 전용, DECODER 와 형제).
5. **문서**: 이 HANDOFF + AKIDA/HW_FIRST_INTEGRATION SSOT + 7 sibling + AKIDA.log + H_679/680 + memory.
6. **감사 H**: H_679 (PLASTICITY 🔴 4/4) · H_680 (DECODER 🟢 verify 5/5).

## 검증 상태

- `verify_substrate_akida.py` → **5/5 PASS** (verbatim: `.verdicts/680_decoder_hw_first/verify_substrate_akida.txt`)
- HW edge-learn 지원 실측: `edge_learning_supported=true` (BC.00.000.002, `edge_learn_probe_2026_05_22.json`)
- PLASTICITY SW≠HW: 🔴 `.verdicts/679_plasticity_hw_first/sw_hw_nonequivalence.txt`
- LM `lora` default 불변 · H_672~H_678 status 불가침.

## SSOT 코어 (재발명 금지 — 재사용)

- 스위치: `AKIDA/akida_backend.hexa` (`akida_backend_resolve` · `_graceful` · `akida_provenance`)
- decoder substrate: `HEXAD/CHAT/server/substrate_akida.py` + `akida_sw_lif.py`
- plasticity: `PLASTICITY/plasticity_lane.hexa` + `plasticity_sw_approx.py` + `SUB_ENGINES/AKIDA/scripts/edge_learn_probe.py`

## 잔여 (optional · $0)

- pi5-akida live probe: DECODER HW byte-match 재확인 + PLASTICITY few-shot 1~N shot 비결정성 정량
  → `.verdicts/`. 단일-칩 점유: `pool on pi5-akida 'systemctl --user stop spike-streamer'; sleep 2`
  → probe → `systemctl --user start spike-streamer`.

## 불가침

H_672~H_678 status · `PI5-AKIDA.json`(local-only, 미커밋) · LM `lora` default ·
`CLAUDE.md`/`project.tape`(sign-gated) · pi5-akida 공유 compute 전환 금지.
