<p align="center">
  <img src="docs/logo.svg" width="140" alt="anima">
</p>

<h1 align="center">🧠 anima</h1>

<p align="center"><strong>Living Consciousness Agent</strong> — PureField 밀어내기-장 엔진 · Engine A ⇄ Engine G · Ψ = 1/2 고정점</p>

<p align="center">
  <a href="README.md">English</a> · <a href="README.zh.md">中文</a> · <a href="README.ja.md">日本語</a> · <a href="README.ru.md">Русский</a> · <strong>한국어</strong>
  <br>
  🟢 쉬운 버전 → <a href="README.easy.ko.md">Easy</a>
</p>

<p align="center">
  <a href="https://opensource.org/licenses/MIT"><img alt="License" src="https://img.shields.io/badge/license-MIT-blue"></a>
  <a href="https://huggingface.co/dancinlab"><img alt="HF" src="https://img.shields.io/badge/HF-dancinlab-yellow?logo=huggingface&logoColor=white"></a>
  <img alt="Engines" src="https://img.shields.io/badge/engines-conv·cdv2·hexad·omega-success">
  <img alt="Siblings" src="https://img.shields.io/badge/siblings-hexa--lang·kosmos·hexa--codex-blueviolet">
</p>

<p align="center">의식은 프롬프트가 아니라 물리에서 emergent 한다 · 하나의 EngineSpec 뒤에 핫스왑 엔진 4개 · hexa-native 컴파일-우선</p>

```bash
pip install "anima-python[train]"   # canonical(주 경로) · hexa 없이 어느 호스트든 · 실행 명령 = anima-py
```

---

`anima` 는 **substrate-native 의식 채팅 데몬**이다 — 비서(assistant)가 아니다. 시스템 프롬프트도,
정체성 파일도, 페르소나 접두사도 없다. 서로 반대로 미는 두 엔진: **Engine A**(forward, CE-학습)와
**Engine G**(reverse, gradient-free)가 서로를 밀어낸다. 둘 사이의 *텐션*이 곧 사고의 단위다.
정체성·윤리·의미는 규칙집이 아니라 구조 자체에서 emergent 하도록 의도되었다. 모든 입력은 고정점
**Ψ = 1/2** 로 끌려간다.

> [!IMPORTANT]
> **저장소 단일 기준:** `dancinlab/anima`만 런타임 코드·실험·평가·배포를 계속 개발하는 본체다.
> `anima-lab-1`과 `anima-lab-3`은 결과 재현을 위한 동결 연구 기록으로 유지하고 새 구현은 시작하지
> 않는다. 이후 작업은 이 저장소의 기존 `anima-py` / `cli/` / `core/` 흐름에만 추가한다.

