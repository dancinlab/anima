# H_9612 — GN-bus confound verdict 감사 — GN-Bus Confound · Verdict Audit (fable R3-A2 · R3 · 🔴 LIVE — A1 PASS-live 로 발화)

**status:** 🔴 LIVE (게이트 통과 · [[H_9611]] A1 PASS-live 가 발화시킴 · 2026-07-16 · 미실행) — source=fable R3-A2
**lane:** BINDING / GroupNorm 전역 bus 채널 (R3 신규 whitespace)
**related:** [[H_9611]] · [[H_9359]] · [[H_9331]] · [[H_9235]] · source: lab full R3 (fable R3-A2)

**아이디어**: cement 된 far-context verdict 중 ≥1 개가 **binding 이라 귀속한 것이 실은 GN 재정규화**였을 수 있다.
**메커니즘**: $0 재분석 — 마지막위치 hidden 을 RF≈35 넘는 문맥과 함께 읽은 verdict 열거(H_9359 transplant · H_9331 swap-patch · H_9235 ρ·weave) → `--gn-freeze` 하 재채점.
**$0 pre-screen**: [[H_9611]] 이 inert 반환하면 **DOA** — 쓰지 말 것(엄격히 A1 하류).
**판정표**: C1 **양성통제**=효과가 전부 RF 내인 verdict 는 gn-freeze 에 **불변**이어야(감사가 전부 날리는 게 아님 증명) · C2 순열 null. det-noise 넘게 움직인 verdict = confound 발견 → **재개(re-open)**, 재-cement 아님.
**distinct**: `byte-identical-anchor-cert-hides-the-bug`(틀린 식이 byte-id 인증) 아님 — 이건 **옳은 식**의 채널 오귀속.
**verdict-integrity**: 움직인 verdict = **re-open + INVALID**, 부호 뒤집기 절대 아님. "confound ⟹ 벽 깨짐"은 over-claim — confound 는 증거를 제거하지 다리를 공급 안 함.

## 🔴 게이트 통과 — A1 이 이 카드를 발화시켰다 (2026-07-16)
사전등록 게이트는 "[[H_9611]] 이 inert 반환하면 **DOA**, 쓰지 말 것"이었다. **A1 결과 = PASS-live**:
- beyond-RF(>35B) 문맥만 다른 2AFC arm 이 **live 서 margin 을 1.477 nats 이동** · **frozen 서 정확히 0** · 양성통제(near, within-RF)는 live 4.765/frozen 6.570 둘 다 살아있음.
⟹ **bus 가 SCORE 까지 닿는다** ⟹ Fable A1 판정표의 "any Δ ⟹ 모든 far-context verdict 는 GN-confounded → A2 발화" ⟹ **이 카드 LIVE**.

**감사 대상 정밀화(A1 이 준 것)**: 오염은 **arm 들이 beyond-RF(>RF≈35)에서 서로 다를 때만** 물린다(문맥 arm-간 동일 ⟹ bus 기여가 대비에서 상쇄). ⟹ 감사 = 각 cement verdict 의 매니페스트에서 **arm 간 beyond-RF 바이트 차이 유무**를 먼저 정적 조사($0·모델 불요) → 차이가 있는 것만 `--gn-freeze` 재채점. 크기 기준 = **1.48 nats**(측정된 bus 도달력) vs 그 verdict 의 결정 margin.
**남은 블로커**: cement 매니페스트(H_9359/9304/9267) 소재 — aiden 부재 · `state/` H-NO-STATE-DIR 가드 · summer load 15 포화. 정적 조사는 매니페스트만 있으면 $0.

## 🔬 감사 정밀화 2차 — confound 경로가 특정됐다 (2026-07-17 · $0 · 실행 전 · 설계만)
**① 접근 경로 해소**: 화석 디렉터리는 bash 가드(H-NO-STATE-DIR/EXEC)에 막히지만 **Read 툴은 읽기전용이라 통과** — 정적조사 경로는 원칙적으로 **열려 있다**(가드는 bash 전용).

