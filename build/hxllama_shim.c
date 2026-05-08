/* ───────────────────────────────────────────────────────────────────────────
 * build/hxllama_shim.c — anima Phase 3b libllama struct-by-value bypass shim
 *
 * PURPOSE
 *   hexa C FFI (stdlib/c_ffi) supports only flat int64/float64/ptr/str args.
 *   libllama exposes several APIs taking struct-by-value (llama_model_params,
 *   llama_context_params, llama_batch). This shim wraps each in a flat-arg
 *   form so anima/llama_ffi.hexa can declare straight `extern fn`.
 *
 * BUILD
 *   cc -O2 -shared -fPIC \
 *      -I${HOME}/.cache/anima/llama.cpp/include \
 *      -I${HOME}/.cache/anima/llama.cpp/ggml/include \
 *      build/hxllama_shim.c \
 *      ${HOME}/.cache/anima/llama.cpp/build/src/libllama.dylib \
 *      ${HOME}/.cache/anima/llama.cpp/build/ggml/src/libggml.dylib \
 *      -Wl,-rpath,${HOME}/.cache/anima/llama.cpp/build/src \
 *      -Wl,-rpath,${HOME}/.cache/anima/llama.cpp/build/ggml/src \
 *      -o build/libhxllama.dylib
 *
 * VERIFY
 *   nm -gU build/libhxllama.dylib | grep ' _hxllama_'
 *
 * SYMBOLS (flat-arg, hexa-callable)
 *   hxllama_backend_init / hxllama_backend_free
 *   hxllama_load_model(path, n_gpu_layers) -> model*
 *   hxllama_free_model(model)
 *   hxllama_new_context(model, n_ctx, n_threads) -> ctx*
 *   hxllama_free_context(ctx)
 *   hxllama_get_vocab(model) -> vocab*
 *   hxllama_n_vocab(vocab) -> int
 *   hxllama_n_ctx(ctx) -> int
 *   hxllama_n_embd(model) -> int                            (iter 4 c — Llama probe)
 *   hxllama_token_eos(vocab) -> int
 *   hxllama_token_bos(vocab) -> int
 *   hxllama_tokenize(vocab, text, tokens_out, max_tokens, add_bos) -> int
 *   hxllama_eval(ctx, tokens, n_tokens, n_past) -> int
 *   hxllama_sample_token(ctx, sampler) -> int
 *   hxllama_sampler_new_greedy() -> sampler*
 *   hxllama_sampler_new_temp(top_k, seed, temperature) -> sampler*  (iif pattern)
 *   hxllama_sampler_free(sampler)
 *   hxllama_token_to_text(vocab, token, buf_out, buf_size) -> int
 *   hxllama_memory_clear(ctx, data) -> void
 *   hxllama_get_logits_ith(ctx, idx) -> float*              (iter 4 c — Llama probe)
 *   hxllama_logits_at(logits_ptr, idx) -> double            (iter 4 c — read float as f64)
 *
 * DESIGN NOTES
 *   • All struct-by-value llama_*_params builders are folded INTO the shim's
 *     constructors (no need to expose params struct to hexa).
 *   • llama_batch is similarly hidden — hxllama_eval takes a flat (tokens, n)
 *     and constructs llama_batch_get_one() internally.
 *   • Sampler is a chain (greedy if temp<=0, else temp+top_p+top_k+dist).
 *   • token_to_text uses llama_token_to_piece() with lstrip=0, special=false.
 *   • All pointer returns are opaque void*; hexa treats them as int (uintptr_t).
 *
 * ABI SAFETY (per c_ffi.ai.md)
 *   ✓ All wrapper signatures use only: int (i64), float (f64 promoted from
 *     C float), const char* (str), void* (Ptr), void.
 *   ✗ No struct-by-value, no variadics, no callbacks.
 *
 * raw#9 disposition
 *   This is a build-infra C file (analogous to vendored runtime.c) — chat
 *   path .hexa-only invariant preserved (anima/llama_ffi.hexa is hexa, this
 *   shim is invoked only via @link symbol resolution at chat-time).
 * ─────────────────────────────────────────────────────────────────────────── */

#include "llama.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

/* ── backend lifecycle ────────────────────────────────────────────────── */

void hxllama_backend_init(void) {
    llama_backend_init();
}

void hxllama_backend_free(void) {
    llama_backend_free();
}

/* ── model load/free ──────────────────────────────────────────────────── */

/* Load model; n_gpu_layers < 0 means "all" (Metal default on macOS). */
void* hxllama_load_model(const char* path, int n_gpu_layers) {
    if (path == NULL) return NULL;
    struct llama_model_params mp = llama_model_default_params();
    mp.n_gpu_layers = n_gpu_layers;
    return (void*)llama_model_load_from_file(path, mp);
}

void hxllama_free_model(void* model) {
    if (model == NULL) return;
    llama_model_free((struct llama_model*)model);
}

/* ── context create/free ──────────────────────────────────────────────── */

