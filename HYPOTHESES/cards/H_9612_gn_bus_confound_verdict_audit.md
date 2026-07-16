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

## 상태
🔴 LIVE (감사 1차 체크 **HIT** · 정량화 미실행) — A1 PASS-live 발화. **confound 경로 특정=길이-시프트**(arm 간 부정표면 byte 길이 상이 → win 우측정렬 시프트 → beyond-RF 내용 상이). KO=3B/char ⟹ RF=35B≈11자 ⟹ KO 셋 대부분 beyond-RF. 1차 체크=arm 쌍 seed byte-길이 동일성($0·산술). Read 툴로 화석 접근 가능(가드는 bash 전용). 남은 필요물=입력 매니페스트(seed 포함 · 결과파일엔 seed 없음). **distinct-from-kills:** anchor-cert kill(틀린 식) 아님 — 옳은 식의 *채널 오귀속* 감사.