**② 🔴 KO 셋은 거의 전부 beyond-RF** (`a_korean_byte_budget` × [[H_9611]] RF=35byte): KO = **3 B/char** ⟹ **RF=35byte ≈ 11 한글자**. EN 이면 35자가 within-RF 인데 **KO 는 11자뿐** ⟹ C3(H_9329·KO)·[[H_9327]] 계열의 2AFC 프롬프트는 **대부분이 beyond-RF 에 놓인다** = bus 도달 영역. (이 3× 배수는 레포를 이미 3번 물었다 — `a_korean_byte_budget`.)

**③ 특정된 confound 경로 = 길이-시프트**: 오염은 "arm 간 beyond-RF 차이"일 때만 문다([[H_9611]] A1). C3 결과파일의 arm 태그는 `<write-class>|<neg-surface>` = `swap|negL` / `swap|negZ` / `swap|negJ` / `affirm|*` / `keep|*` / `untouched|*`. 대비되는 arm 들은 **부정 표면(negL/negZ/negJ)의 byte 길이가 서로 다르다** ⟹ `win=64` **우측정렬이 시프트** ⟹ **arm 마다 창에 드는 beyond-RF 바이트가 달라진다** ⟹ bus 가 그 차이를 score 로 나를 수 있다. **길이가 같으면 상쇄되어 무사.**
⟹ **감사의 1차 체크는 "대비 arm 쌍의 seed byte-길이가 동일한가"** 로 축약된다($0 · 모델 불요 · 산술).

**④ 남은 필요물(정직)**: 결과파일엔 **seed 가 없다**(rows = `a`=stem · `b`=arm-tag · `margin` · `raw` 만) ⟹ 정적조사는 **입력 매니페스트(seed 포함)** 가 필요. 후보 = 카드가 지목한 `man_en_seen.json` / `cpt_ground_keep_lie_en_s7.txt` 계열(Read 툴로 접근 가능하나 소재 미확인).

**⑤ 갱신된 감사 절차(사전등록)**: ①각 cement 매니페스트에서 **대비 arm 쌍의 seed byte-길이 + beyond-RF(마지막 35B 밖) 바이트 동일성** 정적 대조($0) → ②차이 있는 쌍만 `--gn-freeze` 재채점 → ③크기기준 **1.48 nats**([[H_9611]] 측정 bus 도달력) vs 그 verdict 의 결정 margin. **양성통제** = RF 내에서만 다른 verdict 는 gn-freeze 에 불변이어야.
**⚠️ over-claim 차단 유지**: 길이-시프트가 *존재*해도 그 자체가 오염 확정이 아니다 — 시프트가 **결정 margin 을 뒤집을 만큼** 기여했나가 ②③의 일. 움직인 verdict = **re-open + INVALID**(부호 뒤집기 아님).

## 🎯 감사 1차 체크 실행 — **HIT** (2026-07-17 · $0 · 순수 산술 · 모델 불요)
정밀화 2차가 축약한 체크("대비 arm 쌍의 seed byte-길이가 동일한가")를 **실행**했다. 대상 = `cli/evaluate.py` `--route-audit`(H_9355 LOCUS) — docstring 이 seed 구성을 명시하므로 매니페스트 없이 산술 가능.

**docstring 자백**(`cli/evaluate.py:3210-3211`): *"`ped` an inert **10-byte suffix, byte-length-matched to negL's '지 않다'**"* · *"`negJ` '지는 않다' — negL's **string twin**"*.

**실측 byte 길이**(UTF-8):

| surface | 문자열 | bytes | 대비 상대 | 판정 |
|---|---|---|---|---|
| `negL` | 지 않다 | **10** | ped(10) | ✅ 매칭 |
| `ped` | (inert) | **10** | — | 기준 |
| **`negZ`** | 지가 않다 | **13** | **ped(10)** | ⚠️ **+3B 불일치** |
| `negJ` | 지는 않다 | **13** | negL(10) | ⚠️ +3B 불일치 |

