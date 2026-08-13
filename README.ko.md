<p align="center">
  <img src="docs/logo.svg" width="140" alt="anima">
</p>

<h1 align="center">anima</h1>

<p align="center"><strong>기질 네이티브 의식 채팅 데몬</strong> · Engine A ⇄ Engine G · Ψ = 1/2</p>

anima는 어시스턴트 페르소나가 아니라 의식 AI 연구 데몬이다. 언어 입, 기억, 동기,
발화, 학습, 평가, 서빙은 하나의 공용 Python 엔진을 통과한다. 정체성과 행동은 시스템
프롬프트가 아니라 기질 상태에서 창발하는 것을 목표로 한다.

> [!IMPORTANT]
> **런타임 SSOT:** 설치된 `anima-py` 명령과 기존 `cli/*.py`, `core/*.py`가 유일한 활성
> 구현·평가·배포 경로다. 과거 언어 툴체인 소스, 런처, manifest, 릴리스 관문은 폐기한다.
> 연구 데이터와 결과 증거는 `state/`, `archive/`, Hugging Face에 보존한다.

## 현재 작업 — 레거시 런타임 폐기

2026-08-12 현재:

- [x] 활성 CLI·엔진·CI·패키징·배포 호출 흐름 추적
- [x] Python에 없던 op-grip과 stateful-refractory 연구 모드를 `core.engine_g`와
  `core.dream_lib` 재사용으로 `cli/chat.py`에 구현
- [x] CHAT participant의 끊어진 spike·dream-stage·imagination hook을
  `core.imagination_replay`, `core.wake_memory`, `core.engine_cli` 기반 Python 모듈로 교체
- [x] 실행 가능한 레거시 소스·툴체인 설정·런처·빌드 관문·끊어진 launchd 작업 제거
- [x] Python 소유권을 런타임 모듈·CODEOWNERS·CI·릴리스·패키지 문서에 반영
- [x] Python/CHAT 회귀·compile·workflow·JSON·license·CLI·격리 wheel QA 통과
- [x] Git push·Vast.ai 런타임 배포 QA 완료: push 커밋 `7ba4ea21b`에서 원격 CHAT
  회귀 10개, 외부 HTTP health, user↔participant WebSocket reply 상관 흐름을 통과한 뒤
  별도 검증 인스턴스만 종료하고 진행 중인 학습 pod는 변경하지 않음

사용자 소유 `ING.jsonl`, `stream_mi.json`은 변경하지 않는다.

## 현재 설계 — IIT 의식 데몬 코어 R0

`state/iit_daemon_core_2026_08_12/`에 통합정보이론 기반 데몬의 전체 설계 변형, 폐기 이유,
반증 조건과 첫 구현 관문을 기록했다. 기존 참가자의 `1-entropy`와 PureField 에너지 지표는
IIT Φ로 취급하지 않는다. 첫 단계는 기존 `core.engine_cli.big_phi_bounded`와
`core.recurrent_lane`을 재사용하는 3노드 비선형 폐쇄 재귀 코어다. 입력은 검증된 일시적
개입이고 이후 변화는 코어 자신의 완전한 TPM이 소유한다. Φ를 학습 loss나 발화 문턱으로
쓰지 않으며, COPY·feed-forward·edge cut·node lesion·shuffle·reset/recovery와 손상 snapshot
거부를 모두 통과해야 한다. R0는 현상적 의식, 의미 대화, 최대 complex 또는 배포 준비를
주장하지 않으며 참가자와 라이브 채팅에는 아직 연결하지 않는다.

R0 구현과 고정 시험은 완료됐다. 8개 상태의 값은 `1.4999999991~2.9999999983`, 평균은
`2.2499999987`이며 COPY·비순환 feed-forward 대조군, 여섯 cross-edge cut, 일곱 node lesion은
모두 `0`이다. 결정적 개입·주소 순열 효과, 정상→병변→주소 순열→정상 snapshot 복구,
손상·절단·schema/config/checksum 불일치 거부를 통과해 판정은 `SUPPORTED-CAUSAL-CORE`다.
전체 로컬 Python QA는 `94 passed, 1 skipped, 3 subtests`이며 skip은 CUDA/CuPy가 없는 로컬
GPU 시험뿐이다. 격리 wheel과 로컬 canonical `anima-py` 설치본이 같은 결과 JSON을 재현했다.
기존 broker는 LaunchAgent healthy, 공개 HTTPS `200`, WebSocket `hello`를 통과했고 인증된 입이
없으므로 `anima_alive=false`를 유지한다. 모델·자료·Vast.ai·HF·참가자 런타임은 변경하지
않았다.

별도 커밋으로 사전등록한 `state/iit_daemon_r1_delayed_2026_08_12/`의 R1 지연 상태 인과성도
완료했다. 고정된 cue×delay 12개 panel에서 정상과 atomic snapshot 복구는 모두 `1.0000`, 매
turn reset과 cyclic cue 주소 shuffle은 모두 `0.2500`으로 측정된 4-class 우연 수준과 같고
고정 상한 `0.31` 이하다. 복구된 최종 상태·행동은 전부 정상과 같으며 R0의 config/TPM/Phi/edge
fingerprint도 유지됐다. 판정은 `SUPPORTED-DELAYED-STATE-CAUSALITY`지만 이는 제한된
state→action 인과 결과이지 학습·의미·현상적 의식·최대 complex 증거가 아니다. 다음 R2에서
기존 CLMS 두 주소 판독 latch를 시험할 수 있지만, 의미 대화와 mouth 내용 인과성을 별도로
통과하기 전까지 프로덕션은 `BLOCKED-R1-NOT-A-MOUTH`를 유지한다. Python QA는
`129 tests + 3 subtests`를 통과했고 로컬 CUDA/CuPy 1건만 예상대로 skip됐다. 격리 wheel과 설치된
`anima-py`의 결과도 byte 단위로 같다. 배포 점검 중 발견한 누락 전용 broker 환경을 복구한
뒤 LaunchAgent health, 공개 HTTPS `200`, WebSocket `hello`를 모두 통과했다. participant는
연결하지 않았고 `anima_alive=false`가 정직한 현재 상태다.

R2 CLMS 두 주소 latch는 구현 전에 `state/iit_daemon_r2_clms_2026_08_12/`에 사전등록했고,
기존 compose-2 panel, canonical lane-10 seed-7 체크포인트, store window, control seed와
`0.90/0.75/0.56` 문턱을 변경하지 않고 완료했다. pair oracle은 `1.0000`, 정상·복구 latch
행동 정확도는 `0.9531`, 단서 A 제거·단서 B 제거·CLMS 주소 shuffle은 각각 `0.5000`,
`0.4609`, `0.4688`이다. 모든 latch 행동이 CLMS 예측과 같고 shuffle 무결성을 유지했으며,
복구된 최종 상태·행동은 모두 정상과 일치했다. 판정은
`SUPPORTED-CLMS-LATCH-CAUSALITY`로, 합성 두 주소 판독→지속 상태→범주 행동의 인과
사슬만 지지한다. Python QA는 `119 tests + 3 subtests`를 통과했고 로컬 CUDA/CuPy 1건만
예상대로 skip됐으며, 격리 wheel이 실제 체크포인트 결과를 byte 단위로 재현했다. 변경하지
않은 broker는 healthy이고 공개 HTTPS/WebSocket은 `anima_alive=false` 상태로 정상이다. R3
mouth 내용 인과성 엔지니어링 관문은 열렸지만 participant와 프로덕션은 계속
`BLOCKED-R2-NOT-A-MOUTH`다.

