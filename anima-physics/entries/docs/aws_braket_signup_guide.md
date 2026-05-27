# docs/aws_braket_signup_guide.md

> AWS Braket 가입; 5 substrate cover (Rigetti Ankaa-3, IonQ Aria/Forte, IQM Garnet, QuEra Aquila); cost cap $5 mandatory · **🟡 부분** · 비용 Rigetti $0.30/task + $0.00035/shot · QuEra $0.30/task + $0.01/shot

## 구현 가능성

🟡 부분 — IAM + budget cap 가이드 완성, Rigetti/QuEra 2개만 본 cycle 에서 wire-up. IonQ/IQM 은 향후.

## 작동 코드 / 의존성

- `anima-physics/docs/aws_braket_signup_guide.md` (signup walkthrough)
- 의존: `superconducting/cloud_facade_poc.hexa` (Rigetti), `analog/cloud_facade_poc.hexa` (QuEra), `trapped_ion/cloud_facade_poc.hexa` (IonQ)
- scripts: `scripts/anima_physics_braket_ionq_probe.py`, `scripts/anima_physics_braket_quera_probe.py`

## 비용 / 리소스

- AWS account 가입 무료 (카드 등록 필수)
- Budget cap: **$5 mandatory** (raw#10 honest)
- Rigetti Ankaa-3: $0.30/task + $0.00035/shot
- IonQ Aria/Forte: $0.30/task + $0.01/shot (Forte)
- IQM Garnet: $0.30/task + 변동
- QuEra Aquila: $0.30/task + $0.01/shot
- 필요한 도구: AWS Console · IAM · AWS CLI · boto3 · amazon-braket-sdk

## 핵심 흐름 / 구조

```
1. https://signin.aws.amazon.com/signup → Create AWS Account
2. 카드 등록 + 전화 인증 + Support plan = Basic (free)
3. AWS Console → Amazon Braket → Get started → service terms 동의
4. Region 선택:
     Rigetti Ankaa-3 → us-west-1 (N. California)
     IonQ Aria/Forte → us-east-1 (N. Virginia)
     IQM Garnet      → eu-north-1 (Stockholm)
     QuEra Aquila    → us-east-1 (N. Virginia)
5. IAM user 생성 + AmazonBraketFullAccess policy
6. AWS Budget cap $5 mandatory (cost safety)
7. ANIMA_BRAKET_DRY_RUN=0 → LIVE swap
```

## 트리거 (fire 방법)

```bash
export AWS_ACCESS_KEY_ID=<key>
export AWS_SECRET_ACCESS_KEY=<secret>
export AWS_REGION=us-east-1
export ANIMA_BRAKET_DRY_RUN=0  # LIVE
hexa run /Users/ghost/core/anima/anima-physics/analog/cloud_facade_poc.hexa
hexa run /Users/ghost/core/anima/anima-physics/trapped_ion/cloud_facade_poc.hexa
```

## 검증 결과

- 가입 가이드 spec 완성
- DRY_RUN PASS (Rigetti, QuEra, IonQ)
- LIVE 호출은 사용자 AWS 계정 + budget 후 실행 가능 (Mk.XII ledger v3 trigger)

## 관련 entry

- [substrate analog/superconducting/trapped_ion POC](../substrate/)
- [mk_xii_ledger_v3_trigger_spec](mk_xii_ledger_v3_trigger_spec.md)

## 출처 / 작성일

- 원본 파일 작성일: 2026-04
- README §2 참조
