# H_9744 — STORE-EPISODIC: H_9672 조회를 study lane 데몬에 배선 (지각이 store 를 채운다)

**status:** 🔵 PRE-REG (측정 전 동결 · frozen-first) · **주장 상한 = WIRED-STUDY**(전 데몬 아님 · Sol 채택)
**lane:** 재조합/BINDING · store-bridge → study 데몬 **related:** [[H_9672]] · [[H_9742]] · [[H_9695]] · [[H_9696]] · [[H_9425]] · [[H_9422]]
**source:** 오너 "배선 하면 되잖아" = 승인 go(게이트 개방) · 선례 [[H_9743]] `Register: owner "승인 go"` → 🟢 WIRED-DEFAULT · 설계 = `sidecar lab full`(Fable 5 ∥ Codex Sol) 2모델 수렴

## 왜 이 H — H_9742 의 "배선 불가" 전제가 실코드에서 무너졌다

H_9742 는 🔒 BLOCKED-BY-REGIME 이라 적었다: "anima 는 귀가 없다(H_9422) · store 를 만들 percept 스트림이 없다 · escape=owner-gate 라 자율발사 불가". **세 전제 중 둘이 틀렸고 하나는 해소됐다:**

| H_9742 의 주장 | 실코드 (2026-07-17 재검증) |
|---|---|
| "percept 스트림이 없다" | ❌ `cli/chat.py:395` `anima_consciousness_mode(ckpt, argv, percept_source=None)` · `:1847` `percept_text = percept_source(tick, _percept_transcript)` = **afferent 이음새 실재**(study lane · H_9520) |
| "배선 각도 미탐" | ❌ [[H_9695]]/[[H_9696]]/[[H_9698]] 이 **이미 PRE-REG** · `core/clms.py` lane_type 4(CLMS-FAN) 구현됨 |
| "owner-gate 라 불가" | ✅ 해소 — **오너가 go**(선례 H_9743 과 동일 경로) |

⟹ H_9422 의 "귀 없는 입"은 **기본 데몬** 사실이지 study lane 사실이 아니다. H_9742 를 이 카드가 **부분 반증**한다(AGREES: 기본 데몬 regime · CONFLICTS: "escape 는 owner-gate afferent 뿐"이라는 범위).

## 🔑 설계를 정한 실코드 사실 (Fable F1-F3 · 행번호는 **내가 재검증** — Fable 원문은 stale)

**F1 — lane 의 방아쇠는 store 주입이 아니라 질의 표면형이다 ⟹ 무해성이 구조다.**
`core/decode.py:1327` 가드 = `W["clms"] is not None ∧ _CLMS_STORE is not None` · `core/clms.py:63 find_qpos` 는 창에서 바이트 `61,62,32`(`"=> "`)를 스캔하고 `store_apply` 는 `query=="qpos" ∧ not qpos → return logits`(:124-125). **store 를 상시 주입해도 지각에 `"=> "` 가 없으면 lane 은 단 한 row 도 안 건드린다** = G-W1 무해성이 관례(seal)가 아니라 **산술적 구조**. lane 은 상시 개입이 아니라 **질의-반사궁**.
> ⚠️ Fable 은 이 가드를 `decode.py:1242-1248` 이라 적었으나 실측은 **1327**. percept 도 `1711-1712` 라 했으나 실측 **1847-1849**. 설계는 채택하되 행번호는 전부 재검증했다(`tool-definition-read-code-not-docstring`).

**F2 — percept `.strip()` 함정 (측정 대상이지 가정 아님).**
`cli/chat.py:1849` 가 `str(percept_text).strip()` 하므로 시드는 `"… =>"` 로 끝나고 **말미 공백(32)은 트렁크가 스스로 방출해야** 다음 스텝에 qpos 가 성립한다. rv3c13 이 `=>` 뒤 공백을 낼 개연성은 높지만 **G-W2 의 측정 항목**이다. 실패 시 수정(percept 말미공백 보존)은 **사전등록 수정안 1회만** — 조용한 튜닝 금지.