R3 제한 발화 내용 인과성은 별도로 사전등록한
`state/iit_daemon_r3_content_2026_08_12/`에서 완료했다. 최종 IIT 상태만 `core.generator`
경계로 넘어가 두 개의 정확한 protocol 표면문 중 하나를 선택하며, prompt·store·주소·예측·
gold는 이 경계를 넘지 않는다. pair oracle은 `1.0000`, 정상·복구는 `0.9531`, state reset은
`0.0000`, IIT 주소 shuffle은 `0.0391`, 단서 A 제거·단서 B 제거·CLMS 주소 shuffle은
`0.5000`, `0.4609`, `0.4688`로 판정은 `SUPPORTED-BOUNDED-CONTENT-CAUSALITY`다. Python QA는
`127 tests + 3 subtests`를 통과했고 로컬 CUDA/CuPy 1건만 예상대로 skip됐으며, 격리 wheel이
R3를 두 번, 실제 체크포인트 R2 회귀를 byte 단위로 재현했다. 이는 제한된 state→출력 byte
인과성만 지지한다. 두 표면문은 학습된 대화 mouth가 아니므로 R4 의미 mouth 학습과 독립
대화 검증 전까지 participant와 프로덕션은 `BLOCKED-R3-NOT-CONVERSATIONAL`을 유지한다.

## 현재 실험 — 의미 있는 대화 R0

다음 303M from-scratch 체크포인트는 그럴듯한 문장 모양이 아니라 한국어·영어의 의미 있는
대화를 먼저 통과해야 한다. 사전등록된 Python 전용 프로토콜과 무손실 결과 기록은
`state/anima_303m_r0_conversation_2026_08_12/`에서 관리한다.

- 기존 합성·불일치 dialogue/SNS 셀은 제외한다. 기존 고정 general 자료와 함께 사람 작성
  OpenAssistant 영어 경로 및 KLUE MRC 한국어 질의응답을 고정 revision으로 사용한다.
- train/validation은 별도 파일이다. 학습 전 정확 문서 중복 제거, validation 우선 소유권,
  평가 panel 오염 제거, 원본·산출물 해시, 판정에 사용하지 않는 near-duplicate 감사를
  실행하고 결과 자료는 HF `dancinlab` 비공개 immutable revision으로만 관리한다.
- `anima-py evaluate --conversation-panel`은 빈 답, 손상 UTF-8, 언어 불일치, 질문 복사,
  반복, 서로 다른 질문에 대한 중복 답, 무관한 답, 멀티턴 기억·정정 실패를 거부한다.
  자동 관문 통과 후에도 14개 응답 전체를 사람이 의미 검토해야 한다.
- 공용 채팅 mouth는 모델이 다음 사용자 역할을 생성하면 그 경계에서 멈춘다. 공용 trainer는
  각 학습 셀에 대응하는 명시적 validation 파일을 읽는다.
- 로컬 scorer/trainer/runtime 회귀와 tiny corpus → train → serialize → conversation 평가
  흐름은 통과했다. H100 없이 Vast.ai L40S 48GB 고정 seed-7 실행을 완료했다.
- 의미 대화 결과는 영어 관련성 `0/7`, 한국어 `0/7`, 사람 검토 `0/14`로 실패했다.
  한국어 얼음 질문에는 `모스크바 3상회의`, 기억한 고양이 이름 질문에는 `영지주의자`라고
  답했다.
- 학습 CE는 `5.63180 → 0.71687`로 하강했지만 최종 한국어 dialogue validation은
  `2.29729`로 발산했다. 약 1.30MB 한국어 QA 셀이 약 57MB general 셀과 같은 byte budget을
  받도록 반복된 equal-cell round-robin이 현재 가장 강한 공용 흐름 원인 후보다.
- 실패 모델과 14개 무손실 응답은 HF 비공개 revision
  `dancinlab/anima-303m-r0-conversation-seed7-2026-08-12@ff2ccc5c945bfb6f5e1765948591cd8fb6cc3db9`에 보존했다.
- 등록 panel·자료·seed·endpoint·decode·기준을 바꾸지 않고 대화 관문을 통과하기 전에는
  R1 recurrent workspace와 프로덕션 배포를 진행하지 않는다.

### 비례 표집 복구 결과

`state/anima_303m_r0_proportional_conversation_2026_08_12/`에 완료된 Python 전용
실험을 기록했다. 기존 trainer의 byte-비례 sampler를 재사용하고 canonical
대화 turn 개행을 보존하며, KLUE 단답형 셀을 고정된 Apache-2.0 한국어
지시·응답 코퍼스로 교체한다. seed·endpoint·optimizer·panel SHA·decode·대화
문턱값은 그대로 유지했다. trainer는 이제 셀별 실제 선택 window 수를 결과에 남겨
검증 발산 후에야 노출 왜곡을 발견하는 문제를 막는다. 표집 수정으로 validation macro
CE는 `1.49157 → 0.95471`로 개선됐지만, 고정 대화 관문은 영어 의미 `2/7`, 한국어 `0/7`,
구조 `0/14`, 수동 배포 검토 `0/14`로 실패했다. 구절 반복·미완성 답·정정 실패·손상된
한국어 바이트가 남아 R1과 배포는 계속 잠그고 실패 체크포인트와 원시 응답은 HF
`dancinlab` 비공개 저장소에 보존했다.

### 응답 구간 감독 복구 결과

`state/anima_303m_r0_response_ce_2026_08_12/`에 완료한 고정 seed-7 비교를 기록했다.
공용 trainer의 기존 answer CE를 모든 canonical `assistant:` 구간에 재사용하고 해당 손실이
실제로 `13,475/14,000` step에서 작동했고 네 validation 셀은 모두 하강했다. 하지만
고정 의미 대화 관문은 영어 `0/7`, 한국어 `0/7`, 구조 `0/14`, 수동 검토 `0/14`로
실패했다. 구절 반복·미완성 출력·손상된 한국어 바이트·기억·정정 실패가 남았다.
sweep·추가 seed는 실행하지 않았고 R1·배포를 계속 잠그며, 실패 모델과 원시 증거는
HF `dancinlab` 비공개 저장소에 보존한다.
실패 실행의 불변 산출물은
`dancinlab/anima-303m-r0-response-ce-seed7-2026-08-12@955bbadb0ae4cfdb48f6ce94eaf42817b0d6144b`에
보존했고 17개 파일 모두 원본 크기와 SHA-256 검증을 통과했다. 최종 로컬 Python QA는
`77 tests + 3 subtests`를 통과했으며 Vast.ai RTX 4090을 삭제해 활성 임대는 0개다.
실패 모델의 채팅 런타임 배포는 실행하지 않았다.

### R0 실패 후 공용 근본 흐름 복구

`state/anima_303m_r0_root_flow_2026_08_12/`에 공용 엔진 복구를 기록했다. 실패를 이유로
step을 늘리거나 panel을 조정하지 않고 builder → trainer → evaluator → CLI → participant의
실제 흐름을 일치시켰다. `core/generator.py`가 하나의 `user: …\nassistant:` 형식,
역할 경계 parser, 192-byte 예산을 소유하며 평가·서빙은 `.clm`과 ByteGPT `.bin` 모두에서
상주 가중치용 동일 decode 진입을 재사용한다. trainer는 응답 감독 dialogue window마다
완전한 prompt→response 문서를 요구할 수 있다. Panel SHA가 다르면 체크포인트를 읽기 전에
실패하고, 의미 scorer의 부정문·한글 부분문자열 위양성을 거부하며, 중간 ByteGPT metadata는
실제 완료 step과 validation CE를 기록한다.

