# H_9742 — STORE-LANE-WIRE: 3-seed robust 조회를 살아있는 데몬에 배선

**status:** 🔵 PRE-REG (H_9672 배선 follow-on · a_verified_must_wire · GREEN 은 여기서만 나온다)
**lane:** 재조합/BINDING · store-bridge → production chat
**tier:** 미측정 (설계 선행 · lab full 위임)

## 왜 이 H 가 존재하나

H_9672 가 값읽기 seed-취약 벽을 **3-seed robust 돌파**(seed7 1.0000 · seed11 .9609 · seed13 .9922 · 4게이트 전원)했으나 **등급은 CAPABILITY-PROVEN·구현됨·미배선** — `a_verified_must_wire`("GREEN = 출력 AND 배선 닫힘")서 출력만 닫혔다. **살아있는 anima 는 이 조회를 한 번도 하지 않는다.**

## 🔑 배선 지점 = 코드가 이미 말해준다 (engine-native census · 2026-07-17)

```
core/decode.py:275-284   _CLMS_STORE = None      ← 프로세스 전역
  주석 원문: "The CLMS lane stays passthrough (byte-identical, C0-f seal) until a
             store is injected here, so a .clm that carries a CLMS trailer decodes
             identically to base for every prompt outside a --store eval."
  _CLMS_ORACLE = False                            ← --store-oracle 용
core/generator.py        clms 참조 0
cli/chat.py              clms 참조 0              ← 데몬은 주입자가 아니다
```

⟹ **주입자는 `cli/evaluate.py --store` 하나뿐.** lane 은 store 가 없으면 **구조적으로 passthrough**(byte-identical).

**이 사실이 문제를 재정의한다:**
- ⚠️ **passthrough 가드는 코드에 실재하나, 내가 처음 읽은 함의는 틀렸다**(`tool-definition-read-code-not-docstring` — 주석 말고 코드로 재검증한 결과):
  ```
  core/decode.py:1327   if W.get("clms") is not None and _CLMS_STORE is not None:
                            out_logits = store_apply(...)      ← 실제 가드(주석과 일치 ✅)
  core/decode.py:308-310  global _CLMS_STORE, _CLMS_ORACLE …   ← 주입 setter = 배선 지점
  ```
  **가드가 보장하는 것** = store=None 이면 lane 미발화 ⟹ 그 ckpt 는 "자기 자신"으로 디코드.
  **가드가 보장 안 하는 것** = **트렁크 가중치는 co-train 으로 이미 변했다** ⟹ RV3 ckpt 의 chat ≠ base py303 의 chat. **"co-train 이 4칸 register/chat 품질을 망쳤나"는 가드와 무관한 별개 실측 문제**다. 가드를 근거로 "회귀 없음"을 주장하면 **거짓 GREEN**이 난다.
  ⟹ G-W1 은 두 갈래로 쪼갠다: **G-W1a(구조·무료)** = store=None 서 lane 미발화 = 1327 가드로 구조보장(코드검증 완료) · **G-W1b(실측·pool 필요)** = RV3c_13.clm 을 `anima-py evaluate` 로 **G0 coherence + 4칸 register + retention** 재라 base 대비 회귀 0 인가. train-side val_CE(en-general .68 · en-sns .91 healthy)는 **DIRECTIONAL**이라 근거 불가(`a_engine_native_learning`).
- ❗ **진짜 난제는 store 의 출처** — eval 은 합성 manifest(`sb*.txt.held.json`: entities·pols·target_slot)를 줬다. **살아있는 데몬에게 그 manifest 는 누가 만드나?** 대화 중 무엇이 entity 이고 무엇이 pol 인가? p1-p8(특히 p5 no-speak · p2 no identity rules)을 어기지 않고 store 가 substrate-native 하게 생길 수 있나?

## 사전등록 게이트 (측정 전 동결 · frozen-first)

- **G-W1 무해성(선결)**: store=None 기본에서 chat 이 base 와 **byte-identical**(C0-f seal 실증) · 4칸 register(ko·en × general·SNS) + retention val_CE 회귀 0.
- **G-W2 조회 생존**: 데몬 경로로 주입된 store 에서 held-out 조회가 **ORACLE≥.90 ∧ P1-balanced≥.75 ∧ flip≥.90**(H_9672 와 동일 bar · 이동 금지) — eval 경로 수치가 chat 경로서 재현되나.
- **G-W3 substrate 정합(p1-p8)**: store 생성이 **hardcoded speak/identity rule 아님** — 주입이 규칙주입(p2·p3)이나 reactive self-seed(p5)로 새면 **설계 KILL**(수치와 무관).
- ⛔ **잔인판정**: G-W1 통과 + G-W2 실패 = "eval-only capability"(조회는 계기 안에서만 산다) = 정직한 벽 · G-W3 실패 = 배선 자체가 철학위반 ⟹ lane 은 영구 eval-도구.