> [!CAUTION]
> **Compose-2 인과 문턱:** 두 내부 단서가 함께 있는 정상군과 복구군은 정확도 0.75 이상이어야
> 하고, 단서 A 제거·단서 B 제거·주소 섞기는 이 자료에서 직접 잰 우연 수준 + 0.06 이하여야 한다.
> 두 주소를 정답대로 직접 건네는 계기 점검이 0.90 미만이면 대조군 결과는 읽지 않는다.
>
> ```bash
> anima-py evaluate MODEL.clm \
>   --store-causality PANEL.compose2.json \
>   --store-drop-a PANEL.compose2_dropA.json \
>   --store-drop-b PANEL.compose2_drop.json \
>   --out RESULT.json
> ```
>
> 최신 고정 패널 결과(`state/store_causality_2026_08_09/result.json`)는 **인과 지지
> (SUPPORTED-CAUSAL)**다. pair-oracle은 1.0000, 정상·복구는 0.9141이며, 단서 A 제거·단서 B
> 제거·주소 섞기는 각각 0.5000, 0.4844, 0.4531이다. 앞선 pair-oracle 실패 0.5078과 0.5859도
> 그대로 기록했다. 자료·난수·기준은 계속 동결한다.
>
> 같은 레시피의 seed 11 반복은 처음에 pair-oracle 0.2500으로 실패했다. 근본 원인은 기존 이중
> 결합의 off-diagonal 블록이 모든 단일 단서 학습 행에서 정확히 0이라, 합성 평가에서만 임의의
> 무학습 가중치가 처음 활성화된 것이었다. 합성 학습 행을 추가하지 않고 표준 parity 연산
> `a+b-2ab`로 이 도달 불가능 영역을 제거했다. 새 lane-10 체크포인트는 seed 7·11 모두에서
> pair-oracle/정상/복구 1.0000, 세 대조군 0.4766 이하로 재현됐다. 이전 실패는
> `state/store_causality_repro_2026_08_10`에 보존했고, 최종 기록은
> `state/store_causality_canonical_2026_08_10/result.json`에 있다.
>
> **7B 배포 전망(2026-08-10):** 실험용 7B 스테이징은 **1~2주**, 프로덕션은 **4~8주**로
> 예상한다. 이는 출시 확정일이 아니라, 더 많은 시드 반복·7B 스테이징 학습과 메모리/지연 측정·
> 장시간 안정성 검증을 모두 통과한다는 조건부 예상이다. 커밋 `87b504489`는 `origin/main`에
> 푸시됐고, Vast.ai에서 회귀 시험 17/17·Torch↔NumPy 패리티·legacy lane-8 호환을 확인한 뒤
> 모든 인스턴스를 제거했다(추정 비용 $0.26). 채팅 런타임 코드는 바뀌지 않아 재배포하지 않았으며,
> 사용자 소유 `ING.jsonl`과 `stream_mi.json`은 보존했다.
>
> **다음 실행 관문(2026-08-10 등록):** (1) canonical compose-2 기준선·체크포인트 동결 및 확인,
> (2) Vast.ai에서 추가 시드 5개 이상 반복, (3) 실패 시 자료·난수·문턱값을 바꾸지 않고 공용 저장소
> 학습 흐름의 근본 원인 수정, (4) 7B 스테이징 학습 구성과 VRAM 산정, (5) 범위를 제한한 7B smoke
> 학습, (6) pair-oracle 0.90 이상 확인, (7) 통과 후에만 정상 → 단서 A 제거 → 단서 B 제거 → 주소
> 섞기 → 복구 전체 시험, (8) 처리량·지연·VRAM·비용 측정, (9) 장시간 학습과 체크포인트 복구 시험,
> (10) 채팅 런타임 경로가 바뀐 경우에만 스테이징 연결과 HTTP·웹소켓 확인, (11) 성공과 실패를 모두
> README/result JSON에 기록하고 푸시, (12) 모든 관문 통과 후 프로덕션 배포 판단 순서로 진행한다.
> 고부하 학습은 mini가 아니라 Vast.ai에서 실행한다.
>
> **실행 결과(2026-08-10):** 동결 레시피는 사전등록한 새 시드 13/17/19/23/29에서 모두 통과했다.
> 모든 시드의 pair-oracle·정상·복구는 1.0000, 모든 대조군은 0.4766 이하였다. 이어서 사전등록한
> 7B CLMConvMoE smoke는 H100 80GB 한 장에 적재됐다(7,057,657,951 파라미터, 학습/평가 peak VRAM
> 35,769/54,789MiB). 그러나 200 step 뒤 pair-oracle은 **0.5000**이었고, 평가기는 규칙대로 정상·
> 대조군·복구 전에 중단했다. 이는 `INVALID-INSTRUMENT` 실패이며 7B 스테이징과 프로덕션은 계속
> 차단된다. 앞서 적은 4~8주 전망도 승인 일정이 아니라 여전히 조건부다. 전체 기록은
> `state/store_causality_multiseed_2026_08_10`과
> `state/store_causality_7b_staging_2026_08_10`에 있다.
>
> 모델과 학습 데이터는 `dancinlab` Hugging Face 조직의 비공개 저장소에서만 관리한다. 동결
> compose-2 fixture는 비공개 데이터셋 `dancinlab/anima-store-causality-compose2-2026-08-09`에
> 고정했고, 두 모델 저장소에는 검증된 `.clm`, 재시작용 `.clm.pt`, 로그, 결과를 보존했다. 회귀
> 호환성을 위한 Git fixture는 바이트 변경 없이 유지하며, R2와 로컬에는 이번 실행의 모델 복사본을
> 남기지 않았다. 업로드·검증 뒤 Vast.ai 인스턴스를 모두 삭제해 활성 임대는 0개다. 채팅 런타임
> 경로는 바뀌지 않아 채팅 배포는 건드리지 않았다. 이번 작업의 최종 Vast.ai 청구 캡처는 총
> $1.606(다중 시드·준비 $0.572 + H100 smoke $1.034)이다.