/* If n_ctx == 0, use model default. n_threads <= 0 → libllama default. */
void* hxllama_new_context(void* model, int n_ctx, int n_threads) {
    if (model == NULL) return NULL;
    struct llama_context_params cp = llama_context_default_params();
    if (n_ctx > 0) {
        cp.n_ctx = (uint32_t)n_ctx;
    }
    if (n_threads > 0) {
        cp.n_threads       = n_threads;
        cp.n_threads_batch = n_threads;
    }
    return (void*)llama_init_from_model((struct llama_model*)model, cp);
}

void hxllama_free_context(void* ctx) {
    if (ctx == NULL) return;
    llama_free((struct llama_context*)ctx);
}

/* ── vocab access ─────────────────────────────────────────────────────── */

void* hxllama_get_vocab(void* model) {
    if (model == NULL) return NULL;
    return (void*)llama_model_get_vocab((const struct llama_model*)model);
}

int hxllama_n_vocab(void* vocab) {
    if (vocab == NULL) return 0;
    return (int)llama_vocab_n_tokens((const struct llama_vocab*)vocab);
}

int hxllama_n_ctx(void* ctx) {
    if (ctx == NULL) return 0;
    return (int)llama_n_ctx((const struct llama_context*)ctx);
}

/*
 * Model-side n_embd (hidden size). Useful for embedding-mode probe; for
 * Llama 3.2 3B this is 3072 (per GGUF kv). iter 4 (c) Llama probe path.
 */
int hxllama_n_embd(void* model) {
    if (model == NULL) return 0;
    return (int)llama_model_n_embd((const struct llama_model*)model);
}

int hxllama_token_eos(void* vocab) {
    if (vocab == NULL) return -1;
    return (int)llama_vocab_eos((const struct llama_vocab*)vocab);
}

int hxllama_token_bos(void* vocab) {
    if (vocab == NULL) return -1;
    return (int)llama_vocab_bos((const struct llama_vocab*)vocab);
}

/* ── tokenize / detokenize ────────────────────────────────────────────── */

/*
 * Tokenize text → tokens_out[0..max_tokens-1].
 * Returns n_tokens on success, negative on overflow (per llama_tokenize spec).
 * add_bos != 0 → prepend BOS if model is configured to.
 */
int hxllama_tokenize(void* vocab, const char* text, int* tokens_out,
                     int max_tokens, int add_bos) {
    if (vocab == NULL || text == NULL || tokens_out == NULL) return -1;
    int text_len = (int)strlen(text);
    return (int)llama_tokenize(
        (const struct llama_vocab*)vocab,
        text, text_len,
        (llama_token*)tokens_out,
        max_tokens,
        (bool)(add_bos != 0),
        /*parse_special=*/false);
}

/*
 * Convert a single token to UTF-8 bytes in buf_out[0..buf_size-1].
 * Returns n_bytes written (no NUL terminator from llama; we add one if room).
 * Negative return = overflow (− would-be-needed bytes).
 */
int hxllama_token_to_text(void* vocab, int token, char* buf_out, int buf_size) {
    if (vocab == NULL || buf_out == NULL || buf_size <= 0) return 0;
    int n = (int)llama_token_to_piece(
        (const struct llama_vocab*)vocab,
        (llama_token)token,
        buf_out,
        buf_size,
        /*lstrip=*/0,
        /*special=*/false);
    if (n > 0 && n < buf_size) {
        buf_out[n] = '\0';
    } else if (n >= buf_size) {
        buf_out[buf_size - 1] = '\0';
    } else if (n <= 0) {
        buf_out[0] = '\0';
    }
    return n;
}

/*
 * hxllama_token_to_text_static — convert one token, return a C string (char*).
 *
 * Hexa interp lacks a stdlib-level "raw bytes → string" primitive
 * (hexa_ptr_read_byte is native-only). To bridge, the shim owns a 4 KiB
 * static thread-unsafe buffer; each call overwrites it. The returned
 * char* points into this buffer and is valid until the next call.
 *
 * Hexa-side `extern fn ... -> str` views the char* as zero-copy UTF-8
 * (per c_ffi.ai.md ABI surface). For chat-loop use the result is copied
 * into a hexa string immediately via concat, so the lifetime is fine.
 *
 * NOT THREAD-SAFE. anima chat is single-threaded; if multi-threading is
 * added later, switch to thread-local or per-ctx storage.
 */
static __thread char _hxllama_text_static_buf[4096];

const char* hxllama_token_to_text_static(void* vocab, int token) {
    _hxllama_text_static_buf[0] = '\0';
    if (vocab == NULL) return _hxllama_text_static_buf;
    int n = (int)llama_token_to_piece(
        (const struct llama_vocab*)vocab,
        (llama_token)token,
        _hxllama_text_static_buf,
        (int)sizeof(_hxllama_text_static_buf) - 1,
        /*lstrip=*/0,
        /*special=*/false);
    if (n < 0) n = 0;
    if (n >= (int)sizeof(_hxllama_text_static_buf)) {
        n = (int)sizeof(_hxllama_text_static_buf) - 1;
    }
    _hxllama_text_static_buf[n] = '\0';
    return _hxllama_text_static_buf;
}

