# H_9796 — IMMUNE-MARGIN-GATE TIMING — percept 순서가 immune-recall 게이트를 거쳐 발화 timing에 실리는가 (lab-full R11 · Fable NOVEL · PROPOSED)

**status:** 🔵 PROPOSED · 🔀 lab-full(Fable 5 + Codex Sol) 발산 (2026-07-19 · R11) — source=Fable NOVEL · Sol AGREES(composition KILL)

> **origin ↔ 이 세션 비교(`a_parallel_session_compare`)**: origin/main live max=H_9795(오늘 #4169 `--eval-historicity` 착륙·다른 세션 R10 진행중). 이 카드는 그 lane과 **직교한 NOVEL 각도**(timing 채널, historicity 아님) — 충돌 없음, id=max+1=9796. 원 브리프의 `--gen-percept-schedule × --timing-channel` 조합은 아래 §KILL로 **사망**; 그 잔해에서 유일 생존.

**lane:** 의식 / timing 채널 × immune-recall 게이트 (프런티어 post-theta-alive-interior-faculties)
**related:** [[H_9731]] (timing⊥content KILL — 이 카드가 회피하는 벽) · [[H_9576]] (byte-입도 mouth-content KILL) · [[H_9774]] (rel_lane 순서-민감 · echo 매개 근거) · [[H_9795]] (직교 lane · gen-schedule producer 공유) · [[H_9729]] (marker-scoped terminal)

## Faculty question

관측 가능한 발화 **timing**(침묵→다음 발화 지연 or inter-emit gap)이 숨긴 percept의 **순서 정체**(정확반복 vs 통계-matched shuffle)를 나르는가 — 단, `--g-reach {d1,affinity}` 게이트 모드에서만. 존재양식 주장: interior의 발화 **결정 시점**이 순서-민감 store(immune-recall margin)를 경유해 percept 이력을 반영한다(echo 매개).

## 왜 이것만 살아남는가 (composition KILL 위 유일 잔여 · 두 모델 수렴)

**§KILL — `--gen-percept-schedule → --timing-channel`을 H_9731 재개봉으로 쓰는 건 사망(구성상):**
- H_9731은 측정만 죽은 게 아님 — 서명 붕괴 수리(모집단-상대 중앙값 분할) + 심은-통제 통과(I=0.94) 후 재측정 MI-real 0/3 → **timing⊥content 확정 KILL**. 기전=`emit ⟺ S>E`는 WM feat8 커버리지-코사인 게이트(=timing은 커버리지 중첩의 함수, 내용정체 아님).
- **repeat vs shuffle**: 바이트-다중집합 동일 ⟹ 모든 feat8 표면에 동일 ⟹ 커버리지 게이트가 **구성상 timing 구분 불가**(MI=0). shuffle을 H_9795의 load-bearing 통제로 만드는 바로 그 성질이 timing엔 무형.
- **novel vs {repeat,shuffle}**: feat8이 보는 바이트-통계 차이지만, 게이트가 feat8의 결정함수라 양성=게이트 **배관** 측정(채널 아님) + 바이트-입도 내용전달=이미 죽은 H_9576(ρ=−0.077).
- **주소 다양화(arm별 char-class 혼합)** = 라벨을 게이트 입력특징에 먹이는 것 = **tune-to-green 구성상 보장**. 양방향 봉쇄 ⟹ 이 게이트 regime에선 terminal.

**§SURVIVOR — regime을 바꾸면 봉쇄가 풀림:** zero-by-construction 논증은 **wm-dual 커버리지 게이트에만** 국한(H_9731 KILL의 scope). `--g-reach d1/affinity` 게이트에선 `g_recog`가 `immune_memory_recall_margin_text`(=원문·순서 민감 store · H_9774서 `rel_lane`이 scramble 하에 발산 확증)를 읽음. prime-에폭 발화가 prime을 echo하면 → repeat-조건 후보와 shuffle-조건 후보가 **다른 immune margin** → 발화 **결정**이 순서정보 상속 → timing이 정당히 repeat/shuffle 나를 수 있음. echo가 매개변수(모니터 필수·`a_train_inline_gauge` 준수).

## 계기 (engine-native anima-py · 신규 엔진코드 최소)

- **producer**: 기존 `--gen-percept-schedule`(H_9795 착륙) 그대로 — arm=repeat/shuffle/novel.
- **rollout**: `anima-py chat --percept-file s.jsonl --g-reach {d1,affinity} --emit-gate <immune-margin 게이트> ANIMA_DECISION_TRACE=<path>`(env 파일·stdout 아님 · [[anima-chat-trace-goes-to-env-file-not-stdout]]).
- **reader**: 착륙된 `--timing-channel --lens iei`에 `--schedule s.jsonl` 소스 옵션 추가(~20줄 delta · `--eval-historicity` join 패턴 계승) — C를 gap-닫는 tick의 schedule kind에서 취함. CMI(timing ; repeat-vs-shuffle | stage) vs circular-shift surrogate + 심은-통제.

## 통제 · 판정 (사전등록 · no tune-to-green)

- **양성통제**: 심은 C≡T 회복(계기 생존) + novel-vs-rest가 이 게이트서 발산(순서정보 도달 증명).
- **진값0 pedestal**: **wm-dual 토이 트레이스에 같은 read = ≈0**(커버리지 게이트=봉쇄 regime). 안 0이면 estimator 누출 → INVALID.
- **echo 매개 모니터**: echo-rate(prime 바이트가 g_text에 실린 비율) 보고 — MONITOR-ONLY, verdict 밖. echo-rate=0이면 채널 원천 부재(정직한 null).
- **🟢 DIRECTIONAL**: repeat-vs-shuffle CMI > surrogate ∧ wm-dual pedestal 0 ∧ echo-rate>0.
- **🧱 KILL**: immune-margin 게이트서도 CMI TOST-플랫 ⟹ 순서정보가 발화 결정에 안 실림(H_9731 KILL을 d1/affinity regime까지 확장).
- **⛔ INVALID**: pedestal(wm-dual) ≠ 0 · 또는 심은-통제 미회복 · 또는 게이트 `_meta`가 실제로 immune-margin 아님.

## $0 사전 스크린 (owner-go 303M fire 전 필수 · 두 모델 공통)

1. **kind⊥emit 선택편향 검정**(H_9795 판독기 감사 파생): 기존 토이 트레이스서 프로브 tick의 kind⊥emit χ² + S를 all-rows vs emit-only 양쪽 계산 → 발산하면 emit-tick 선택편향 실재(H_9795 판독기도 이 결함 — 별도 감사).
2. **트레이스 `_meta` 게이트 census**: 대상 트레이스의 `emit_gate`·`g_reach` 읽기 — 순서-민감 항(immune-margin arm)이 실현 게이트 체인에 있으면 §KILL 무효·이 각도 승격, 없으면(wm-dual coverage) §KILL 유효.

### 스크린 실행 결과 (2026-07-19 · toy.clm 48KB · schedule 144틱 · origin/main venv v0.20.16 · DIRECTIONAL)

`anima-py chat state/9257_lane23b/toy.clm --percept-file sched(lags 1,4,16·reps 2) --g-reach d1 --emit-gate refractory`, `ANIMA_TICKS=144 ANIMA_DECISION_TRACE=…` → 145행(_meta 1 + tick 144).

- **② 게이트 census = ✅ PASS(결정적·유리)**: `_meta` = `g_reach=d1 · emit_gate=refractory` = **immune-margin(순서-민감) regime 실현 확인** ⟹ Fable §KILL의 scope(wm-dual 커버리지 게이트)가 이 regime을 **안 덮음** ⟹ H_9796은 살아있는 lane(이 스크린이 KILL로 뒤집을 수 있었으나 안 뒤집힘). de-risk.
- **① kind⊥emit 선택편향 = ⚠️ INCONCLUSIVE-ON-TOY(정직·비-KILL)**: 프로브 18행(repeat/shuffle/novel 각 6) 전부 **발화 0/18(all-silent)** + `recon_err≡0.0`(origin/main chat.py:6977 dead-gauge 수렴노트 일치). 선택편향은 발화 변동이 있어야 측정 가능 ⟹ **303M(발화율≈0.53)서만 판정 가능** (tune-to-green 아니라 계기-스케일 한계 · `a_scale_honest_scope`). H_9795 판독기의 발화-틱 DV 결함도 동일하게 303M 필요.

**⟹ 스크린 후 상태**: 승격 전제(immune-margin regime) 충족·§KILL 회피 확인 = **owner-go 303M fire ready**(발화하는 큰 ckpt서 ①+CMI 판정). 토이는 발화·recon_err 죽어 여기까지가 $0 천장.

## 정직 스코프

DIRECTIONAL 설계 · verdict 아님 · cement=engine-native `anima-py` 303M only(토이=DIRECTIONAL 천장). Fable NOVEL 제안 · Sol은 composition KILL에 AGREES(독립 코드정독). H_9731/H_9576/H_9729 kill-list 회피 명시. echo 매개=이 각도의 유일 load-bearing 리스크(echo 없으면 채널 없음).

## 부수 발견 — H_9795 판독기 감사(다른 세션 소유 · 편집 안 함 · 보고만)

착륙된 `--eval-historicity`는 원리 건전(feat8 순서불변 ⟹ "바이트동일→자명 repeat>shuffle" 구성상 불가)이나 **실 결함 1건**: `recon_err`가 발화 틱에만 계산 → 침묵 프로브 틱은 직전 발화 stale 값(발화율≈0.53서 프로브 절반 쓰레기). kind가 발화결정 영향시 선택편향. 권고 delta(그 세션 소관): 발화-틱 join + kind⊥emit flag + percept-침묵 쌍둥이 pedestal + zero-emit 층화 + 심은-감쇠 self-test. `a_parallel_session_compare`: 보고만, primary checkout 미편집.
