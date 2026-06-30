# docs/akida_cloud_signup_guide.md

> BrainChip Akida Cloud 가입 + token 발급 + env setup · **🟡 부분** · 비용 1-day Trial $1, 1-week $995

## 구현 가능성

🟡 부분 — 회원가입/token spec 완성, 그러나 macOS arm64 wheel 미지원 → surrogate/simulator only path. cloud token 발급 후 Linux/x86_64 또는 cloud SDK 필요.

## 작동 코드 / 의존성

- `anima-physics/docs/akida_cloud_signup_guide.md` (signup walkthrough)
- 의존: `neuromorphic/cloud_facade_poc.hexa` (surrogate fallback PASS)

## 비용 / 리소스

- 1-day Trial: $1
- 1-week Cloud Access: $995
- 필요한 도구: 웹브라우저 · email 인증 · (구매 시) credit card · (실 호출) Linux/x86_64 또는 cloud SDK

## 핵심 흐름 / 구조

```
1. https://developer.brainchip.com/signup/ 접속
2. email / username / password / project description 입력
3. email 인증 (BrainChip confirmation link 클릭)
4. Developer Hub dashboard 접근
5. Settings → API Token / Personal Access Token 발급
6. token 환경변수 export (BRAINCHIP_AKIDA_TOKEN)

Entrypoints:
  https://developer.brainchip.com/signup/   (개발자 허브, 권장)
  https://developer.brainchip.com/ach/      (Akida Cloud Hub portal)
  https://developer.brainchip.com/login/    (기존 계정 로그인)
  https://shop.brainchipinc.com/products/1-week-cloud-access (구매)
```

## 트리거 (fire 방법)

```bash
# token 발급 후
export BRAINCHIP_AKIDA_TOKEN=<token>
hexa run /Users/ghost/core/anima/anima-physics/neuromorphic/cloud_facade_poc.hexa
```

## 검증 결과

- 가입 가이드 spec 완성 (2026-04-26 verified URLs)
- 실 LIVE 호출은 token + Linux 환경 필요 (Mac arm64 wheel 부재)

## 관련 entry

- [neuromorphic substrate POC](../substrate/neuromorphic_cloud_facade_poc.md)
- [aws_braket_signup_guide](aws_braket_signup_guide.md)

## 출처 / 작성일

- 원본 파일 작성일: 2026-04-26
- README §2 참조