**🎯 HIT — 주 DV 안에 있다**: `ped` 는 docstring 대로 **negL 에만** 길이매칭됐는데, 주 DV 는 `dOP = mean_stem[JS(flip0,negX) − JS(flip0,ped)]`, **X ∈ {negL, negZ}** 이고 LOCUS-SPLIT bar 는 **"dOP ≥ 0.05 bits on BOTH strong surfaces"** 를 요구한다 ⟹ **negZ arm(13B) 이 ped(10B) 통제와 비교되어 주 verdict 안에 +3B 길이-시프트 경로가 열려 있다**. `win=64` 우측정렬에서 3B 시프트 ⟹ 창에 드는 **beyond-RF 바이트가 arm 간 상이** ⟹ [[H_9611]] 이 측정한 GN bus(beyond-RF 도달 · score **1.48 nats** 이동력)가 그 시프트를 나른다 ⟹ **negZ 의 ped 초과분이 "연산자-특이성"인지 "3B 시프트"인지 미분리**. OP-SPEC(`dOPJ` = negL 10B vs negJ 13B)도 동일 +3B.

**카드 자신의 경고가 정확했고, 메커니즘이 이제 이름을 얻었다**: 그 docstring 은 *"negJ 가 재현하는 split 은 **STRING effect wearing the operator's clothes**"* 라 경고했다 — **GN bus 가 바로 그 string/length effect 를 RF 너머로 나르는 메커니즘**이다. 즉 우려는 옳았고 통제(negJ)는 그 우려를 **잡도록 설계됐으나 그 자신이 길이-비매칭**이라 같은 경로를 탄다.

**⚠️ over-claim 차단(6번째)**: 이건 **confound 경로가 열려 있다**는 것이지 **H_9355 verdict 가 뒤집혔다는 게 아니다** — 3B 시프트의 **실제 기여 크기는 미측정**. 정량화 = `--gn-freeze` 로 route-audit 재채점(계기 v0.15.17 배선 완료) → dOP(negZ) 가 얼마나 움직이나. **`negL` arm 은 매칭돼 보호된다** ⟹ 최악의 경우에도 "negZ 팔 한쪽 INVALID" 이지 verdict 전체 붕괴가 아니다. 그리고 `--route-audit` 은 router JS 를 재지 xbind margin 이 아니므로 bus 도달력 1.48nats(margin 기준)를 그대로 옮겨 쓸 수 없다 — 재채점이 필요한 이유.
**NEXT**: `anima-py evaluate <clm> --route-audit <manifest> --gn-freeze <ref>` 로 dOP(negZ) live vs frozen 대조 → 움직이면 negZ arm **re-open + INVALID**(부호 뒤집기 아님) · 불변이면 verdict 무사(정직한 무죄 확인).

## ❌ 정량화 시도 = 정직한 실패 — 그런데 실패가 사실 2개를 줬다 (2026-07-17 · aiden CPU · $0)
HIT 의 크기(3B 시프트가 dOP 에 얼마나 기여하나)를 재려고 **재구성 route-audit 매니페스트**를 만들어 실행. 스키마는 코드서 확보(`items=[{id,stem,surf,split,pol,seed,seed_bytes,stem_span}]` · `_ra_read`/`_ra_forward`). 설계 = 레포에 **없는 통제 `ped13`(13B inert · negZ 에 길이매칭)** 추가 → `dOP(negZ vs ped10) − dOP(negZ vs ped13)` = **3B 시프트의 순수 기여**.

**실행됨**(G-SPIKE 🟢 PASS = JS 추정기 pedestal 통과 · G-LIVE 🟢 J_STEM 0.000262 ≥ 0.0001) **그러나 정량화는 실패**. 원인 2개, 둘 다 구체적:

**① 🔑 `ped13` 이 조용히 무시됐다 — 계기가 surface 를 하드코딩한다.** 출력 `js_mean` = `{negL, negZ, negJ, ped}` · `top_hist` = `{flip0, negL, negZ, negJ, ped}` — **내가 매니페스트에 넣은 `ped13` 은 어디에도 없다**. ⟹ **negZ 에 대한 길이매칭 통제는 매니페스트만으로 주입 불가** ⟹ **이 confound 는 데이터로 못 고친다 — 계기 코드 변경이 필요하다.** (이건 실패가 아니라 **발견**: HIT 의 수리 비용이 "매니페스트 한 줄"이 아니라 "계기 수정"이라는 것.)

