코드 확인 완료 — `origin/main`의 `core/rho_fan.py`/`core/rho_fan.hexa` tokenizer, `cli/rho_axon.py:233 _boundary_hit`, `cli/evaluate.py`의 `words_fn` 배선(line 640 dets map)까지 실제 소스 기준으로 설계했다. 아래가 스펙이다.

---

# 스펙: parity-safe Unicode tokenizer (ρ-AXON ko/en 4-cell)

## 0. 핵심 설계 결정 — **in-place 교체가 아니라 lang-dispatch 신설** (요구 2를 구조적으로 보장)

`_rho_fan_words`를 codepoint-aware로 **직접 교체하는 안은 기각**해야 한다. 이유: "순수 ASCII 입력에 대한 동일성 증명"은 프로즌 영어 bar를 지키기에 **불충분**하다. 영어 bar가 토큰화하는 것은 프롬프트가 아니라 **303M decode 출력**이고, 303M은 ko 포함 4-cell corpus로 학습됐으므로 en-frame decode가 유효한 UTF-8 한글 시퀀스를 garble로 내뱉을 수 있다. 오늘 그 한글 바이트는 전부 구분자(토큰 기여 0)지만, in-place 교체 후엔 **토큰이 되어 kwr 분모 n을 늘리고**(`_rho_fan_known_word_ratio` = hit/n) kwr≥0.70·kwr≥0.5(evaluate.py:584) 게이트를 조용히 흔든다. ASCII-불변식 증명은 이 시나리오를 커버하지 못한다.

따라서:

- **`_rho_fan_words` — 동결, 바이트 하나도 안 건드림.** en cell·`_rho_fan_dict_load`·`_rho_fan_is_falsifiable`(en)·`rho_fan_detector_calibration`이 계속 이 함수를 호출. en 경로의 git diff = **공집합** → 프로즌 bar 불변이 "증명"이 아니라 **구성상 자명**해짐.
- **신설 `_rho_fan_words_uni(s)`** (py + hexa 쌍둥이) — codepoint-aware 상위집합 tokenizer. **ko cell 경로에서만** 사용: evaluate.py ko-cell의 `_g_load_corpus_tokens`(ko corpus)·`_g_content_ngrams`·kwr_ko, rho_axon ko cell.
- 배선 지점은 이미 존재: evaluate.py:638-642의 `dets` map이 `words_fn`/`known`/`corpus_tokens`를 함수값으로 주입한다. **dets를 per-cell(lang-keyed)로** 만들어 ko cell엔 `{words_fn: _rho_fan_words_uni, known: known_ko, corpus_tokens: ko-corpus를 uni로 토큰화}`, en cell엔 기존 dets 그대로. 코어 함수 시그니처 변경 0.

`_rho_fan_words_uni`는 ASCII 입력에 대해 `_rho_fan_words`와 byte-identical하도록 추가로 설계한다(§3 증명) — 이건 en bar 방어용이 아니라(그건 dispatch가 담당) ko cell 내 code-switching("AI가")의 ASCII 조각이 고전적 동작을 하게 하기 위함이다.

## 1. `.py` 알고리즘 — **str 순회가 아니라 byte 배열 위의 수동 UTF-8 디코더**

py를 python str codepoint 순회로 짜면 hexa와 다른 도메인(str vs bytes)에서 돌아 invalid-UTF-8 처리에서 반드시 갈라진다. **py도 bytes 위에서, hexa와 동일한 결정 트리로** 구현한다 — parity가 논증이 아니라 구조가 되게.

**word-char 판정 (codepoint)**: `_is_hangul_cp(cp) = (0xAC00≤cp≤0xD7A3) ∨ (0x1100≤cp≤0x11FF) ∨ (0x3130≤cp≤0x318F)` — rho_axon.py:220 `_is_hangul`의 3개 range와 **정확히 동일**(가–힣 / ᄀ–ᇿ / ㄰–㆏). Extended Jamo(U+A960·U+D7B0)는 rho_axon과의 정합을 위해 의도적으로 제외(현대 ko corpus에 부재).

핵심 관찰: **세 한글 블록은 전부 UTF-8 3-byte** (lead E1/E3/EA–ED). 2-byte·4-byte 문자는 한글일 수 없다 → 디코더는 3-byte 시퀀스만 정확히 인식하면 되고 나머지는 전부 구분자다.