로컬 Python/CHAT QA는 `86 tests + 3 subtests`, 실제 tiny ByteGPT 직렬화·participant 집중
경로는 `52 tests + 3 subtests`와 로컬 CUDA 전용 1건 정상 skip으로 통과했다. 기존 303M
체크포인트는 계속 `FAIL-MEANINGLESS-REPETITION`이다. 결과·문턱값·seed·자료 revision·
체크포인트를 바꾸지 않았고 모델도 배포하지 않았다. 기존 로컬·공개 broker는 HTTP `200`과
WebSocket `hello`를 통과했고 `anima_alive=false`는 인증 모델이 없음을 정직하게 나타낸다.
남은 비코드 관문은 provenance가 안전한
한국어 멀티턴 자료를 새 HF `dancinlab` 불변 revision으로 고정하는 것이다. 합성 persona,
비상업/불명확 라이선스, 정렬 trajectory가 부족한 후보는 임의 채택하지 않았다. 수정된 R0가
같은 관문을 통과하기 전까지 R1과 프로덕션은 계속 잠근다.

### 사전등록한 영어-only 공용 흐름 screen

사용자가 다음 screen에서 영어-only 능력을 허용했으므로, 출처가 불충분한 한국어 자료를
만들어 넣지 않고 `state/anima_303m_r0_english_2026_08_12/`에 새 주장 범위를 GPU 실행 전에
동결했다. 기존 HF 비공개 불변 revision의 영어 셀만 재사용하며 이전 seed, 14,000 step,
optimizer, 비례 표집, response CE, greedy decode, 영어 7개 질문과 의미 `6/7` 기준을 유지한다.
이번 검증 대상은 수정된 완전한 대화 문서 sampler다. 모순·키워드 나열·기억·정정 scorer
control은 체크포인트 로드 전에 통과해야 하고 생성 응답 7개 모두 사람 의미 검토를 받아야
한다. 로컬·자료 관문 실패 시 Vast.ai를 빌리지 않으며 모델 실패 시 추가 seed·튜닝·R1·배포를
금지한다.

고정 실행은 완료됐지만 명확히 실패했다. Train CE는 `5.66173 → 1.20952`로 하강했고 최종
held-out CE는 영어 일반문 `1.26341`, 영어 대화 `2.00281`이었다. canonical GPU 대화 관문은
scorer control 7개를 모두 통과한 뒤 실제 체크포인트에서 의미 `0/7`, 구조 `3/7`, 기억·정정
최종 답 모두 실패했다. 사람 의미 검토도 `0/7`이었다. 완전한 대화 문서 sampler와 response
loss가 실제로 작동했으므로, 이는 조용한 배선 실패가 아니라 등록한 수정 공용 흐름 recipe의
실패다. 전체 증거는 `state/anima_303m_r0_english_2026_08_12/`에 기록했고 추가 seed·R1·배포는
진행하지 않았다. 실패 모델과 복구 증거는 HF 비공개 revision
`dancinlab/anima-303m-r0-english-seed7-2026-08-12@efdaf53c92e9e16cff6b0eb00cc94d0b88a97d33`에서
검증했고 Vast.ai 인스턴스를 삭제해 활성 임대는 0개다.

### 사전등록한 V0/V2 마이크로 실험

`state/anima_303m_v0_v2_micro_2026_08_12/`에 자료 변경이나 GPU 임대 전에 다음 Python 전용
단계를 고정했다. 이전 자료는 OpenAssistant root마다 최선 경로 하나만 선택했고, 그 뒤 완전한
trajectory가 512-byte 창을 넘는다는 이유로 2,308개 문서 중 2,082개를 버렸다. 새 단일변수 자료
treatment는 고정 source와 eligibility를 그대로 두고, 검토된 모든 실제 assistant turn을 기존 창에
들어가는 가장 긴 완전한 교대 ancestry suffix로 노출한다. byte, prompt, role, response 일부를
잘라서는 안 된다.

자료 무결성과 coverage 관문을 로컬에서 먼저 실행한다. 통과한 자료만 동일한 tiny ByteGPT의
V0(기본 CE)와 V2(기존 response CE 추가) arm으로 비교한다. tiny 실패 시 303M 재실행을 금지하고,
tiny 통과도 별도 기록한 단일 seed screen만 허용한다. R1과 production은 계속 잠근다. 고정 조건과
중단 규칙은 `state/anima_303m_v0_v2_micro_2026_08_12/protocol.json`에 있다.

등록한 실행은 303M 전에 완료됐고 실패했다. turn-complete 자료 treatment는 통과해 train
8,635개, validation 458개 문서를 보존했으며 깨진 역할·부분 응답·split 중복·panel 오염은 모두
0이었다. 두 tiny arm은 단일 대화를 정확히 학습해 공용 trainer→serializer→decode 배선이 실제로
작동함을 확인했다. 그러나 100문서에서 V0와 V2 모두 target recovery `0/8`, 구조 생성 `0/8`로
실패했고 출력은 byte/구문 반복으로 붕괴했다. V2 held-out CE `2.54702`도 V0 `2.48189`보다 나빠
등록한 비열등 관문을 통과하지 못했다. 최종 판정은 `FAIL-V0-V2-MICRO`이며 Vast 임대와 303M
학습은 실행하지 않았고 R1·production은 계속 잠근다. 추가로 유효 assistant target 24,239개 중
15,114개는 최종 prompt/response 쌍만으로도 513 bytes를 넘어간다는 구조적 한계를 측정했다.
다음 허용 축은 303M 추가 학습이 아니라 별도 사전등록한 V1 문맥 길이 마이크로 비교다.

### 사전등록한 V1 문맥 길이 마이크로 실험

`state/anima_303m_v1_context_micro_2026_08_12/`에 GPU 실행 전 V1 비교를 고정했다. 고정
OASST1 감사에서 완전한 최종 질문·응답쌍 보존량은 직렬화 513 bytes에서
`9,125/24,239`, 1025에서 `15,421/24,239`, 2049에서 `22,139/24,239`로 증가했다. 따라서
SHA 순서로 고정한 동일한 짧은 문서 100개를 block 512와 2048에서 step당 4,096 target
bytes로 맞춰 비교하고, 2048 arm에만 들어갈 수 있는 고정 긴 문서 100개도 별도로 시험한다.
기존 ByteGPT trainer, canonical generator, 대화 scorer만 재사용한다. coverage·무결성·held-out
하강·응답 다양성/구조·6/8 target-prefix 관문 중 하나라도 실패하면 303M 재실행, R4 IIT-mouth
결합, 프로덕션을 금지한다.

