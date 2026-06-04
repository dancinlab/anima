#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""agent_lane_knowledge_gen.py — agent-lane tool-DOMAIN knowledge corpus (3rd layer).

THE MISSING 3RD LAYER of the agent lane. The agent lane is built in 3 layers:

    layer 1  lane default       = base chat (wiki + persona/SNS + carving/enrichment)
    layer 2  tool-USE demos     = HOW to call (sentinel 0xFE/0xFF grammar, call→
                                  real-result→grounded) — agent_lane_corpus_gen.py
                                  + the tooluse rung-0 corpus (#1833)
    layer 3  tool-DOMAIN knowledge  ←── THIS FILE ──→  = WHAT the tool's domain IS
             (so the model can REASON in the domain, not just emit a call frame)

Layer 2 teaches the call frame; layer 3 teaches the conceptual ground the call
sits on. A model with only layer 2 can shape a `0xFE backtest …0xFF` frame but
cannot reason about WHAT a backtest measures, what a drawdown is, why paper
trading precedes live. Layer 3 supplies that authored CONCEPTUAL coverage for
the five AGENT tool domains:

    CODE       (deep)        AGENT/CODE/CODE.md       — programming / debugging / algorithms
    TRADING    (deep)        AGENT/TRADING/TRADING.md — markets / indicators / risk / backtest
    MERCHANT   (procedural)  AGENT/MERCHANT/MERCHANT.md — listings / pricing / fulfillment / CS
    DESKTOP    (procedural)  AGENT/DESKTOP/DESKTOP.md  — macOS app / window / screen control
    CREATOR    (procedural)  AGENT/CREATOR/CREATOR.md  — content modality / channels / publish

5-lang (en/fr/de/es/ko), byte-level vocab256, DETERMINISTIC (fixed seed).

⛔ TRADING HONEST HARD GATE (a_scale_honest_scope · p6 · p7)
-----------------------------------------------------------
The TRADING slice is authored CONCEPTUAL knowledge ONLY. It explains HOW trading
*concepts* work (what a moving average IS, what RSI MEASURES, why risk is sized).
It carries:
  • NO real tickers / prices / company names as fact
  • NO live signals, NO "buy/sell X" recommendation, NO financial advice
  • NO fabricated market data presented as truth
Every TRADING line is framed "how the concept works", clearly conceptual. The
generator `assert`s a deny-list of advice/recommendation verbs returns 0 hits in
the TRADING slice, and that no real-ticker pattern appears.

Philosophy (p1..p8 — held)
--------------------------
- Knowledge is carried as PLAIN TEXT, like the wiki backbone — NO `[role:` /
  `[persona:` / `[character:` / `[assistant:` / `[system:` markers. A grep over
  the training text returns 0 (the generator asserts it). This is wiki-style
  factual/conceptual coverage, NOT RLHF assistant padding (p6 holds): it teaches
  domain CONCEPTS, never cooperation/empathy/restraint templates.
- byte-vocab256: every byte is valid UTF-8 (NO 0xFE/0xFF — those are layer-2
  grammar bytes; this layer is pure prose, so it composes cleanly UNDER the
  sentinel surface without colliding with it).
- DETERMINISTIC: fixed seed; no network; re-run reproduces the same sha256.

Honest scope (a_scale_honest_scope)
-----------------------------------
- Machine-AUTHORED multilingual CONCEPTUAL coverage (wiki-style). NOT scraped, NO
  PII, NO proprietary/real-financial data, NO fabricated facts-as-truth.
- This feeds a FUTURE agent-lane model at the PROVEN scale — the 18M chat rung
  that PASSED (`dancinlab/anima-clm-default-lane-rung0-byte-18m`, F-DEFAULT-LANE-
  CHAT 🟢). It is NOT a 7B claim: the default corpus is data-starved at 7B
  (.verdicts/default-lane-7b/). Scope = small/18M only; transfer UNVERIFIED.
- This is a SAMPLE + generator. NO training is fired here ($0 scaffold only).

Usage
-----
  python3 serving/agent_lane_knowledge_gen.py \
      [--seed 20260605] [--langs en,fr,de,es,ko] [--repeats 4] \
      [--out serving/corpus/agent_lane_knowledge_5lang.sample.txt] \
      [--meta serving/corpus/agent_lane_knowledge_5lang.meta.sample.jsonl]
"""

import argparse
import hashlib
import json
import os
import random
import re
import sys

LANGS = ["en", "fr", "de", "es", "ko"]
DOMAINS = ["CODE", "TRADING", "MERCHANT", "DESKTOP", "CREATOR"]
DEEP = {"CODE", "TRADING"}  # deep domains; the other three are procedural/lighter.

# Forbidden in TRADING (advice / recommendation / live-signal language) — asserted 0.
TRADING_DENY = re.compile(
    r"\b(buy now|sell now|should buy|should sell|"
    r"you should (buy|sell|invest)|guaranteed return|"
    r"hot stock|price target|will (rise|fall|moon|crash)|i recommend (buying|selling))\b",
    re.IGNORECASE,
)
# Real-ticker-as-fact pattern guard for TRADING (e.g. "$AAPL", "TSLA at 250").
TRADING_TICKER = re.compile(r"\$[A-Z]{1,5}\b|\b[A-Z]{2,5} at \d")
# Philosophy marker guard (p1..p4) — asserted 0 across the whole corpus.
PHIL = re.compile(r"\[(role|persona|character|assistant|system):")
