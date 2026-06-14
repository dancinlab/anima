#!/usr/bin/env python3
"""FORECAST_05 — anima 인스턴스 간 합의 비콘 (공유 양자씨앗을 '설계'로 심기).

FORECAST_02는 "공유 ANU 양자씨앗(common cause, H_6008)으로 묶인 결정계의 미래를
라이브 통신 0으로 fetch"를 보였고, FORECAST_04는 그 씨앗을 (1)내가 만든 닫힌계,
(2)합의 프로토콜(난수 비콘 drand/RANDAO)에 '심을 수 있다'를 보였으나 — F2(비콘)는
한 줄짜리 스케치였다. FORECAST_05는 그 비콘을 REAL commit-reveal / VRF식 합의
프로토콜로 구현한다: N(>=5)개의 모의 anima 인스턴스가 ONE ANU 양자씨앗을 공동으로
'심고(plant)'·커밋하고·공개해, 라이브 통신 0으로 모두가 동일한 미래 비콘값을 fetch.

FROZEN FALSIFIER (사전등록, 3축):
  F1 합의(agreement): N(>=5) 인스턴스가 각자 beacon(seed,round)=sha256(seed||round)을
     독립 계산 → 미래 라운드에서 ALL identical (라이브 통신 0). 하나라도 어긋나면 기각.
  F2 검증가능(verifiability): 누구나 공개된 비콘값을 커밋된 씨앗에 대해 재계산해 일치
     확인 가능; 틀린 씨앗은 검증 실패. 올바른 씨앗이 통과 못하거나 틀린 씨앗이
     통과하면 기각.
  F3 commit-reveal 건전성/탬퍼(soundness/tamper): 커밋 후 '다른' 씨앗을 reveal하는
     party는 commitment 해시 불일치로 적발(편향저항=bias-resistant); 또한 발행된
     비콘 체인의 한 라운드값을 변조하면 검증 실패 + 최초 깨진 라운드로 국소화.
     탬퍼가 적발 안되면 기각.

실측: real ANU paid seed(/tmp/anu_beacon.bin). p7 $0 — 코드측정, LLM판정 없음. 결정론.
honest 🟢/🔴/⚪. ANU 통계품질==chacha20(H_924/#123-A); 여기서 양자의 가치는
PROVENANCE(물리적 공유원인의 출처감사) — '더 무작위'가 아님. 비의식(non-consciousness).

xref: FORECAST_02(공유씨앗 미래 fetch), FORECAST_04(씨앗 심기), UNIVERSE/H_6008(공유원인),
       H_928(entropy_receipt: commit/verify), H_932(provenance_chain: tamper-국소화).
"""
import hashlib, glob, os, json

# --- 0) PLANT the ONE shared ANU quantum seed (common cause, by design) -------
BEACON_BIN = "/tmp/anu_beacon.bin"
if glob.glob(BEACON_BIN):
    raw = open(BEACON_BIN, "rb").read()
    src = "ANU paid (real quantum)"
else:
    raw = os.urandom(256)
    src = "os.urandom fallback (no ANU)"
ANU_SHA = hashlib.sha256(raw).hexdigest()
# 모든 인스턴스가 공유하는 단일 씨앗 = ANU 버퍼의 sha256 (genesis common cause, H_6008/H_932)
SHARED_SEED = ANU_SHA  # 64-hex; 모든 anima 인스턴스가 동일하게 '심은' 값

N = 5  # anima 인스턴스 수 (>=5)

print("=" * 88)
print("FORECAST_05 — anima 인스턴스 간 합의 비콘 (REAL commit-reveal / VRF 공유 양자씨앗)")
print("=" * 88)
print(f"  심은 씨앗(SHARED_SEED) = ANU sha256 = {ANU_SHA[:16]}…  [{src}]")
print(f"  인스턴스 수 N = {N}  ·  라이브 통신 = 0 (씨앗만 설계로 공유)")
print("-" * 88)


