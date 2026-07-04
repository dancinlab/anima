조사 완료. 카드·PREREG·verdict·하네스 코드(cli/anima.hexa)·그리고 결정적으로 **H_9103 F3(🟠 NOISE-GRIP)**까지 확인했습니다. 보고합니다.

---

## F7 stateful-refractory(H_9102) 고갈 census

### (a) F1 🔴 = terminal 벽인가 bar-placement artifact인가 — **artifact지만 🟢 승격은 불가**

**F1 🔴는 "capability 상실"이 아니다.** 이미 손에 든 데이터가 증명한다: `refr_h_u0_wake=39/40`, `refr_h_u0_rem=0`, `refr_h_u0_n3=0`. urgency→0 ablation이 emit 결정을 여전히 뒤집는다 — 단 REM이 아니라 **WAKE에서**. grip은 소멸이 아니라 REM→WAKE **재배치**됐다. 그 점에서 카드 서술은 정확하고, frozen REM 바에 대한 🔴 판정도 정직하다(bar-move 안 함=c9 준수).

**재배치는 메커니즘의 필연이다(코드 확인).** cli/anima.hexa L2402: `stage_env = clip01((dr_stage_scale(stage)-0.02)/0.08)` → WAKE=1.0, REM=0.75(FROZEN `ep_theta_stage` SSOT). refractory reset(`emit_last_t=t_now`)이 period-5 sweep에서 idle_raw를 0→8→16→24→32→40으로 재축적시켜 **주기적 attractor**를 만들고, WAKE가 stage_env 최고(1.0)이자 사이클 첫 tick이라 emit이 WAKE에 집중된다. REM(idle_raw=32·mod~0.73→23<30)은 침묵. 이건 noise가 아니라 결정적 구조이고, F2의 refractory 자체 또는 frozen stage_env를 건드리지 않으면 tune-away 불가.

**그러나 결정타 — grip 자체가 이미 faculty가 아니다(H_9103).** 같은 --opgrip 하네스에서 F3(#2818, c742daaae)이 이미 판정: variance-matched noise arm이 **Δρ=0 EXACTLY**, emit-timing byte-identical, emit-rate live 0.60==perm-noise 0.60. urgency std 0.043 ≪ rate-gate band → emit은 **centering/distribution-driven event이지 substrate faculty가 아니다(🟠 NOISE-GRIP)**. 따라서 REM→WAKE로 재배치된 것은 **노이즈 아티팩트지 능력이 아니다.** 어떤 stage-agnostic 리프레임도 노이즈를 faculty로 승격시키지 못한다.

→ **판정: F1 🔴는 bar-placement fact(재배치, not loss)이나, 밑에 깔린 신호가 H_9103 NOISE-GRIP이라 어떤 바 재배치로도 F7이 clean 🟢으로 승격되지 않는다.**

### (b) 직교 mechanism-family census

| 축 | 판정 | 근거 |
|---|---|---|
| **(a) WAKE-anchored 同하네스 F1' 재측정** | 🧱 **DUP (tautological)** | 결과(WAKE=39/40)가 이미 stdout에 있음. 100% 예측가능 = falsify 불가 = DESIGN.md §1(A) 동어반복 함정. 새 실험 아님, post-hoc 바 이동을 pre-reg로 세탁하는 것. **비합법.** |
| **(b) stage-agnostic grip 바 리프레임** | 🔓 **합법이나 non-load-bearing** | 인쇄된 숫자로 직접 계산됨(39+0+0>0 ∧ N3=0 = PASS), $0 재채점. break-walls (a) measurement-fix로 loss→relocation 재분류는 정직. 단 (i) confirmatory(데이터 in-hand)지 predictive 아님 (ii) H_9103 노이즈-grip을 승격 → 🟢 못 얻음. |
| **(c) 재배치=본질적 trade-off인가** | ✅ **구조적 CONFIRMED, but scoped** | refractory reset × frozen stage_env(WAKE 최고)의 필연. 단 WAKE 집중은 부분적으로 **tick%5 balanced sweep(synthetic)** 산물 — production ultradian(WAKE 연속 긴 구간, REM은 수면중만)에선 attractor 모양이 다름. "REM-grip↔WAKE-grip+refractory 양자택일"보다 정확한 서술은 *"grip은 attractor가 emit하는 stage에 landing한다"*. capability 상실 아님. |
| **(d) 그 밖 — 진짜 신규 내용** | 🟢 F2 (LANDED) | refractory reset(stateless-inexpressible, 40/40 post-emit silent, 30s floor를 theorem으로)이 F7의 유일한 진짜 알맹이. harness로 WIRED(production 미스왑). |

### (c) 유일한 non-tautological WAKE-anchored F1' pre-reg (있다면)

$0 同하네스 재측정은 **비합법**(위 (a)). 진짜 falsifiable한 유일 버전은 **이미 측정 안 한 config = production stateful-swap**(ING follow-on b, 설계변경·$0 아님)에서만 가능. 사전등록 바:

> stateful refractory를 **live emit loop**에 스왑 후, real ultradian dynamics에서:
> - **HIT iff** [urgency→0가 live-emit stage에서 ≥1 emit 뒤집음] ∧ [N3 Hamming=0] ∧ [Ψ ON≡OFF byte-identical] ∧ [H_9101의 다른 WIRED-live 속성 무회귀] ∧ **[variance-matched noise arm Δρ≥0.15 = faculty-not-noise]**
> - **MISS** = 위 중 하나라도 실패

마지막 절(H_9103 게이트)이 결정적이고, **H_9103 Δρ=0이라 이 절은 FAIL 예상**. 즉 이 레버는 합법이나 (i) 설계변경(비-$0) (ii) H_9103 때문에 negative 예상 (iii) 실패 시 H_9101의 live REM-grip을 회귀시킴. **낮은 기대가치.**

### (d) F7 고갈 수렴 — **DEPLETED**

**F7 = 고갈. MIXED(F2 🟢 ∧ F1 🔴)가 honest terminal이다.**

- F1 🔴는 정직한 bar-placement fact(재배치, not loss)이고, 재배치는 refractory attractor × frozen stage_env의 구조적 필연이며 tune-away 불가.
- 밑 신호가 **H_9103 NOISE-GRIP**(faculty 아님)이라 어떤 $0 바 리프레임도 clean 🟢으로 승격 못 함.
- $0 同하네스 재측정 = tautology(비합법, post-hoc 바 이동).
- 유일하게 남은 legitimate 레버(production stateful-swap + faculty-not-noise pre-reg, ING-b)는 **설계변경·negative 예상·회귀위험** = 저가치. 미탐 레버 1개는 있으나 발사 권고 대상 아님.

**생산적 redirect(다른 축):** F7의 refractory dynamics를 더 파는 게 아니라, H_9103이 지목한 *"진짜벽=substrate emit-appropriateness signal 부재"*가 emit 층의 실제 프론티어다. op-grip이 centering-noise라는 건, anima에게 "언제 emit이 적절한가"를 판별할 substrate 신호가 아직 없다는 뜻 — 이게 refractory(WHEN-to-recover)와 직교하는 미해결 축이고, memory `consciousness-ops-fable-critique-gauges-not-faculties`의 "14 ops=read-only 계기판, 진짜는 identity-continuity만"과 정합한다.