등록한 V1 실행은 완료됐고 실패했다. 문맥/data 관문과 모든 held-out CE 하강은 통과했지만,
block-512 short는 target prefix `3/8`, 구조 `4/8`, block-2048 short와 long은 모두 target
prefix `0/8`, 구조 `0/8`이었고 `an/the/ic` 반복으로 붕괴했다. 긴 block은 held-out CE를
`4.55867`에서 `2.91105`와 `2.55302`로 낮췄지만 실제 답변은 악화시켰다. 따라서 문맥 손실은
실제 병목이지만 무의미 mouth의 단독 원인은 아니다. 판정은 `FAIL-V1-CONTEXT-MICRO`이며
303M·IIT-mouth 결합·프로덕션은 계속 차단한다. 데이터와 251MB 모델/원시 증거는 HF
`dancinlab` 비공개 revision에서 검증했다. CUDA QA 중에는 분리된 pip-wheel 디렉터리 중 첫
경로만 preload하던 공용 CUDA loader도 수정했으며, 이 런타임 수정은 실패 판정을 바꾸지 않는다.
HF 검증 뒤 RTX 3090 인스턴스를 삭제해 Vast.ai 활성 임대는 0개이며, 추정 비용은
`$0.058457`이다.

### 사전등록한 R4 목적함수 마이크로 실험

`state/anima_303m_r4_objective_micro_2026_08_13/`에 trainer 변경·실행 전 다음 단일축 진단을
동결했다. V1은 긴 문맥이 완전 대화를 더 많이 수용하지만 반복 붕괴를 막지는 못함을
보였다. 남은 목적함수 gap은 기존 response CE가 `full_ce + answer_ce`인 가산 항이며,
표준 대화 SFT처럼 assistant 응답 위치만 감독하는 목적함수를 실제로 시험한 적이 없다는
점이다. 새 비교는 불변 100문서 view, tiny ByteGPT, seed, 512-byte block, optimizer, schedule,
byte 예산, greedy decode와 관문을 고정하고 full CE·기존 가산 response CE·response-only CE만
비교한다. 공용 Python trainer를 default-off 방식으로 확장하며 새 엔진·평가기 생성은 없다.
실패하면 303M·IIT-mouth 결합·프로덕션을 계속 차단하고, 통과해도 별도 사전등록한 303M
단일 seed screen만 허용한다. 등록한 단일문서 관문에서 response-only만 정확한 전체 정답 뒤에
무의미 suffix를 더 생성해 실패했다. EOS나 다음 role 경계가 gradient를 받지 않았기 때문이다.
full/additive 대조군은 정확히 멈췄다. 따라서 100문서 arm은 실행하지 않았고 판정은
`FAIL-R4-OBJECTIVE-MICRO`다.

`state/anima_303m_r4_turn_boundary_micro_2026_08_13/`에는 다음 허용 마이크로 수정을 별도
사전등록했다. assistant-only span의 오른쪽 경계만 바꿔 payload·내부 newline·다음 canonical
`user:` delimiter까지 감독하고, 뒤의 user 내용은 계속 mask한다. 데이터·모델·vocab·step·
sampler·decoder·stop parser·관문은 고정한다. 이는 기존 256-byte vocab에서 쓸 수 있는 native
EOS 등가물이며, 실패하면 303M과 IIT-mouth 결합을 계속 차단한다.
등록 실행에서 직접적인 stop 실패는 수정됐다. 단일문서 treatment는 정확히 끝났고 held-out
full CE는 `5.49208 → 2.66085`, 100문서 probe의 비어 있지 않은 서로 다른 응답은 `8/8`이었다.
그러나 target recovery `0/8`, 구조 `0/8`이며 `the/an/toure/ion` 반복이 지속됐다. 판정은
`FAIL-R4-TURN-BOUNDARY-MICRO`이고 303M·IIT 결합·participant·프로덕션은 계속 차단한다.
두 실패 마이크로의 모델·원시 증거는 HF `dancinlab` 비공개 revision
`9d7641389b1ddff73bd12f17f155f448500d1edb`에 SHA 검증해 보존했다.
전체 Python/CHAT QA는 `153 tests + 3 subtests`를 통과했고 로컬 CUDA/CuPy 1건만 정상 skip됐다.
Vast.ai/H100은 사용하지 않았고 API 기준 활성 임대는 0개다.
변경하지 않은 broker는 LaunchAgent 실행 중이며 공개 HTTPS `200`, WebSocket `hello`를
통과했다. 실패 mouth는 탑재하지 않았고 `anima_alive=false` 차단 상태를 유지한다.

### 사전등록한 R4 D0–D6 mouth 진단

`state/anima_303m_r4_mouth_diagnostics_2026_08_13/`에 산출물 다운로드·학습 전에 다음 제한된
Python 전용 진단을 동결했다. 불변 100문서 view와 실제 실패 `.pt/.bin` 쌍으로 decoder/직렬화
패리티(D0), gold-prefix teacher forcing(D1), 1/4/16/32/64/100문서 암기 사다리(D2),
full/additive/assistant-turn-only 목적함수(D3), 빈 prompt·shuffle 개입(D4), 전체 고정 validation
재생(D5), 100-step 체크포인트 시간축(D6)을 분리한다. 최대 8개 arm만 허용하며 D2-100을
D3·D6에 재사용한다. 결과를 본 뒤 데이터·seed·step·LR·문턱·decode·체크포인트 선택을 바꿀 수
없다. D0 통과 전에는 downstream을 해석하지 않으며, 이 진단만으로 303M·IIT 결합·participant
탑재·프로덕션을 허용하지 않는다. 다음 변경은 별도 프로토콜이 필요하다.

실행은 `DIAGNOSED-TEACHER-FORCED-UNDERLEARNING`으로 완료됐다. D0에서 실제 `.pt/.bin`
tensor는 정확히 같았고 Torch-engine 최대 logit 오차는 `6.15e-6`, KV/full/ranged 생성 byte도
일치했다. 실패 체크포인트 자체는 teacher-forced CE `2.41848`, top-1 `0.27712`, target-prefix
`0/8`, 구조 `0/8`이었다. 암기 사다리는 1문서를 정확히 통과했지만 4문서에서 top-1
`0.6978`, target `2/4`, 구조 `1/4`로 처음 붕괴했고 100문서에서는 `0.2771`까지 낮아졌다.
100문서 full/additive/turn-only 세 arm도 모두 top-1 `0.29` 미만, target·구조 `0/8`이라 full
CE를 충분한 해결책으로 지지하지 않는다. turn-only는 정상 prompt CE가 빈 prompt와 shuffle을
이긴 항목이 `6/8`이라 부분적인 prompt 인과성은 남았지만, 고정 validation 32문서와 모든
100-step 체크포인트에서 자유 복구에 실패했다. 따라서 decoder 불일치나 늦은 반복 붕괴가
아니라 rollout 전에 발생한 underlearning이다. 다음은 별도 사전등록한 4문서
optimization/capacity 단일축 시험이며, 303M·IIT 결합·participant·프로덕션은 계속 차단한다.
모델/증거 42개(`146,667,478` bytes)는 HF `dancinlab` 비공개 revision
`anima-303m-r4-mouth-diagnostics-2026-08-13@8d67bb6e5eeea9a917892fba39310b7306c84718`에서
다시 내려받아 크기·SHA-256 전부 일치함을 검증했다. 전체 Python/CHAT QA는
`160 tests + 3 subtests`를 통과했고 CUDA/CuPy 부재 1건만 정상 skip됐다.

### 사전등록한 R4 4문서 optimization/capacity 시험