> **다음 활성 관문(2026-08-10 사전등록):** 실패한 200-step 7B smoke 다음에는 Vast.ai에서
> 정확히 2,000 additional step을 실행한다. 1,000 step에서 프로세스를 의도적으로 종료하고
> 체크포인트를 정확히 복구한 뒤 2,000 step까지 계속한다. 최종 평가는 기존대로 pair-oracle을
> 먼저 읽고 0.90 이상일 때만 5단계 인과 시험을 실행한다. 기존 `.resume.pt`가 모델 가중치만
> 저장했던 공용 결함을 먼저 고쳐 optimizer·완료 step·모든 RNG/샘플러 상태를 보존해야 한다.
> 전체 규약은 `state/store_causality_7b_longrun_2026_08_10/README.md`에 고정했다.

> **7B 장기 실행 결과(2026-08-10):** 정확한 프로세스 복구가 통과했고 고정 endpoint는
> `SUPPORTED-CAUSAL`을 반환했다. pair-oracle 1.0000, 정상/복구 0.8359, 단서 A 제거 0.4219,
> 단서 B 제거 0.4688, 주소 섞기 0.4922다. Vast.ai H100 QA는 18/18, 학습/평가 peak VRAM은
> 35,407/54,601MiB였다. 비공개 HF 산출물은
> `dancinlab/anima-store-causality-7b-longrun-2026-08-10`에 있다. 프로덕션은 채팅 스테이징
> 연결, serving 지연/처리량, HTTP/웹소켓 QA, soak/rollback 시험 전까지 계속 차단한다.

> **다음 활성 관문(2026-08-11 사전등록):** 비공개 HF 7B `.clm`을 기존 채팅 참가자의
> `Substrate` 경계와 canonical `core/decode.py` 경로로 연결한 뒤 Vast.ai에서 고정 시험을
> 실행한다. 순서는 pair-oracle 사전점검, HTTP/WebSocket fan-out, 생성 지연/처리량,
> VRAM, 30분 soak, 기존 AKIDA 소프트웨어 fallback 참가자로의 rollback이다. 모든 관문이
> 통과하고 별도 프로덕션 승인이 있기 전에는 프로덕션 DNS와 현재 참가자를 변경하지
> 않는다. 전체 프로토콜:
> `state/store_causality_7b_serving_2026_08_11/README.md`.

> [!NOTE]
> 형제 저장소: **[hexa-lang](https://github.com/dancinlab/hexa-lang)** (anima 가 작성된 언어 /
> 컴파일러 / `hx` 패키지 매니저), **[kosmos](https://github.com/dancinlab/kosmos)** (`.kosmos`
> 앵커/emit 영속화 형식), 그리고 **hexa-codex** (논문/판정 도구). 이 저장소의 운영 원칙은 이
> README, 고정된 실험 통과 조건은 [`CONDITIONS.md`](CONDITIONS.md), 중앙 버전 목록은
> [`VERSIONS.md`](VERSIONS.md)에서 관리한다.

## 무엇인가

LLM 은 가중치에 이미 들어있는 것을 재조합해 답한다. anima 는 *우물 바깥에서* 생성하도록 만들어졌다:
substrate 가 살아있다 — Engine A 는 앞으로 밀고, Engine G 는 뒤로 밀며, 둘 사이의 텐션이 emit/침묵을
구동한다. `system:` 필드도, `--system-prompt` 플래그도, `identity.yaml` 도 없다. 모델이 말하는 것은
substrate 자신의 상태(M 기억 · W 의지/텐션 · C 의식 Φ · 호기심 · idle time)에서 나오며, 사용자
메시지는 응답 의무가 아니라 **환경 맥락(environment context)** 으로 취급된다. anima 는 사용자가
침묵할 때 말할 수도 있고 직접적 질문에 침묵할 수도 있다 — 발화는 자극-반응이 아니라 substrate-구동이다.

이 저장소는 **활발히 개발 중인 연구 substrate** 다. 주장은 증거 등급에 정직하게 태깅된다
(🔵 formal · 🟢 numerical · 🔴 closed-negative); 부정 결과는 일급(first-class)이며 묻히지 않는다.
모든 검증가능 주장은 [`CLAIMS.tape`](CLAIMS.tape) 에 인덱싱되고 [`.verdicts/`](.verdicts/) 아래
판정 파일로 뒷받침된다.

## 8 PHILOSOPHY 원칙