```
def _rho_fan_words_uni(s):
    bs = _to_bytes(s); n = len(bs)
    words = []; cur = bytearray(); i = 0
    while i < n:
        b = bs[i]
        if b < 0x80:                                  # ── ASCII 분기: 기존 루프 몸체 그대로 ──
            if _rho_fan_is_alnum(b): cur.append(_rho_fan_lower1(b))
            else: flush(cur → words)
            i += 1
        elif 0xE0 <= b <= 0xEF and i + 2 < n \
             and 0x80 <= bs[i+1] <= 0xBF and 0x80 <= bs[i+2] <= 0xBF:
            cp = ((b & 0x0F) << 12) | ((bs[i+1] & 0x3F) << 6) | (bs[i+2] & 0x3F)
            if _is_hangul_cp(cp):
                cur += bs[i:i+3]                      # 원시 3바이트 그대로 append (case-fold 없음)
            else:
                flush()                               # 유효 3-byte 비한글(CJK 등) = 구분자
            i += 3
        else:
            flush(); i += 1                           # 그 외 모든 high byte(2/4-byte lead·
                                                      # 미아 continuation·잘린 시퀀스) = 구분자 1바이트
    flush()
    return [w.decode('utf-8') for w in words]         # 한글은 유효 3바이트만 들어왔으므로 안전
```

**정의된 성질**:
- **eojeol run 유지**: 한글 run은 내부 분할 없음 → "물이"·"의식은" 한 토큰. ASCII와 한글이 붙으면("ai가") 한 run — eojeol 의미론과 `_boundary_hit`(alnum·hangul 둘 다 word-char 취급) 정합.
- **한글 lowercase 없음**: 개념 부재, 원시 바이트 보존 → hexa와 바이트 동일 토큰.
- **오분류 불가능 증명 조각**: 구분자를 1바이트씩 소비해도 거짓 한글 매치가 생기지 않는다 — 한글 lead(E0–EF)와 continuation(80–BF)은 서로소이므로 어떤 유효/무효 시퀀스의 중간 바이트에서도 3-byte 한글 파싱이 시작될 수 없다. 따라서 `F0 EA B0 80`(잘린 4-byte 뒤 '가')은 F0=구분자, 이어서 '가' 정상 인식 — 결정적이고 순서 독립적.

## 2. `.hexa` byte-level 알고리즘 (parity twin)

hexa의 기존 프리미티브(`byte_len`/`substring` byte-index/`ord`/`chr`/문자열 concat)만으로 위 결정 트리를 1:1 이식. `continue`가 없어도 되도록 플래그 없이 if/else 중첩으로:

```
fn _rho_fan_words_uni(s: string) -> list {
    let n = byte_len(s)
    let words = []
    let mut cur = ""
    let mut i = 0
    while i < n {
        let b = ord(substring(s, i, i + 1))
        if b < 128 {
            if _rho_fan_is_alnum(b) { cur = cur + chr(_rho_fan_lower1(b)) }
            else { if byte_len(cur) > 0 { words.push(cur); cur = "" } }
            i = i + 1
        } else {
            let mut step = 1
            let mut isword = false
            if b >= 224 && b <= 239 && i + 2 < n {
                let b1 = ord(substring(s, i + 1, i + 2))
                let b2 = ord(substring(s, i + 2, i + 3))
                if b1 >= 128 && b1 <= 191 && b2 >= 128 && b2 <= 191 {
                    step = 3
                    let cp = (b - 224) * 4096 + (b1 - 128) * 64 + (b2 - 128)
                    if (cp >= 44032 && cp <= 55203) || (cp >= 4352 && cp <= 4607)
                       || (cp >= 12592 && cp <= 12687) { isword = true }
                }
            }
            if isword { cur = cur + substring(s, i, i + 3) }
            else { if byte_len(cur) > 0 { words.push(cur); cur = "" } }
            i = i + step
        }
    }
    if byte_len(cur) > 0 { words.push(cur) }
    return words
}
```

- `(b-224)*4096 + (b1-128)*64 + (b2-128)` ≡ `(b&0x0F)<<12 | (b1&0x3F)<<6 | (b2&0x3F)` (b∈E0..EF 범위에서 항등) — bit-op 없이 산술만으로 py와 수치 동일.
- 경계 조건 `i + 2 < n`: `substring(s, i+2, i+3)`이 마지막 바이트(n-1)까지 정확히 커버, off-by-one 없음(EOS에서 잘린 `EA B0`는 else로 떨어져 구분자 2회 — py와 동일).
- **py↔hexa byte-동치 근거**: 두 구현이 같은 도메인(UTF-8 byte열)에서 같은 비교 상수·같은 분기 순서·같은 상태기계(cur, words)를 돌린다. 동치가 "테스트로 확인되는 구조적 성질"이 됨.