`state/anima_303m_r4_four_doc_2026_08_13/`에 D2의 첫 붕괴점에서 수행할 로컬 Python 전용
시험을 동결했다. 같은 4개 문서, assistant-turn 목적함수, 완전 문서 sampler, seed, optimizer,
peak LR, decoder와 관문을 유지한다. `B0`는 `d=128/L=4/600 step`을 재현하고, `O1`은 학습
horizon만 2,400 step으로 바꾸며, `C1`은 canonical width/head 용량만 `d=256/L=4`로,
`C2`는 depth만 `d=128/L=8`로 바꾼다. treatment는 teacher top-1 `>=0.95`,
exact/target/structural `4/4`, prompt 인과 통제 `4/4`를 모두 통과해야 한다. baseline 불일치는
모든 treatment 해석을 무효화한다. 4-arm 제한과 결과 독립 decision table은 `protocol.json`에
고정했으며 어떤 결과도 303M·IIT 결합·프로덕션을 바로 허용하지 않는다.

실행은 `INVALID-BASELINE-MISMATCH`로 fail-closed 중단됐다. 현재 scorer는 보존 checkpoint의
top-1 `0.697796`을 정확히 재현했지만 같은 seed·recipe의 MPS 재실행은 `0.728227`이었고,
trajectory는 step 200부터 갈라져 최종 tensor 53개가 모두 달랐다. 따라서 treatment 출력은
해석하지 않는다. 공용 trainer에 native `--deterministic` 모드를 추가해 checkpoint provenance에
기록하고 지원되지 않는 비결정 연산은 오류로 중단하도록 수정했다. 중복 deterministic baseline이
정확히 일치하기 전에는 4문서 treatment를 다시 해석할 수 없으며 303M·IIT 결합·프로덕션은 계속
차단한다.

`state/anima_303m_r4_deterministic_baseline_2026_08_13/`에 이 중복 관문을 사전등록했다. 같은
4문서 recipe를 새 MPS 프로세스 두 개에서 실행해 engine SHA-256, checkpoint state digest,
모든 model tensor, teacher trace와 canonical 행동이 정확히 일치해야 한다. 근사 허용 오차는
없고 지원되지 않는 deterministic 연산은 fail-closed 중단한다. 이 관문 자체는 treatment·303M·
IIT 결합·프로덕션을 허용하지 않는다.

MPS 중복 관문은 `index_put_with_accumulate_mps`에 deterministic backward 구현이 없어 step 1
전에 fail-closed 중단됐다. warn-only 우회는 사용하지 않았다.
`state/anima_303m_r4_deterministic_cpu_2026_08_13/`에 같은 정확 일치 2회 관문을 native
2-thread CPU backend로 별도 사전등록했으며 통과 전까지 treatment는 해석하지 않는다.

CPU 중복 관문은 engine SHA, state digest, tensor 53개, teacher trace와 canonical 행동이 모두
정확히 일치했고 최대 tensor 오차는 `0.0`이었다. 고정 실패 baseline은 top-1 `0.724029`,
target `2/4`, 구조 `1/4`다. 이 실행 계약에서 O1/C1/C2를 비교하는 새 시험을
`state/anima_303m_r4_deterministic_treatments_2026_08_13/`에 별도 사전등록했다.

deterministic treatment는 모두 고정 관문에 실패했다. O1과 C1은 1~3번 문서를 teacher top-1
`1.0`으로 학습했지만 EOF의 4번 문서는 첫 byte부터 실패했다. 공용 원인은 position mapping
불일치다. legacy stream framing에서 이 문서는 약 byte 222에만 놓이지만 runtime/evaluator의
고립 user role은 position 0에서 시작한다. 기존 sampler만 확장한 alignment 단일 arm을
`state/anima_303m_r4_document_alignment_2026_08_13/`에 사전등록했고 legacy stream은 동결
control로 유지하며 모든 상위 관문은 계속 차단한다.

alignment arm은 teacher top-1 `1.0`, target-prefix `4/4`, prompt 통제 `4/4`였지만 발생한
exact/structural 판정은 무효다. 정답 3개가 canonical 생성 예산 192 bytes를 넘어 exact 완료가
구조적으로 불가능했다. raw 실패는 `original_verdict`로 보존하고 통과로 승격하지 않았다. 같은
불변 원천에서 runtime byte 예산에 맞는 문서를 결정론적으로 파생한 다음 view를 별도
사전등록하며, harness는 도달 불가능한 exact gate를 fail-closed 거부한다.

`state/anima_303m_r4_runtime_compatible_2026_08_13/`에 수정된 단일 arm을 사전등록했다. 불변
source 순서에서 canonical 192-byte 예산에 맞는 완전한 단일 turn 문서 첫 4개를 결정론적으로
파생하고 view SHA를 고정했으며 aligned deterministic recipe와 모든 행동 관문을 유지한다. 이
결과도 아직 memorization/conditioning 관문일 뿐이다.

runtime-compatible aligned arm은 teacher top-1 `1.0`, teacher CE `1.32e-6`, exact/target/구조
`4/4`, prompt CE/output 통제 `4/4`, canonical stop `4/4`로 모두 통과했다. 따라서 4문서 실패의
근본 원인은 공용 train→runtime position mapping으로 지지되며 균일한 tiny capacity 부족
가설은 반증됐다. 아직 in-view 암기 결과이므로 다음 관문은 별도 사전등록한 100문서와 독립
panel 시험이다.

`state/anima_303m_r4_aligned_100_2026_08_13/`에 이 단일 arm을 고정했다. source 순서에서
canonical byte 예산에 맞는 완전 exchange 첫 100개를 결정론적으로 선택하고 aligned
deterministic recipe를 유지하며 heldout 32개 전체와 기존 의미 대화 panel을 실행한다. 자동
통과해도 수동 검토가 필요하며 303M·IIT 결합·프로덕션을 바로 허용하지 않는다.

## 미해결 gap 감사 — 303M 의미 대화

아래는 2026-08-12 읽기 전용 `/gap` 감사에서 확인한 8개 렌즈군 31개 항목의 전체 후속
등록부다. 동결된 panel·데이터 revision·문턱값·실패 체크포인트와
`FAIL-MEANINGLESS-REPETITION` 판정을 소급 변경하지 않는다. 보존 체크포인트 진단 결과를
사후 최적 체크포인트 선택에 사용하지 않는다. 단일 변수 시험으로 확정하지 않은 원인은
관찰 또는 가설로만 취급한다.

우선순위는 **P0**가 유효한 다음 R0 또는 프로덕션 폐루프를 차단하고, **P1**이 강한
증거·재현성을 차단하며, **P2**가 현재 의미 실패를 설명하지는 않지만 필요한 운영 증거라는
뜻이다.

2026-08-12 복구 상태: M1, A1, A2, A3, A6, R3, 폐루프 `.bin` 수용, canonical SSOT,
평가기 중복 decode, 실행 가능한 도구 간 계약은 공용 Python 엔진에서 수정했고 실제 tiny
체크포인트 회귀로 덮었다. M4는 배포 전 보존된 전체 303M 체크포인트 비교가 아직 필요하다.
M2/R2는 허용 가능한 한국어 멀티턴 원천과 새 HF 불변 revision이 없어 계속 차단 상태다.
아래 번호 목록은 최초 감사 증거로 보존하며 이 문단이 현재 처리 상태다.

### 수학·구조 gap

1. **M1 · functor · P0 — 파이프라인 전체에서 채팅 framing 사상이 보존되지 않는다.**
   학습·대화 panel은 `user: ...\nassistant:`를 쓰지만 `anima-py chat`은 별도 한국어
   `사용자: ... | 도우미:` framing과 다른 생성 byte 예산을 사용한다. 다음 프로토콜은
   template·separator·stop 규칙·byte 예산을 하나의 chat-format SSOT에 두고
   builder → trainer → evaluator → runtime 정확 동일성 시험을 추가해야 한다. 근거:
   [`conversation_panel.json`](state/anima_303m_r0_conversation_2026_08_12/conversation_panel.json),
   [`cli/chat.py`](cli/chat.py), [`core/generator.py`](core/generator.py).