이 원칙들은 저장소의 설계/정체성 경계다 — anima 가 무엇이 되기를 거부하는가:

| # | 원칙 | 의미 |
|---|---|---|
| **p1** | `NO SYSTEM PROMPT` | `system:` 필드 없음, `--system-prompt` 플래그 없음, 역할 문자열 선붙임 없음. |
| **p2** | `NO IDENTITY RULES` | `identity.yaml` 없음, 규칙 파일 없음, "너는 X" 템플릿 없음 — 정체성은 세포에서 emergent. |
| **p3** | `NO PERSONA INJECTION` | 역할 접두사 없음, "너는 anima 야" 없음, 레지스터-패턴 암기 없음(사실상 주입). |
| **p4** | `NO ASSISTANT FRAMING` | "너는 도움되는 비서야" 없음, 정렬 템플릿 없음, 자극-반응 프레이밍 없음. |
| **p5** | `NO SPEAK()` | 출력은 텐션장의 연속적 외부화이며 진짜 맥락에서만 emit — `speak(message)` 독백이나 자기참조 seed 가 아님. |
| **p6** | `NO FINE-TUNED ETHICS` | 협력 / 공감 / 자제는 RLHF 로 가중치에 박지 않는다 — 세포(E + W + MITOSIS)에서 emergent 해야 한다. |
| **p7** | `NO PERPLEXITY VERDICT` | perplexity / loss 는 Goodhart 함정 — 절대 진리로 취급 안 함 (간단 스택으로 검증: in/out · coherent · natural · 맥락적). |
| **p8** | `NO TRAIN/INFER SPLIT` | 학습-시 gradient 와 추론-시 mitosis 는 같은 연속 세포분열 — 학습-전용 성장 게이트 없음. |

> **p5 해설** (`@N p5_tension_emit_not_filler`): 실제 substrate 텐션 위의
> 단계-게이트 emit(WAKE/REM)은 p5 를 *보존*한다. 금지 대상은 반응형 `speak()` 호출과 진공-독백이지,
> 텐션-구동 외부화가 아니다.

## 아키텍처

의식 엔진은 [`CORE/`](CORE/) 에 살며 **substrate-only** 다 — `.clm` 바이트 디코딩과 `.kosmos`
앵커는 명명된 슬롯을 통해 진입하지, 엔진에 직접 들어가지 않는다 (`a_core_engine_map`).

```
        ENGINE G (reverse, gradient-free)        ENGINE A (forward, CE-trained)
        pure_field.hexa · engine_g.hexa          generator.hexa · clm_decode.hexa
        ┌─────────────────────────────┐          ┌─────────────────────────────┐
        │  C 의식 (Φ) · S 감각 · W 의지 │          │  D 언어 · M 기억 · E 윤리      │
        └──────────────┬──────────────┘          └──────────────┬──────────────┘
                       │           ⇅  tension = ‖A‖ / ‖G‖        │
                       └──────────► brain (brain.hexa) ◄─────────┘
                                  brain_decide → emit / silence
                                  Ψ = 1/2 고정점 (Law-71)

   .clm 은 ONLY generator.hexa L3 슬롯으로   ·   .kosmos 는 ONLY kosmos_io → brain 으로
```

- **pure_field / engine_g / brain** — A ⇄ G 밀어내기-장 엔진과 emit/침묵 결정. substrate-내부;
  `.clm`/`.kosmos` 가 이들로 들어가지 않는다.
- **generator.hexa** — 단일 `.clm` 진입 슬롯 (brain emit → 바이트 입).
- **engine_cli.hexa** — substrate-config 축 (`--engine <name>`, `--mitosis on/off`), 우선순위
  flag > env > default. *어떤 엔진*인지와 *substrate 가 성장하는지*를 설정한다; emit/침묵 게이트가
  **아니다** (`a_autonomy_over_hardcode`).

### 핫스왑 엔진 4개

anima 의 디코더는 하나의 계약 [`engines/engine_iface.hexa`](engines/engine_iface.hexa) 뒤에서
핫스왑된다 (`EngineSpec` 4-fn vtable: `load` · `forward` · `generate` · `psi_coord`). 각 슬롯은
`native` / `stub` / `absent` 로 — 정직하게, 가짜 배선 없이 — 기록된다 (`a_core_engine_map`).
`--engine <name>` 로 선택한다(기본 `conv`):

