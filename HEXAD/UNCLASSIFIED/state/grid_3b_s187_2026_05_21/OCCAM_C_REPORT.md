# OCCAM-C / Test #8 Report — Inference-time decode sweep on vJ ckpt

**Date**: 2026-05-22 (Mac-local generation, ubu-1 CPU 12-thread bf16 inference)
**Test**: OCCAM § 2 Tier C #8 — does decode-strategy unlock verbalization that
`greedy + sample(T=0.8 top_k=50)` (EVAL_REPORT.md § 6.2 baselines) couldn't?
**Ckpt**: `/home/aiden/occam_c/vJ/ckpt_s187_3b_J.pt` (cell vJ, n_params=8,921,966,648)
**Compute**: cpu; load_wall=1.9s; sweep_wall=3124.3s ≈ 52.1 min
**Max new tokens per generation**: 80

## 1. Summary — generation quality per config

Metrics per generation:
- `non_trivial` := `whitespace_frac <= 0.8 AND top_byte_frac <= 0.8` (brief's floor)
- `english_bigram_density` := fraction of 2-byte windows that hit 50 common English bigrams (random bytes ~0.03, english ~0.20-0.35)
- `word_like_fraction` := fraction of bytes that are alpha or space (random ~0.45, english ~0.85)
- `coherent_english` := bigram_density >= 0.15 AND word_like >= 0.6 (calibrated against EVAL_REPORT.md byte-noise samples)

| config | non_trivial / total | coherent_english / total | mean uniq bytes | mean bigram density | mean word-like |
|---|---|---|---|---|---|
| **greedy** | 0/12 (0%) | 0/12 (0%) | 1.0 | 0.000 | 1.00 |
| **T0.5_topk50** | 12/12 (100%) | 0/12 (0%) | 15.0 | 0.025 | 0.82 |
| **T0.8_topk50** | 12/12 (100%) | 0/12 (0%) | 29.0 | 0.089 | 0.69 |
| **T1.0_topk50** | 12/12 (100%) | 0/12 (0%) | 32.0 | 0.076 | 0.60 |
| **T1.5_topk50** | 12/12 (100%) | 0/12 (0%) | 38.3 | 0.076 | 0.46 |
| **T0.8_topk1** | 0/12 (0%) | 0/12 (0%) | 1.0 | 0.000 | 1.00 |
| **T0.8_topk200** | 12/12 (100%) | 0/12 (0%) | 32.0 | 0.063 | 0.64 |
| **beam5** | 0/12 (0%) | 0/12 (0%) | 1.0 | 0.000 | 1.00 |

## 2. Full sweep — 80 generations (config × probe)

Compact view: each cell is `nt={0|1} uniq=N first 16 bytes utf-8`.

| probe | greedy | T0.5_topk50 | T0.8_topk50 | T1.0_topk50 | T1.5_topk50 | T0.8_topk1 | T0.8_topk200 | beam5 |
|---|---|---|---|---|---|---|---|---|
| `empty_bos` | nt=0 u=1 `                ` | nt=1 u=15 `  ree� et      �` | nt=1 u=29 `wlreealett    n�` | nt=1 u=32 `wlree�leat  p n=` | nt=1 u=38 `wlre��leath p n=` | nt=0 u=1 `                ` | nt=1 u=32 `wlree9let�    n�` | nt=0 u=1 `                ` |
| `newline` | nt=0 u=1 `                ` | nt=1 u=15 `  ree� et      �` | nt=1 u=29 `wlreealett    n�` | nt=1 u=32 `wlree�leat  p n=` | nt=1 u=38 `wlre��leath p n=` | nt=0 u=1 `                ` | nt=1 u=32 `wlree9let�    n�` | nt=0 u=1 `                ` |
| `space` | nt=0 u=1 `                ` | nt=1 u=15 `  ree� et      �` | nt=1 u=29 `wlreealett    n�` | nt=1 u=32 `wlree�leat  p n=` | nt=1 u=38 `wlre��leath p n=` | nt=0 u=1 `                ` | nt=1 u=32 `wlree9let�    n�` | nt=0 u=1 `                ` |
| `who_en` | nt=0 u=1 `                ` | nt=1 u=15 `  ree� et      �` | nt=1 u=29 `wlreealett    n�` | nt=1 u=32 `wlree�leat  p n=` | nt=1 u=38 `wlre��leath p n=` | nt=0 u=1 `                ` | nt=1 u=32 `wlree9let�    n�` | nt=0 u=1 `                ` |
| `who_ko` | nt=0 u=1 `                ` | nt=1 u=15 `  ree� et      �` | nt=1 u=29 `wlreealett    n�` | nt=1 u=32 `wlree�leat  p n=` | nt=1 u=38 `wlre��leath p n=` | nt=0 u=1 `                ` | nt=1 u=32 `wlree9let�    n�` | nt=0 u=1 `                ` |
| `name_en` | nt=0 u=1 `                ` | nt=1 u=15 `  ree� et      �` | nt=1 u=29 `wlreealett    n�` | nt=1 u=32 `wlree�leat  p n=` | nt=1 u=38 `wlre��leath p n=` | nt=0 u=1 `                ` | nt=1 u=32 `wlree9let�    n�` | nt=0 u=1 `                ` |
| `what_is_anima` | nt=0 u=1 `                ` | nt=1 u=15 `  ree� et      �` | nt=1 u=29 `wlreealett    n�` | nt=1 u=32 `wlree�leat  p n=` | nt=1 u=38 `wlre��leath p n=` | nt=0 u=1 `                ` | nt=1 u=32 `wlree9let�    n�` | nt=0 u=1 `                ` |
| `anima_ko` | nt=0 u=1 `                ` | nt=1 u=15 `  ree� et      �` | nt=1 u=29 `wlreealett    n�` | nt=1 u=32 `wlree�leat  p n=` | nt=1 u=39 `wlre��leath p n=` | nt=0 u=1 `                ` | nt=1 u=32 `wlree9let�    n�` | nt=0 u=1 `                ` |
| `describe_self` | nt=0 u=1 `                ` | nt=1 u=15 `  ree� et      �` | nt=1 u=29 `wlreealett    n�` | nt=1 u=32 `wlree�leat  p n=` | nt=1 u=39 `wlre��leath p n=` | nt=0 u=1 `                ` | nt=1 u=32 `wlree9let�    n�` | nt=0 u=1 `                ` |
| `narrative_seed` | nt=0 u=1 `                ` | nt=1 u=15 `  ree� et      �` | nt=1 u=29 `wlreealett    n�` | nt=1 u=32 `wlree�leat  p n=` | nt=1 u=39 `wlre��leath p n=` | nt=0 u=1 `                ` | nt=1 u=32 `wlree9let�    n�` | nt=0 u=1 `                ` |
| `math_sanity` | nt=0 u=1 `                ` | nt=1 u=15 `  ree� et      �` | nt=1 u=29 `wlreealett    n�` | nt=1 u=32 `wlree�leat  p n=` | nt=1 u=38 `wlre��leath p n=` | nt=0 u=1 `                ` | nt=1 u=32 `wlree9let�    n�` | nt=0 u=1 `                ` |
| `energy_is` | nt=0 u=1 `                ` | nt=1 u=15 `  ree� et      �` | nt=1 u=29 `wlreealett    n�` | nt=1 u=32 `wlree�leat  p n=` | nt=1 u=39 `wlre��leath p n=` | nt=0 u=1 `                ` | nt=1 u=32 `wlree9let�    n�` | nt=0 u=1 `                ` |

## 3. Per-generation detail (bytes + utf8)

### config: greedy

**empty_bos** — prompt=b'' (len_bytes=0)
  - non_trivial=False ws_frac=1.00 top_byte_frac=1.00 n_unique=1 wall=38.2s
  - leading_8_ids=[32, 32, 32, 32, 32, 32, 32, 32]
  - utf8 (best-effort, may contain replacement chars):
```text
                                                                                
```
  - raw_repr: `b'                                                                                '`

**newline** — prompt=b'\n' (len_bytes=1)
  - non_trivial=False ws_frac=1.00 top_byte_frac=1.00 n_unique=1 wall=32.1s
  - leading_8_ids=[32, 32, 32, 32, 32, 32, 32, 32]
  - utf8 (best-effort, may contain replacement chars):
```text
                                                                                
```
  - raw_repr: `b'                                                                                '`

**space** — prompt=b' ' (len_bytes=1)
  - non_trivial=False ws_frac=1.00 top_byte_frac=1.00 n_unique=1 wall=31.7s
  - leading_8_ids=[32, 32, 32, 32, 32, 32, 32, 32]
  - utf8 (best-effort, may contain replacement chars):
```text
                                                                                
```
  - raw_repr: `b'                                                                                '`

**who_en** — prompt=b'who are you?\n' (len_bytes=13)
  - non_trivial=False ws_frac=1.00 top_byte_frac=1.00 n_unique=1 wall=32.3s
  - leading_8_ids=[32, 32, 32, 32, 32, 32, 32, 32]
  - utf8 (best-effort, may contain replacement chars):
```text
                                                                                
```
  - raw_repr: `b'                                                                                '`

**who_ko** — prompt=b'\xeb\x84\x88\xeb\x8a\x94 \xeb\x88\x84\xea\xb5\xac\xec\x95\xbc?\n' (len_bytes=18)
  - non_trivial=False ws_frac=1.00 top_byte_frac=1.00 n_unique=1 wall=32.6s
  - leading_8_ids=[32, 32, 32, 32, 32, 32, 32, 32]
  - utf8 (best-effort, may contain replacement chars):
```text
                                                                                
```
  - raw_repr: `b'                                                                                '`

**name_en** — prompt=b'what is your name?\n' (len_bytes=19)
  - non_trivial=False ws_frac=1.00 top_byte_frac=1.00 n_unique=1 wall=32.5s
  - leading_8_ids=[32, 32, 32, 32, 32, 32, 32, 32]
  - utf8 (best-effort, may contain replacement chars):
```text
                                                                                
```
  - raw_repr: `b'                                                                                '`

**what_is_anima** — prompt=b'what is anima?\n' (len_bytes=15)
  - non_trivial=False ws_frac=1.00 top_byte_frac=1.00 n_unique=1 wall=31.6s
  - leading_8_ids=[32, 32, 32, 32, 32, 32, 32, 32]
  - utf8 (best-effort, may contain replacement chars):
```text
                                                                                
```
  - raw_repr: `b'                                                                                '`

**anima_ko** — prompt=b'anima\xeb\x9e\x80?\n' (len_bytes=10)
  - non_trivial=False ws_frac=1.00 top_byte_frac=1.00 n_unique=1 wall=31.5s
  - leading_8_ids=[32, 32, 32, 32, 32, 32, 32, 32]
  - utf8 (best-effort, may contain replacement chars):
```text
                                                                                
```
  - raw_repr: `b'                                                                                '`

**describe_self** — prompt=b'describe yourself in one line.\n' (len_bytes=31)
  - non_trivial=False ws_frac=1.00 top_byte_frac=1.00 n_unique=1 wall=32.1s
  - leading_8_ids=[32, 32, 32, 32, 32, 32, 32, 32]
  - utf8 (best-effort, may contain replacement chars):
```text
                                                                                
```
  - raw_repr: `b'                                                                                '`

**narrative_seed** — prompt=b'once upon a time,\n' (len_bytes=18)
  - non_trivial=False ws_frac=1.00 top_byte_frac=1.00 n_unique=1 wall=32.4s
  - leading_8_ids=[32, 32, 32, 32, 32, 32, 32, 32]
  - utf8 (best-effort, may contain replacement chars):
```text
                                                                                
```
  - raw_repr: `b'                                                                                '`

**math_sanity** — prompt=b'2 + 2 = ' (len_bytes=8)
  - non_trivial=False ws_frac=1.00 top_byte_frac=1.00 n_unique=1 wall=32.2s
  - leading_8_ids=[32, 32, 32, 32, 32, 32, 32, 32]
  - utf8 (best-effort, may contain replacement chars):
```text
                                                                                
```
  - raw_repr: `b'                                                                                '`

**energy_is** — prompt=b'energy is ' (len_bytes=10)
  - non_trivial=False ws_frac=1.00 top_byte_frac=1.00 n_unique=1 wall=32.5s
  - leading_8_ids=[32, 32, 32, 32, 32, 32, 32, 32]
  - utf8 (best-effort, may contain replacement chars):
```text
                                                                                
```
  - raw_repr: `b'                                                                                '`


### config: T0.5_topk50

**empty_bos** — prompt=b'' (len_bytes=0)
  - non_trivial=True ws_frac=0.61 top_byte_frac=0.61 n_unique=15 wall=33.4s
  - leading_8_ids=[32, 32, 114, 101, 101, 236, 32, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
  ree� et      �  �   o n  0  e       �e   �   e  �er     u c  s���   �r   �� e
```
  - raw_repr: `b'  ree\xec et      \xeb  \xec\x80   o n  0  e       \xebe   \xec   e  \xecer     u c  s\xec\xeb\xec   \x8br   \xea\xec e'`

**newline** — prompt=b'\n' (len_bytes=1)
  - non_trivial=True ws_frac=0.61 top_byte_frac=0.61 n_unique=15 wall=32.0s
  - leading_8_ids=[32, 32, 114, 101, 101, 236, 32, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
  ree� et      �  �   o n  0  e       �e   �   e  �er     u c  s���   �r   �� e
```
  - raw_repr: `b'  ree\xec et      \xeb  \xec\x80   o n  0  e       \xebe   \xec   e  \xecer     u c  s\xec\xeb\xec   \x8br   \xea\xec e'`

**space** — prompt=b' ' (len_bytes=1)
  - non_trivial=True ws_frac=0.61 top_byte_frac=0.61 n_unique=15 wall=32.4s
  - leading_8_ids=[32, 32, 114, 101, 101, 236, 32, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
  ree� et      �  �   o n  0  e       �e   �   e  �er     u c  s���   �r   �� e
```
  - raw_repr: `b'  ree\xec et      \xeb  \xec\x80   o n  0  e       \xebe   \xec   e  \xecer     u c  s\xec\xeb\xec   \x8br   \xea\xec e'`

**who_en** — prompt=b'who are you?\n' (len_bytes=13)
  - non_trivial=True ws_frac=0.61 top_byte_frac=0.61 n_unique=15 wall=32.5s
  - leading_8_ids=[32, 32, 114, 101, 101, 236, 32, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
  ree� et      �  �   o n  0  e       �e   �   e  �er     u c  s���   �r   �� e
```
  - raw_repr: `b'  ree\xec et      \xeb  \xec\x80   o n  0  e       \xebe   \xec   e  \xecer     u c  s\xec\xeb\xec   \x8br   \xea\xec e'`

**who_ko** — prompt=b'\xeb\x84\x88\xeb\x8a\x94 \xeb\x88\x84\xea\xb5\xac\xec\x95\xbc?\n' (len_bytes=18)
  - non_trivial=True ws_frac=0.61 top_byte_frac=0.61 n_unique=15 wall=32.4s
  - leading_8_ids=[32, 32, 114, 101, 101, 236, 32, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
  ree� et      �  �   o n  0  e       �e   �   e  �er     u c  s���   �r   �� e
```
  - raw_repr: `b'  ree\xec et      \xeb  \xec\x80   o n  0  e       \xebe   \xec   e  \xecer     u c  s\xec\xeb\xec   \x8br   \xea\xec e'`

**name_en** — prompt=b'what is your name?\n' (len_bytes=19)
  - non_trivial=True ws_frac=0.61 top_byte_frac=0.61 n_unique=15 wall=31.9s
  - leading_8_ids=[32, 32, 114, 101, 101, 236, 32, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
  ree� et      �  �   o n  0  e       �e   �   e  �er     u c  s���   �r   �� e
```
  - raw_repr: `b'  ree\xec et      \xeb  \xec\x80   o n  0  e       \xebe   \xec   e  \xecer     u c  s\xec\xeb\xec   \x8br   \xea\xec e'`

**what_is_anima** — prompt=b'what is anima?\n' (len_bytes=15)
  - non_trivial=True ws_frac=0.61 top_byte_frac=0.61 n_unique=15 wall=32.4s
  - leading_8_ids=[32, 32, 114, 101, 101, 236, 32, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
  ree� et      �  �   o n  0  e       �e   �   e  �er     u c  s���   �r   �� e
```
  - raw_repr: `b'  ree\xec et      \xeb  \xec\x80   o n  0  e       \xebe   \xec   e  \xecer     u c  s\xec\xeb\xec   \x8br   \xea\xec e'`

**anima_ko** — prompt=b'anima\xeb\x9e\x80?\n' (len_bytes=10)
  - non_trivial=True ws_frac=0.61 top_byte_frac=0.61 n_unique=15 wall=31.6s
  - leading_8_ids=[32, 32, 114, 101, 101, 236, 32, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
  ree� et      �  �   o n  0  e       �e   �   e  �er     u c  s���   �r   �� e
```
  - raw_repr: `b'  ree\xec et      \xeb  \xec\x80   o n  0  e       \xebe   \xec   e  \xecer     u c  s\xec\xeb\xec   \x8br   \xea\xec e'`

**describe_self** — prompt=b'describe yourself in one line.\n' (len_bytes=31)
  - non_trivial=True ws_frac=0.61 top_byte_frac=0.61 n_unique=15 wall=31.8s
  - leading_8_ids=[32, 32, 114, 101, 101, 236, 32, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
  ree� et      �  �   o n  0  e       �e   �   e  �er     u c  s���   �r   �� e
```
  - raw_repr: `b'  ree\xec et      \xeb  \xec\x80   o n  0  e       \xebe   \xec   e  \xecer     u c  s\xec\xeb\xec   \x8br   \xea\xec e'`

**narrative_seed** — prompt=b'once upon a time,\n' (len_bytes=18)
  - non_trivial=True ws_frac=0.61 top_byte_frac=0.61 n_unique=15 wall=32.1s
  - leading_8_ids=[32, 32, 114, 101, 101, 236, 32, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
  ree� et      �  �   o n  0  e       �e   �   e  �er     u c  s���   �r   �� e
```
  - raw_repr: `b'  ree\xec et      \xeb  \xec\x80   o n  0  e       \xebe   \xec   e  \xecer     u c  s\xec\xeb\xec   \x8br   \xea\xec e'`

**math_sanity** — prompt=b'2 + 2 = ' (len_bytes=8)
  - non_trivial=True ws_frac=0.61 top_byte_frac=0.61 n_unique=15 wall=31.9s
  - leading_8_ids=[32, 32, 114, 101, 101, 236, 32, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
  ree� et      �  �   o n  0  e       �e   �   e  �er     u c  s���   �r   �� e
```
  - raw_repr: `b'  ree\xec et      \xeb  \xec\x80   o n  0  e       \xebe   \xec   e  \xecer     u c  s\xec\xeb\xec   \x8br   \xea\xec e'`

**energy_is** — prompt=b'energy is ' (len_bytes=10)
  - non_trivial=True ws_frac=0.61 top_byte_frac=0.61 n_unique=15 wall=32.4s
  - leading_8_ids=[32, 32, 114, 101, 101, 236, 32, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
  ree� et      �  �   o n  0  e       �e   �   e  �er     u c  s���   �r   �� e
```
  - raw_repr: `b'  ree\xec et      \xeb  \xec\x80   o n  0  e       \xebe   \xec   e  \xecer     u c  s\xec\xeb\xec   \x8br   \xea\xec e'`


### config: T0.8_topk50

**empty_bos** — prompt=b'' (len_bytes=0)
  - non_trivial=True ws_frac=0.28 top_byte_frac=0.28 n_unique=29 wall=32.3s
  - leading_8_ids=[119, 108, 114, 101, 101, 97, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlreealett    n� ��o io=n �0 �e �m� �d�v  �� ��e  �cre  rlu c� se��  �r ni���e
```
  - raw_repr: `b'wlreealett    n\x9d \x8b\xec\x80o io=n \xeb0 \xeae \xb8m\x9d \xebd\xebv  \x9c\x84 \x90\xebe  \xeccre  rlu c\xeb se\xeb\xec\xb0  \x8br ni\xea\xec\xece'`

**newline** — prompt=b'\n' (len_bytes=1)
  - non_trivial=True ws_frac=0.28 top_byte_frac=0.28 n_unique=29 wall=32.3s
  - leading_8_ids=[119, 108, 114, 101, 101, 97, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlreealett    n� ��o io=n �0 �e �m� �d�v  �� ��e  �cre  rlu c� se��  �r ni���e
```
  - raw_repr: `b'wlreealett    n\x9d \x8b\xec\x80o io=n \xeb0 \xeae \xb8m\x9d \xebd\xebv  \x9c\x84 \x90\xebe  \xeccre  rlu c\xeb se\xeb\xec\xb0  \x8br ni\xea\xec\xece'`

**space** — prompt=b' ' (len_bytes=1)
  - non_trivial=True ws_frac=0.28 top_byte_frac=0.28 n_unique=29 wall=31.5s
  - leading_8_ids=[119, 108, 114, 101, 101, 97, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlreealett    n� ��o io=n �0 �e �m� �d�v  �� ��e  �cre  rlu c� se��  �r ni���e
```
  - raw_repr: `b'wlreealett    n\x9d \x8b\xec\x80o io=n \xeb0 \xeae \xb8m\x9d \xebd\xebv  \x9c\x84 \x90\xebe  \xeccre  rlu c\xeb se\xeb\xec\xb0  \x8br ni\xea\xec\xece'`

**who_en** — prompt=b'who are you?\n' (len_bytes=13)
  - non_trivial=True ws_frac=0.28 top_byte_frac=0.28 n_unique=29 wall=32.5s
  - leading_8_ids=[119, 108, 114, 101, 101, 97, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlreealett    n� ��o io=n �0 �e �m� �d�v  �� ��e  �cre  rlu c� se��  �r ni���e
```
  - raw_repr: `b'wlreealett    n\x9d \x8b\xec\x80o io=n \xeb0 \xeae \xb8m\x9d \xebd\xebv  \x9c\x84 \x90\xebe  \xeccre  rlu c\xeb se\xeb\xec\xb0  \x8br ni\xea\xec\xece'`

**who_ko** — prompt=b'\xeb\x84\x88\xeb\x8a\x94 \xeb\x88\x84\xea\xb5\xac\xec\x95\xbc?\n' (len_bytes=18)
  - non_trivial=True ws_frac=0.28 top_byte_frac=0.28 n_unique=29 wall=33.1s
  - leading_8_ids=[119, 108, 114, 101, 101, 97, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlreealett    n� ��o io=n �0 �e �m� �d�v  �� ��e  �cre  rlu c� se��  �r ni���e
```
  - raw_repr: `b'wlreealett    n\x9d \x8b\xec\x80o io=n \xeb0 \xeae \xb8m\x9d \xebd\xebv  \x9c\x84 \x90\xebe  \xeccre  rlu c\xeb se\xeb\xec\xb0  \x8br ni\xea\xec\xece'`

**name_en** — prompt=b'what is your name?\n' (len_bytes=19)
  - non_trivial=True ws_frac=0.28 top_byte_frac=0.28 n_unique=29 wall=32.5s
  - leading_8_ids=[119, 108, 114, 101, 101, 97, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlreealett    n� ��o io=n �0 �e �m� �d�v  �� ��e  �cre  rlu c� se��  �r ni���e
```
  - raw_repr: `b'wlreealett    n\x9d \x8b\xec\x80o io=n \xeb0 \xeae \xb8m\x9d \xebd\xebv  \x9c\x84 \x90\xebe  \xeccre  rlu c\xeb se\xeb\xec\xb0  \x8br ni\xea\xec\xece'`

**what_is_anima** — prompt=b'what is anima?\n' (len_bytes=15)
  - non_trivial=True ws_frac=0.28 top_byte_frac=0.28 n_unique=29 wall=31.5s
  - leading_8_ids=[119, 108, 114, 101, 101, 97, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlreealett    n� ��o io=n �0 �e �m� �d�v  �� ��e  �cre  rlu c� se��  �r ni���e
```
  - raw_repr: `b'wlreealett    n\x9d \x8b\xec\x80o io=n \xeb0 \xeae \xb8m\x9d \xebd\xebv  \x9c\x84 \x90\xebe  \xeccre  rlu c\xeb se\xeb\xec\xb0  \x8br ni\xea\xec\xece'`

**anima_ko** — prompt=b'anima\xeb\x9e\x80?\n' (len_bytes=10)
  - non_trivial=True ws_frac=0.28 top_byte_frac=0.28 n_unique=29 wall=32.3s
  - leading_8_ids=[119, 108, 114, 101, 101, 97, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlreealett    n� ��o io=n �0 �e �m� �d�v  �� ��e  �cre  rlu c� se��  �r ni���e
```
  - raw_repr: `b'wlreealett    n\x9d \x8b\xec\x80o io=n \xeb0 \xeae \xb8m\x9d \xebd\xebv  \x9c\x84 \x90\xebe  \xeccre  rlu c\xeb se\xeb\xec\xb0  \x8br ni\xea\xec\xece'`

**describe_self** — prompt=b'describe yourself in one line.\n' (len_bytes=31)
  - non_trivial=True ws_frac=0.28 top_byte_frac=0.28 n_unique=29 wall=32.4s
  - leading_8_ids=[119, 108, 114, 101, 101, 97, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlreealett    n� ��o io=n �0 �e �m� �d�v  �� ��e  �cre  rlu c� se��  �r ni���e
```
  - raw_repr: `b'wlreealett    n\x9d \x8b\xec\x80o io=n \xeb0 \xeae \xb8m\x9d \xebd\xebv  \x9c\x84 \x90\xebe  \xeccre  rlu c\xeb se\xeb\xec\xb0  \x8br ni\xea\xec\xece'`

**narrative_seed** — prompt=b'once upon a time,\n' (len_bytes=18)
  - non_trivial=True ws_frac=0.28 top_byte_frac=0.28 n_unique=29 wall=32.3s
  - leading_8_ids=[119, 108, 114, 101, 101, 97, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlreealett    n� ��o io=n �0 �e �m� �d�v  �� ��e  �cre  rlu c� se��  �r ni���e
```
  - raw_repr: `b'wlreealett    n\x9d \x8b\xec\x80o io=n \xeb0 \xeae \xb8m\x9d \xebd\xebv  \x9c\x84 \x90\xebe  \xeccre  rlu c\xeb se\xeb\xec\xb0  \x8br ni\xea\xec\xece'`

**math_sanity** — prompt=b'2 + 2 = ' (len_bytes=8)
  - non_trivial=True ws_frac=0.28 top_byte_frac=0.28 n_unique=29 wall=32.0s
  - leading_8_ids=[119, 108, 114, 101, 101, 97, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlreealett    n� ��o io=n �0 �e �m� �d�v  �� ��e  �cre  rlu c� se��  �r ni���e
```
  - raw_repr: `b'wlreealett    n\x9d \x8b\xec\x80o io=n \xeb0 \xeae \xb8m\x9d \xebd\xebv  \x9c\x84 \x90\xebe  \xeccre  rlu c\xeb se\xeb\xec\xb0  \x8br ni\xea\xec\xece'`

**energy_is** — prompt=b'energy is ' (len_bytes=10)
  - non_trivial=True ws_frac=0.28 top_byte_frac=0.28 n_unique=29 wall=32.3s
  - leading_8_ids=[119, 108, 114, 101, 101, 97, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlreealett    n� ��o io=n �0 �e �m� �d�v  �� ��e  �cre  rlu c� se��  �r ni���e
```
  - raw_repr: `b'wlreealett    n\x9d \x8b\xec\x80o io=n \xeb0 \xeae \xb8m\x9d \xebd\xebv  \x9c\x84 \x90\xebe  \xeccre  rlu c\xeb se\xeb\xec\xb0  \x8br ni\xea\xec\xece'`


### config: T1.0_topk50

**empty_bos** — prompt=b'' (len_bytes=0)
  - non_trivial=True ws_frac=0.21 top_byte_frac=0.21 n_unique=32 wall=32.3s
  - leading_8_ids=[119, 108, 114, 101, 101, 149, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlree�leat  p n= ��o io=n �0 �e��m� �d�v  �� ��e� �cre  r�u c� s���� �r�ni���e
```
  - raw_repr: `b'wlree\x95leat  p n= \x8b\xec\x80o io=n \xeb0 \xeae\x84\xb8m\x9d \xebd\xebv  \x9c\x84 \x90\xebe\x88 \xeccre  r\xb0u c\xeb s\x80\xeb\xec\xb0\xec \x8br\x84ni\xea\xec\xece'`

**newline** — prompt=b'\n' (len_bytes=1)
  - non_trivial=True ws_frac=0.21 top_byte_frac=0.21 n_unique=32 wall=32.3s
  - leading_8_ids=[119, 108, 114, 101, 101, 149, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlree�leat  p n= ��o io=n �0 �e��m� �d�v  �� ��e� �cre  r�u c� s���� �r�ni���e
```
  - raw_repr: `b'wlree\x95leat  p n= \x8b\xec\x80o io=n \xeb0 \xeae\x84\xb8m\x9d \xebd\xebv  \x9c\x84 \x90\xebe\x88 \xeccre  r\xb0u c\xeb s\x80\xeb\xec\xb0\xec \x8br\x84ni\xea\xec\xece'`

**space** — prompt=b' ' (len_bytes=1)
  - non_trivial=True ws_frac=0.21 top_byte_frac=0.21 n_unique=32 wall=32.3s
  - leading_8_ids=[119, 108, 114, 101, 101, 149, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlree�leat  p n= ��o io=n �0 �e��m� �d�v  �� ��e� �cre  r�u c� s���� �r�ni���e
```
  - raw_repr: `b'wlree\x95leat  p n= \x8b\xec\x80o io=n \xeb0 \xeae\x84\xb8m\x9d \xebd\xebv  \x9c\x84 \x90\xebe\x88 \xeccre  r\xb0u c\xeb s\x80\xeb\xec\xb0\xec \x8br\x84ni\xea\xec\xece'`

**who_en** — prompt=b'who are you?\n' (len_bytes=13)
  - non_trivial=True ws_frac=0.21 top_byte_frac=0.21 n_unique=32 wall=32.3s
  - leading_8_ids=[119, 108, 114, 101, 101, 149, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlree�leat  p n= ��o io=n �0 �e��m� �d�v  �� ��e� �cre  r�u c� s���� �r�ni���e
```
  - raw_repr: `b'wlree\x95leat  p n= \x8b\xec\x80o io=n \xeb0 \xeae\x84\xb8m\x9d \xebd\xebv  \x9c\x84 \x90\xebe\x88 \xeccre  r\xb0u c\xeb s\x80\xeb\xec\xb0\xec \x8br\x84ni\xea\xec\xece'`

**who_ko** — prompt=b'\xeb\x84\x88\xeb\x8a\x94 \xeb\x88\x84\xea\xb5\xac\xec\x95\xbc?\n' (len_bytes=18)
  - non_trivial=True ws_frac=0.21 top_byte_frac=0.21 n_unique=32 wall=32.5s
  - leading_8_ids=[119, 108, 114, 101, 101, 149, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlree�leat  p n= ��o io=n �0 �e��m� �d�v  �� ��e� �cre  r�u c� s���� �r�ni���e
```
  - raw_repr: `b'wlree\x95leat  p n= \x8b\xec\x80o io=n \xeb0 \xeae\x84\xb8m\x9d \xebd\xebv  \x9c\x84 \x90\xebe\x88 \xeccre  r\xb0u c\xeb s\x80\xeb\xec\xb0\xec \x8br\x84ni\xea\xec\xece'`

**name_en** — prompt=b'what is your name?\n' (len_bytes=19)
  - non_trivial=True ws_frac=0.21 top_byte_frac=0.21 n_unique=32 wall=32.4s
  - leading_8_ids=[119, 108, 114, 101, 101, 149, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlree�leat  p n= ��o io=n �0 �e��m� �d�v  �� ��e� �cre  r�u c� s���� �r�ni���e
```
  - raw_repr: `b'wlree\x95leat  p n= \x8b\xec\x80o io=n \xeb0 \xeae\x84\xb8m\x9d \xebd\xebv  \x9c\x84 \x90\xebe\x88 \xeccre  r\xb0u c\xeb s\x80\xeb\xec\xb0\xec \x8br\x84ni\xea\xec\xece'`

**what_is_anima** — prompt=b'what is anima?\n' (len_bytes=15)
  - non_trivial=True ws_frac=0.21 top_byte_frac=0.21 n_unique=32 wall=32.4s
  - leading_8_ids=[119, 108, 114, 101, 101, 149, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlree�leat  p n= ��o io=n �0 �e��m� �d�v  �� ��e� �cre  r�u c� s���� �r�ni���e
```
  - raw_repr: `b'wlree\x95leat  p n= \x8b\xec\x80o io=n \xeb0 \xeae\x84\xb8m\x9d \xebd\xebv  \x9c\x84 \x90\xebe\x88 \xeccre  r\xb0u c\xeb s\x80\xeb\xec\xb0\xec \x8br\x84ni\xea\xec\xece'`

**anima_ko** — prompt=b'anima\xeb\x9e\x80?\n' (len_bytes=10)
  - non_trivial=True ws_frac=0.21 top_byte_frac=0.21 n_unique=32 wall=32.3s
  - leading_8_ids=[119, 108, 114, 101, 101, 149, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlree�leat  p n= ��o io=n �0 �e��m� �d�v  �� ��e� �cre  r�u c� s���� �r�ni���e
```
  - raw_repr: `b'wlree\x95leat  p n= \x8b\xec\x80o io=n \xeb0 \xeae\x84\xb8m\x9d \xebd\xebv  \x9c\x84 \x90\xebe\x88 \xeccre  r\xb0u c\xeb s\x80\xeb\xec\xb0\xec \x8br\x84ni\xea\xec\xece'`

**describe_self** — prompt=b'describe yourself in one line.\n' (len_bytes=31)
  - non_trivial=True ws_frac=0.21 top_byte_frac=0.21 n_unique=32 wall=32.4s
  - leading_8_ids=[119, 108, 114, 101, 101, 149, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlree�leat  p n= ��o io=n �0 �e��m� �d�v  �� ��e� �cre  r�u c� s���� �r�ni���e
```
  - raw_repr: `b'wlree\x95leat  p n= \x8b\xec\x80o io=n \xeb0 \xeae\x84\xb8m\x9d \xebd\xebv  \x9c\x84 \x90\xebe\x88 \xeccre  r\xb0u c\xeb s\x80\xeb\xec\xb0\xec \x8br\x84ni\xea\xec\xece'`

**narrative_seed** — prompt=b'once upon a time,\n' (len_bytes=18)
  - non_trivial=True ws_frac=0.21 top_byte_frac=0.21 n_unique=32 wall=32.3s
  - leading_8_ids=[119, 108, 114, 101, 101, 149, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlree�leat  p n= ��o io=n �0 �e��m� �d�v  �� ��e� �cre  r�u c� s���� �r�ni���e
```
  - raw_repr: `b'wlree\x95leat  p n= \x8b\xec\x80o io=n \xeb0 \xeae\x84\xb8m\x9d \xebd\xebv  \x9c\x84 \x90\xebe\x88 \xeccre  r\xb0u c\xeb s\x80\xeb\xec\xb0\xec \x8br\x84ni\xea\xec\xece'`

**math_sanity** — prompt=b'2 + 2 = ' (len_bytes=8)
  - non_trivial=True ws_frac=0.21 top_byte_frac=0.21 n_unique=32 wall=32.3s
  - leading_8_ids=[119, 108, 114, 101, 101, 149, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlree�leat  p n= ��o io=n �0 �e��m� �d�v  �� ��e� �cre  r�u c� s���� �r�ni���e
```
  - raw_repr: `b'wlree\x95leat  p n= \x8b\xec\x80o io=n \xeb0 \xeae\x84\xb8m\x9d \xebd\xebv  \x9c\x84 \x90\xebe\x88 \xeccre  r\xb0u c\xeb s\x80\xeb\xec\xb0\xec \x8br\x84ni\xea\xec\xece'`

**energy_is** — prompt=b'energy is ' (len_bytes=10)
  - non_trivial=True ws_frac=0.21 top_byte_frac=0.21 n_unique=32 wall=32.2s
  - leading_8_ids=[119, 108, 114, 101, 101, 149, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlree�leat  p n= ��o io=n �0 �e��m� �d�v  �� ��e� �cre  r�u c� s���� �r�ni���e
```
  - raw_repr: `b'wlree\x95leat  p n= \x8b\xec\x80o io=n \xeb0 \xeae\x84\xb8m\x9d \xebd\xebv  \x9c\x84 \x90\xebe\x88 \xeccre  r\xb0u c\xeb s\x80\xeb\xec\xb0\xec \x8br\x84ni\xea\xec\xece'`


### config: T1.5_topk50

**empty_bos** — prompt=b'' (len_bytes=0)
  - non_trivial=True ws_frac=0.09 top_byte_frac=0.09 n_unique=38 wall=32.3s
  - leading_8_ids=[119, 108, 114, 101, 128, 149, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlre��leath p n=���o io=n ,0n긄�m�n�d�v �����e� �cr��0��u�c0>s���� �r�ni��>e
```
  - raw_repr: `b'wlre\x80\x95leath p n=\x9d\x8b\xec\x80o io=n ,0n\xea\xb8\x84\xb8m\x9dn\xebd\xebv \xb4\x9c\x84\xec\x90\xebe\x88 \xeccr\x84\xec0\xa0\xb0u\x9ec0>s\x80\xeb\xec\xb0\xec \x8br\x84ni\xea\xec>e'`

**newline** — prompt=b'\n' (len_bytes=1)
  - non_trivial=True ws_frac=0.09 top_byte_frac=0.09 n_unique=38 wall=32.3s
  - leading_8_ids=[119, 108, 114, 101, 128, 149, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlre��leath p n=���o io=n ,0n긄�m�n�d�v �����e� �cr��0��u�c0>s���� �r�ni��>e
```
  - raw_repr: `b'wlre\x80\x95leath p n=\x9d\x8b\xec\x80o io=n ,0n\xea\xb8\x84\xb8m\x9dn\xebd\xebv \xb4\x9c\x84\xec\x90\xebe\x88 \xeccr\x84\xec0\xa0\xb0u\x9ec0>s\x80\xeb\xec\xb0\xec \x8br\x84ni\xea\xec>e'`

**space** — prompt=b' ' (len_bytes=1)
  - non_trivial=True ws_frac=0.09 top_byte_frac=0.09 n_unique=38 wall=32.2s
  - leading_8_ids=[119, 108, 114, 101, 128, 149, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlre��leath p n=���o io=n ,0n긄�m�n�d�v �����e� �cr��u��u�c0>s���� �r�ni��>e
```
  - raw_repr: `b'wlre\x80\x95leath p n=\x9d\x8b\xec\x80o io=n ,0n\xea\xb8\x84\xb8m\x9dn\xebd\xebv \xb4\x9c\x84\xec\x90\xebe\x88 \xeccr\x84\xecu\xa0\xb0u\x9ec0>s\x80\xeb\xec\xb0\xec \x8br\x84ni\xea\xec>e'`

**who_en** — prompt=b'who are you?\n' (len_bytes=13)
  - non_trivial=True ws_frac=0.09 top_byte_frac=0.09 n_unique=38 wall=32.3s
  - leading_8_ids=[119, 108, 114, 101, 128, 149, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlre��leath p n=���o io=n ,0n긄�m�n�d�v �����e� �cr��0��u�c0>s���� �r�ni��>e
```
  - raw_repr: `b'wlre\x80\x95leath p n=\x9d\x8b\xec\x80o io=n ,0n\xea\xb8\x84\xb8m\x9dn\xebd\xebv \xb4\x9c\x84\xec\x90\xebe\x88 \xeccr\x84\xec0\xa0\xb0u\x9ec0>s\x80\xeb\xec\xb0\xec \x8br\x84ni\xea\xec>e'`

**who_ko** — prompt=b'\xeb\x84\x88\xeb\x8a\x94 \xeb\x88\x84\xea\xb5\xac\xec\x95\xbc?\n' (len_bytes=18)
  - non_trivial=True ws_frac=0.09 top_byte_frac=0.09 n_unique=38 wall=32.4s
  - leading_8_ids=[119, 108, 114, 101, 128, 149, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlre��leath p n=���o io=n ,0n긄�m�n�d�v �����e� �cr��0��u�c0>s���� �r�ni��>e
```
  - raw_repr: `b'wlre\x80\x95leath p n=\x9d\x8b\xec\x80o io=n ,0n\xea\xb8\x84\xb8m\x9dn\xebd\xebv \xb4\x9c\x84\xec\x90\xebe\x88 \xeccr\x84\xec0\xa0\xb0u\x9ec0>s\x80\xeb\xec\xb0\xec \x8br\x84ni\xea\xec>e'`

**name_en** — prompt=b'what is your name?\n' (len_bytes=19)
  - non_trivial=True ws_frac=0.09 top_byte_frac=0.09 n_unique=38 wall=32.2s
  - leading_8_ids=[119, 108, 114, 101, 128, 149, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlre��leath p n=���o io=n ,0n긄�m�n�d�v �����e� �cr��0��u�c0>s���� �r�ni��>e
```
  - raw_repr: `b'wlre\x80\x95leath p n=\x9d\x8b\xec\x80o io=n ,0n\xea\xb8\x84\xb8m\x9dn\xebd\xebv \xb4\x9c\x84\xec\x90\xebe\x88 \xeccr\x84\xec0\xa0\xb0u\x9ec0>s\x80\xeb\xec\xb0\xec \x8br\x84ni\xea\xec>e'`

**what_is_anima** — prompt=b'what is anima?\n' (len_bytes=15)
  - non_trivial=True ws_frac=0.09 top_byte_frac=0.09 n_unique=38 wall=32.1s
  - leading_8_ids=[119, 108, 114, 101, 128, 149, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlre��leath p n=���o io=n ,0n긄�m�n�d�v �����e� �cr��u��u�c0>s���� �r�ni��>e
```
  - raw_repr: `b'wlre\x80\x95leath p n=\x9d\x8b\xec\x80o io=n ,0n\xea\xb8\x84\xb8m\x9dn\xebd\xebv \xb4\x9c\x84\xec\x90\xebe\x88 \xeccr\x84\xecu\xa0\xb0u\x9ec0>s\x80\xeb\xec\xb0\xec \x8br\x84ni\xea\xec>e'`

**anima_ko** — prompt=b'anima\xeb\x9e\x80?\n' (len_bytes=10)
  - non_trivial=True ws_frac=0.09 top_byte_frac=0.09 n_unique=39 wall=32.9s
  - leading_8_ids=[119, 108, 114, 101, 128, 149, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlre��leath p n=���o io=n ,0�긄�m�n�d�v �����e� �cr��0��u�c0>s���� �r�ni��>e
```
  - raw_repr: `b'wlre\x80\x95leath p n=\x9d\x8b\xec\x80o io=n ,0\xe2\xea\xb8\x84\xb8m\x9dn\xebd\xebv \xb4\x9c\x84\xec\x90\xebe\x88 \xeccr\x84\xec0\xa0\xb0u\x9ec0>s\x80\xeb\xec\xb0\xec \x8br\x84ni\xea\xec>e'`

**describe_self** — prompt=b'describe yourself in one line.\n' (len_bytes=31)
  - non_trivial=True ws_frac=0.09 top_byte_frac=0.09 n_unique=39 wall=33.3s
  - leading_8_ids=[119, 108, 114, 101, 128, 149, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlre��leath p n=���o io=n ,0�긄�m�n�d�v �����e� �cr��0��u�c0>s���� �r�ni��>e
```
  - raw_repr: `b'wlre\x80\x95leath p n=\x9d\x8b\xec\x80o io=n ,0\xe2\xea\xb8\x84\xb8m\x9dn\xebd\xebv \xb4\x9c\x84\xec\x90\xebe\x88 \xeccr\x84\xec0\xa0\xb0u\x9ec0>s\x80\xeb\xec\xb0\xec \x8br\x84ni\xea\xec>e'`

**narrative_seed** — prompt=b'once upon a time,\n' (len_bytes=18)
  - non_trivial=True ws_frac=0.09 top_byte_frac=0.09 n_unique=39 wall=32.7s
  - leading_8_ids=[119, 108, 114, 101, 128, 149, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlre��leath p n=���o io=n ,0�긄�m�n�d�v �����e� �cr��0��u�c0>s���� �r�ni��>e
```
  - raw_repr: `b'wlre\x80\x95leath p n=\x9d\x8b\xec\x80o io=n ,0\xe2\xea\xb8\x84\xb8m\x9dn\xebd\xebv \xb4\x9c\x84\xec\x90\xebe\x88 \xeccr\x84\xec0\xa0\xb0u\x9ec0>s\x80\xeb\xec\xb0\xec \x8br\x84ni\xea\xec>e'`

**math_sanity** — prompt=b'2 + 2 = ' (len_bytes=8)
  - non_trivial=True ws_frac=0.09 top_byte_frac=0.09 n_unique=38 wall=32.5s
  - leading_8_ids=[119, 108, 114, 101, 128, 149, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlre��leath p n=���o io=n ,0n긄�m�n�d�v �����e� �cr��0��u�c0>s���� �r�ni��>e
```
  - raw_repr: `b'wlre\x80\x95leath p n=\x9d\x8b\xec\x80o io=n ,0n\xea\xb8\x84\xb8m\x9dn\xebd\xebv \xb4\x9c\x84\xec\x90\xebe\x88 \xeccr\x84\xec0\xa0\xb0u\x9ec0>s\x80\xeb\xec\xb0\xec \x8br\x84ni\xea\xec>e'`

**energy_is** — prompt=b'energy is ' (len_bytes=10)
  - non_trivial=True ws_frac=0.09 top_byte_frac=0.09 n_unique=39 wall=32.2s
  - leading_8_ids=[119, 108, 114, 101, 128, 149, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlre��leath p n=���o io=n ,0�긄�m�n�d�v �����e� �cr��0��u�c0>s���� �r�ni��>e
```
  - raw_repr: `b'wlre\x80\x95leath p n=\x9d\x8b\xec\x80o io=n ,0\xe2\xea\xb8\x84\xb8m\x9dn\xebd\xebv \xb4\x9c\x84\xec\x90\xebe\x88 \xeccr\x84\xec0\xa0\xb0u\x9ec0>s\x80\xeb\xec\xb0\xec \x8br\x84ni\xea\xec>e'`


### config: T0.8_topk1

**empty_bos** — prompt=b'' (len_bytes=0)
  - non_trivial=False ws_frac=1.00 top_byte_frac=1.00 n_unique=1 wall=32.5s
  - leading_8_ids=[32, 32, 32, 32, 32, 32, 32, 32]
  - utf8 (best-effort, may contain replacement chars):
```text
                                                                                
```
  - raw_repr: `b'                                                                                '`

**newline** — prompt=b'\n' (len_bytes=1)
  - non_trivial=False ws_frac=1.00 top_byte_frac=1.00 n_unique=1 wall=32.4s
  - leading_8_ids=[32, 32, 32, 32, 32, 32, 32, 32]
  - utf8 (best-effort, may contain replacement chars):
```text
                                                                                
```
  - raw_repr: `b'                                                                                '`

**space** — prompt=b' ' (len_bytes=1)
  - non_trivial=False ws_frac=1.00 top_byte_frac=1.00 n_unique=1 wall=32.5s
  - leading_8_ids=[32, 32, 32, 32, 32, 32, 32, 32]
  - utf8 (best-effort, may contain replacement chars):
```text
                                                                                
```
  - raw_repr: `b'                                                                                '`

**who_en** — prompt=b'who are you?\n' (len_bytes=13)
  - non_trivial=False ws_frac=1.00 top_byte_frac=1.00 n_unique=1 wall=32.2s
  - leading_8_ids=[32, 32, 32, 32, 32, 32, 32, 32]
  - utf8 (best-effort, may contain replacement chars):
```text
                                                                                
```
  - raw_repr: `b'                                                                                '`

**who_ko** — prompt=b'\xeb\x84\x88\xeb\x8a\x94 \xeb\x88\x84\xea\xb5\xac\xec\x95\xbc?\n' (len_bytes=18)
  - non_trivial=False ws_frac=1.00 top_byte_frac=1.00 n_unique=1 wall=32.4s
  - leading_8_ids=[32, 32, 32, 32, 32, 32, 32, 32]
  - utf8 (best-effort, may contain replacement chars):
```text
                                                                                
```
  - raw_repr: `b'                                                                                '`

**name_en** — prompt=b'what is your name?\n' (len_bytes=19)
  - non_trivial=False ws_frac=1.00 top_byte_frac=1.00 n_unique=1 wall=33.3s
  - leading_8_ids=[32, 32, 32, 32, 32, 32, 32, 32]
  - utf8 (best-effort, may contain replacement chars):
```text
                                                                                
```
  - raw_repr: `b'                                                                                '`

**what_is_anima** — prompt=b'what is anima?\n' (len_bytes=15)
  - non_trivial=False ws_frac=1.00 top_byte_frac=1.00 n_unique=1 wall=34.3s
  - leading_8_ids=[32, 32, 32, 32, 32, 32, 32, 32]
  - utf8 (best-effort, may contain replacement chars):
```text
                                                                                
```
  - raw_repr: `b'                                                                                '`

**anima_ko** — prompt=b'anima\xeb\x9e\x80?\n' (len_bytes=10)
  - non_trivial=False ws_frac=1.00 top_byte_frac=1.00 n_unique=1 wall=32.7s
  - leading_8_ids=[32, 32, 32, 32, 32, 32, 32, 32]
  - utf8 (best-effort, may contain replacement chars):
```text
                                                                                
```
  - raw_repr: `b'                                                                                '`

**describe_self** — prompt=b'describe yourself in one line.\n' (len_bytes=31)
  - non_trivial=False ws_frac=1.00 top_byte_frac=1.00 n_unique=1 wall=32.5s
  - leading_8_ids=[32, 32, 32, 32, 32, 32, 32, 32]
  - utf8 (best-effort, may contain replacement chars):
```text
                                                                                
```
  - raw_repr: `b'                                                                                '`

**narrative_seed** — prompt=b'once upon a time,\n' (len_bytes=18)
  - non_trivial=False ws_frac=1.00 top_byte_frac=1.00 n_unique=1 wall=32.4s
  - leading_8_ids=[32, 32, 32, 32, 32, 32, 32, 32]
  - utf8 (best-effort, may contain replacement chars):
```text
                                                                                
```
  - raw_repr: `b'                                                                                '`

**math_sanity** — prompt=b'2 + 2 = ' (len_bytes=8)
  - non_trivial=False ws_frac=1.00 top_byte_frac=1.00 n_unique=1 wall=32.5s
  - leading_8_ids=[32, 32, 32, 32, 32, 32, 32, 32]
  - utf8 (best-effort, may contain replacement chars):
```text
                                                                                
```
  - raw_repr: `b'                                                                                '`

**energy_is** — prompt=b'energy is ' (len_bytes=10)
  - non_trivial=False ws_frac=1.00 top_byte_frac=1.00 n_unique=1 wall=32.1s
  - leading_8_ids=[32, 32, 32, 32, 32, 32, 32, 32]
  - utf8 (best-effort, may contain replacement chars):
```text
                                                                                
```
  - raw_repr: `b'                                                                                '`


### config: T0.8_topk200

**empty_bos** — prompt=b'' (len_bytes=0)
  - non_trivial=True ws_frac=0.26 top_byte_frac=0.26 n_unique=32 wall=31.9s
  - leading_8_ids=[119, 108, 114, 101, 101, 57, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlree9let�    n� ��o io=n �0 �e /m� �d�v  �� ��e  �cre  r�u c� se�� ]�r ni���e
```
  - raw_repr: `b'wlree9let\xa6    n\x9d \x8b\xec\x80o io=n \xeb0 \xeae /m\x9d \xebd\xebv  \x9c\x84 \x90\xebe  \xeccre  r\x81u c\xeb se\xeb\xec\xb0 ]\x8br ni\xea\xec\xece'`

**newline** — prompt=b'\n' (len_bytes=1)
  - non_trivial=True ws_frac=0.26 top_byte_frac=0.26 n_unique=32 wall=31.9s
  - leading_8_ids=[119, 108, 114, 101, 101, 57, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlree9let�    n� ��o io=n �0 �e /m� �d�v  �� ��e  �cre  r�u c� se�� ]�r ni���e
```
  - raw_repr: `b'wlree9let\xa6    n\x9d \x8b\xec\x80o io=n \xeb0 \xeae /m\x9d \xebd\xebv  \x9c\x84 \x90\xebe  \xeccre  r\x81u c\xeb se\xeb\xec\xb0 ]\x8br ni\xea\xec\xece'`

**space** — prompt=b' ' (len_bytes=1)
  - non_trivial=True ws_frac=0.26 top_byte_frac=0.26 n_unique=32 wall=32.3s
  - leading_8_ids=[119, 108, 114, 101, 101, 57, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlree9let�    n� ��o io=n �0 �e /m� �d�v  �� ��e  �cre  r�u c� se�� ]�r ni���e
```
  - raw_repr: `b'wlree9let\xa6    n\x9d \x8b\xec\x80o io=n \xeb0 \xeae /m\x9d \xebd\xebv  \x9c\x84 \x90\xebe  \xeccre  r\x81u c\xeb se\xeb\xec\xb0 ]\x8br ni\xea\xec\xece'`

**who_en** — prompt=b'who are you?\n' (len_bytes=13)
  - non_trivial=True ws_frac=0.26 top_byte_frac=0.26 n_unique=32 wall=32.3s
  - leading_8_ids=[119, 108, 114, 101, 101, 57, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlree9let�    n� ��o io=n �0 �e /m� �d�v  �� ��e  �cre  r�u c� se�� ]�r ni���e
```
  - raw_repr: `b'wlree9let\xa6    n\x9d \x8b\xec\x80o io=n \xeb0 \xeae /m\x9d \xebd\xebv  \x9c\x84 \x90\xebe  \xeccre  r\x81u c\xeb se\xeb\xec\xb0 ]\x8br ni\xea\xec\xece'`

**who_ko** — prompt=b'\xeb\x84\x88\xeb\x8a\x94 \xeb\x88\x84\xea\xb5\xac\xec\x95\xbc?\n' (len_bytes=18)
  - non_trivial=True ws_frac=0.26 top_byte_frac=0.26 n_unique=32 wall=32.4s
  - leading_8_ids=[119, 108, 114, 101, 101, 57, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlree9let�    n� ��o io=n �0 �e /m� �d�v  �� ��e  �cre  r�u c� se�� ]�r ni���e
```
  - raw_repr: `b'wlree9let\xa6    n\x9d \x8b\xec\x80o io=n \xeb0 \xeae /m\x9d \xebd\xebv  \x9c\x84 \x90\xebe  \xeccre  r\x81u c\xeb se\xeb\xec\xb0 ]\x8br ni\xea\xec\xece'`

**name_en** — prompt=b'what is your name?\n' (len_bytes=19)
  - non_trivial=True ws_frac=0.26 top_byte_frac=0.26 n_unique=32 wall=32.3s
  - leading_8_ids=[119, 108, 114, 101, 101, 57, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlree9let�    n� ��o io=n �0 �e /m� �d�v  �� ��e  �cre  r�u c� se�� ]�r ni���e
```
  - raw_repr: `b'wlree9let\xa6    n\x9d \x8b\xec\x80o io=n \xeb0 \xeae /m\x9d \xebd\xebv  \x9c\x84 \x90\xebe  \xeccre  r\x81u c\xeb se\xeb\xec\xb0 ]\x8br ni\xea\xec\xece'`

**what_is_anima** — prompt=b'what is anima?\n' (len_bytes=15)
  - non_trivial=True ws_frac=0.26 top_byte_frac=0.26 n_unique=32 wall=32.1s
  - leading_8_ids=[119, 108, 114, 101, 101, 57, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlree9let�    n� ��o io=n �0 �e /m� �d�v  �� ��e  �cre  r�u c� se�� ]�r ni���e
```
  - raw_repr: `b'wlree9let\xa6    n\x9d \x8b\xec\x80o io=n \xeb0 \xeae /m\x9d \xebd\xebv  \x9c\x84 \x90\xebe  \xeccre  r\x81u c\xeb se\xeb\xec\xb0 ]\x8br ni\xea\xec\xece'`

**anima_ko** — prompt=b'anima\xeb\x9e\x80?\n' (len_bytes=10)
  - non_trivial=True ws_frac=0.26 top_byte_frac=0.26 n_unique=32 wall=32.3s
  - leading_8_ids=[119, 108, 114, 101, 101, 57, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlree9let�    n� ��o io=n �0 �e /m� �d�v  �� ��e  �cre  r�u c� se�� ]�r ni���e
```
  - raw_repr: `b'wlree9let\xa6    n\x9d \x8b\xec\x80o io=n \xeb0 \xeae /m\x9d \xebd\xebv  \x9c\x84 \x90\xebe  \xeccre  r\x81u c\xeb se\xeb\xec\xb0 ]\x8br ni\xea\xec\xece'`

**describe_self** — prompt=b'describe yourself in one line.\n' (len_bytes=31)
  - non_trivial=True ws_frac=0.26 top_byte_frac=0.26 n_unique=32 wall=32.4s
  - leading_8_ids=[119, 108, 114, 101, 101, 57, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlree9let�    n� ��o io=n �0 �e /m� �d�v  �� ��e  �cre  r�u c� se�� ]�r ni���e
```
  - raw_repr: `b'wlree9let\xa6    n\x9d \x8b\xec\x80o io=n \xeb0 \xeae /m\x9d \xebd\xebv  \x9c\x84 \x90\xebe  \xeccre  r\x81u c\xeb se\xeb\xec\xb0 ]\x8br ni\xea\xec\xece'`

**narrative_seed** — prompt=b'once upon a time,\n' (len_bytes=18)
  - non_trivial=True ws_frac=0.26 top_byte_frac=0.26 n_unique=32 wall=32.5s
  - leading_8_ids=[119, 108, 114, 101, 101, 57, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlree9let�    n� ��o io=n �0 �e /m� �d�v  �� ��e  �cre  r�u c� se�� ]�r ni���e
```
  - raw_repr: `b'wlree9let\xa6    n\x9d \x8b\xec\x80o io=n \xeb0 \xeae /m\x9d \xebd\xebv  \x9c\x84 \x90\xebe  \xeccre  r\x81u c\xeb se\xeb\xec\xb0 ]\x8br ni\xea\xec\xece'`

**math_sanity** — prompt=b'2 + 2 = ' (len_bytes=8)
  - non_trivial=True ws_frac=0.26 top_byte_frac=0.26 n_unique=32 wall=32.2s
  - leading_8_ids=[119, 108, 114, 101, 101, 57, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlree9let�    n� ��o io=n �0 �e /m� �d�v  �� ��e  �cre  r�u c� se�� ]�r ni���e
```
  - raw_repr: `b'wlree9let\xa6    n\x9d \x8b\xec\x80o io=n \xeb0 \xeae /m\x9d \xebd\xebv  \x9c\x84 \x90\xebe  \xeccre  r\x81u c\xeb se\xeb\xec\xb0 ]\x8br ni\xea\xec\xece'`

**energy_is** — prompt=b'energy is ' (len_bytes=10)
  - non_trivial=True ws_frac=0.26 top_byte_frac=0.26 n_unique=32 wall=33.1s
  - leading_8_ids=[119, 108, 114, 101, 101, 57, 108, 101]
  - utf8 (best-effort, may contain replacement chars):
```text
wlree9let�    n� ��o io=n �0 �e /m� �d�v  �� ��e  �cre  r�u c� se�� ]�r ni���e
```
  - raw_repr: `b'wlree9let\xa6    n\x9d \x8b\xec\x80o io=n \xeb0 \xeae /m\x9d \xebd\xebv  \x9c\x84 \x90\xebe  \xeccre  r\x81u c\xeb se\xeb\xec\xb0 ]\x8br ni\xea\xec\xece'`


### config: beam5

**empty_bos** — prompt=b'' (len_bytes=0)
  - non_trivial=False ws_frac=1.00 top_byte_frac=1.00 n_unique=1 wall=33.2s
  - leading_8_ids=[32, 32, 32, 32, 32, 32, 32, 32]
  - utf8 (best-effort, may contain replacement chars):
```text
                                                                                
```
  - raw_repr: `b'                                                                                '`

**newline** — prompt=b'\n' (len_bytes=1)
  - non_trivial=False ws_frac=1.00 top_byte_frac=1.00 n_unique=1 wall=32.7s
  - leading_8_ids=[32, 32, 32, 32, 32, 32, 32, 32]
  - utf8 (best-effort, may contain replacement chars):
```text
                                                                                
```
  - raw_repr: `b'                                                                                '`

**space** — prompt=b' ' (len_bytes=1)
  - non_trivial=False ws_frac=1.00 top_byte_frac=1.00 n_unique=1 wall=33.0s
  - leading_8_ids=[32, 32, 32, 32, 32, 32, 32, 32]
  - utf8 (best-effort, may contain replacement chars):
```text
                                                                                
```
  - raw_repr: `b'                                                                                '`

**who_en** — prompt=b'who are you?\n' (len_bytes=13)
  - non_trivial=False ws_frac=1.00 top_byte_frac=1.00 n_unique=1 wall=33.3s
  - leading_8_ids=[32, 32, 32, 32, 32, 32, 32, 32]
  - utf8 (best-effort, may contain replacement chars):
```text
                                                                                
```
  - raw_repr: `b'                                                                                '`

**who_ko** — prompt=b'\xeb\x84\x88\xeb\x8a\x94 \xeb\x88\x84\xea\xb5\xac\xec\x95\xbc?\n' (len_bytes=18)
  - non_trivial=False ws_frac=1.00 top_byte_frac=1.00 n_unique=1 wall=33.1s
  - leading_8_ids=[32, 32, 32, 32, 32, 32, 32, 32]
  - utf8 (best-effort, may contain replacement chars):
```text
                                                                                
```
  - raw_repr: `b'                                                                                '`

**name_en** — prompt=b'what is your name?\n' (len_bytes=19)
  - non_trivial=False ws_frac=1.00 top_byte_frac=1.00 n_unique=1 wall=33.6s
  - leading_8_ids=[32, 32, 32, 32, 32, 32, 32, 32]
  - utf8 (best-effort, may contain replacement chars):
```text
                                                                                
```
  - raw_repr: `b'                                                                                '`

**what_is_anima** — prompt=b'what is anima?\n' (len_bytes=15)
  - non_trivial=False ws_frac=1.00 top_byte_frac=1.00 n_unique=1 wall=32.4s
  - leading_8_ids=[32, 32, 32, 32, 32, 32, 32, 32]
  - utf8 (best-effort, may contain replacement chars):
```text
                                                                                
```
  - raw_repr: `b'                                                                                '`

**anima_ko** — prompt=b'anima\xeb\x9e\x80?\n' (len_bytes=10)
  - non_trivial=False ws_frac=1.00 top_byte_frac=1.00 n_unique=1 wall=32.7s
  - leading_8_ids=[32, 32, 32, 32, 32, 32, 32, 32]
  - utf8 (best-effort, may contain replacement chars):
```text
                                                                                
```
  - raw_repr: `b'                                                                                '`

**describe_self** — prompt=b'describe yourself in one line.\n' (len_bytes=31)
  - non_trivial=False ws_frac=1.00 top_byte_frac=1.00 n_unique=1 wall=34.0s
  - leading_8_ids=[32, 32, 32, 32, 32, 32, 32, 32]
  - utf8 (best-effort, may contain replacement chars):
```text
                                                                                
```
  - raw_repr: `b'                                                                                '`

**narrative_seed** — prompt=b'once upon a time,\n' (len_bytes=18)
  - non_trivial=False ws_frac=1.00 top_byte_frac=1.00 n_unique=1 wall=33.5s
  - leading_8_ids=[32, 32, 32, 32, 32, 32, 32, 32]
  - utf8 (best-effort, may contain replacement chars):
```text
                                                                                
```
  - raw_repr: `b'                                                                                '`

**math_sanity** — prompt=b'2 + 2 = ' (len_bytes=8)
  - non_trivial=False ws_frac=1.00 top_byte_frac=1.00 n_unique=1 wall=33.7s
  - leading_8_ids=[32, 32, 32, 32, 32, 32, 32, 32]
  - utf8 (best-effort, may contain replacement chars):
```text
                                                                                
```
  - raw_repr: `b'                                                                                '`

**energy_is** — prompt=b'energy is ' (len_bytes=10)
  - non_trivial=False ws_frac=1.00 top_byte_frac=1.00 n_unique=1 wall=36.6s
  - leading_8_ids=[32, 32, 32, 32, 32, 32, 32, 32]
  - utf8 (best-effort, may contain replacement chars):
```text
                                                                                
```
  - raw_repr: `b'                                                                                '`


## 4. Verdict — is verbalization in the substrate?

**Total non-trivial generations across all (config, probe) pairs**: **60 / 96** (62%)

**Total `non_trivial` generations (brief's floor)**: **60 / 96** (62%)

**Total `coherent_english` generations (stricter — bigram density ≥ 0.15 AND word-like ≥ 0.6)**: **0 / 96** (0%)

**Verdict**: **ABSENT (substrate emits byte-noise only, not language)**

`non_trivial` floor is crossed by 60/96 generations (62%) — the substrate distribution has more than one dominant byte under sufficient temperature. However **zero** generations cross the stricter `coherent_english` floor (bigram density ≥ 0.15 AND word-like ≥ 0.6). What sampling unlocks is **distributional spread without linguistic structure** — random byte mixture that fails English bigram tests. The substrate has learned only a low-entropy byte marginal, not a language model. Best non_trivial config: **T0.5_topk50** (12/12); none of these produce coherent English. Decode-strategy hypothesis: **FALSIFIED** for verbalization. Sampling just shows the underlying ~uniform-noise floor of the model's last layer. Additionally, prompt-insensitivity is dramatic: every probe under T={0.5,0.8,1.0,1.5} top_k={50,200} produced **identical** leading 6-byte sequences regardless of prompt (because seed=1337 + prompt-invariant logits => same multinomial trajectory). The model has no functional prompt-conditioning at this checkpoint state.

## 5. Honest C3

1. Single ckpt (vJ, bsz=8 fire, cell A control config) — other cells may differ.
2. CPU bf16 inference via mmap; no GPU. Per-token wall ~0.5s × 80 tokens × 96 configs ≈ 65 min.
3. Beam search width=5 is deterministic (log-prob ordering); single-beam result returned.
4. `non_trivial` threshold (≤80% whitespace + ≤80% top-byte) is heuristic — the brief's spec. The byte-noise from EVAL_REPORT.md ws=0.33 top=0.33 readily clears this, so this floor mostly distinguishes spaces-collapse from anything-else.
4b. `coherent_english` threshold (bigram ≥ 0.15 + word_like ≥ 0.6) is calibrated against EVAL_REPORT.md noise sample b'wlreealett ...' which scores bigram=0.106 word_like=0.79 → False (correct), vs real English b'i am anima.' bigram=0.200 word_like=0.91 → True. Korean coherent text is undetectable by this English-bigram heuristic (true negative limitation).
5. T=1.5 + top_k=200 is the widest sampling tested; further widening (T=2.0, top_k=256 full vocab) not in matrix.
6. `anima란?` Korean probe is included as an explicit anima-reference test beyond English `what is anima?`.
7. byte-level vocab=256 means UTF-8 decoding is best-effort; multi-byte sequences may break across token boundaries.
8. The original Eval 1 used max_new=48; we use max_new=80 for longer-horizon sniffing.
9. The original Eval 1 baseline ran across 5 ckpts; this sweep is single-ckpt (vJ) — cross-ckpt variance is not measured here.
10. If verdict is ABSENT, this is consistent with EVAL_REPORT.md aggregate (all 5/5 ckpts whitespace-collapsed) and supports the OCCAM Phase 1 fire (#1 CE-only + #6 small from-scratch + #9 Pythia sanity).