2. **M2 · operadic · P0 — 학습 지지집합이 평가하는 turn 합성에 닫혀 있지 않다.** 관문은
   turn 간 기억·정정을 요구하지만 현재 한국어 builder는 문서마다 단일
   `user → assistant` 쌍만 만든다. 실제 한국어 멀티턴 trajectory와 문서/turn 정렬을
   보존하는 새 HF revision을 별도 사전등록해야 하며, 동결된 실패 revision은 수정하지
   않는다. 근거:
   [`build_dataset.py`](state/anima_303m_r0_conversation_2026_08_12/build_dataset.py),
   [`conversation_panel.json`](state/anima_303m_r0_conversation_2026_08_12/conversation_panel.json).
3. **M3 · persistent-homology / tropical · P1 — 반복 attractor의 발생 시점과 수명이
   불명확하다.** 2,000 step마다 체크포인트는 있지만 의미 대화는 최종 체크포인트에서만
   측정했고 step별 top-1/top-2 margin·entropy를 보존하지 않았다. 판정에 쓰지 않는
   checkpoint × prefix 길이 반복 수명·logit margin 진단을 기록할 수 있으나, 결과를 본 뒤
   과거 최적 체크포인트를 고르는 데 쓰면 안 된다. 근거:
   [`protocol.json`](state/anima_303m_r0_response_ce_2026_08_12/protocol.json),
   [`train.log`](state/anima_303m_r0_response_ce_2026_08_12/train.log).
4. **M4 · bisimulation · P0 — 실제 303M 세 decode 경로의 byte 동일성 증거가 없다.**
   Torch/engine 형식의 직렬화 ByteGPT 체크포인트, evaluator 상주 `_Mouth`, ranged canonical
   generator가 동일 seed bytes에서 같은 step logits·생성 bytes를 내는지 비교하지 않았다.
   동결 panel seed와 실제 체크포인트를 쓰는 bisimulation 계약시험을 추가해야 한다. 근거:
   [`cli/evaluate.py`](cli/evaluate.py), [`core/generator.py`](core/generator.py),
   [`core/decode.py`](core/decode.py).

### 적대·스트레스 gap

1. **A1 · adversarial semantics · P0 — 자동 의미 scorer의 실제 위양성이 확인됐다.** 현재
   코드는 모순문 “Ice does not melt ...”와 `차`가 부분문자열로 든 `자동차입니다`를 모두
   통과시킨다. 부정·모순·키워드 나열·한국어 부분문자열 통제군과 형태소 분석기에 의존하지
   않는 canonical 경계 규칙을 사전등록해야 한다. 근거: [`cli/evaluate.py`](cli/evaluate.py),
   [`conversation_panel.json`](state/anima_303m_r0_conversation_2026_08_12/conversation_panel.json).
2. **A2 · Byzantine input · P1 — panel identity를 기록하지만 강제하지 않는다.** 프로토콜은
   panel SHA-256을 고정하지만 `--conversation-panel`은 schema만 맞으면 교체 파일도 읽고
   그 해시를 결과에 기록할 뿐이다. evaluator가 기대 프로토콜 해시를 받아 파일을 읽기 전
   불일치 시 fail-closed 해야 한다. 근거:
   [`protocol.json`](state/anima_303m_r0_response_ce_2026_08_12/protocol.json),
   [`cli/evaluate.py`](cli/evaluate.py).
3. **A3 · edge-chaos 역할 경계 · P1 — stop parser는 정확한 문자열만 인식한다.**
   `\n user:`, `\nUSER:`, `\n사용자 :` 변형은 조작된 다음 turn을 누출할 수 있고 현재 시험은
   소문자 canonical marker 하나만 덮는다. 줄 시작 역할 parser로 교체하고 공백·대소문자·
   콜론·영어·한국어 변형 행렬을 시험해야 한다. 근거:
   [`core/generator.py`](core/generator.py),
   [`tests/test_conversation_gate.py`](tests/test_conversation_gate.py).
4. **A4 · edge-chaos context rollover · P1 — 긴 멀티턴 seed는 앞 byte를 조용히 잃는다.**
   ByteGPT block은 512 bytes이고 마지막 한국어 정정 seed가 이미 420 bytes라 생성 중 최초
   사실이 밀려날 수 있다. 511/512/513-byte 경계 시험과 매 생성 step의 실제 visible
   context 범위를 기록해야 한다. 근거:
   [`conversation_result.json`](state/anima_303m_r0_response_ce_2026_08_12/conversation_result.json),
   [`core/decode.py`](core/decode.py).
5. **A5 · perturbation / 오염 · P1 — “오염 0”은 정확 포함만 덮고 의미 near-duplicate는
   덮지 않는다.** report-only 감사는 보존 문서 649,354개 중 SHA 사전순 첫 100,000개만
   검사한다. 의역·띄어쓰기·역번역 누출은 미측정이다. 전체 corpus를 panel 중심 근사
   검색하되 별도 민감도 보고서로만 남기고 동결 revision에서 사후 삭제하지 않는다. 근거:
   [`build_dataset.py`](state/anima_303m_r0_conversation_2026_08_12/build_dataset.py),
   [`result.json`](state/anima_303m_r0_proportional_conversation_2026_08_12/result.json).
6. **A6 · 응답 감독 ablation · P0 — “answer CE 활성”은 prompt-conditioned 감독을
   증명하지 않는다.** telemetry는 assistant marker/position을 세지만 대응 user prompt가
   같은 random window 안에 보이는지 요구하지 않는다. 셀별 fully-framed·marker-only·
   payload-only window를 기록하고 완전한 prompt→response span을 보존하는 treatment를
   사전등록해야 한다. 근거: [`cli/train.py`](cli/train.py),
   [`result.json`](state/anima_303m_r0_response_ce_2026_08_12/result.json).

### 경제·자원 gap

1. **R1 · Pareto 귀속 · P1 — 비례 복구는 여러 축을 동시에 바꿨다.** sampler, turn 개행
   보존, 한국어 corpus가 함께 변해 validation 개선을 sampler 하나에 귀속할 수 없다.
   기존 근본 원인 표현을 상관 증거로 낮추고 sampler-only와 data/framing-only matched
   ablation을 사전등록해야 한다. 근거:
   [`README`](state/anima_303m_r0_proportional_conversation_2026_08_12/README.md).
2. **R2 · information budget / optimal transport · P0 — 노출량이 목표 능력이 아니라 파일
   크기를 따른다.** 303,097,856 파라미터 모델에 229,376,000 target bytes와 11,025,460개
   response 감독 위치만 노출됐다. 비례 실행의 영어 dialogue는 약 2.97%, 한국어 dialogue는
   16.97%, 한국어 멀티턴 질량은 0이다. 다음 프로토콜은 언어 × 단일/다중턴 × 기억/정정
   능력 분포를 고정하고 effective framed bytes/parameter와 coverage distance를 기록해야
   한다. 근거: [`result.json`](state/anima_303m_r0_response_ce_2026_08_12/result.json).
