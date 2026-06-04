---
license: cc-by-sa-4.0
language: [en, fr, de, es, ko]
pretty_name: anima agent-lane tool-DOMAIN knowledge corpus (layer-3, byte-vocab256, conceptual)
tags: [anima, agent, tool-domain-knowledge, conceptual, multilingual, byte-vocab, coverage-corpus, authored-synthetic]
---

# anima-agent-lane-tool-knowledge — the 3rd layer of the agent lane

The **tool-DOMAIN knowledge** surface (layer 3) of the anima agent lane. It
supplies authored CONCEPTUAL coverage of the five AGENT tool domains so the
byte-LM can REASON in those domains — not merely emit a tool-call frame.

## the 3-layer agent lane

```
layer 1  lane default        = base chat (wiki + persona/SNS + carving/enrichment)
                                — NO tools, 0xFE/0xFF byte-frequency exactly 0.
layer 2  tool-USE demos       = HOW to call: sentinel 0xFE/0xFF grammar,
                                call → real-result → grounded continuation.
                                (serving/agent_lane_corpus_gen.py + tooluse rung-0)
layer 3  tool-DOMAIN knowledge  ←── THIS CORPUS ──→  = WHAT each tool's domain IS.
                                authored conceptual coverage (wiki-style prose).

    lane agent = layer 1  +  layer 2  +  layer 3     (lane agent ⊃ lane default)
```

Layer 2 teaches the call frame; layer 3 teaches the conceptual ground the call
sits on. A model with only layer 2 can shape a `0xFE backtest …0xFF` frame but
cannot reason about WHAT a backtest measures, what a drawdown is, or why paper
trading precedes live. Layer 3 closes that gap.

## the five domains (depth by domain)

| domain | depth | source md | what it covers (CONCEPTS) |
|---|---|---|---|
| **CODE** | deep | `AGENT/CODE/CODE.md` | variables · functions · loops · recursion · data structures · big-O complexity · debugging · error types · version control · testing · paradigms · concurrency |
| **TRADING** | deep | `AGENT/TRADING/TRADING.md` | markets/bid-ask · moving average · RSI · volatility · position sizing · stops · drawdown · backtest · **paper-vs-live** · order types · diversification — **CONCEPTUAL ONLY** (see hard gate below) |
| **MERCHANT** | procedural | `AGENT/MERCHANT/MERCHANT.md` | listings · pricing/margin · fulfillment · inventory · customer service · settlement |
| **DESKTOP** | procedural | `AGENT/DESKTOP/DESKTOP.md` | app control · accessibility tree · input events · window ops · OCR · dry-run |
| **CREATOR** | procedural | `AGENT/CREATOR/CREATOR.md` | modality (still/prog/gen) · script · channel · publish job · provenance · brand consistency |

Depth = number of authored concepts per domain: CODE 12, TRADING 11 (deep);
MERCHANT / DESKTOP / CREATOR 6 each (procedural). Each concept is authored in all
5 languages, so coverage is uniform across en/fr/de/es/ko.

## ⛔ TRADING HONEST HARD GATE (a_scale_honest_scope · p6 · p7)

The TRADING slice is **authored CONCEPTUAL knowledge ONLY**. It explains *how
trading concepts work* (what a moving average IS, what RSI MEASURES, why risk is
sized, how a backtest must charge fees). It carries:

- **NO** real tickers / prices / company names as fact
- **NO** live signals, **NO** "buy/sell X" recommendation, **NO** financial advice
- **NO** fabricated market data presented as truth

Every TRADING line is framed *"As a trading concept, …"* and describes the
concept, never a course of action. Indicator lines explicitly state that they
*describe* (momentum / trend / risk) and do **not** imply any action; the
backtest line states a good past result *describes history, never a promise about
the future*. The generator **asserts** a deny-list of advice / live-signal verbs
(`buy now`, `should buy/sell`, `price target`, `will rise/fall`, `guaranteed
return`, `i recommend buying/selling`, …) returns **0** hits in the TRADING
slice, and that **no** real-ticker-as-fact pattern (`$AAPL`, `XXX at 250`)
appears. This is **not** financial advice and **not** a trading system.