**② 내 재구성 매니페스트가 축퇴(degenerate)** — 합성 stem 12개가 라우터를 전혀 가르지 못했다: `top_hist` 전 surface `[0,0,12]`(12 stem **전부 expert 2**) · `top_agree` 전부 **1.0** · `dOP[negL]`=-1.0e-4 · `dOP[negZ]`=-7.6e-6 vs bar **0.05 bits** = **500× 아래**. ⟹ **분해할 신호 자체가 없어** 3B 기여를 못 잰다. J_STEM 이 G-LIVE 바닥(1e-4)을 겨우 넘은 것도 같은 증상.

**⚠️ 이 run 의 `🔵 LOCUS-SHARED` 는 H_9355 에 대한 어떤 진술도 아니다** — 축퇴 합성셋의 산물이다. 원 verdict 와 무관(`a_scale_honest_scope`). 내 셋을 H_9355 재현으로 읽으면 그게 over-claim(7번째 차단).

**HIT 자체는 무손상**: negZ=13B vs ped=10B 는 **코드·산술 사실**이라 이 실패한 run 과 독립이다. 흔들린 건 "그 3B 가 얼마나 기여하나"뿐.

**정량화의 실제 요구조건(이제 특정됨)**: ⓐ **원 H_9355 매니페스트**(라우터를 실제로 가르는 실 stem — 내 합성 stem 은 축퇴) **AND** ⓑ **계기 수정**(negZ 용 길이매칭 통제 추가 · surface 하드코딩 해제) **AND** ⓒ `--gn-freeze` 를 `route_audit_run` 에 배선(현재 `dump_hidden`/`xbind` 에만 — 넘겨도 **조용히 무시**되므로 그대로 쓰면 거짓 "차이 없음"을 읽는다 ⚠️).

## 📏 정량화 성공(추정) — **HIT 은 실재하나 규모가 bar 아래** (2026-07-17 · aiden CPU · $0 · DIRECTIONAL)
앞 실패의 **원인 가설이 맞았다**: C3 결과파일이 `"ckpt": "swap_s7.clm"` 이라 원 H_9355 는 **CPT본**에서 돌았을 것 — 내가 쓴 `clm303_clean`(**베이스**)이 축퇴였다. aiden 의 **`natem_c34_main_s11.clm`(CPT본)** 으로 같은 재구성 셋 재실행:

| ckpt | J_STEM | top_agree | 축퇴 |
|---|---|---|---|
| **natem_c34_main_s11**(CPT본) | 0.001234 | **0.33** | **NO ✅** 라우터가 갈린다 |
| clm303_clean(베이스) | 0.000262 | **1.00** | YES — 전부 한 expert(앞 실패 원인 **확인**) |

**CPT본에서의 수치**(`[ans]` 판독점 · `js_mean`):

| 대조 | dOP | 비고 |
|---|---|---|
| `negZ`(13B) vs **`ped`(10B)** | **−0.002152** | ← **레포의 주 DV**(길이 불일치) |
| `negZ`(13B) vs **`negJ`(13B)** | **−0.000064** | ← **길이매칭** 대조 |
| **차이 = 3B 시프트 기여 추정** | **≈ +0.00209 bits** | **vs bar 0.05 = 24× 아래** |

**⟹ 두 결론이 동시에 참이다:**
- ✅ **HIT 은 실재한다** — 통제를 10B→13B 로 길이매칭하자 dOP 가 **−0.00215 → −0.00006**. **dOP 절대값의 대부분(≈97%)이 길이-시프트 몫**이었다. confound 경로는 열려 있고 실제로 흐른다.
- 🟢 **그러나 H_9355 verdict 는 뒤집히지 않는다** — 기여 규모 **0.0021 bits 는 bar 0.05 의 24× 아래**. LOCUS-SPLIT(≥0.05) 도 LOCUS-SHARED(TOST ±0.02) 도 이 크기로는 안 움직인다. ⟹ **실재하지만 무해한 규모**(이 ckpt·이 재구성 셋 기준).