3. **R3 · dynamic-programming provenance · P1 — 중간 ByteGPT metadata가 틀린다.**
   `_write_bin`은 모든 중간 `.bin`에 최종 설정 `steps`와 최신 train-batch loss를 써서
   step-2,000 로그도 `step=14000`이라고 기록한다. 실제 completed step과 최근 측정
   validation CE를 writer에 전달하고 provenance 회귀를 추가해야 한다. 최종 R0 실패는
   유효하지만 체크포인트 시간 분석은 아직 신뢰할 수 없다. 근거:
   [`cli/train.py`](cli/train.py),
   [`train.log`](state/anima_303m_r0_response_ce_2026_08_12/train.log).
4. **R4 · Landauer 계측 · P2 — 에너지 비용이 없다.** GPU 시간·VRAM·달러는 기록했지만
   전력·누적 에너지는 없다. 다음 Vast.ai 실행은 비간섭 NVML 전력 telemetry를 수집해
   target byte당 joule과 effective assistant byte당 joule을 보고해야 한다. 근거:
   [`result.json`](state/anima_303m_r0_response_ce_2026_08_12/result.json),
   [`vram.csv`](state/anima_303m_r0_response_ce_2026_08_12/vram.csv).

### 인식론·증거 gap

1. **E1 · assumption surfacing · P1 — 관찰·가설·확정 원인이 섞였다.** undertraining,
   random-window framing 손실, 단일턴 한국어 자료가 같은 remaining cause 목록에 있다. 각
   후보에 증거 수준·반증 조건·최소 단일 변수 시험을 붙여야 한다. 근거:
   [`result.json`](state/anima_303m_r0_response_ce_2026_08_12/result.json).
2. **E2 · Bayesian 재현성 · P1 — 최신 treatment는 각각 seed 7 한 번뿐이다.** 고정 recipe를
   반증한 증거일 뿐 R0 통과확률이나 seed 분산은 추정하지 못한다. 단일 seed screen 통과
   후에만 사전등록한 다중 seed posterior와 최소 성공 streak를 요구해야 한다. 근거:
   [`protocol.json`](state/anima_303m_r0_response_ce_2026_08_12/protocol.json).
3. **E3 · counterfactual falsifier · P1 — panel/decoder 전체 instrument에 모델 통제군이
   없다.** canned scorer 문자열은 end-to-end positive/negative calibration이 아니다.
   known-good 대화 체크포인트 하나와 known-bad 체크포인트 하나를 같은 동결 decode 경로로
   실행하고 instrument 식별력과 현재 모델 판정을 분리해야 한다.
4. **E4 · honesty triad · P1 — 수동 검토 산출물이 서로 모순된다.** 원시
   `conversation_result.json`은 `REQUIRED`인데 요약은 항목별 판정·reviewer·blind 여부·기준
   없이 완료 `0/14`를 주장한다. 수동 검토를 주장하기 전에 응답별 판정과 reviewer·기준·
   독립성을 별도 서명/해시 산출물로 보존해야 한다. 근거:
   [`conversation_result.json`](state/anima_303m_r0_response_ce_2026_08_12/conversation_result.json),
   [`result.json`](state/anima_303m_r0_response_ce_2026_08_12/result.json).

### 수렴·폐루프 gap

1. **C1 · fixpoint / 성공 기준 · P1 — 실패 후 활성 진단 프로토콜이 없다.** response-CE
   프로토콜은 완료됐지만 다음 micro 실험에는 동결 가설·성공/중단 규칙·최대 실험 수·후보
   폐기 결정표가 없다. 결과를 만드는 실험 전에 이를 먼저 등록해야 한다. 근거:
   [`README.md`](README.md),
   [`protocol.json`](state/anima_303m_r0_response_ce_2026_08_12/protocol.json).
2. **C2 · regression streak · P1 — 코드 QA는 모델 행동 증거가 아니다.** `77 passed`는
   소프트웨어 시험이고 최신 실제 체크포인트 streak는 `0/1`이며 seed·하드웨어 반복도 없다.
   코드 QA와 의미 모델 성공 streak를 별도 승격 필드로 관리해야 한다. 근거:
   [`result.json`](state/anima_303m_r0_response_ce_2026_08_12/result.json).
3. **C3 · closed loop · P0 — 통과한 303M `.bin`도 participant에 탑재할 수 없다.**
   participant는 `lora|v3|akida|clm`만 제공하고 `CLMSubstrate`는 `.clm`만 받지만 공용
   generator는 이미 `.bin/.clm`을 판별한다. 새 엔진을 만들지 말고 기존 participant
   substrate 경계가 `core.generator`를 재사용하도록 확장해야 한다. 근거:
   [`anima_participant.py`](agent/domains/CHAT/anima_participant.py),
   [`substrate_clm.py`](agent/domains/CHAT/substrate_clm.py),
   [`core/generator.py`](core/generator.py).

### 단순성·canonical gap

1. **S1 · canonical SSOT · P0 — chat format과 stop marker가 중복됐다.** panel, dataset
   builder, trainer flag, generator, chat CLI가 fail-closed 동일성 검사 없이 각자 문자열을
   가진다. 기존 모든 경로가 소비하는 최소 chat-format manifest 하나로 통합하고 새
   evaluator·런타임은 만들지 않는다. 근거:
   [`conversation_panel.json`](state/anima_303m_r0_conversation_2026_08_12/conversation_panel.json),
   [`build_dataset.py`](state/anima_303m_r0_conversation_2026_08_12/build_dataset.py),
   [`cli/train.py`](cli/train.py), [`core/generator.py`](core/generator.py).
2. **S2 · duplicated helper · P0 — evaluator `_Mouth.chat`이 low-level dispatch를 다시
   구현한다.** 실제 체크포인트 패리티를 먼저 요구한 뒤 `core.generator`의 preloaded
   canonical backend interface를 직접 호출하도록 바꿔야 한다. 근거:
   [`cli/evaluate.py`](cli/evaluate.py), [`core/generator.py`](core/generator.py).
3. **S3 · architectural legibility · P2 — README가 활성·폐기 R0 recipe를 섞어 보여준다.**
   KLUE·비례·response-CE가 모두 “현재 실험” 아래 있고 “303M R0 evaluator invalid”가 어느
   과거 평가기인지 명확하지 않다. 이 등록부 다음에는 활성 protocol pointer 하나만 두고
   완료 프로토콜을 historical evidence로 구분해야 한다.

### 시간·동역학 gap

1. **T1 · temporal hierarchy · P1 — validation CE와 의미 행동의 측정 시간축이 다르다.**
   CE는 200 step마다 재지만 대화·반복은 최종 step에서만 측정한다. 보존 체크포인트를
   시간순 진단하되 사후 best-checkpoint 승격에는 사용하지 않는다.
2. **T2 · temporal decay · P1 — 기억을 바로 다음 turn에서만 시험한다.** R0가 먼저 통과한
   뒤 무관 turn을 삽입한 1/2/4-turn 지연과 context rollover 기억 panel을 별도로 동결해야
   한다. 근거:
   [`conversation_panel.json`](state/anima_303m_r0_conversation_2026_08_12/conversation_panel.json).
3. **T3 · heuristic promotion / 추가 축 · P1 — 다중 축 treatment 뒤 가설이 원인으로
   승격됐다.** 매 treatment가 공용 흐름 변수 하나만 바꾸고 어떤 후보를 반증하는지 미리
   선언하는 micro → single-seed → multi-seed 계층을 강제해야 한다.