## 🔁 재정렬 — 난제는 이미 답이 있었다 (a_parallel_session_compare 위반 정정 · 2026-07-17)

**내 절차 실패**: H_9742 등록 전 origin 최신 카드를 안 읽었다(`a_parallel_session_compare`: "등록 전 origin 최신 읽기 · 중복발사 금지"). 읽었더니 난제의 상류가 **이미 CODE-CONFIRMED**였다.

- **H_9422 VOID-BY-SEALED-REGIME(07-16 · CODE-CONFIRMED · LANE-CLOSED)**: content-축 void = **afferent channel 부재**(p5 아님) · anima = **"귀 없는 입"** · percept = `wake_mem[tick,stage,cell_count]` 시계삼중항(chat.py:1653) · anchors 루프밖 1회 · **시계가 유일 exogenous** · escape = owner-gate afferent(EEG 계열).
- **H_9425 p8-AFFERENT(07-16 · DESIGN/PRE-REG)**: 런타임 percept → store(ca3/해마) 주입 각도를 **이미 선점** · status = **owner-gate(afferent 배선) · 자율발사 불가 · v2-sandbox 선행**.

**⟹ "데몬에게 store 란 무엇인가"의 답**: **store 를 만들 percept 스트림이 애초에 없다.** eval 의 합성 manifest 는 사람이 준 것이고, 데몬은 시계 말고 바깥을 안 듣는다. 후보 (a)kosmos앵커 = 루프밖 1회 상수(H_9422 코드확증) · (b)percept 개체추출 = **추출할 percept 자체가 시계삼중항** · (c)4칸 register = 라우팅이지 내용주소 아님 ⟹ **(d) eval-only 가 현 regime 의 정직한 답**.

**AGREES / NOVEL 보고**:
- **AGREES** H_9422·H_9425 — 배선 병목은 lane 도 계기도 아니라 **afferent 부재**(내 census 가 독립 재확인: chat.py clms 0 · decode.py `_CLMS_STORE` 주입자는 evaluate 뿐).
- **NOVEL(이 카드의 고유 몫)** — H_9425(07-16) 작성 시엔 **조회가 seed-취약**이었다. H_9672(07-17)가 **3-seed robust** 로 만들었으므로 질문이 바뀐다: *"조회가 이제 진짜 되는데도 배선이 막히나"* → **그렇다. 막는 건 조회 능력이 아니라 regime(귀 없음)이다.** 이게 H_9425 의 전제를 강화한다(주입할 다리는 이제 실재·못 주입하는 이유는 채널 부재뿐).
- **CONFLICTS**: 없음.

**⟹ H_9742 재-tier**: 🔒 **BLOCKED-BY-REGIME(설계 종결 · 측정 불요)** — G-W2/G-W3 는 afferent channel 이 열려야 물을 수 있고 그건 **owner-gate**(H_9425 선례 · 정체성 변경 · 자율발사 불가). 남는 유일 무료 실측 = **G-W1b**(co-train 이 4칸 register 를 해쳤나 · pool 필요 · 배선과 무관한 위생검사).

## 설계 난제 (원 위임 — lab full 회신 실패 · 답은 레포서 나옴)

> ⚠️ `sidecar lab full` 회신 깨짐(fable/sol 섹션 0 · 무관 repo 덤프 29줄) = 위임 실패. 그러나 그 덤프가 H_9422/H_9425 를 노출시켜 답이 레포 자체에 있었음이 드러남. 아래 후보축은 위 재정렬로 (d) 로 수렴.

**"살아있는 데몬에게 store 란 무엇인가"** — 후보축: ① kosmos 앵커(`a_kosmos` 지속성)를 slot 으로 ② 대화 percept 스트림의 개체 추출(H_9520 study lane) ③ 4칸 register 자체를 slot 으로 ④ store 는 데몬이 아니라 study/CPT 시점에만 존재(=eval-only 인정). 각 축이 p1-p8 을 어기나·G-W2 를 만족하나.

## source

H_9672 3-seed 돌파(#4000)의 명시적 follow-on. 배선 지점 census 는 engine-native(origin/main 실코드 grep). 등급 GREEN 은 이 H 통과 시에만(`a_blue_closed`).