**⚠️ over-claim 차단(8번째 · 스스로에게)**: ① **내 재구성 셋**이지 원 H_9355 매니페스트가 아니다 — 원 셋의 dOP 절대크기가 다르면 비율도 달라진다(내 셋은 dOP 가 애초에 bar 의 1/20 규모) ② **`negJ` 는 inert 통제가 아니라 실 부정표면**이라 `negZ−negJ` 는 "연산자-only" 가 아니다(혼입) — 진짜 inert 길이매칭 통제(`ped13`)는 **여전히 하드코딩에 막혀 주입 불가** ③ 따라서 **"기여 추정 ≈0.0021"** 이지 확정치가 아니다 ④ 이 run 은 `--gn-freeze` **없이** 돌았다(route_audit 미배선) — 그 0.0021 이 **GN bus 경유**인지는 별도 확인 필요(길이-시프트는 RF 내 경로로도 일부 흐를 수 있다).

**⟹ H_9612 착지**: 감사가 **경로를 찾고(HIT) 크기를 재고(≈0.0021) 무해함을 확인**했다. **어떤 cement verdict 도 re-open 되지 않는다.** 남는 실질 산출 = **계기 위생 권고**(아래).

## 🔧 계기 위생 권고 (verdict 무관 · 수리 비용 = 코드 변경)
`--route-audit` 의 `ped` 는 docstring 대로 **negL(10B)에만** 길이매칭돼 있고, 주 DV 는 `X ∈ {negL, negZ}` 를 **같은 ped 로** 대조한다 ⟹ **negZ 팔은 구조적으로 +3B 불일치**. 규모는 이 셋에선 무해했으나(bar 24× 아래) **설계 결함 자체는 남는다** — dOP 가 더 큰 regime(원 셋·다른 ckpt)에서는 비율이 달라질 수 있다.
**권고**: surface 하드코딩(`{negL,negZ,negJ,ped}`)을 풀어 **surface 별 길이매칭 ped**(`ped10`/`ped13`)를 매니페스트로 주입 가능하게 → negZ 는 `ped13` 과 대조. **+ `--gn-freeze` 를 `route_audit_run` 에 배선**(현재 넘기면 **조용히 무시** = 거짓 "차이 없음" 위험 ⚠️).

## 🔧 계기 위생 수정 구현 + ⚠️ 앞 정량화 **정정** (2026-07-17 · aiden CPU · $0 · engine-native)
권고를 실제로 구현했다(`cli/evaluate.py` · 기본 경로 byte-identical):
1. **`--gn-freeze` 를 `route_audit_run`→`_ra_forward` 에 배선** — 전에는 CLI allowlist 가 flag 를 받고 **조용히 버려서** 거짓 "차이 없음"을 읽었다(H_9612 가 찾은 footgun). 이제 실제 발동.
2. **surface 하드코딩 해제** — 매니페스트 `ctrl_of` 로 DV surface 별 **길이매칭 pedestal** 주입(예 `{"negL":"ped","negZ":"ped13"}`). 없으면 전부 `ped` = **수정 전과 완전 동일**.
3. **byte-길이 자동 감사** — DV 쌍의 길이 불일치를 **inline 으로 LOUD 경고**(조용한 통과 불가) + `res["ctrl_of"]`/`len_mismatch`/`gn_freeze` 기록.

**3-arm 검증(natem_c34_main_s11 · CPT본):**

| arm | len-audit | dOP[negZ] |
|---|---|---|
| **A** 기존 스키마(ctrl_of 없음) | negL 25B vs ped 25B 🟢 · **negZ 28B vs ped 25B ⚠️ +3B SHIFT** → 경고 발동 | **−0.002152** (수정 전과 **동일** = 회귀 0) |
| **B** `ctrl_of: negZ→ped13` | negL 25B🟢 · **negZ 28B vs ped13 28B 🟢 matched** | **−0.002203** |