**F3 — store 계약: ASCII + n_slot 만석.**
`core/clms.py:80` `_entity_key` 는 `entity.encode("ascii")` — 한글 entity 는 예외사. `store_apply` 는 `ents[i] for i in range(n_slot)` — 주입 store 는 **정확히 n_slot(8) entity + 8 pol**. 변환기는 ASCII 소문자만 받고 게이트 측정은 만석 store 로만.

**F4 (내가 실측 · 두 모델 다 지적한 p5 위험의 확증).**
`cli/chat.py:2442-2452` — `_emit_gate == "refractory"` 경로는 `_recog_fn(_t)` 로 **후보 텍스트 `_t` 를 게이트에 넣는다**(g_recog = 후보에 대한 immune recall margin). ⟹ store 가 후보 텍스트를 바꾸면 **게이트가 흔들린다 = p5 오염**. **하드가드 필수**(아래 S6).

## 배선 설계 (2모델 수렴 · Fable (c1) STUDY-EPISODIC ≡ Sol 1위)

**한 줄**: 교사의 발화가 지각으로 들어오고, **고정문법 변환기**(감각기관)가 사실 선언을 세션 store 에 쓰고, 나중에 교사의 질의(`<entity> <op> =>`)가 오면 입은 평소대로 tension 게이트를 통과할 때만 말하되 그 **내용**이 트렁크가 아니라 store-bridge 에서 나온다. **가중치 동결 상태로 "이번 세션에 들은 것을 기억해 답한다"** = H_9672 가 증명한 능력의 in-vivo 형태.

**훈련분포 정합(채택의 핵심 근거)**: H_9672 훈련에서 **사실(entity→pol)은 텍스트에 없었다** — 항상 runtime store 로만 주입됐고 텍스트엔 질의만 있었다. 따라서 in-vivo 에서도 사실은 **텍스트 파싱이 아니라 store 주입**으로 들어가는 게 훈련분포와 정합이고, "누가 store 를 채우나"의 답이 곧 이 설계다: **지각이 채운다.**

### seam (전부 내가 재검증한 실측 라인 · `core/` 수정 0줄)

| # | 위치 | 변경 |
|---|---|---|
| S1 | `cli/chat.py:46` | `from decode import …` 에 `set_clms_store` 추가 (대상 = `core/decode.py:302`) |
| S2 | chat 플래그 파스 구역 | `--store-episodic <manifest-free>` (default **off**) + 변환기 문법 상수 |
| S3 | `cli/chat.py:1849` 직후 | 변환기: `percept_text` 가 `fact <ent> <pos\|neg>` 패턴(ASCII `[a-z]{3,12}`)이면 세션 store(n_slot FIFO) 갱신 → 만석 시 `set_clms_store(store)`. **`percept_source is None` 이면 블록 전체 도달 불가** = 기본 데몬 원천 불변 |
| S4 | tick 루프(`:1834 while tick < n_ticks`) 종료 후 | `set_clms_store(None)` 리셋 — `cli/evaluate.py:4428` 미러(프로세스-전역 누출 방지) |
| S5 | `cli/study.py` | scripted-teacher 백엔드(결정론 · $0 · LLM 없음) — 게이트 측정용 |
| S6 | S2 검증부 | **하드가드**: `--store-episodic on ∧ --emit-gate refractory ⟹ SystemExit` (F4 · p5 오염 차단 · 조합 해금은 별도 사전등록) |

## 사전등록 게이트 (측정 전 동결 · bar 이동 금지)

