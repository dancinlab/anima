# v0.241.x hexa decode micro-bench — boxing/gemm/decode 실측

Pod: vast 41625379 (96 cores, 503GB RAM, RTX 5060 Ti, ssh7.vast.ai:25378) — torn down after bench.
hexa toolchain: **v0.241.10** (install.sh pulled latest; one patch newer than the v0.241.9 target — includes all v0.241.9 boxing/GEMM fixes; `read_f32_at` confirmed present in runtime.a).
ckpt: h1441_contrastive.bin (303M: vocab256/d1024/24L/16H/block512, 1.21GB) — md5 9147a6f9ad3e7081602702b2641d3a0d, **byte-verified** local==pod (no scp corruption).
Decoder: CORE/bytegpt_decode.hexa via state/1431_bind_compose/engine_decode_batch_cli.hexa (bg_load_ranged → _bg_rd_farr_at). prompt "The quick brown fox", gen N, top_k 8, temp 0.8.

## ★ BOXING (peak RSS) — the headline fix

| path | _bg_rd_farr_at impl | peak RSS | output |
|------|---------------------|----------|--------|
| baseline (boxing) | `read_bytes_at` slice → _bg_rd_farr (boxed-byte) | **26.18 GB** | "es a lower distance than this" |
| v0.241.x fixed | `read_f32_at` (direct f32→farr, no boxing) | **7.63 GB** | byte-IDENTICAL |

→ **26.18GB → 7.63GB = 3.4× RSS drop, byte-identical output.** read_f32_at compiles cleanly on v0.241.10 (the runtime-level unbox path is shipped). NOTE: the historical "79GB" figure was an earlier/worse loader variant; this 303M decode path's boxing peak measured here is 26GB (matches the 24-27GB documented in bytegpt_decode.hexa comments), dropping to 7.6GB with read_f32_at.

## ★ DECODE speed (single job)

| path | gen30 |
|------|-------|
| baseline (read_bytes_at) | 208 s |
| read_f32_at | 191 s |

≈ 6.4 s/token → gen110 ≈ ~700s/~12min (NOT separately measured — ssh dropped + coordinator stop signal). prior v0.241.8 gen30=230s. Decode is COMPUTE-bound (per-token GEMM), so the read_f32_at fix mainly helps the one-time LOAD RSS, not steady-state token rate.

## verdict
- boxing/farr32 unbox: **WORKS** (read_f32_at present + compiles + 3.4× RSS drop, byte-identical) — kills the load-RSS/OOM wall.
- decode速度: still ~6s/token scalar CPU GEMM — the 48min/frag wall is per-token compute, NOT load; BLIS/GEMM codegen gains (#3652 62-79% roofline, #3656 +20% epilogue-fusion) are compiled into matmul but single-job CPU decode is still minutes-scale. Faster decode needs the mm fast-path / GPU, not just the boxing fix.

## anima-side wiring note (ING)
CORE/bytegpt_decode.hexa `_bg_rd_farr_at` STILL ships the portable `read_bytes_at` path (kept for hosts whose hexa lacks read_f32_at). To capture the 3.4× RSS drop in anima's live decode, swap its body to `return read_f32_at(path, byte_off, n)` once the SSOT toolchain guarantees the builtin (byte-identical, verified max|Δ|=0 here). → ING follow-on.
