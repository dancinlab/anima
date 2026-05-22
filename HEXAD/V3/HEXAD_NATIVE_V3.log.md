# hexad_native_v3 — historical log

> Spec at [./HEXAD_NATIVE_V3.md](./HEXAD_NATIVE_V3.md).

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
detail: HEXAD/V3/EASY.md § 6 · HEXAD_V3_FIRE_2026_05_22.md § 8.

### 2026-05-23 — 코퍼스축 fire (E3/E2) — CLOSED 완전

§ 8.6 closure 가 R1-R7 sweep 내내 코퍼스 비율 (`wiki_frac=0.3`) 을 한 번도
변경 안 한 채 코퍼스를 범인으로 지목한 logical gap → 마지막 미검증 축
sweep. E3 (anima 0%, `P21H_WIKI_FRAC=1.0`, pod `xhjxwzrpadm89y`) + E2
(anima 50%, `P21H_WIKI_FRAC=0.5`, pod `fguxy010l1wtmu`) 병렬 fire — A-fire
decisive recipe 그대로, env-var override only (신규 .py/.sh 0). 둘 다
A100-SXM, osc-detect v2.2, 둘 다 osc-stop @ step 1125.

E3 FAIL 0S/1P/4W — `anima_register_hits` 11/20 (A) → **0/20**, register
collapse 소멸 (§ 8.6 메커니즘 진단 검증). 그러나 register 0 인데도 EN/ZH/
RU/JA 4 langs WEAK, final_CE 6.55 — multilingual underfit (Chinchilla
under-budget). E3 "KO PARTIAL 15/20" 은 coherence-metric 산물 (native-
script digit loop). E2 FAIL 0S/0P/5W — register hits 9/20, 50% anima 만
으로 collapse 거의 복귀.

corpus axis VINDICATED 실패 → V3 fire 7 회 0 PASS, 전 축 (scale R1 ·
mitosis R2 · head_g R4 · pool R6 · step R7 · corpus E2/E3) 소진. V3
blocker = register collapse + Chinchilla under-budget 이중 구속.
artifacts → `vP21H_e3/` + `vP21H_e2/` + HF `dancinlab/anima-v3-e3` ·
`dancinlab/anima-v3-e2`. detail: HEXAD_V3_FIRE_2026_05_22.md § 9.