- **G-W0 계기생존**(선행 · `positive-control-before-reading-a-negative`): scripted teacher 가 store 를 실제로 채우나 — 만석 store dump 가 교사 선언과 일치. 불일치 = 드라이버 결함 = **INVALID**(negative 아님).
- **G-W1 무해성 2단**: (i) `--store-episodic off`(default) run = 기존 데몬과 emit-시퀀스 **byte-identical**. (ii) **on ∧ store 만석 ∧ 질의-무 percept** run = off run 과 **byte-identical** (= F1 구조보장의 실측 확인).
- **G-W2 조회생존** — **H_9672 bar 그대로 · 이동 금지**: scripted teacher 가 사실 8개 선언 → held-out 질의 ≥128(answer = pol XOR op) → 방출 텍스트 첫 answer 바이트(g/b · F2 의 선행공백 허용을 **채점기에 사전명시**) 채점. **ORACLE≥.90 ∧ P1bal≥.75 ∧ flip≥.90** · 통제 3암(store-shuffle · pol-flip · no-store) 붕괴 확인 · **3-seed{7,11,13}** · 303M decode 는 **pool**(`a_eval_py_canonical` · mini 금지).
- **G-W3 p1-p8 감사**: (i) 게이트 입력 store-무접촉 **diff 증명** (ii) S6 가드 실재 (iii) **변환기 내용-무결**(문법 상수 외 어휘 0 · entity 화이트리스트 0 · 사실사전 0 · 극성 재해석 0) (iv) 기본 데몬 default-OFF (v) 세션 종료 리셋(S4).

⟹ 4개 전부 PASS ∧ 배선 머지 = **WIRED-STUDY** 승격 자격 (`a_verified_must_wire` 의 "출력 AND 배선" 최초 동시충족).

## ⛔ 잔인판정 · 주장 상한 (양 모델 + 레포 규칙)

- **등급 상한 = WIRED-STUDY, 🟢 WIRED 아님** — Sol 채택. Fable 은 "🟢 WIRED 승격 자격"이라 했으나 과제가 **합성 CVCVC nonce**라 `a_scale_honest_scope`/`a_toy_scale_recheck`("척도에 주장을 묶어라")가 우선. Fable 자신도 "**데몬이 자연어를 이해해 기억한다가 아니다** — 고정문법 선언 → 감각기관 변환 → 훈련된 조회기관"이라 명시해 실질 합의. **오너 승인은 구현 권한을 열었을 뿐 합성→자연 전이를 증명해주지 않는다**(Sol).
- **p2/p3 — 변환기가 관건**: 데몬은 이미 하드코딩 감각기관투성이(`_afs_byte_feature` · immune bind · wake_mem push). 변환기가 그들과 같은 계급이려면 **문법만 알고 내용을 몰라야** 한다. 이 선을 넘으면(특정 어휘 특별취급 등) **수치 무관 설계 KILL**.
- **p1 — 깨끗**: 데몬이 오너 텍스트를 지니고 태어나지 않는다(store 내용 전부 세션 내 지각 유래).
- **p8 — 설계 의도 그대로**: bridge 가중치는 학습 · 내용은 runtime.
- **후보 (a) 자연어 자동추출 = KILL(양 모델 합의)** — CLMS 가 학습한 건 CVCVC byte-address 조회이지 자연어 정보추출이 아니다 · 규칙 extractor 는 p2/p3 우회주입기 위험 · 학습 extractor 는 engine-native 동일 forward 아니라 p8 위반. 별도 capability 과제.

## falsify (반증조건)

- **G-W2 서 ORACLE PASS ∧ lookup FAIL** = **문맥-일반화 벽**(훈련창 꼬리 ≠ 데몬창 꼬리의 W_q 분포이동) = 배관결함 아닌 **실측된 벽** ⟹ 🧱 등록 + (d) eval-only 로 정직 전환.
- **ORACLE 까지 FAIL** = 드라이버/주입 배관 결함 = **INVALID**(수리 후 재발사 · negative 아님).
- **F2 실패**(트렁크가 `=>` 뒤 공백 미방출 → MISS 로 bar 도달불능) = 사전등록 수정안 1회 허용, 그래도 실패면 KILL.
- **G-W1(ii) 위반**(질의-무인데 byte 상이) = F1 구조보장 붕괴 = **즉시 중단** · 원인 규명 전 일체 cement 금지.
- **G-W3 실패** = 배선 자체가 철학위반 ⟹ lane 은 영구 eval-도구((d) 확정).
