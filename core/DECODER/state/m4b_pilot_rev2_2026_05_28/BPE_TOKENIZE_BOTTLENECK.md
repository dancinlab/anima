# M4b-fire-rev2 — BPE tokenize O(N) bottleneck (honest surface · 2026-05-28)

sign-gate UNBLOCK 후 FIRE_BLOCKED.md 7-step 전부 실행 — transpile/corpus/pod/scp/build
모두 PASS. 발사 단계에서 **새로운 blocker** 발견: `flame_bpe_corpus_load` 의
corpus tokenization 이 real-scale diverse corpus 에서 사실상 종료 불가 (O(N_merges)
linear scan).

## 진행 완료 (전부 PASS)
- Mac transpile (sign window 내) — `hexa build --c-only` + `trim` sed patch ✅
- diverse corpus 재생성 — build_corpus_diverse_v2.hexa (2000 lines) ✅
- pod — RunPod H100 SXM 80GB `yfqcywjlxavmgr` ($3.29/hr, sm_90, GLIBC 2.35) ✅
- scp bundle — trainer.c + glue.c + runtime fragments + Qwen BPE + corpus ✅
- pod-side `dir_create` codegen-gap patch (신규 발견, trim 과 동종) ✅
- build — nvcc runtime_cuda.o + clang link (glue.c + `-lcuda`) RC=0, trainer 998KB ✅
- GPU preflight cudaMalloc smoke GPU_OK ✅

## blocker: BPE tokenize O(words × word_len² × N_merges)

`stdlib/flame/flame_bpe_corpus_lib.hexa` → `self/ml/tokenizer_bpe.hexa`:

- `bpe_encode` 가 corpus 전체를 word 단위로 `bpe_merge_word` 적용.
- `bpe_merge_word` (line ~338) 는 `while len(tokens) > 1` 루프 안에서 인접 pair
  마다 `get_merge_rank` 호출 → **per-word O(word_len² × N_merges)**.
- `get_merge_rank` (line 201) 는 `merge_ranks` 배열 (151,388 entries) 을 **매 호출
  linear scan** (`while i < n { if merge_ranks[i][0] == key ... }`). hash map 아님.
- `bpe_token_lookup` (line 402) 도 `tok.vocab` (151,643) linear scan per token.

→ 단어 1개 토크나이즈 ≈ 151,388 × word_len² 연산. Korean text 는 byte-level
char 가 syllable 당 3 byte-char (UTF-8) 라 word_len 폭증 → word_len² 항이 치명적.

### 실측
| corpus | lines | bytes | wall @ stall | 상태 |
|--------|-------|-------|--------------|------|
| diverse v2 full | 2000 | 1.2MB | 5+ min, out=227 | 미종료 |
| trim 120 | 120 | 38KB | 5.5+ min, out=227 | 미종료 |
| trim 24 | 24 | 6.6KB | (관측중) | — |

out_bytes=227 = 헤더 3줄만 flush, `bpe: V=...` (tokenize 완료 후 첫 print) 미도달.
CPU 100% 단일스레드 (work 진행중 = hang 아님, 단지 algorithmically intractable).

Phase 5a/5b 가 통과한 이유 = corpus 400 byte (~수십 word). real diverse corpus
(수천 word) 는 현재 encoder 로 불가.

## 정석 fix (a_completeness_over_cheap — corpus 축소 회피)

corpus 를 계속 줄이면 rev2 의 핵심 (diverse corpus = D3 #1269 root-cause fix) 가
훼손됨. 본선 = hexa-lang stdlib O(N) → O(1) 전환:

1. `merge_ranks` array-of-pairs → **dict/hashmap** (`#{key: rank}`). `get_merge_rank`
   O(151388) → O(1).
2. `tok.vocab` linear lookup → **dict** (`#{token_str: id}`). `bpe_token_lookup`
   O(151643) → O(1).
3. (선택) `bpe_merge_word` 의 pair-rescan → priority-queue / incremental min.

→ hexa-lang `stdlib/flame/` + `self/ml/tokenizer_bpe.hexa` 변경 + bootstrap rebuild.
a_runpod_inbox: hexa-lang INBOX.log.md 보고 대상.

## 신규 cross-backend codegen gap (별건, 이미 우회)
trainer.c 의 `hexa_call1(dir_create, X)` 가 Linux gen2 backend 에서 undeclared
(trim 과 동일 #1527 류). 우회 = `sed 's/hexa_call1(dir_create,/rt_fs_mkdir_p(/g'`.
hexa-lang INBOX 보고 대상.

## pod 상태
- pod `yfqcywjlxavmgr` 보존 (teardown 前 결론 미정 — tiny corpus 결과 대기).
- 미종료 시 teardown + 본 문서 = 다음 라운드 인계 (hexa-lang BPE O(1) fix 선결).