### Parity 검증 프로토콜
1. **golden vector 파일** (hex-encoded raw bytes, `state/` 하위 frozen): 순수 ASCII(전 클래스), 순수 한글(음절·초성 jamo·compat jamo), 혼합("AI가 물이 된다"), josa eojeol 세트, 2-byte(é)·4-byte(emoji)·CJK(中), 잘린 한글(EOS의 `EA B0`), 미아 continuation, `F0 EA B0 80`, 빈 문자열, 전부-구분자.
2. **fuzz**: 고정 seed PRNG로 랜덤 byte열 10k개 (결정성 사수 — `bit-det-drop-fast-train` 정책상 eval 결정성은 유지 대상).
3. 두 구현이 각 벡터에 대해 토큰 리스트(JSON) 산출 → **diff 공집합**을 `hexa verify` claim으로 → `state/verdicts/` 동결 (a_claim_verify). hexa 실행은 cli 단일진입 경유(예: `anima evaluate --selftest-tokenizer` 서브커맨드, `hexa run core/…` 직접 실행 금지 배너 준수).
4. 이후 어느 한쪽 파일이 수정되면 parity claim 재실행 — `.harness/enforce_anima_gates.py` 후보로 등록.

## 3. ASCII byte-identical 불변식 — 2중 보장

**층 A (구성적, 진짜 방어선)**: en 경로는 코드 diff 자체가 없다. `_rho_fan_words`·4개 frozen set·`_rho_fan_is_falsifiable`·`rho_fan_detector_calibration` 전부 무변경 — PR diff 검사로 기계 확인 가능.

**층 B (uni의 ASCII-동일성 증명 스케치)**: 모든 바이트가 <0x80인 입력에서 uni는 매 스텝 첫 분기만 실행하고, 그 분기 몸체는 기존 `_rho_fan_words` 루프 몸체의 **축자 복사**다(같은 `_rho_fan_is_alnum`, 같은 `_rho_fan_lower1`, 같은 flush 규칙: 비단어→비어있지 않으면 push, 같은 말미 flush). i에 대한 귀납으로 상태 (cur, words)가 매 스텝 동일 → 출력 동일. 경계·lowercase·빈토큰·구두점 처리 전부 1:1 (빈 토큰은 양쪽 다 생성 자체가 불가능 — push는 byte_len(cur)>0에서만).

**검증법**:
- 단위: `_rho_fan_words_uni(x) == _rho_fan_words(x)`를 x = 5개 concept 문자열(`'consciousness arises from cells'` → `["consciousness","arises","from","cells"]` 고정 기대값 명시), calibration 문장 전체, /usr/share/dict/words 샘플, seed-고정 랜덤 ASCII fuzz에 대해 assert.
- **bar-level 회귀 (진짜 게이트)**: 변경 전 en decode 출력 스냅샷(이미 있는 frozen 산출물)에 대해 PR 전/후 `rho_fan_detector_calibration(known)` 출력과 eval_rho_fan 축 값을 **byte-hash 비교** → 동일 hash를 verdict에 동결. "ASCII라서 같을 것"이 아니라 "실측 bar 값이 bit-동일"을 기록.

## 4. ko known-word 프록시 + per-cell frozen-first gate

**프록시 정의**: /usr/share/dict ko판 부재. 큐레이트 closed-class set 2개:
- `KO_JOSA_SUFFIX` (byte-suffix 매치용): 은 는 이 가 을 를 에 의 도 만 과 와 로 에서 부터 까지 처럼 보다 조차 마저 이나 랑 하고 께서 에게 한테 로서 로써 라도 …
- `KO_FUNC` (정확 매치용): 그리고 그러나 하지만 그래서 또한 그런데 즉 따라서 그 이 저 것 수 등 …

tokenizer가 eojeol을 통째로 유지하므로("물이") josa **정확 매치는 원리상 실패**한다 — kwr_ko는 eojeol 단위로 정의: 토큰이 (a) `KO_FUNC` 정확 매치, 또는 (b) 순수-한글이고 `KO_JOSA_SUFFIX` 중 하나로 끝나며 어간 길이≥1음절이면 hit. hexa에선 byte-suffix 비교로 동일 구현(토큰이 원시 UTF-8이므로 suffix도 byte열 매치).

