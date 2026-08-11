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