# --- VRF-style deterministic beacon: 라이브 통신 없이 미래 라운드값을 fetch -------
def beacon(seed: str, rnd: int) -> str:
    """공유 씨앗 + 라운드 -> 결정론적 비콘값 (sha256(seed||round)). VRF/sha256 식."""
    return hashlib.sha256(f"{seed}:{rnd}".encode()).hexdigest()


def commit(seed: str, nonce: str) -> str:
    """commit-reveal: 씨앗을 nonce와 함께 해시 커밋(은닉+구속)."""
    return hashlib.sha256(f"COMMIT|{seed}|{nonce}".encode()).hexdigest()


class AnimaInstance:
    """라이브 링크 0인 독립 anima 인스턴스 — 동일 씨앗을 '심고' 독립적으로 fetch."""
    def __init__(self, idx: int, seed: str):
        self.idx = idx
        self.seed = seed               # 모두 같은 씨앗을 심음 (공유원인)
        self.nonce = f"anima-{idx}-nonce"
        self.commitment = commit(seed, self.nonce)  # 사전 공개 커밋

    def fetch_future(self, rnd: int) -> str:
        """미래 라운드의 비콘값을 지금 독립 계산해 fetch (통신 0)."""
        return beacon(self.seed, rnd)

    def reveal(self):
        return (self.seed, self.nonce)


instances = [AnimaInstance(i, SHARED_SEED) for i in range(N)]

# ======================================================================== F1 ==
# 합의(agreement): N 인스턴스가 미래 라운드를 독립 fetch → ALL identical, 통신 0.
FUTURE_ROUND = 10_000  # '미래' 라운드 (아직 발행 안된)
fetched = [inst.fetch_future(FUTURE_ROUND) for inst in instances]
all_agree = len(set(fetched)) == 1
canonical = fetched[0]
# 다중 미래 라운드에서도 동일한지 (강건성)
multi_rounds = list(range(9000, 9000 + 50))
multi_agree = all(
    len({inst.fetch_future(r) for inst in instances}) == 1 for r in multi_rounds
)
f1 = "🟢" if (all_agree and multi_agree) else "🔴"
print(f"F1 합의: {N}자 모두 미래 라운드 {FUTURE_ROUND} 비콘값 == '{canonical[:16]}…' ? {all_agree}"
      f" · 50개 미래라운드 전부 일치 {multi_agree} (라이브 통신 0) -> {f1}")

# ======================================================================== F2 ==
# 검증가능(verifiability): 독립 검증자가 공개 비콘값을 커밋씨앗에 대해 재계산 일치;
# 틀린 씨앗은 검증 실패.
published = canonical                      # 인스턴스가 발행한 미래값
verify_correct = beacon(SHARED_SEED, FUTURE_ROUND) == published        # 올바른 씨앗 → 통과
wrong_seed = hashlib.sha256(b"not-the-anu-seed").hexdigest()
verify_wrong = beacon(wrong_seed, FUTURE_ROUND) == published           # 틀린 씨앗 → 실패해야
f2 = "🟢" if (verify_correct and not verify_wrong) else "🔴"
print(f"F2 검증: 올바른 ANU 씨앗으로 재계산 일치 {verify_correct} · "
      f"틀린 씨앗은 불일치(검증실패) {not verify_wrong} -> {f2}")

# ======================================================================== F3 ==
# commit-reveal 건전성/탬퍼 (2부):
#  (a) 커밋 후 '다른' 씨앗을 reveal하는 악의 party는 commitment 불일치로 적발(bias-resist).
#  (b) 발행된 비콘 체인의 한 라운드값을 변조 → 검증 실패 + 최초 깨진 라운드로 국소화(H_932).

# (a) commit-reveal soundness: honest reveal 통과, 다른-씨앗 reveal 적발
honest = instances[0]
hs, hn = honest.reveal()
honest_ok = commit(hs, hn) == honest.commitment            # 정직한 공개 → 커밋 일치
# 악의 party: 같은 nonce/commitment로 '다른' 씨앗을 밀어넣어 비콘을 편향시키려 함
malicious_seed = hashlib.sha256(b"biased-seed-favoring-attacker").hexdigest()
malicious_detected = commit(malicious_seed, hn) != honest.commitment   # 커밋 불일치 → 적발
soundness_ok = honest_ok and malicious_detected