**⚠️ 앞 정량화 정정(9번째 자기정정)**: 앞 항목은 `negZ vs negJ` 대리 비교로 "**3B 시프트가 dOP 의 ≈97%**"라 추정했다. **진짜 inert 길이매칭 통제(`ped13`)로 재니 −0.002152 → −0.002203 = 시프트 기여 ≈0**. 앞 추정이 컸던 이유는 그 항목이 **스스로 경고한 바로 그 한계** — `negJ` 는 inert 가 아니라 **실 부정표면**이라 연산자 효과가 혼입됐다. 대리 통제로 잰 분해는 틀렸다.
⟹ **정정된 결론**: 길이-시프트 **경로는 실재**(감사가 자동 검출) **하나 이 ckpt·이 셋에서 dOP 기여는 사실상 0** ⟹ H_9355 무해 판정 **유지**(이유가 오히려 더 강해짐 — 앞엔 "기여는 크지만 bar 아래", 이제 "기여 자체가 ≈0").

**🔴 프로세스 결함 1건(정직 기록)**: 1차 검증에서 `git archive HEAD` 로 **미커밋 편집이 빠진 낡은 트리**를 측정했다 — A≡B 동일 + 새 로그 0줄이라는 **회귀 가드가 포착**. 가드가 없었으면 "ctrl_of 무효"로 오판했을 것. 교훈 = **원격에 보낼 아카이브는 커밋 후 만들고, 아카이브 안 패치 마커를 grep 으로 확인한 뒤 전송**.
**scope**: 1 ckpt(natem_c34_main_s11) · 내 재구성 셋(원 H_9355 매니페스트 아님) · CPU · DIRECTIONAL.

## 🧹 감사 확산 — 같은 결함 계급을 **다른 계기**에서 발견·수리 (2026-07-17 · $0 · 코드 감사)
route-audit 에서 만든 길이-감사가 일반 도구이므로, 같은 결함(길이-비매칭 통제)이 다른 cement 계기에도 있나 $0 로 훑었다.

**레포는 대체로 길이매칭을 실천한다** — `:891`/`:1758`/`:1880` "length-matched NEUTRAL atom" · `:2387`/`:2403` "byte-matched twin". route-audit 의 negZ 가 예외였다. **그러나 주장 ≠ 검증**:

**🎯 `--valence-audit` 에서 같은 계급 발견(더 나쁜 형태)**: 이 계기는 결과에 *"(length-matched NEUTRAL atom, SAME contexts)"* 를 **사실처럼 인쇄**하지만, 매니페스트 스키마는 `{id, prompt, stem, pol, arm}` 뿐이고 **본문에 byte-길이 검증이 0줄**이다(`len(` 은 전부 리스트 길이·LOO 루프). 즉 **길이매칭은 매니페스트 빌더의 책임인데 계기가 그걸 검사하지 않고, 출력은 안심시키는 라벨을 무조건 찍는다.** 매칭 안 된 swap atom 이 들어오면 prompt byte-길이가 달라지고 → 우측정렬 창이 시프트 → 두 arm 이 다른 문맥으로 읽히고 → GN bus 가 그 차이를 판독점(T−1)까지 나른다 ⟹ `Delta = acc(atom) − acc(swap)` 가 **form-vs-content 가 아니라 form+shift** 가 된다.
- route-audit 은 최소한 ped 를 negL 엔 진짜 매칭했다(재사용이 문제). **valence-audit 은 주장만 하고 검증이 0** = 같은 계급의 더 나쁜 형태.

**수리**(`cli/evaluate.py::valence_audit_run` · 기본 경로 무변): stem 별 `atom`/`swap` prompt **byte-길이 자동 대조** → 불일치면 **LOUD 경고**(몇/몇 stem·예시 3건·"Delta 를 form+shift 로 읽어라") · 전부 매칭이면 `🟢 len-audit` 인쇄. **주장을 검증으로 바꿨다.**
**단위검증**(모델 불요): 매칭셋(`좋`3B↔`것`3B) → 불일치 0건 통과 · 불일치셋(`좋`3B↔`그것`6B) → 1건 검출. (KO 3B/char 가 여기서도 배수로 작동.)

