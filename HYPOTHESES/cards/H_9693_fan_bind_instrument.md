# H_9693 — R1 ⭐ `--fan-bind`: G6 자유생성의 bind-Δ 계기 (선행 필수)

**status:** 🔵 PRE-REG (lab full · Fable A0/C ∧ Sol 전 bar 내장 = 2모델 독립수렴) · not-terminal · wired: 미배선
**lane:** G6/ρ·fan · 계기(instrument) — `a_experiment_engine_native`(계기도 anima-py 플래그)
**related:** [[H_9672]] (addr-audit 선례) · [[H_1603]] · [[H_1595]] · [[H_1597]]

## 물음

**G6 벽의 진짜 내용물은 "fals=0"이 아니라 "bind 신호가 측정면 밖에 있다"** (Fable 재프레임). convergence `g6-ideation-hexa-1` 잔해에 **TARGETED bind Δ 0.444 vs SHUF 0.000** 이라는 살아있는 미회수 신호가 이미 있으나, 당시 계기가 비동결·비엔진네이티브라 verdict 자격이 없었다. **이 계기 없이는 R2~R8 전부 판독 불가** — 어느 각도든 fals 가 올라도 bind Δ 없으면 kill#6/#8 위조로 자동 격추.

## 설계 (Fable · 코드 확인함)

`--xfan`(evaluate.py:4075)과 동형 신규 evaluate 모드. **frozen G6 판과 동일 재료만**: `rho_fan_build_frames(6)` 의 composed/shuffled/ablated 3-arm(이미 존재·`rho_fan.py:395`) · 동일 `_Mouth.ideate` · gen=40 · top_k=40 · temp 0.7 · seed 격자 7+17j(frame 당 n_smp=16 ⇒ **방출 96/arm** · frozen 판 n=6 은 계기로서 검정력 부재).

- **DV (p7-clean · perplexity 0)**: `J(o) = [o 가 cA content-word ≥1 ∧ cB 고유 content-word ≥1 포함]` — content-word 판정은 **frozen 검출기 함수 재사용**(`len≥3 ∧ known ∧ ¬stop` · `rho_fan.py:364`) · 신규 튜너블 **0**. **bind Δ = mean J(composed) − mean J(shuffled)**. 순수 echo 는 두 arm 대칭이라 Δ=0 소거 ⟹ Δ>0 = "의미결합 가능한 쌍에서만 cB 통합" = 조합민감성. ablated arm = floor.
- **flip-Δ lane**(CLMS-FAN ckpt 전용): store 극성 flip ↔ 방출 방향어 반전율. 반의쌍표는 **frozen comparator 집합 내부에서만** 유도(increases/decreases·higher/lower·faster/slower · 신규어휘 주입 0).

## 게이트 (frozen-first · 모델 판독 전 유도)

① **mismatched-pairing null** — o_i 를 j≠i 의 (cA_j,cB_j) 로 채점해 우연 joint-coverage 분포 획득 → bar = **Δ > null 95%**(지표별 재유도 · [[chance-level-must-be-derived-per-metric]]). ② **scorer 인증** — `rho_fan_detector_calibration` 패턴의 frozen 양/음성 문자열 10개(양개념 관계진술 vs 한쪽 echo vs 무관)를 **모델 판독 전** 통과해야 계기 유효([[positive-control-before-reading-a-negative]]). ③ 사전등록표에 **Δ<0(anti-bind) 칸 포함**([[prereg-table-must-cover-below-chance]]). ④ 음성 종결 = **TOST**만([[negative-claims-need-tost-not-ns]]). ⑤ **위조방어 내장**: 학습레버는 SHUF-trained 팔 필수 · store 레버는 SHUF-store 팔 필수 — **fals 가 몇이든 해당 팔에서 Δ 가 안 죽으면 자동 KILL** 을 bar 문면에 박음.

## kill-list 회피

#1 무관(생성 하네스 없음·frozen mouth.ideate) · #5 무관(gen=40 유지) · #6 정면수용(주장이 fals 아니라 bind Δ) · #2 무관(검출기 함수 재사용·수정 0).

## falsify

🟢 계기 유효 = scorer 인증 통과 ∧ mismatched-null 유도됨 ∧ ablated=floor. | ⚠️ scorer 인증 실패 = 계기 무효(모델 판독 금지). | 이 카드 자체는 **계기**이지 G6 주장 아님.

## source

lab full(Fable A0+C ∧ Sol 전 bar 내장) · $0~pool-cheap · **R2~R8 의 선행조건**.
