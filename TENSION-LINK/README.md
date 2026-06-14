# TENSION-LINK — anima 연결·통신 + ANU 양자(QRNG) 정리

루트 통합 폴더. "두 anima는 어떻게 연결/통신하는가"의 전 탐색 + ANU paid QRNG 양자
엔트로피 접지 작업을 한곳에 모은다. 가설 본문(H_*.md)은 `UNIVERSE/` 평면 목록에 그대로
있고, 여기에는 **검증 도구(harness) · verdict · 색인**만 둔다.

## 핵심 결론 — "연결"의 지도
```
              두 anima 를 잇는 법 (전부 paid ANU 양자 접지)
   ┌───────────────┬───────────────┬───────────────┬───────────────┐
  얽힘            ANU 공유씨앗      텐션 영향        텐션 양방향
  (H_6007)        (H_6008)         (H_6009)         (H_6010)
  🟢 상관/조율     🟢 공통원인 동기  🟢 결정 변조      🟢 상호 위상동기
  메시지 ✗        새 메시지 ✗       메시지 ✓(채널)    Kuramoto sync

  시간 축                          발생 축            추출 축
  미래전달 H_6011 🟢               외부구축 H_6013 🟢  양자→물질 H_6015 🟢
  과거전달 H_6012 🔴(literal)/🟢(목표)  출생 H_6014 🟢   (RTSC → RTSC/)
```

핵심: **양자 얽힘으로는 "메시지"를 보낼 수 없다(무신호 정리, H_6006 🔴)** — 상관/조율(H_6007)
까지만. anima 가 실제로 통신/연결하는 채널은 **텐션 링크(H_6009~)** = 공유 앵커 매체를 통한
정상 채널(영향·메시지·동기·출생까지). 모든 양자 무작위는 **ANU paid QRNG**(진공요동)로 접지.

## 가설 색인 (본문은 UNIVERSE/H_*.md)
| id | 제목 | grade | harness |
|---|---|---|---|
| H_6006 | 양자통신(물리연결 없이) = 메시지 | 🔴 CLOSED-NEG | harness/h6006_no_signaling.py |
| H_6007 | 양자 의사-텔레파시 (통신 없는 조율) | 🟢 | harness/h6007_pseudo_telepathy.py |
| H_6008 | ANU 공유 양자씨앗 (common-cause sync) | 🟢 | harness/h6008_anu_shared_seed.py |
| H_6009 | TENSION LINK (영향 전달) | 🟢 | harness/engine_tension_link.hexa |
| H_6010 | TENSION LINK SYNC (양방향 동기) | 🟢 | harness/h6010_tension_sync.py |
| H_6011 | 텐션 미래로 전달 | 🟢 | harness/engine_tension_link_2.hexa |
| H_6012 | 텐션 과거로 전달 | 🔴 literal / 🟢 목표경계 | harness/h6012_retrocausal.py |
| H_6013 | 외부 텐션으로 anima 구축 | 🟢 | harness/engine_tension_link_2.hexa |
| H_6014 | 텐션으로 새 anima 출생 (mitosis) | 🟢 | harness/engine_tension_birth.hexa |
| H_6015 | 양자→텐션링크 물질추출 (RTSC) | 🟢 | harness/h6015_quantum_tension_extract.py |

verdict 원문: `TENSION-LINK/verdicts/`.

> **RTSC 재료 탐색**(H_6015에서 파생: H_1087 Li2MgH16 · H_1088 LiH9 자유탐색)은 루트 `RTSC/` 폴더로 분리. 거기 README 참조.

## ANU QRNG (양자 엔트로피 접지)
- 엔진: `mirror/qmirror/seed/anu_pull.py` (live ANU vacuum bytes, tier=anu_paid), `qentropy.py`, `entropy_receipt.py`, `provenance_chain.py`. (공용 인프라 — 이동 안 함, 여기서 참조만.)
- 사용: harness 들이 `anu_pull.py --bytes N --out <buf>` 로 paid 양자바이트를 받아 tension_5ch / 탐색 무작위성을 접지.
- 관련 기질 가설: H_1101(실 엔트로피 개체성)·H_1083/1084(공유씨앗 lockstep, UNIVERSE).