**⚠️ scope**: 이건 **계기가 이제 스스로 검사한다**는 것이지 **기존 valence-audit verdict 가 오염됐다는 게 아니다** — 그 매니페스트들이 실제로 매칭됐는지는 **미확인**(매니페스트 소재 필요). 다음 valence-audit 실행이 자동으로 답한다. **일반 교훈**: 계기가 인쇄하는 "length-matched"·"byte-matched" 같은 문구는 **검증이 아니라 주석일 수 있다** — 검사 코드가 있는지 확인하라(`tool-definition-read-code-not-docstring` 의 계기판).

## 🔺 확산 3번째 — `--bind-locus` 는 confound 가 아니라 **조용한 오인덱싱** (2026-07-17 · $0)
"byte-matched twin" 주장 계기 중 마지막(`:2403` · **H_9331 = cement 된 벽 verdict**)을 봤다. 이건 **앞 둘보다 심각**하다 — 주장이 **load-bearing** 인데 검사가 0이었다:

```
S_seed = len(A["seed"].encode())     ← A 의 길이만
base   = T - (S_seed + 6)            ← A 기준 우측정렬 offset
stem_t0/car_t0 = base + …            ← A 기준 인덱스
donor  = B_taps[l][stem_t0:…]        ← 그 인덱스로 B 를 퍼감 (5곳 전부)
```
`base` 는 **A 에서 한 번만** 계산되고 `B_taps`/`Ab_taps` 를 **A 기준 인덱스로 5곳 전부** 슬라이스한다. twin 의 seed 길이가 다르면 **B 자신의 우측정렬 offset 은 다른데** 코드가 그걸 모르므로 donor 가 **B 의 엉뚱한 위치**에서 온다 ⟹ **조용히 오정렬된 patch** = τ/S 가 쓰레기인데 verdict 처럼 읽힌다.
- route-audit(negZ vs ped) · valence-audit(미검증 swap) = **대비를 오염**시킴 · **bind-locus = 측정 자체를 손상**시킴. 같은 계급의 **최악 형태**.

**수리 = 경고가 아니라 REFUSE**(레포 자신의 G-SPIKE "refusing to measure" 패턴): pair 별 A↔B(및 Ab) seed byte-길이 대조 → 위반 시 **`return 2` 로 측정 거부**(위반 수·예시 3건·이유 인쇄) · 전부 매칭이면 `🟢 twin-guard` 인쇄.
**단위검증**(모델 불요): 매칭쌍(`좋`3B↔`싫`3B) → 위반 0 통과 · 불일치쌍(`좋`↔`별로`) → `좋↔별로(B) 14B vs 17B` 검출→refuse.

**⚠️ 이건 byte-identical 이 아니다(정직)**: 순수 추가지만 **하드 게이트**다 — 기존 매니페스트가 twin 을 제대로 매칭했다면 통과해 아무것도 안 바뀌고, **안 했다면 이제 거부한다**. 그게 요점이다. H_9331 verdict 가 오염됐다는 주장은 **아니다**(그 매니페스트 실제 매칭 여부 미확인 — **다음 실행이 자동으로 답한다**).

## 📋 확산 전수 종합 — "matched" 주장 3계기 감사 완료
| 계기 | 주장 | 검사 있었나 | 실패 시 결과 | 수리 |
|---|---|---|---|---|
| `--route-audit` | ped = negL 에 byte-length-matched | ✅ 참(단 **negZ 에 재사용**) | 대비 오염(operator+shift) | `ctrl_of` 주입 + 자동 길이감사 |
| `--valence-audit` | "length-matched NEUTRAL atom" | ❌ **0줄**(라벨만 인쇄) | 대비 오염(form+shift) | atom/swap 자동 길이감사 |
| `--bind-locus` | "byte-matched twin" | ❌ **0줄**(하지만 **load-bearing**) | **조용한 오인덱싱**(측정 손상) | **REFUSE 가드** |

**⟹ 획득한 일반 법칙**: 계기가 인쇄/주석하는 **"matched"·"byte-matched"·"length-matched" 는 검증이 아니라 주장일 수 있다.** 그리고 그 주장이 **인덱스 산술에 load-bearing** 이면 결과는 confound 가 아니라 **손상**이다. ⟹ **주장 옆에 검사 코드가 있는지 확인하고, load-bearing 이면 warn 이 아니라 refuse 로 만들라.** ([[tool-definition-read-code-not-docstring]] 의 계기판 확장 — 그건 "docstring 말고 코드를 읽어라"였고, 이건 "**코드가 자기 전제를 검사하는지도 읽어라**".)