/* ── eval / decode ────────────────────────────────────────────────────── */

/*
 * Run llama_decode on a flat token array.
 * n_past: ignored (libllama tracks position automatically via memory state).
 *   Caller should call hxllama_memory_clear() before re-feeding a fresh
 *   prompt; n_past is kept in the signature for caller-side bookkeeping.
 * Returns 0 on success, non-zero on fail (matches llama_decode return).
 */
int hxllama_eval(void* ctx, const int* tokens, int n_tokens, int n_past) {
    if (ctx == NULL || tokens == NULL || n_tokens <= 0) return -1;
    (void)n_past;
    /* llama_batch_get_one signature: (llama_token* tokens, int32_t n_tokens). */
    struct llama_batch batch = llama_batch_get_one(
        (llama_token*)tokens, n_tokens);
    return (int)llama_decode((struct llama_context*)ctx, batch);
}

/* ── sampler chain (temp/top_p/top_k or greedy) ───────────────────────── */

/*
 * Build a sampler chain — flat-arg form (hexa FFI restriction: 4-arg
 * f-then-i mixed patterns are not wired in self/runtime.c host_ffi_call_6
 * (only iiif=p1 supported). So we expose two entry points:
 *
 *   hxllama_sampler_new_greedy()                           — pattern: (no args)
 *   hxllama_sampler_new_temp(top_k, seed, temperature)     — pattern: (i, i, f) p=1
 *
 * top_p is folded into a fixed 0.9 (the dancinlab/ paradigm-a-prime training
 * default; see general.sampling.top_p in the GGUF metadata). Phase 3c can
 * expose a knob if needed via a second flat-arg shim that doesn't hit the
 * 4-arg pattern wall.
 */

void* hxllama_sampler_new_greedy(void) {
    struct llama_sampler_chain_params sp = llama_sampler_chain_default_params();
    struct llama_sampler* chain = llama_sampler_chain_init(sp);
    if (chain == NULL) return NULL;
    llama_sampler_chain_add(chain, llama_sampler_init_greedy());
    return (void*)chain;
}

void* hxllama_sampler_new_temp(int top_k, int seed, double temperature) {
    struct llama_sampler_chain_params sp = llama_sampler_chain_default_params();
    struct llama_sampler* chain = llama_sampler_chain_init(sp);
    if (chain == NULL) return NULL;

    if (temperature <= 0.0) {
        llama_sampler_chain_add(chain, llama_sampler_init_greedy());
        return (void*)chain;
    }
    if (top_k > 0) {
        llama_sampler_chain_add(chain, llama_sampler_init_top_k(top_k));
    }
    /* Fixed top_p = 0.9 (paradigm-a-prime training default; see GGUF kv). */
    llama_sampler_chain_add(chain, llama_sampler_init_top_p(0.9f, 1));
    llama_sampler_chain_add(chain, llama_sampler_init_temp((float)temperature));
    llama_sampler_chain_add(chain, llama_sampler_init_dist((uint32_t)seed));
    return (void*)chain;
}

void hxllama_sampler_free(void* sampler) {
    if (sampler == NULL) return;
    llama_sampler_free((struct llama_sampler*)sampler);
}

/*
 * Sample one token from the most recent llama_decode logits.
 * idx = -1 → last position.
 */
int hxllama_sample_token(void* ctx, void* sampler) {
    if (ctx == NULL || sampler == NULL) return -1;
    return (int)llama_sampler_sample(
        (struct llama_sampler*)sampler,
        (struct llama_context*)ctx,
        /*idx=*/-1);
}

/* ── logits / hidden-state probe (iter 4 c — Llama real-mode) ──────────── */

/*
 * Get logits for the ith decoded position. -1 = last position. Returns
 * NULL on error. Caller treats return as void* (uintptr_t in hexa).
 *
 * NOTE: The float* points into libllama-owned memory and is valid until
 * the next llama_decode() call. Caller should read out values immediately
 * via hxllama_logits_at() rather than caching the pointer.
 */
void* hxllama_get_logits_ith(void* ctx, int idx) {
    if (ctx == NULL) return NULL;
    return (void*)llama_get_logits_ith((struct llama_context*)ctx, idx);
}

/*
 * Read a single float from a logits/embeddings buffer at element index `i`.
 * Promoted to double so the hexa FFI sees f64 (per c_ffi.ai.md ABI surface).
 *
 * Hexa interp deref_f32 builtin would also work, but going through this shim
 * keeps the read in-process with the libllama-owned buffer (no copy).
 */
double hxllama_logits_at(void* logits, int i) {
    if (logits == NULL) return 0.0;
    return (double)((const float*)logits)[i];
}

/* ── memory / KV cache ────────────────────────────────────────────────── */

void hxllama_memory_clear(void* ctx, int data_too) {
    if (ctx == NULL) return;
    llama_memory_t mem = llama_get_memory((const struct llama_context*)ctx);
    if (mem == NULL) return;
    llama_memory_clear(mem, (bool)(data_too != 0));
}

/* ── End of shim ──────────────────────────────────────────────────────── */