## honest invariants (the generator refuses to emit a dishonest corpus)

- **philosophy markers = 0** — `grep -E '\[role:|\[persona:|\[character:|\[assistant:|\[system:'`
  over the corpus returns 0. Knowledge is carried as PLAIN PROSE like the wiki
  backbone (p1..p4 held). This is wiki-style conceptual coverage, **NOT** RLHF
  assistant padding — it teaches domain CONCEPTS, never cooperation / empathy /
  restraint templates (p6 held). No perplexity verdict is implied (p7).
- **0xFE / 0xFF absent** — layer 3 is pure prose, so it composes cleanly UNDER
  the layer-2 sentinel grammar with no byte collision (asserted 0 / 0).
- **TRADING gate = 0 / 0** — advice/signal phrases 0, real-ticker patterns 0
  (asserted, see hard gate above).
- **byte-vocab256 clean** — the whole corpus decodes as valid UTF-8.
- **5-lang balanced** — every concept is authored in all 5 languages (uniform
  per-lang block count).

## scope (a_scale_honest_scope — NO 7B claim)

Machine-AUTHORED multilingual CONCEPTUAL coverage. **NOT** scraped, **NO** PII,
**NO** proprietary/real-financial data, **NO** fabricated facts-as-truth. This
feeds a FUTURE agent-lane model at the **PROVEN scale** — the 18M chat rung that
PASSED (`dancinlab/anima-clm-default-lane-rung0-byte-18m`, F-DEFAULT-LANE-CHAT
🟢). It is **NOT** a 7B claim: the default corpus is data-starved at 7B
(`.verdicts/default-lane-7b/`). Scope = small / 18M only; mid/7B transfer
UNVERIFIED. This is a SAMPLE + generator only — **NO training is fired here**
($0 CPU scaffold; the agent-lane rung is GATED).

## artifacts & manifest (this commit)

| file | role | bytes | sha256 |
|---|---|---|---|
| `agent_lane_knowledge_gen.py` | generator (committed) | — | `004ec72b3c1691125c75c7efb6112668a2af12d80c2baf4cbaf2462124bf7030` |
| `agent_lane_knowledge_5lang.head.txt` | committed sample head (120 blocks) | 26,779 | `918a9a63b9832af3a5185defec275b96b9fa8aa4714afc87cb8d9ef1afee2ef9` |
| `agent_lane_knowledge_5lang.sample.txt` | sample (820 blocks, repeats=4) — HF | 185,984 | `fdc158a648d8047c36f65d44c75dd9bfddab9c8f2321cf5bd854d7dc1c8fe19a` |
| `agent_lane_knowledge_5lang.full.txt` | full corpus (2,460 blocks, repeats=12) — HF | 557,952 | `825a51880ed6e1510f596fda9a7e14270de81063264287d9709e8fdce9939b01` |

### full corpus — per-domain byte split (repeats=12)

| domain | depth | blocks | bytes | % |
|---|---|---|---|---|
| CODE | deep | 720 | 140,940 | 25.26% |
| TRADING | deep | 660 | 169,272 | 30.34% |
| DESKTOP | procedural | 360 | 83,772 | 15.01% |
| CREATOR | procedural | 360 | 80,772 | 14.48% |
| MERCHANT | procedural | 360 | 80,736 | 14.47% |
| **total** | | **2,460** | **557,952** | 100% |

### full corpus — per-lang block split (5-way balanced)

| lang | blocks |
|---|---|
| en | 492 |
| fr | 492 |
| de | 492 |
| es | 492 |
| ko | 492 |

## reproduce

```
python3 serving/agent_lane_knowledge_gen.py                 # 820-block sample
python3 serving/agent_lane_knowledge_gen.py --repeats 12 \
  --out serving/corpus/agent_lane_knowledge_5lang.full.txt \
  --meta serving/corpus/agent_lane_knowledge_5lang.meta.full.jsonl
```

- generator : `serving/agent_lane_knowledge_gen.py`
- **deterministic** : fixed seed (`--seed 20260605`), no network — re-run
  reproduces the same sha256.
- metadata  : per-block `domain / depth / concept / lang / bytes`.
