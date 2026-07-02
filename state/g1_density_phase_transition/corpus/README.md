# G1 조합-커버리지 설계 코퍼스 (coverage-designed corpus)

AI/ML 재조합-일반화(compositional generalization) 연구용으로 **조합 커버리지를 일부러 설계한** 자연어 byte 코퍼스 한 쌍. G1 재조합벽 처방("조합-커버리지 코퍼스가 held-out 재조합을 여는가")을 낡은 코퍼스 co-occurrence 세기가 아니라 **매칭 크기 통제실험**으로 실측하기 위한 것.

## 무엇인가

30개 구체 개념어(`ocean·clock·forest·… ·hollow`)로 가능한 무순서 개념쌍 435개(=C(30,2)) 중 **40쌍을 held-out**으로 빼고, 나머지 395쌍(POOL)에서 커버리지 비율만 다르게 두 코퍼스를 만든다 — 크기는 ~1.2MB로 동일하게 매칭.

| 파일 | 커버리지 | 학습에 등장하는 쌍 | 크기 |
|---|---|---|---|
| `high_coverage.txt` | 60% | POOL의 60% (≈237쌍) | 1,200,010 B |
| `low_coverage.txt` | 8% | POOL의 8% (≈31쌍) | 1,200,009 B |

두 코퍼스 모두 **held-out 40쌍은 문장으로 등장하지 않는다**(재조합 held-out 무결). 차이는 오직 "학습 중 얼마나 다양한 개념쌍 조합을 봤는가"뿐.

## 문장 템플릿 (4종)

각 문장은 개념쌍 `(a,b)` + 동사 + 결과절을 조합:

```
1. "the {a} and the {b} {verb} until {result}."
2. "when {a} meets {b}, {result}."
3. "between the {a} and the {b} a quiet force {verb}s."
4. "{a} remembers {b}; together they {verb}."
```

동사 10종(`merge·echo·dissolve·…`) × 결과절 8종(`a new pattern forms·meaning shifts·…`).

## 왜 이렇게 설계했나

toy(20×20 격자)에서 조합 커버리지가 5→80%로 오를 때 held-out 재조합이 상전이(2%→92%)했다 — attention·ConvMoE-L1 둘 다(H_6182, arch-무관). 이 코퍼스는 그 처방을 **자연어 byte scale + production-근접 arch**에서 재검하기 위한 것: HIGH>LOW면 조합-커버리지가 G1 lever임을 NL scale에서 확증, HIGH≈LOW(특히 conv)면 좁은 수용영역(RF)이 병목(fable G6 분석과 합류).

## 재현

```bash
python3 build_and_test.py attn   # transformer (RF=full)
python3 build_and_test.py conv   # ConvMoE-L1 (RF=K bytes, production-근접)
```

`build_and_test.py`가 두 코퍼스를 결정적(seed 1/2)으로 생성하고, byte-GPT(d384·6층·BLOCK128)를 HIGH·LOW 각각 학습한 뒤 held-out 40쌍의 재조합을 측정한다(seen-sanity + shuffle control 3종 세트). **torch DIRECTIONAL** — engine-native 재검은 별도(a_engine_native_learning).

## 검증 스코프 (정직)

- 코퍼스는 결정적 생성물(재실행 byte-identical) — held-out 40쌍은 두 파일 어디에도 문장으로 없음(설계 무결).
- 학습/held-out verdict(H_6183)는 별도 실측 착륙 — 이 README는 **코퍼스 artifact**만 문서화.
- HF: `dancinlab/anima-g1-coverage-designed-corpus` (PRIVATE·연구 artifact).