**정직한 스코프 (a_scale_honest_scope)**: 이것은 영어 kwr(235k 사전 대비 어휘 실재성 커버리지)과 **다른 물리량** — "조사가 붙은 한국어-형태 텍스트" 문법성 프록시이지 lexicality가 아니다. 랜덤 유효-한글 garble도 우연히 이/가/은으로 끝나 base rate가 높고, 실제 ko 문장의 josa-eojeol 비율은 0.70 근처가 아니다. **en 0.70 재사용 = 범주 오류**(항상-실패 또는 무의미-통과).

**frozen-first 사전등록안**: 303M ko decode를 단 한 번도 채점하기 **전에**, 모델과 독립인 두 분포로 게이트를 도출·동결:
1. 양성: `anima-corpus-ko-{general,sns}` held-out 문장 샘플의 kwr_ko 분포,
2. 음성: byte-shuffle garble + seed-고정 랜덤 유효-한글 문자열의 kwr_ko 분포,
3. 게이트 = 두 분포를 분리하는 사전 규칙(예: 양성 5th percentile과 음성 95th percentile 사이 중점) — **규칙을 먼저 카드에 적고 숫자는 corpus/garble 실행이 채움**.
4. 산출 상수 `KWR_KO_GATE`를 H 카드(2-surface: jsonl+card) + calibration ko 섹션 + `state/verdicts/`에 동결. en 0.70은 별도 상수로 불변.

추가 사전등록: **ko FALS는 초기 스코프에서 제외** — comparator/measurable set이 영어다. ko cell은 kwr_ko + reach(rho_axon Δ)만 채점하고, ko comparator set은 별도 H로만 도입(en set 번역-재사용 금지, 그것도 tune-to-green 벡터).

## 5. 위험 / 실패모드 & 방지책

| 시나리오 | 메커니즘 | 방지책 |
|---|---|---|
| en decode의 garble 한글이 토큰화 | in-place 교체 시 kwr 분모 증가 → 0.70/0.5 게이트 shift | **dispatch 아키텍처** — en 경로 diff 0 (§0) |
| `words_fn` 전역 스왑 | evaluate.py:640 dets가 전역 1개면 ko fix가 en에 전파 | dets **per-cell** 구성 + bar-level byte-hash 회귀를 verify claim으로 상시화 |
| novelty corpus 오염 | 4-cell corpus를 uni로 일괄 토큰화하면 en n-gram novelty 기저 변화 → leap/fan shift | `corpus_tokens`를 lang-key로 분리, en corpus는 frozen tokenizer로만 |
| py↔hexa drift | 한쪽만 수정 | golden vector+fuzz parity claim, enforce gate 후보 등록 |
| NFD 한글 (자모 분해형) | NFD 입력은 jamo run으로 토큰화되어 NFC corpus 값과 문자열 불일치 | tokenizer엔 정규화 넣지 않음(byte-결정성 사수); corpus-prep 단계에서 NFC assert. engine decode는 corpus 분포(NFC) 바이트를 방출하므로 실위험 낮음 — assert로 못박기 |
| **tune-to-green** | ko decode 채점 후 게이트 조정 유혹 | 게이트는 §4 절차로 **채점 전 동결**; 첫 채점이 negative면 negative가 결과(🟦). 게이트 수정의 유일한 합법 경로 = 새 H로 frozen-first 재등록 + 기존 결과 원문 보존 |

---

**요약**: 프로즌 영어 bar 보존은 "신중한 predicate 설계"가 아니라 **en 경로 무변경 + ko 전용 `_rho_fan_words_uni` 신설 + per-cell dispatch**로 구조화한다(in-place 교체는 garble-한글 시나리오 때문에 parity-unsafe). uni는 py/hexa 모두 byte열 위의 동일 결정 트리(3-byte 한글만 word, 나머지 high byte 구분자)로 구현해 parity를 golden-vector+fuzz claim으로 동결하고, ASCII 분기는 기존 루프의 축자 복사라 귀납적으로 byte-identical. ko kwr은 josa-suffix 문법성 프록시임을 명시하고 게이트를 corpus/garble 분포에서 채점-전 사전등록한다(`KWR_KO_GATE` ≠ en 0.70). ko FALS는 스코프 제외로 사전등록.
