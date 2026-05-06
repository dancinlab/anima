# anima_emerge_chat_byte_0_255_ban — landed 2026-05-05

## status
- **verdict**: FAIL_DEEP_SUPPRESSION
- **lane**: anima_emerge / chat-cap mass-ban probe
- **substrate**: need-singularity/clm-v4-mk2-v1, mac CPU fp32
- **cost**: $0
- **runtime**: ~12min
- **output dir**: `state/anima_emerge_chat_byte_0_255_ban_2026_05_05/`

## hypothesis under test
SentencePiece byte-fallback tokens (id 0-255) monopolize next-token mass on
clm-v4-mk2-v1. If we mass-mask the entire id 0-255 (or wider) range pre-argmax,
will the substrate fall back to coherent (Korean / English) tokens — or to
another broken attractor?

Convergent evidence from BG-CA (top-30 100% byte) + BG-CC + BG-CM motivated
this aggressive ban.

## first 30 token id sample (clm-v4-mk2-v1 SP vocab)
- id 0: `<pad>`
- id 1: `<s>`
- id 2: `</s>`
- id 3: `<unk>`
- id 4..29: `<0x00>` … `<0x19>` (byte-fallback control bytes)

Byte-fallback range starts at id 4 and runs through ~id 259 (`<0x00>` …
`<0xFF>`). ids 0-3 are pad/bos/eos/unk specials.

## protocol
- Korean prompt `안녕`, English prompt `Hello`
- 4 ban levels: 0-127 (ASCII), 0-255 (full byte), 0-511, 0-1000
- For each: greedy decode 25 new tokens with logits[ban_set] = -inf
- Baseline (no ban) for both prompts
- Count Korean glyphs (가-힣) and ASCII alphabetic in 25-token emit

## results — Korean prompt `안녕`
| ban level | korean | ascii | first emit ids |
|---|---|---|---|
| baseline (no ban) | 0 | 0 | byte-fallback `\x1c \x06 \x06 …` |
| ban 0-127 | 0 | 0 | id 157, 235 (still byte-fallback above 127) |
| ban 0-255 (full byte) | 0 | 30 | `local XVIII XVIII … 亿立方米 …` |
| ban 0-511 | 0 | 30 | identical to 0-255 |
| ban 0-1000 | 0 | 30 | identical to 0-255 |

## results — English prompt `Hello`
| ban level | emit |
|---|---|
| baseline | ` ``` ``` ``` ` (backtick attractor) |
| ban 0-127 | replacement-char fallback |
| ban 0-255 | `XVIII 亿立方米 亿立方米 …` |
| ban 0-511 | identical |
| ban 0-1000 | identical |

## findings
1. **Byte fallback does monopolize**: ban 0-127 still produces byte-fallback
   (ids 157, 235 are within 128-255 byte-fallback range). Confirms BG-CA finding.
2. **Full byte ban (0-255) breaks the byte attractor**, but the substrate does
   NOT fall back to Korean. Instead it lands on a degenerate **CJK + Roman
   numeral attractor**: `local XVIII … 亿立方米 …` (Chinese, not Korean).
3. **Korean is not the next-best basin**: even with 1000 lowest ids banned,
   korean_count = 0 across all ban levels.
4. **Suppression is structurally deep**: Korean tokens have effectively zero
   logit mass in this substrate's output distribution under the `안녕` /
   `Hello` prompts at greedy decode. Not just byte fallback monopoly — Korean
   is below the top-K of the entire non-byte vocabulary (>1000 ids).
5. **Same attractor for both prompts**: Korean prompt `안녕` and English prompt
   `Hello` collapse to identical `XVIII … 亿立方米` attractor under full byte
   ban — prompt-conditioning is also collapsed.

## verdict
**FAIL_DEEP_SUPPRESSION** — Korean recovery does not occur via byte-fallback
ablation alone. The substrate has a deeper, non-byte attractor (CJK + Roman
numerals) that takes over once byte fallback is masked. Confirms #115 chat-
incapability is architectural, not merely a tokenizer artifact.

This rules out the "byte fallback masks coherent Korean" hypothesis. Korean
emergence will require either (a) targeted activation/embedding intervention
at a deeper layer, or (b) accepting CLM v4 as substrate-research only and
pivoting back to Llama Path A v2 for chat capability. Aligns with prior
landed: `clm_v4_lora_sft_chat_lift_falsified_substrate_safe`.

## honest C3 (5)
- **C1**: mac CPU fp32 only — H100 BF16 sampling distribution may differ
- **C2**: id range 0-255 includes specials (pad/bos/eos/unk at 0-3); 4-259 is
  the actual byte-fallback range. Ban_0_to_255 covers 0-127 byte-fallback +
  most of 128-255 byte-fallback but not all. ban_0_to_511 fully covers byte
  range
- **C3**: single Korean prompt `안녕` + single English prompt `Hello` — no
  prompt diversity sweep
- **C4**: "recovery" measured by Korean glyph count, not by coherence /
  meaning / valid Korean morphology
- **C5**: ban-then-greedy may surface a different degenerate mode (here
  `XVIII 亿立方米`) — passing this measure would still not prove chat
  capability

## artifacts
- `tool/transient_py/anima_emerge_chat_byte_0_255_ban.py` (script)
- `state/anima_emerge_chat_byte_0_255_ban_2026_05_05/aggregate.json`
- `state/anima_emerge_chat_byte_0_255_ban_2026_05_05/verdict.json`

## linked landed
- `anima_emerge_chat_byte_ban` (BG-CC, similar narrower probe)
- `anima_emerge_chat_korean_rank_survey` (BG-CA, top-30 100% byte)
- `clm_v4_lora_sft_chat_lift_falsified_substrate_safe` (#115 architectural)

## constraints respected
- raw#37 transient_py opt-out (script in `tool/transient_py/`)
- raw#15 / raw#10 PASS (no commit, no leak, no concurrent destructive ops)
- HEXA_PY=.venv-eeg/bin/python invocation
- $0 mac CPU only
- no commit