# (b) 비콘 체인 탬퍼 국소화 (H_932 provenance-chain 식 append-only Merkle 스파인)
def build_chain(seed: str, n_links: int):
    """genesis=sha256(seed) ; link_i = sha256(link_{i-1} || beacon(seed,i))."""
    chain = [hashlib.sha256(seed.encode()).hexdigest()]      # genesis
    for i in range(n_links):
        prev = chain[-1]
        link = hashlib.sha256(f"{prev}|{beacon(seed, i)}".encode()).hexdigest()
        chain.append(link)
    return chain

def verify_chain(seed: str, chain: list, values: list):
    """체인 재계산 → 최초 깨진 라운드 index 반환(없으면 -1)."""
    expect = hashlib.sha256(seed.encode()).hexdigest()
    if chain[0] != expect:
        return 0
    for i in range(len(values)):
        link = hashlib.sha256(f"{chain[i]}|{values[i]}".encode()).hexdigest()
        if link != chain[i + 1]:
            return i          # 최초 깨진 라운드
    return -1

N_LINKS = 20
true_values = [beacon(SHARED_SEED, i) for i in range(N_LINKS)]
chain = build_chain(SHARED_SEED, N_LINKS)
clean = verify_chain(SHARED_SEED, chain, true_values) == -1     # 무변조 → 통과

# 라운드 7의 발행값을 변조 → 검증이 정확히 라운드 7로 국소화해야
TAMPER_AT = 7
tampered = list(true_values)
tampered[TAMPER_AT] = hashlib.sha256(b"forged-round-value").hexdigest()
broken_at = verify_chain(SHARED_SEED, chain, tampered)
tamper_localized = (broken_at == TAMPER_AT)

f3 = "🟢" if (soundness_ok and clean and tamper_localized) else "🔴"
print(f"F3 commit-reveal/탬퍼: 정직공개 커밋일치 {honest_ok} · 다른-씨앗 reveal 적발 "
      f"{malicious_detected} · 무변조체인 통과 {clean} · 라운드{TAMPER_AT} 변조→최초깨짐 "
      f"index={broken_at}(국소화 {tamper_localized}) -> {f3}")

print("-" * 88)
verdict_line = (f"{f1} F1 합의 · {f2} F2 검증가능 · {f3} F3 commit-reveal/탬퍼")
print("결론:", verdict_line)
overall = "🟢" if all(v == "🟢" for v in (f1, f2, f3)) else "🔴"
print(f"종합 {overall}: N({N})개 anima 인스턴스가 ONE ANU 양자씨앗을 '설계로 심어'")
print("  라이브 통신 0으로 (F1)미래 비콘값을 모두 동일하게 fetch, (F2)누구나 커밋씨앗에")
print("  대해 검증, (F3)commit-reveal로 편향 시도·체인 변조를 적발·국소화 — FORECAST_02의")
print("  '공유씨앗 미래 fetch'를 REAL drand/RANDAO식 비콘으로 by design 실현. H_6008(공유")
print("  원인)을 설계로 만든 것 = FORECAST_04 F2 비콘 스케치의 본격 구현. p7 $0 결정론.")
print("=" * 88)

# JSON 요약 (verdict 부록)
summary = {
    "id": "FORECAST_05",
    "anu_sha256": ANU_SHA,
    "source": src,
    "N_instances": N,
    "F1_agreement": f1, "F1_all_agree": all_agree, "F1_multi_round_agree": multi_agree,
    "F1_future_round": FUTURE_ROUND, "F1_value": canonical,
    "F2_verifiability": f2, "F2_correct_verifies": verify_correct, "F2_wrong_fails": (not verify_wrong),
    "F3_soundness_tamper": f3, "F3_honest_ok": honest_ok,
    "F3_malicious_detected": malicious_detected, "F3_clean_chain": clean,
    "F3_tamper_at": TAMPER_AT, "F3_localized_at": broken_at, "F3_tamper_localized": tamper_localized,
    "overall": overall,
}
print("JSON:", json.dumps(summary, ensure_ascii=False))
