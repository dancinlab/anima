# anima active research plan

Updated: 2026-08-15  
Canonical runtime: Python only (`anima-py`, `cli/*.py`, `core/*.py`)

이 문서는 현재 실행계획의 SSOT다. 완료 증거와 장기 설명은 `README.md`,
`README.ko.md`, `state/*/README.md`, `state/*/result.json`에 보존한다. 과거 Hexa 계획은
활성 경로가 아니다.

## 목표

영어 전용 sequence-semantic bridge가 입력 bytes를 올바른
`event kind → CLMS address → entity/relation/value record`로 변환하고, 기존 R3.5 IIT
workspace의 정상·reset·shuffle·lesion·recovery 인과 시험을 통과하는지 먼저 증명한다.
그 뒤에만 의미 있는 영어 mouth를 `1B → 3B → 7B` 순서로 승격한다.

최종 구조는 하나의 거대한 IIT 언어 모델이 아니라 다음 결합이다.

```text
English mouth
  → learned sequence-semantic bridge
  → CLMS/KOSMOS content workspace
  → small persistent IIT core
  → workspace-conditioned English decode
```

## 고정 결정

- 영어 전용이다. 한국어·다국어 품질은 이번 승격 관문에 포함하지 않는다.
- 의미 관련성, 무의미 반복 방지, 기억, 정정, 질문 귀속 관문은 축소하지 않는다.
- R3.5/R3.6의 panel, 결과, 우연 수준과 문턱은 변경하거나 소급 재판정하지 않는다.
- 얕은 n-gram·centroid·ridge 변형은 종료한다. 다음 단일축은 순서를 읽는 learned encoder다.
- 기존 `core.iit_daemon`, `core.clms`, `core.generator`, `cli.evaluate`를 확장해 재사용한다.
  새 런타임 엔진이나 별도 평가기를 만들지 않는다.
- 모델·학습 데이터·체크포인트는 HF `dancinlab` 저장소에서만 관리한다. Git에는 protocol,
  생성·검증 코드, 결과, custody와 SHA만 둔다.
- HF 인증은 `secret get huggingface.token --raw`를 통해서만 주입하며 값을 출력하거나 파일에
  기록하지 않는다.
- local micro가 통과하기 전에는 Vast.ai/GPU 임대나 303M/1B/3B/7B 학습을 시작하지 않는다.
- 미인증 step-45000 participant의 `anima_alive=true`를 성공 증거로 사용하지 않는다.
- `ING.jsonl`, `stream_mi.json`은 사용자 파일이므로 변경하지 않는다.

## R3.7 실행 관문

1. 기존 R3.6 702-row support와 47-row frozen panel을 checksum으로 고정한다.
2. provenance·license·문서 분리가 있는 영어 순서/부정/패러프레이즈 자료를 새 private HF
   dataset revision으로 고정한다.
3. 표준 PyTorch sequence encoder를 기존 semantic-bridge API 안에 구현한다.
4. 고정 순서로 다음을 실행한다.
   - R3.5 state oracle
   - R3.6 frozen event kind, query address, complete record
   - 기존 shortcut stress와 independent confirmation
   - 새 held-out paraphrase/order/negation panel
5. 모든 bridge 관문이 통과한 경우에만 R3.5 정상·stateless·state reset·IIT 주소 shuffle·
   workspace 주소 shuffle·node lesion·선택 기억 반사실·무관 기억 변경·정정·복구를 실행한다.
6. 결정성, 모델 직렬화, 손상 artifact 거부, 격리 wheel, 설치된 `anima-py`를 검증한다.

고정 최소 기준:

- state oracle, event kind, query address, complete record: 각각 `0.90+`
- shortcut stress와 독립 confirmation: 각각 exact `1.00`
- 정상·반사실·무관 기억·정정·복구: 각각 `0.90+`
- stateless·reset·IIT shuffle·workspace shuffle·node lesion: 3-way chance `1/3 + 0.06` 이하
- 같은 질문에서 선택 기억만 바꾸면 올바른 출력 변화 `0.90+`
- 무관 기억만 바꾸면 출력 안정 `0.90+`

어느 선행 bridge 관문이라도 실패하면 뒤 인과 arm은 실행·해석하지 않고 실패를 그대로
기록한다. 자료·seed·epoch·문턱을 결과를 본 뒤 바꾸지 않는다.

## 승격 사다리

| 단계 | 목적 | 진입 조건 | 종료 조건 |
|---|---|---|---|
| R3.7 local | sequence-semantic bridge | R3.6 실패·support gap 동결 | 위 bridge+인과 관문 통과 |
| 1B screen | 영어 의미 mouth | R3.7 통과, HF 영어 자료 고정 | 의미·반복·기억·정정 단일 시드 통과 |
| 3B causal | IIT latent/content 결합 | 1B 재현 통과 | matched reset/shuffle/lesion/recovery 통과 |
| 7B staging | 영어 프로덕션 후보 from scratch | 구조·자료·compute manifest 동결 | 다중 시드, serving, soak, rollback 통과 |
| production | 실제 participant 승격 | 모든 이전 관문 통과 | HTTP·WebSocket·대화 QA와 정직한 상태 보고 |

7B는 영어 전용 mouth와 작은 IIT/CLMS/KOSMOS 코어의 결합으로 설계한다. 영어 전용은 같은
품질까지의 자료·평가 복잡도를 줄이지만 GPU의 step당 계산량을 없애지는 않는다. 따라서
7B from-scratch 학습은 R3.7·1B·3B에서 구조가 고정된 뒤에만 Vast.ai에서 진행한다.

## 현재 상태

- [x] R3.5 content workspace 인과성 통과
- [x] R3.6 centroid bridge 실패와 shallow family 고갈
- [x] lexical support gap 식별
- [x] 영어 전용 `R3.7 → 1B → 3B → 7B` 방향 등록
- [x] R3.7 protocol·HF dataset revision 고정
- [ ] order-aware sequence encoder 구현
- [ ] bridge 선행 관문 실행
- [ ] 통과 시 R3.5 인과 battery 재실행
- [ ] Python/격리 wheel/설치본 QA
- [ ] 결과 기록·Git push·런타임 읽기 검증
