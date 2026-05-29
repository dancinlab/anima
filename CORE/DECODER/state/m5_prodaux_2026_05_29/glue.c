/* glue.c — cuBLAS-engagement glue for M4b-fire-rev2 (hexa-lang #1671 local replica)
 *
 * runtime.c registers `cuda_available` → `hexa_cuda_available`, but only ships a
 * WEAK definition returning hexa_int(0). Under -DHEXA_CUDA the real CUDA impl
 * `_hx_cuda_runtime_available()` lives in runtime_cuda.o but nothing strong-binds
 * `hexa_cuda_available` to it, so cuBLAS Dgemm silently CPU-fallbacks.
 *
 * This TU provides STRONG (non-weak) definitions of `hexa_cuda_available` and
 * `hexa_cuda_device_count` that forward to the real CUDA runtime impls. At link
 * time the strong symbol overrides runtime.c's weak stub → mm() takes the GPU
 * path. Proven by CORE/DECODER/cublas_probe.hexa (cuda_available()==1 + cuBLAS
 * Dgemm byte-identical + GPU util/mem nonzero). Upstream fix = hexa-lang #1671.
 */
#include "runtime.h"

extern int _hx_cuda_runtime_available(void);
extern int _hx_cuda_device_count_impl(void);

/* STRONG override of the weak stub in runtime.c — defeats the 0-return. */
HexaVal hexa_cuda_available(void) {
    return hexa_int((int64_t)_hx_cuda_runtime_available());
}

HexaVal hexa_cuda_device_count(void) {
    return hexa_int((int64_t)_hx_cuda_device_count_impl());
}
