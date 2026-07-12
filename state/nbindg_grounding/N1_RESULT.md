# NBIND-G N1 결과 — carrier-transfer 사다리 (🟢-dir CARRIER-ROBUST · 2026-07-12)

**측정**: 기존 H_9272 main ckpt(`nbind_main_s7.clm`·303M) · summer RTX5070 GPU(default-on) · $0 ·
`anima-py evaluate --xbind` · seed 7 · 재학습 없음. 동일 40 held-out (p,form) 셀, carrier만 3레벨.

| carrier level | carrier | held-out D-acc | margin_med | margin_pos | sampled_maj |
|---|---|---|---|---|---|
| **C0** 학습 프레임 | `이 영화 <surf> =>` | **0.750** | 3.152 | 0.675 | 0.75 |
| **C1** 근전이 | `<대체 영화도메인 명사구> <surf> =>` | **0.675** | 4.036 | 0.725 | 0.65 |
| **C2** wild-natural | `<verbatim 실제 NSMC 리뷰> <surf> =>` | **0.700** | 8.525 | 0.700 | 0.70 |

## 판정 = 🟢-dir CARRIER-ROBUST (FORMAT-🧱 반증)
사전동결 로직 그대로:
- **C0 0.750** → H_9272 재현 기준 0.700±0.10 안 → **harness/ckpt VALID**(not INVALID). (0.75 vs 0.70 = span-sampling
  노이즈, n=40 SE≈0.077 안.)
- **CARRIER-ROBUST bar**(C1·C2 ≥ C0−0.10 = 0.650): C1 0.675 ✅ · C2 0.700 ✅ → **충족**.
- **FORMAT-🧱 bar**(C1/C2 ≤0.55 chance 붕괴): **미발동**(둘 다 0.65 이상).

⟹ grid가 학습한 XOR flip 연산자는 **literal "이 영화" 학습 프레임에 구속되지 않는다**. carrier 명사구를 바꿔도
(근전이 0.675), 심지어 **관계없는 실제 NSMC 리뷰를 앞에 통째로 붙여도**(wild-natural 0.700) 합성이 유지된다.
연산자가 memorized template이 아니라 **carrier-general operation**임을 실증 = **H_9272 강화**(단순 template-match
아님을 배제).

## scope honesty (중요 · 소급 불변)
- 이것은 **grounded grid atom(20개·모델이 pol 학습완료)의 carrier 전이**다. **atom-GROUNDING 전이 아님** —
  극성이 자연 분포서만 접지된 P_nat 원자는 이 ckpt에 접지 소스가 없어 측정 불가(=N2 spend-gated).
- N1이 답한 것 = **"연산자 설치가 프레임-general"** (grounding 전이의 전제조건 = 확인됨). grounding 본체
  (feature-from-nature) = N2.
- margin_med가 C2(8.53) ≫ C0(3.15)로 큰 것은 흥미로우나 **context 길이 차(리뷰 prepend로 토큰↑)가 NLL
  스케일을 밀었을 가능성** — 절대 margin은 레벨 간 직접비교 불가. robust 신호 = D-acc(0.70~0.75 전 레벨 유사).
- 어떤 결과든 H_9267 CRACK · H_9272 DIRECTIONAL 소급 불변.

## infra 격리 (verdict 무영향 · verdict-integrity)
- summer 설치 anima-py **stale**: line 1399 `json.dump(res, open(out_path,"w"), ensure_ascii=False)` = origin/main
  1413의 `_json_safe(res)`+`encoding=utf-8` 수정(evaluate-py-11) **미반영** → out-json write가 byte-LM raw
  surrogate로 크래시. **summary D-acc는 write 전에 print되어 clean**(로그 `log_C{0,1,2}.txt` 보존). 결과는 clean
  summary 위에만 섬(infra-wall-noneval). fix = summer anima-py를 origin/main으로 재설치(N2 대비 opportunistic).
- 1차 run은 ssh 파이프 non-utf8 로케일 stdout 크래시 → `PYTHONUTF8=1 LC_ALL=C.UTF-8`로 해소(재측정 clean).

## 원시
`state/nbindg_grounding/`: gen_nbindg.py · nbindg_carrier_ladder_manifest.json · nbindg_C{0,1,2}.json ·
log_C{0,1,2}.txt(summary) · N0_AUDIT.json · P_nat_freeze.json. ckpt = summer `~/nbind_mig/nbind_main_s7.clm`.
