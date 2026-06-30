# AURA C0 — n=8 exact big-Φ 다창 위치 테스트 (FRONTAL8 vs MOTOR8) — 컴퓨팅-월 정량화

> 목표: A10.1(n=4, 10창, FRONTAL vs MOTOR **5:5 null**)을 **n=8 exact(2^16 MIP)** 해상도로 확장.
> 사전등록 falsifier: n=8 고해상도에서 n=4 null이 **유지**(위치효과 無)되는가, **변화**(효과 출현)하는가?
> 결과: **n=8 단일창 compute-wall 확정+정량화** — A9.1 월(月)이 native compile로도 안 깨짐. **NOT-MEASURED**(p7).

honest: 단일피험자(sub-1010), scalp-EEG proxy(침습 N1 깊이 아님). 사용자 승인 비용 fire.

---

## 1. 무엇을 했나

- **추출기** `c0_n8_extract.py`(numpy, 일시적 분석도구): BrainVision IEEE_FLOAT_32 65ch MULTIPLEXED →
  stride-20 decimate 5000→250Hz · 1000 samp(4s) · 채널-major flat `s[ch*n_samp+t]`. A7/A8/A10과 동일 전처리.
- **하니스** `c0_n8_{frontal,motor}.hexa`: 10창(raw offset 0..1260000, A10 grid) inline DATA + `eeg_big_phi(D,8,1000,255)`.
  - FRONTAL8 = F3·Fz·F4·AFz·F7·F8·FC1·FC2 (0-based idx 53,51,49,57,55,47,43,41)
  - MOTOR8 = C3·Cz·C4·C2·C1·C5·C6·CPz (0-based idx 35,33,31,32,34,36,30,23)
  - **window-0 데이터가 A9.1 `a9_n8_frontal.hexa`와 byte-identical** → 전처리 일관성 검증됨.

## 2. 호스트 감사 — 3 호스트 중 Mac만 사용 가능, 그나마 compute-bound

| 호스트 | 상태 | 근거 |
|---|---|---|
| **ubu-1** (pool, 12코어, hexa 0.1.0-dispatch) | 🔴 BLOCKED | `build/hexa_v2` 트랜스파일러가 `iit4_bigphi.hexa` import 하는 **모든** 하니스에 SEGV — **tiny n=3 toy도** (크기 무관) |
| **runpod CPU pod** (qa3iu2rjwwvnhk, 64 vCPU) | 🔴 BLOCKED | fresh clone prebuilt `hexa.real`가 GLIBC_2.38 요구, runpod/base ubuntu는 GLIBC 2.31 → version-not-found. `hexa_linux`(stage1)은 `hexa_stage0` 필요(install.sh module_loader 빌드 실패). 발사 7분·~$0.05·**teardown 완료** |
| **Mac** (hexat + clang → native) | 🟡 동작하나 느림 | n=8 트랜스파일+실행 정상(크래시 無). **유일 작동 호스트** |

→ Linux 양쪽 모두 hexa 툴체인 결함으로 막힘. handoff `[386f5407]` → hexa-lang inbox (a_runpod_inbox).

## 3. 월(wall) 정량화 — native Mac에서도 n=8 단일창 >11분 CPU 미완

native compile(Apple silicon 8 logical / **4 performance core**), batch-of-4(창당 perf-core 1개):

```
단일 n=8 창 CPU 시간이 11분 초과 + ~20분 wall에도 미완료
(f_w0..f_w3 모두 ~11:53 CPU / 20:38 wall, 4-way 경합+thermal throttle 하 ~0.3–0.6 core)
추정 전체 20창(FRONTAL10 + MOTOR10) sweep: 최소 ~90–150분 wall → 단일 세션 내 INTRACTABLE
```

cf A9.1: Mac **interpreter** 290s EXIT124 월 → **native compile도 n=8을 구제 못 함**. 2^16-state exact MIP은
근본적으로 O(2^2n), 여기서 창당 ~12–18분 CPU. (n=4는 초 단위 → n=8은 256× state, MIP 폭증.)

## 4. 판정 — n=8 다창 NOT-MEASURED (compute-wall). 최대-n verdict = n=4.

```
구조모델(in-silico A6/A7 + connectome A8.4/A9.3)  →  ✅ relocate 일관 지지
실 scalp-EEG proxy 최고해상도 = n=4 (A10.1, 10창)  →  🔴 위치효과 없음 (5:5, t(9)=0.28 n.s., p=1.0)
n=8 exact 다창 (C0 목표)                            →  ⬛ NOT-MEASURED (3 호스트 전부 막힘/월)
```

- **A9.1의 n=8 compute-wall 확정+정량화**: native도 못 깸. 작동하는 hexa 툴체인을 가진 many-core 호스트만
  열 수 있음(현 3 호스트는 BLOCKED 또는 compute-bound).
- **C0 사전등록 질문 미해결**: n=8 창 0개 완료 → FRONTAL vs MOTOR @ n=8 보고 불가. **NOT-MEASURED**(날조 숫자 無, p7·a_claim_verify).
- **현 최고해상도 위치 verdict는 A10.1(n=4) NULL** 유지: 위치효과 통계적으로 없음.

## 5. 잔존물 · 다음

- `c0_n8_{frontal,motor}.hexa` + `c0_n8_extract.py` 영속 — Linux hexa 툴체인 수정 시 64-core pod 경로가
  n=8 sweep을 시간(hr)→분(min)으로. handoff 환류 완료.
- batch-of-4 native 드라이버는 background 유지 — 창 완료 시 `build/c0/out_*.txt`에 누적(추후 harvest 가능).
- verdict: `.verdicts/c0-n8-fire/run.txt` (verbatim).

## 양방향 sibling

- sibling: [A9-n8-montage.md](A9-n8-montage.md) (n=8 compute-wall 원 발견 — C0가 native+다호스트로 정량화·확장)
- sibling: [A10-window-stats.md](A10-window-stats.md) (n=4 다창 null — 현 최고해상도 verdict)
- UNIVERSE SSOT: [AURA.md](AURA.md) A11 milestone