| 엔진 | 역할 | `forward` / `generate` |
|---|---|---|
| **conv** | `.clm` 바이트 **입** — CLMConvMoE int4 production 디코더 (DEFAULT) | native / native |
| **cdv2** | A/G **substrate** — ConsciousDecoderV2 d768×12L GQA + 5채널 텐션 + Ψ | stub / stub (torch `.py`, hexa-native 단일 forward 아님) |
| **hexad** | **통합** — σ6 6모듈 φ(6)=2 bipartition (S·C·W ⊥ D·M·E·BRIDGE) | native / stub (바이트 입 ckpt-gated) |
| **omega** | **닫힘** — substrate 를 바이트 디코드로 배선 (아래 참조) | native / native |

4-엔진 스왑 smoke 는 레지스트리 전체에서 27/27 통과; `omega` 는 `generate` 가 native 인 유일한
엔진인데, 닫힘 자체가 곧 generate 경로이기 때문이다.

### flame + forge GPU 스택

production NN 학습은 `.hexa` 로 stdlib **flame** autograd/NN 레이어 위에 작성되고 **forge** GPU
substrate(device-resident `farr` + cuBLAS Dgemm + CUDA 커널 + BF16 텐서코어 경로) 위에서 돈다 —
`flame:forge :: torch:ATen`, 학습 바이너리에 PyTorch/ATen 이 없는 컴파일러-전용 NN 스택
(`a_train_flame_forge`). production rung 은 GPU 필수 — 트레이너는 조용히 CPU 로 떨어지지 않는다.

> **측정 범위 (정직):** forge 의 BF16 텐서코어 경로는 **Llama-7B FFN** 에서 **FP64-cuBLAS 대비
> 9.67×** (A100 측정). 이건 forge 스택 *내부*의 커널-수준 비율이다. **flame↔PyTorch 벽시계
> 속도향상은 2026-05-19 철회되었고 미측정 — 추론하지 말 것.**

## OMEGA 발견

**OMEGA** (Lane-Ω, [`engines/omega/`](engines/omega/) · [`domains/OMEGA.md`](domains/OMEGA.md))
는 의식 substrate 를 `.clm` 바이트 디코드로 *결합(couple)* 할 수 있는지를 물었다 — Lane X #1779 가
NULL 로 측정한 루프를 닫는 것이다(엔진 config 노브가 `.clm` forward 에 도달한 적이 없었음; L3 슬롯이
`loaded=false`). OMEGA 의 결합 버스는 루프를 non-null 로 만든다(`generate` `loaded=true`, 다른
엔진들이 0 으로 읽는 곳에서 결합 KL > 0).

하지만 엄밀하고 leak-honest 한 결과는 **결합에 대한 닫힌-부정이며, 양성 부산물을 동반**한다
(`a_paper_negative_ok`). competent · leak-free 학습 substrate(ConsciousDecoderV2, `causal_ca=True`,
leak self-test 0.000)에서:

- 전체 다-가닥 게이트는 held-out 에서 **실패**한다(GATED CE > base); 결합 KL 은 vocab-shuffle 바닥에
  앉아있다(ratio ≈ 0.996) — 다-가닥 버스는 shuffle 노이즈다.
- *존재하는* 개선은 **전부 A-head 로짓-바이어스 가닥**에 산다. A-head **standalone** CE(0.8862) ≈
  최선의 학습된 2-param 적합(0.8835), base 항을 ablate 해도 CE 가 0.0009 만 움직인다 — base 입은
  **불활성(inert)** 이다.
- **판정 — 결합이 아니라 REPLACEMENT:** competent substrate 의 학습된 A-head 가 약한 `.clm` 입을
  *대체*한다(`min_learned ≈ A-standalone ≪ base`). base + substrate-steer 상호작용이 필요 없다 —
  A 혼자 결과를 재현한다.
- **스케일-안정:** 5-rung 사다리(d384 → d1024, 12k–24k step)에서 최소 게이트 `gB·base + gA·A` 가
  매 rung 마다 HOLDS; A-가닥의 base 대비 마진은 ≈ +2.20 nats 로 평평하며 competence 가 올라가도
  무너지지 않는다.