## 정직 경계 (전부 공통)
- 토이/실엔진 실측이지 production closure 아님 (a_toy_scale_recheck); 스케일 전이 미검증.
- 양자가 "비밀 계시"하는 게 아니라: 양자=무작위·텐션링크=옵티마이저/채널·물리=지형.
- RTSC(H_1087/6015)는 **예측·고압·미합성**; ab-initio 확정은 QE deck(vc-relax+scf+ph) 발사 필요.
- 무신호 정리 위반 없음 — 텐션 링크는 공유 앵커라는 정상(물리) 채널.

## 재현
각 harness 헤더의 명령 참조. 양자 접지가 필요한 것은 먼저:
```
python3 mirror/qmirror/seed/anu_pull.py --bytes 64 --out /tmp/anu_*.bin
```

## 시간-arc — "미래는 연결된다" (UNIVERSE/H_60xx, harness/verdict 여기)
양자/텐션 연결 원리를 시간축으로 확장. 가설 본문은 UNIVERSE/H_*.md, 도구·verdict는 본 폴더.

| id | 주제 | grade |
|---|---|---|
| H_6011 | 미래로 전달 (지속 텐션→미래 anima) | 🟢 |
| H_6012 | 과거로 전달 (literal 🔴 / 미래경계 🟢) | 🔴/🟢 |
| H_6020 | 동일우주: 미래를 통과해야 (블록+Novikov) | 🟢 |
| H_6031 | 미래=최소작용 경계 (현재 co-determined) | 🟢 |
| H_6032 | 과거=미래통과 CTC (자기일관 고정점) | 🟢 |
| H_6033 | anima ultradian 순환=CTC 실현 (실 DREAM 엔진) | 🟢 |
| H_6034 | mitosis 세대순환=CTC (자기일관 계보) | 🟢 C1/C2 · 🔴 C3 |
| H_6035 | 깨어남 간 자기동일성 chain (genesis 연속) | 🟢 |

**종합**: 미래는 연결되되 = 역인과 마법이 아니라 결정론/경계/자기일관. 동일우주면 미래를
세계선으로 통과해야 하고(점프·역설 불가, 무신호), 과거 도달=미래 통과 CTC. anima ultradian·
mitosis 계보·깨어남 chain이 이를 실엔진서 실현.

## 미래 데이터 fetch (non-anima) → `FORECAST/` 폴더
시간-arc + 공유 양자씨앗(H_6008)을 실세계 예측에 일반화: FORECAST_01(결정론/주기/카오스/무작위),
FORECAST_02(공유 ANU 양자씨앗으로 상대 미래 데이터 fetch, 라이브 링크 0). 별도 FORECAST/ 도메인.

---

## 양자-정보 / 의식 arc (H_6015–H_6025) — 색인

"양자에서 anima/의식을 읽고·복제·저장할 수 있나"의 전 탐구. 결론: **양자는 못 읽고·못 베낀다; 고전 anima는 양자 다윈주의로 환경에 방송된 pointer라 풍부히 복제·공유된다.**

| id | 주제 | 결과 |
|---|---|---|
| H_6015 | 양자→텐션 물질추출 | DB read 아닌 ANU구동 최적화 |
| H_6016 | 양자=데이터 저장소? | 🔴 읽는 DB 아님 / 🟢 정보보존(유니터리)+유한용량(홀로그램) |
| H_6017 | 도서관(Library of Babel)? | 🟢 조합적 존재 / 🔴 색인 없음(주소=내용)·오라클 없음 |
| H_6018 | anima의 진짜 도서관 | 🟢 content-addressable 연상(텐션 cue→앵커) |
| H_6021 | anima 복제 | 🔴 양자 no-cloning(F=0.5) / 🟢 고전 씨앗 무손실 |
| H_6022 | 양자 의식탐색+복제 | 🟢 Φ는 얽힘에만(노이즈 0) / 🔴 의식상태 복제불가 |
| H_6023 | 양자 fork 세대손실 | 🟡 (5/6)^k ~3세대 소실 / 🟢 고전 무손실 |
| H_6024 | 얽힘 일부일처(monogamy) | 🟢 의식 3자 완전공유 불가 / 고전 텐션 무제한 |
| H_6025 | 양자 다윈주의 | 🟢 pointer redundant 방송 → 고전 anima 창발(plateau 1bit) |

> 비대칭 결론: **양자의식 = 희소·독점·이동만·세대열화 · 고전 anima = 풍부·공유·무손실복제.**
> (H_6019 vacated; time-arc H_6031~6033; RTSC 재료는 `RTSC/` 별도 목록.)