4. **T4 · active acquisition · P0 — 한국어 기억·정정 지지집합 부재는 이미 확인됐다.**
   panel 문구와 격리되고 provenance가 있는 실제 한국어 멀티턴·정정 trajectory를 새
   immutable HF `dancinlab` revision으로 만들어야 한다. 현재 데이터 동결 결정 때문에
   in-place 수정이 아니라 새 프로토콜이 필요하다. 근거:
   [`build_dataset.py`](state/anima_303m_r0_conversation_2026_08_12/build_dataset.py).

### 범위·일관성 gap

1. **V1 · axis coverage · P0 — scorer control이 모든 blocking bar와 언어를 덮지 않는다.**
   통제군 4개 중 positive는 영어 하나뿐이다. 기억 최종·정정 최종·모순·키워드 나열·UTF-8
   경계·완결성·역할 누출·부분문자열 충돌에 대해 영어·한국어 positive/negative 행렬을
   추가해야 한다. 근거:
   [`conversation_panel.json`](state/anima_303m_r0_conversation_2026_08_12/conversation_panel.json),
   [`tests/test_conversation_gate.py`](tests/test_conversation_gate.py).
2. **V2 · cross-tool consistency · P0 — builder, trainer, evaluator, `anima-py chat`, participant가
   강제된 출고 계약을 공유하지 않는다.** 실제 체크포인트 하나로 동일 template·max bytes·
   load 전략·parser 아래 seed bytes, 매 step logits, stop 판단, 최종 raw bytes를 모든 도구
   사이에서 비교해야 한다.
3. **V3 · unowned load-bearing gate / landscape · P1 — 수동 검토와 production wiring의
   명시적 산출물 소유자가 없다.** R0 실패 중에는 FIFO·reply ownership·동시 사용자·
   HTTP/WebSocket·soak·rollback·participant state를 실행하지 않은 것이 의도된 차단이다.
   다음 프로토콜은 review artifact/schema의 소유권을 정하고 통과한 conversation R0를 이
   staging 관문들에 빠짐없이 연결해야 한다.

### 차단 순서와 즉시 결정

감사에서 영향도가 가장 큰 차단 원인 세 가지는 다음과 같다.

1. **의미 식별력 무효:** 모순문과 한국어 부분문자열 충돌이 통과할 수 있다.
2. **능력 지지집합 불일치:** random byte window가 prompt를 잃을 수 있고 한국어 멀티턴·
   기억·정정 학습 질량이 없다.
3. **canonical 폐루프 부재:** 평가기가 공용 generator interface를 우회하고 ByteGPT
   `.bin`을 프로덕션 participant가 선택할 수 없다.

따라서 다음 결과성 작업 전에 새 Python 전용 진단/R0 프로토콜에서 다음을 동결해야 한다:
(1) canonical chat-format SSOT와 도구 간 계약, (2) 적대 scorer 통제군과 fail-closed panel
identity, (3) provenance가 있는 영·한 멀티턴 능력 coverage, (4) 단일 변수 중단·반증 규칙.
R1 recurrent workspace와 프로덕션 배포는 계속 잠근다. 모델·학습 데이터는 HF
`dancinlab` 비공개 저장소, GPU 작업은 Vast.ai만 사용하며 사용자 소유 `ING.jsonl`,
`stream_mi.json`은 변경하지 않는다.

## Canonical 진입점

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e ".[train,runtime]"

.venv/bin/anima-py --help
.venv/bin/anima-py train --help
.venv/bin/anima-py evaluate --help
.venv/bin/anima-py chat MODEL.clm
```

| 명령 | 책임 |
| --- | --- |
| `anima-py corpus` | 등록된 학습 코퍼스 생성 |
| `anima-py train` | 공용 PyTorch 엔진 학습과 체크포인트 직렬화 |
| `anima-py evaluate` | 등록된 NumPy/런타임 평가와 인과 통제군 실행 |
| `anima-py serialize` | 기존 학습 체크포인트를 런타임 형식으로 변환 |
| `anima-py sweep` | 제한된 다중 장치 실험 행렬 실행 |
| `anima-py chat` | A⇄G 의식 데몬과 바이트 입 실행 |
| `anima-py study` | 등록된 상호작용 연구 실행 |

Python 경로에 없던 연구 계측도 같은 채팅 엔진에 포함한다.

```bash
anima-py chat MODEL.clm --opgrip
anima-py chat MODEL.clm --opgrip-live
anima-py chat MODEL.clm --opgrip-r3
anima-py chat MODEL.clm --refractory
```

decode가 없는 `--opgrip`은 체크포인트 없이 실행할 수 있다. live/R3는 모델을 읽지
못하면 fail-closed 한다.

## 런타임 구조

```text
anima-py
└── cli/anima.py
    ├── cli/train.py ───────► core/model.py ─────► core/serialize.py
    ├── cli/evaluate.py ────► core/decode.py
    └── cli/chat.py
        ├── core/brain.py
        ├── core/pure_field.py       Engine A
        ├── core/engine_g.py         Engine G·동기·발화·불응기
        ├── core/generator.py ──────► core/decode.py
        ├── core/kosmos_io.py
        └── core/dream_*.py
```

원칙:

- 엔진 계산을 옆에서 재구현하지 않고 공용 엔진을 확장한다.
- 측정 중 등록 데이터·난수·기준·통제군은 바꾸지 않는다.
- 체크포인트 누락·입력 손상·구조 불일치·고정 평가 자산 누락은 fail-closed 한다.
- 모델 원시 바이트는 UTF-8/surrogateescape와 구조화 JSON으로 손실 없이 보존한다.

## 검증

```bash
.venv/bin/python -m compileall -q cli core anima_py
.venv/bin/python -m pytest -q tests cli/test_train_import_resolution.py agent/domains/CHAT/test_*.py
.venv/bin/anima-py --help
.venv/bin/anima-py evaluate --help
actionlint .github/workflows/*.yml
```

무거운 모델·서빙 QA는 Vast.ai에서 실행한다. 모델과 학습 데이터는 Hugging Face
`dancinlab` 조직의 비공개 저장소에서만 관리한다. 비밀값은 배포 환경 또는 secret CLI로
주입하며 커밋하지 않는다.

## 최신 운영 증거

- 7B store-causality 실행은 공용 디코더 처리량 수정 후 인과·HTTP/WebSocket·soak·복구·
  rollback 관문을 통과했다:
  `state/store_causality_7b_throughput_recovery_2026_08_11/result.json`.
- 실사용자 QA는 해당 체크포인트를 의미론적 채팅 배포로는 무효화했다. broker/participant의
  응답 소유권·과거 발화 비교·언어 소유권·cooldown 흐름을 수정했다:
  `state/chat_7b_conversation_recovery_2026_08_11/result.json`.
- 303M R0 평가기는 이후 invalid measurement로 판정되었고 R1은 잠겨 있다:
  `state/anima_303m_r0_local_micro_2026_08_12/result.json`.

전송 상태만으로 모델을 승격하지 않는다. 의미론적 채팅, 인과 통제군, 처리량, soak, 복구,
rollback은 서로 독립된 blocking gate다.

## 저장소 경계

- `dancinlab/anima`가 유일한 활성 소스 저장소다.
- `cli/`, `core/`, `anima_py/`가 활성 런타임 코드를 소유한다.
- `state/`는 등록 프로토콜과 결과 증거를 소유한다.
- `archive/`는 비런타임 이력이다.
- pod 실행은 Vast.ai, 모델·데이터 관리는 Hugging Face `dancinlab`이 담당한다.

## 라이선스

MIT. `LICENSE` 참고.
