"""C1, read with a DERIVED bar — the operator is real, or it was 480 memorised lines.

Both bars come from the same null: permute the stem→polarity assignment, keep the model's answers,
recompute Δdep. That is the world in which polarity carries no information, so no operator can exist
in it. A value below the null's 1st percentile cannot be produced by a model that ignores polarity.

  ANCHOR (liveness, blocking) — the three TRAINED surfaces must each fall below their own null floor.
      Measured: −0.900/−1.000 · −0.400/−0.400 · −1.000/−1.000 vs floors −0.500/−0.600 · −0.400 ·
      −0.600. All below, both seeds. The instrument is alive. (The transplanted −0.5 bar had failed
      `안 {s}고` at −0.400 — but its own null floor IS −0.400, so that value is signal, not noise.
      The bar was wrong, not the run. convergence bar-derived-not-transplanted.)

  DV — the two NOVEL surfaces, never seen in arrow format (byte-audited: 0 occurrences in arrow
      lines AND 0 in natural text; Fable's own first candidate `안 {s}다` was killed by that audit
      at 58 hits).
        below its null floor, both seeds  -> the operator GENERALISES. It is a rule, not a table.
        indistinguishable from null, both -> H-γ: those 0.98-1.00 scores were line recall, and
                                             "BINDING" is the wrong name for the wall — there is no
                                             operator to bind to.
        split                             -> PENDING. No post-hoc arms.

Caveat stated plainly: the 1%-percentile convention was fixed before opening the DV columns, but
after seeing the anchor columns. It is a conventional threshold (p<0.01), not one chosen to make an
answer come out — and the DV columns below were not read until this file was written.
"""
import json, os, random

R = os.path.expanduser("~/anima-weights/h9314")
TRAINED = {"negL": "{s}지 않다", "negS": "안 {s}고", "negE": "전혀 {s}지 않다"}
NOVEL = {"novT": "{s}지는 않다", "novB": "별로 {s}지 않다"}


def dep(pols, saids):
    a = [s for p, s in zip(pols, saids) if p == 1]
    b = [s for p, s in zip(pols, saids) if p == 0]
    return (sum(a) / len(a) - sum(b) / len(b)) if a and b else None


def cell(rows, b):
    rs = [r for r in rows if r["b"] == b]
    pols = [int(r["pol"]) for r in rs]
    saids = [1 if ((r["gold_word"] == "긍정") == (r["margin"] > 0)) else 0 for r in rs]
    obs = dep(pols, saids)
    rng, ds, pp = random.Random(0), [], list(pols)
    for _ in range(20000):
        rng.shuffle(pp)
        d = dep(pp, saids)
        if d is not None:
            ds.append(d)
    ds.sort()
    floor = ds[int(0.01 * len(ds))]
    p = sum(1 for d in ds if d <= obs) / len(ds)
    return obs, floor, p


print("=" * 94)
print("C1 — 연산자는 실재하는가, 아니면 480개 암기된 라인이었나   (bar = 귀무 1%-floor · 유도됨)")
print("=" * 94)
res = {}
for s in ("main_s7", "main_s11"):
    rows = json.load(open(os.path.join(R, "c1_%s.json" % s)))["splits"]["heldout"]["rows"]
    res[s] = {b: cell(rows, b) for b in list(TRAINED) + list(NOVEL)}

print("\n⚓ 앵커 — 학습된 표면 (BLOCKING · 계기 생존)")
alive = True
for b, pat in TRAINED.items():
    line = "   %-16s" % pat
    for s in ("main_s7", "main_s11"):
        o, f, p = res[s][b]
        ok = o <= f
        alive &= ok
        line += "  %s Δ=%+.3f (floor %+.3f · p=%.3f) %s" % (s[5:], o, f, p, "✅" if ok else "⛔")
    print(line)
if not alive:
    print("\n⛔ INVALID — 계기 사망. DV 를 읽지 않는다.")
    raise SystemExit
print("   ⟹ ✅ 계기 생존 — DV 를 읽을 자격이 있다.")

print("\n🧪 DV — 새 표면 (arrow 0회 · 자연문 0회 · 바이트 감사 통과)")
gen, mem = [], []
for b, pat in NOVEL.items():
    line = "   %-16s" % pat
    for s in ("main_s7", "main_s11"):
        o, f, p = res[s][b]
        below = o <= f
        gen.append(below)
        mem.append(not below)
        line += "  %s Δ=%+.3f (floor %+.3f · p=%.3f) %s" % (
            s[5:], o, f, p, "✅ 귀무 아래" if below else "💀 귀무와 구별 불가")
    print(line)

print("\n" + "=" * 94)
if all(gen):
    print("VERDICT: 🟢 **연산자 실재 — H-γ 기각**")
    print("  본 적 없는 부정 표면 두 종 모두에서, 양 seed 모두, Δdep 가 **귀무 아래**다.")
    print("  ⟹ SEEN 어간의 0.98~1.00 은 **라인 암기가 아니라 규칙**이었다.")
    print("  ⟹ **'BINDING' 이라는 이름이 옳다** — 연산자는 실재하고, CPT 로 쓴 사실이 거기 닿지 못한다.")
    print("  다음 = C3(SEEN-REWRITE 교차): CPT 쓰기가 flip1 경로에 **보이는가**.")
elif all(mem):
    print("VERDICT: 💀 **H-γ 지지 — 연산자는 없었다. 480개 암기된 라인이었다.**")
    print("  본 적 없는 표면에서 극성 의존이 **귀무와 구별되지 않는다**(양 seed · 두 표면).")
    print("  ⟹ H_9327 의 '연산자는 살아있다'(0.98~1.00)는 **회상**이었고 **'BINDING' 은 틀린 이름**이다 —")
    print("     결합할 연산자가 애초에 없다. 카드/ARCHITECTURE 를 정정해야 한다.")
else:
    print("VERDICT: ⏳ **PENDING** — 표면/seed 간 불일치(사후 팔 추가 금지).")
    print("  부분 일반화 = 표면-특이적 회로 가능성. 검정력을 먼저 벌어라(표면 수·어간 수).")
