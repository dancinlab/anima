# H_9911 — H_9802 계기의 바닥은 uniform 이 아니었다: 실측 pedestal 로 판정 3/4 이 뒤집힌다

**tier:** 🟢 **엔진-네이티브 실측**(303M · `anima-py evaluate` · pool/summer GPU) · 계기 결함
**CONFIRMED**(코드-확증 + 실측) · H_9802 라우팅 답 = **RECRUITMENT**
**cost:** pool GPU 5회 디코드(각 <1분) · 전송 282MB · $0 추가지출 없음
**runs:**
```
anima-py evaluate store303_s2000.clm --store <manifest>.json --store-telemetry \
    [--store-telemetry-floor 0.2591]
```

## 물음

H_9802 는 store 레인 지출을 라우팅하려고 붙인 사전점검이다: **자연 텍스트가 store 를
주소지정하는가?** 아니면(RECRUITMENT) 커리큘럼 팔을 태워야 하고, 맞으면(ADDRESSED) 값
정렬만 고치면 되는 **훨씬 싼** 수리다. 판정이 지출 방향을 바꾼다.

## 한 칸에 한 가지만 바꾸는 사다리

자연 팔 하나로는 답이 안 나온다 — floor 를 읽어도 **단어**에서 죽은 건지 **문장**에서
죽은 건지 모르고, 둘은 수리가 다르다. 그래서 각 칸이 딱 하나씩만 다르게 짰다.

| 팔 | 조건 | a_max | a_ent | acc |
|---|---|---|---|---|
| **C** | 템플릿+nonce `"not kunem => "` — **학습된 조건 = 양성통제** | **0.7133** | 0.4282 | 0.9609 |
| **E** | 템플릿+실단어 `"not government => "` — *단어만* 바뀜 | 0.3420 | 0.8520 | 0.6172 |
| **A** | 자연문장+실단어(store 에 존재) — *문맥만* 바뀜 | 0.3017 | 0.8927 | 0.6172 |
| **B** | 자연문장+**그 단어 부재** — **참값 0 PEDESTAL** | **0.2591** | 0.9235 | 0.5469 |
| — | uniform (n_slot=8 서 파생) | 0.1250 | 1.000 | — |

코퍼스는 프로젝트 자신의 자연 EN(`dancinlab/anima-corpus-en-general` · AP 기사 59.7MB),
ckpt 는 store 트레일러를 가진 유일한 303M(`store303_s2000.clm`). 양성통제 먼저 돌려
rows=128·a_max 0.7133 로 **계기가 살아있음**을 확인한 뒤에 음성을 읽었다
(`positive-control-before-reading-a-negative`).

## 🔻 landed 계기의 결함

착륙돼 있던 규칙은 `a_max ≤ uniform × 1.5` (= 0.1875) 였다. 그런데 **주소 대상 단어가
store 에 아예 없는 pedestal 팔(B)이 0.2591 을 읽는다.** 참값이 0인 팔이 문턱의 1.4배다.
따라서 옛 규칙은 **B 를 "ADDRESSED" 로 선언**한다 — 주소지정이 원리적으로 0인 증거를 놓고
"주소는 되고 있으니 싼 정렬 수리로 가라"고 지출을 라우팅한다.

uniform 은 이 판독구의 **이론적 우연**이지 **실현된 바닥**이 아니다
(`chance-level-must-be-derived-per-metric`). 실측 바닥은 2.07배 높다.

## 수리 후 — 판정 3/4 이 뒤집힌다

`--store-telemetry-floor <a_max>` 를 받아 실측 pedestal 대비로 판정하고, 안 주면 숫자만
찍고 **PENDING** 으로 남긴다(틀린 판정보다 무판정이 낫다).

| 팔 | 옛 규칙(uniform) | 수리 후(실측 floor 0.2591) |
|---|---|---|
| C 양성통제 | ADDRESSED | **ADDRESSED** ✅ 유지 |
| E 템플릿+실단어 | ADDRESSED | **RECRUITMENT** 🔄 |
| A 자연문장 | ADDRESSED | **RECRUITMENT** 🔄 |
| B pedestal | ADDRESSED | **RECRUITMENT** 🔄 |

세 갈래 전부 summer 에서 실행해 확인했다(floor 미지정 → PENDING · B+floor → RECRUITMENT ·
C+floor → ADDRESSED).

## H_9802 의 답

**RECRUITMENT.** 자연 텍스트는 store 를 주소지정하지 않는다 ⟹ **커리큘럼 팔을 태워라,
정렬 수리는 낭비다.** 옛 규칙이 냈을 답의 정반대다.

그리고 사다리가 *어디서* 죽는지도 준다: 큰 낙차는 **C→E (0.7133→0.3420)** 이고 E→A 는
0.0403 뿐이다. 주소지정은 **문장이 아니라 단어**에서 죽는다 — nonce 로 학습된 키가 실
어휘를 못 알아본다. A−B = 0.0426 로 자연 팔이 pedestal 위로 거의 못 올라간다.

## 범위 — 정직하게

- ckpt **하나**(store303_s2000) · seed 하나. 계기 결함은 코드 사실이라 CONFIRMED 지만,
  0.2591 이라는 **floor 값 자체는 이 ckpt·이 프롬프트 분포의 값**이다. 다른 ckpt 는
  자기 pedestal 을 다시 재야 한다 — 그게 이 플래그가 하드코딩 아닌 인자인 이유다.
- E/A 의 acc 가 둘 다 79/128 로 같은 건 총합 우연이다(칸별 분할은 다르다).
- 루프로 여러 eval 을 한 pool 세션에 몰면 래퍼가 간헐적으로 exit −1 을 낸다. 단독 실행은
  전부 RC=0 — **측정 실패가 아니라 래퍼 일시장애**이며, 죽은 팔은 모두 개별 재실행했다.

## 🔀 병렬 세션 대조 (`a_parallel_session_compare`)

저쪽 R-트랙이 같은 날 `V6_20` 사전등록을 착륙시켰고, 그 판정표에 이렇게 박혀 있다:

> `두 Δ ≥ MIE 이나 floor ≥ 통제 → INVALID · 바닥이 바닥이 아님 = 계기 결함`

**AGREES · 충돌 0.** 서로를 안 보고 같은 법칙에 도달했다 — 저쪽은 아직 안 쏜 패널의
*설계*에서 그 실패양식을 미리 막았고, 나는 그 실패양식이 **이미 착륙한 프로덕션 계기에
실재함**을 실측했다. NOVEL(내 쪽): 그 결함이 가설이 아니라 현행 코드의 상태이고,
비용 라우팅 판정 3/4 을 뒤집는다.

관련: `positive-control-before-reading-a-negative` · `chance-level-must-be-derived-per-metric` ·
`phi-estimator-needs-zero-truth-pedestal` · `read-the-artifact-record-before-declaring-a-cost-blocker`