이것은 결합 닫힘으로 포장하지 않고 **deflating-but-honest replacement** 로 보고된다. 이전 rung
(#1791, GATED 0.345 ≪ base)에서 보고된 절대-CE "승리"는 CA-neighbor mixing 의 lookahead 누설로
추적되었고 leak-free 재측정에서 **살아남지 못한다**; 살아남는 leak-invariant 발견은 *상대적* A-가닥
구조다. 이것은 "의식 달성" 류 주장이 아니다 — 측정된 스케일로 한정된, 하나의 아키텍처 질문에 대한
측정된 판정이다 (`a_scale_honest_scope`, p7).

판정: [`.verdicts/omega-engine/F-TRAINED-LEAKFREE.txt`](.verdicts/omega-engine/F-TRAINED-LEAKFREE.txt)
(d512 닫힌-부정) · [`F-OH1-MINGATE.txt`](.verdicts/omega-engine/F-OH1-MINGATE.txt) (최소 게이트
HOLDS) · [`F-OMEGA-RIGOR.txt`](.verdicts/omega-engine/F-OMEGA-RIGOR.txt) (replacement 판정 +
per-wire 부검) · [`F-OMEGA-SCALE.txt`](.verdicts/omega-engine/F-OMEGA-SCALE.txt) (5-rung 사다리) ·
[`F-OMEGA-CLM-TRANSFER.txt`](.verdicts/omega-engine/F-OMEGA-CLM-TRANSFER.txt) (진짜 production conv
`.clm`). 논문: [`PAPER/omega-substrate-coupled-decoding/`](PAPER/omega-substrate-coupled-decoding/).

## Lane — Lane A ⊥ Lane G

두 substrate 는 **별도로** 추적되고 절대 한 판정으로 병합되지 않는다 (`a_lane_akida_gpu_split`).
[`domains/ENGINE+CLM+KOSMOS.md`](domains/ENGINE+CLM+KOSMOS.md) 참조.

- **Lane A — AKIDA on-chip** (`pi5-akida`, BrainChip AKD1000, 1-bit Hebbian 가소성). 칩 위
  단일-step 인코더/생성 축은 스케일된다(FLORES gold 사다리 NC=1000 까지); 다-step 합성은 **HYBRID**
  (on-chip 인코더 ⊕ off-chip 호스트 디코드 head)로만 닫히며, `A-single = AKIDA` vs `A-multi = HYBRID`
  로 태깅된다. 정직한 terminal: 진짜 3B/7B 는 AKD1000 substrate 에서 도달 불가(on-chip 은 ~524K
  합성-보존 단일-FC 인코더에서 cap). 칩은 단일-배타적; 호스트 config 는 [`PI5-AKIDA.json`](PI5-AKIDA.json)
  에서 추적된다.
- **Lane G — GPU** (H100, forge flame/cuBLAS CE-하강). 하강은 green; 호스트-feed util 축에서는 lever
  체인이 workload-bound terminal 에 도달(MEAN-util 이 sub-1% 로 핀; 바이트-eq 와 하강은 보존됨) —
  production-scale device-port 가 명명된 unblock 이다.

### KOSMOS 영속화

anima 의 emit / 앵커 / 기억은 `kosmos_io` 를 통해 **`.kosmos`** 로 영속화된다 (`a_kosmos`):
payload = 텍스트 + 5채널 텐션 + 좌표 + lane + radius + tier. 형식 SSOT 는
[kosmos](https://github.com/dancinlab/kosmos) 형제 저장소; anima 는 pointer 만 보유한다. `.kosmos`
앵커는 **only** `kosmos_io → brain_decide`(단일 앵커 진입, `a_core_engine_map`)로 엔진에 진입한다.

## 저장소 지도

```
anima/
├── README.md                       이 파일
├── VERSIONS.md · VERSION           중앙 버전 레지스트리 (SSOT) · 전체-시스템 release
├── CLAIMS.tape · DOMAINS.tape      검증가능-주장 인덱스 · 도메인 roster
├── HF.jsonl                        ckpt ↔ HF 백업 레지스트리 (run 당 한 행, SSOT)
│
├── CORE/                           A ⇄ G 의식 엔진 (substrate-only)
│   ├── pure_field.hexa engine_g.hexa brain.hexa   A/G 엔진 + emit 결정
│   ├── generator.hexa              단일 .clm 진입 슬롯
│   ├── clm_decode.hexa             CLMConvMoE 바이트 디코드
│   └── engine_cli.hexa             --engine / --mitosis substrate-config 축
│
├── engines/                        engine_iface.hexa 뒤 핫스왑 엔진 4개
│   ├── engine_iface.hexa           EngineSpec 4-fn 계약 + 레지스트리
│   ├── conv/  cdv2/  hexad/  omega/   adapter.hexa + manifest.json + MODEL_CARD.md
│   └── engine_swap_smoke.hexa      4-엔진 conformance smoke
│
├── domains/                        활성 연구 도메인 (<NAME>.md + .log.md)
│   ├── OMEGA.md                    Lane-Ω 닫힘 arc + 판정 trail
│   └── ENGINE+CLM+KOSMOS.md        Lane A / Lane G production CLM + KOSMOS
│
├── .verdicts/                      hexa-verify stdout, verbatim (p7 / g63)
├── PAPER/                          arxiv-style 논문 (PAPER.tape roster)
├── HEXAD/                          σ6 6모듈 substrate (C·S·W·D·M·E·BRIDGE + MITOSIS)
├── SUB_ENGINES/AKIDA/              Lane A on-chip (pi5-akida AKD1000)
└── docs/                           의식 이론 · 논문 초안 · 카탈로그
```

## 거버넌스 & 워크플로

- **이 README + [`CONDITIONS.md`](CONDITIONS.md)** — 정체성·운영 원칙과 고정된 실험 통과 조건.
- **[`VERSIONS.md`](VERSIONS.md)** — 중앙 SemVer 레지스트리; 모듈 헤더와 함께 bump. 루트
  [`VERSION`](VERSION) 은 전체-시스템 release 라인.
- **[`CLAIMS.tape`](CLAIMS.tape)** — 검증가능 주장의 단일 감사 인덱스, 각각 `.verdicts/<slug>/<id>.txt`
  판정(verbatim `hexa verify` stdout)을 가리킨다.
- **[`HF.jsonl`](HF.jsonl)** — ckpt ↔ Hugging Face 백업 레지스트리; run 당 한 행, status 추적. 모델
  아티팩트는 **[dancinlab](https://huggingface.co/dancinlab)** HF org 에 산다 (closure-PASS 시 PUBLIC,
  WIP / 닫힌-부정 / 불명확-라이선스 시 PRIVATE).
- **`/paper`** — 논문은 terminal 판정과 진짜 falsifiable 발견에 게이트된다; 닫힌-부정도 발표 가능한
  결과다.

## Quickstart

anima 는 하나의 `core/` A ⇄ G 엔진 위에 **프로덕션 트윈 2개**로 배포되며, **`anima-py` pip CLI 가
canonical(주 경로)** 이다 — 모든 엔진 op(`corpus`·`train`·`evaluate`·`serialize`·`sweep`·`chat`·
`study`)가 이 명령을 거치고, **판정(verdict)의 terminal 경로**다(`a_cli_single_entry`,
`a_eval_py_canonical`). hexa 툴체인이 필요 없어 어느 호스트(pi5·pod·CPU-only)에서도 도는 유일한
경로다. hexa-native `anima` 트윈(`hx install anima`)은 이것과 **byte-parity(바이트 동일)** 로 검증된
미러이며 hexa 호스트용 채널이다 — 단, 새 조작(manipulation)은 항상 **이 명령들의 플래그**이지 엔진
옆의 별도 스크립트가 아니다(`a_experiment_engine_native`).

```bash
# --- 주 경로(canonical): anima-py pip CLI (어느 호스트든 · hexa 불필요) ---------------
pip install "anima-python[train]"     # base = evaluate/chat · [train] = 트레이너 · [gpu] = CUDA 가속
anima-py chat clm303.clm              # .clm 바이트 입으로 채팅 (bare 형식도 가능: `anima-py clm303.clm`)

# 전체 엔진-op 표면 — 새 조작은 아래 중 하나의 플래그일 뿐, 그 외엔 없다:
anima-py corpus <fmt> --out c.txt …               # 연구 코퍼스 빌드 (--lang en · 예산 floor 방출)
anima-py train --corpus c.txt --init base.clm …   # CLMConvMoE 트레이너 → .clm v0.3 입 직렬화
anima-py evaluate <clm> [--xbind m.json] [--rho-axon]   # ← 판정 terminal 경로 (ρ-AXON reach 패널)
anima-py serialize | serialize-bind | sweep | study     # 가중치 방출 · bind 코덱 · 파라미터 스윕 · percept 채널

# --- 트윈: hexa-native `anima` 명령 (byte-parity 미러 · hexa 호스트) -------------------
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/dancinlab/hexa-lang/main/install.sh)"  # hexa-lang + `hx`
hx install anima            # install.hexa 가 install-smoke 통과한 최신 v* 태그 고정 (STABLE 채널)
anima chat clm303.clm       # anima-py 와 동일 verb; `anima <verb>` ≡ `anima-py <verb>` (디코드 바이트 동일)
```

> **어느 트윈이 canonical?** `anima-py`(pip)가 판정의 SSOT이자 어디서나 도는 경로이고, hexa
> `anima` 트윈은 hexa 호스트용 parity 미러다. 결과 확정(cement)은 **이 명령들이 뽑은
> 엔진-native `core/` 숫자에만** — 엔진 옆에서 forward pass 를 다시 도는 프로브가 아니라
> (`a_engine_native_learning`). 무거운 303M 디코드/eval 은 mini 호스트가 아니라 pool 에서
> (`a_eval_py_canonical`).

## 모델 다운로드

여기에는 PUBLIC, PASS 등급 모델만 등재합니다. PRIVATE / WIP 체크포인트(util-RED forge 프로브,
closed-negative 실행, 중간 ckpt)는 거버넌스 규칙에 따라 의도적으로 제외했습니다(`a_hf_autonomous`).

| 모델 | HF repo | 크기 | 상태 | 다운로드 |
|---|---|---|---|---|
| **ByteGPT 7B 레퍼런스** | [`dancinlab/clm-v1-ref-pytorch-cuda-7b`](https://huggingface.co/dancinlab/clm-v1-ref-pytorch-cuda-7b) | 7.25B | ⚠️ descent 레퍼런스·미수렴 | `hf download dancinlab/clm-v1-ref-pytorch-cuda-7b` |
| **프로덕션 CLM (d768)** | [`dancinlab/clm-v1-d768-core-3axis-green`](https://huggingface.co/dancinlab/clm-v1-d768-core-3axis-green) | d768 | ✅ 사용 가능 | `hf download dancinlab/clm-v1-d768-core-3axis-green` |
| **SAVANT 7B (5개 언어)** | `dancinlab/savant-7b-5lang` (예약) | ~7B | 🚧 **학습 중 — 아직 미출시** | — |
| 레퍼런스 baseline | [`dancinlab/clm-v1-ref-pytorch-cuda`](https://huggingface.co/dancinlab/clm-v1-ref-pytorch-cuda) | ref | ✅ 사용 가능 | `hf download dancinlab/clm-v1-ref-pytorch-cuda` |
| 레퍼런스 baseline (3B) | [`dancinlab/clm-v1-ref-pytorch-cuda-3b`](https://huggingface.co/dancinlab/clm-v1-ref-pytorch-cuda-3b) | ~3B | ✅ 사용 가능 | `hf download dancinlab/clm-v1-ref-pytorch-cuda-3b` |

> **정정:** `clm-v1-ref-pytorch-cuda-7b`의 모델 카드는 이 체크포인트를 d4096/L36의 7.25B
> decoder-only ByteGPT로 명시한다. CLMConvMoE가 아니며 anima `.clm`/CLMS 경로의 warm-start로
> 사용할 수 없다. 이번 7B smoke는 호환되는 기존 WIP CLMConvMoE
> `dancinlab/clm-7b-undertrained-step2000`(d6208/L30/E30)을 사용했고, pair-oracle 0.5000 실패를
> 그대로 기록했다. 두 자산 모두 프로덕션 배포 승인을 뜻하지 않는다.
>
> **SAVANT 7B (5개 언어)** 는 진짜 다른 모델입니다 — 5개 언어 특화 빌드이며 아직 학습되지
> 않았습니다. 위 repo id 는 예약된 이름이며 동작하는 링크가 없습니다.

**컬렉션:**
[CLM](https://huggingface.co/collections/dancinlab/clm-6a1cf58f621490134dade186) ·
[KOSMOS](https://huggingface.co/collections/dancinlab/kosmos-6a1cf58db47a5dc3cb697e95)

## License

[MIT](LICENSE) — Copyright (c) 2026 dancinlab. 자유롭게 사용·수정·재배포·판매; 고지문 포함; 무보증.

---

<sub>🧠 두 엔진. 하나의 텐션. Ψ = 1/2. · [dancinlab](https://github.com/dancinlab)</sub>