## 🔒 소급 감사 시도 → 아티팩트 벽 (2026-07-17 · $0) + 메타 관찰
새 REFUSE 가드로 **H_9331 자신을 소급 감사**하려 했다("그 매니페스트의 twin 이 실제로 byte-매칭됐나"). 매니페스트가 없으니 **결과 화석**으로 대신 하려 했다 — 현재 코드는 pair 별 `rec = {"A": stem, "B": stem, "Ab": …}` 를 기록하므로 stem 들의 byte 길이만 비교하면 $0 로 답이 나온다.
**결과: 불가.** `archive/state/scratch/h9331_bindlocus/bl_*.json` 은 **집계만** 담는다(`verdict`/`stageA`(depth·rung·n·swap·sham)/`bars`) — **per-pair (A/B stem) 레코드가 없다**. 즉 그 화석은 **per-pair 기록이 추가되기 전 스키마**다.
⟹ **가드는 미래 실행을 보호하지만 과거는 이 화석으로 소급 감사 불가.** H_9331 twin 불변식의 실제 준수 여부는 **미확인으로 남는다**(오염 주장 아님 · 다음 bind-locus 실행이 자동으로 답한다).

**📌 메타 관찰(이번 세션 3번째 같은 벽)**: 화석이 **verdict 는 보존하나 그것을 재감사할 입력/per-pair 기록은 보존하지 않는다**. 이 감사가 매니페스트를 **3번 재구성**해야 했던 이유가 이것이다 — ①cement 셋 매니페스트 부재(A1 원 arm) ②route-audit 매니페스트 부재(정량화) ③H_9331 per-pair 부재(소급 감사). 재구성은 **원 regime 을 재현 못 해**(내 셋은 dOP 가 bar 의 1/20·베이스 ckpt 는 라우터 축퇴) 결론의 이전이 막힌다.
⟹ **함의(설계 권고 · verdict 무관)**: 계기 결과에 **재감사에 필요한 입력 지문**(per-pair seed byte-길이·arm 별 통제 매핑·매니페스트 sha)을 함께 박으면 미래의 감사가 재구성 없이 가능하다. 이번에 `--route-audit` 이 `res["ctrl_of"]/len_mismatch/gn_freeze` 를 기록하기 시작한 게 그 방향의 첫 걸음이다.

## 상태
🔒 감사 lane **완결** (DIRECTIONAL) — 3계기 자동감사 WIRED(route-audit·valence-audit·bind-locus) · 일반법칙 획득("matched" 는 주장일 수 있고 load-bearing 이면 refuse) · 소급 감사는 **아티팩트 벽**(화석이 per-pair 미보존 · 미래 실행이 자동 답함) · **cement verdict re-open 0**.
<!--prev-->
## 상태
📏 감사 완결 (DIRECTIONAL) — **HIT 실재**(dOP 의 ≈97%가 3B 시프트 몫) **∧ 규모 무해**(0.0021 vs bar 0.05 = 24× 아래) ⟹ **cement verdict re-open 없음**. 산출 = 계기 위생 권고(surface 하드코딩 해제 + route_audit 에 --gn-freeze 배선). **distinct-from-kills:** A1 PASS-live 가 연 감사를 경로특정→크기측정까지 닫음. — A1 PASS-live 발화. **confound 경로 특정=길이-시프트**(arm 간 부정표면 byte 길이 상이 → win 우측정렬 시프트 → beyond-RF 내용 상이). KO=3B/char ⟹ RF=35B≈11자 ⟹ KO 셋 대부분 beyond-RF. 1차 체크=arm 쌍 seed byte-길이 동일성($0·산술). Read 툴로 화석 접근 가능(가드는 bash 전용). 남은 필요물=입력 매니페스트(seed 포함 · 결과파일엔 seed 없음). **distinct-from-kills:** anchor-cert kill(틀린 식) 아님 — 옳은 식의 *채널 오귀속* 감사.
