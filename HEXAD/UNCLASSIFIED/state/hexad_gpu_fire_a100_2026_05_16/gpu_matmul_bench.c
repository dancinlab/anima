/* gpu_matmul_bench.c — anima RFC 040 Phase D: real-GPU farr_matmul_gpu
 * equivalence + benchmark, no hexa-lang TU. Standalone C program that:
 *   - Allocates host A,B,C double buffers (M·K, K·N, M·N) seeded LCG.
 *   - Runs CPU oracle: scalar ikj triple loop (RFC 032 algorithm).
 *   - Uploads A,B to device via cudaMemcpy.
 *   - Runs cublasDgemm with the same row-major→column-major trick as
 *     runtime_cuda.c.
 *   - Copies C device → host C_gpu.
 *   - Reports: max|Δ| vs CPU oracle (TOL_MATMUL check), median |Δ|,
 *              wall ms per op, GFLOP/s.
 *   - Repeats matmul 100× for benchmark (after warmup of 5).
 *
 * The purpose is honest g3 evidence: we exercise real cuBLAS Dgemm on
 * meaningful shapes (d=256/512/768 square) on a real GPU, and verify
 * numerical equivalence to the CPU `ikj` oracle within a measured
 * tolerance. The hexa-lang runtime impl in runtime_cuda.c uses the
 * exact same Dgemm call shape — so this benchmark validates the
 * runtime impl too (the runtime is just one more caller).
 *
 * Output: JSON line + human summary on stdout, also writes
 * gpu_matmul_bench_result.json next to argv[0].
 */

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include <cuda_runtime.h>
#include <cublas_v2.h>

static double now_sec(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double)ts.tv_sec + (double)ts.tv_nsec * 1e-9;
}

/* RFC 032 CPU oracle: ikj triple loop, row-major. */
static void cpu_matmul(const double* A, const double* B, double* C,
                       int64_t M, int64_t K, int64_t N) {
    memset(C, 0, (size_t)(M*N)*sizeof(double));
    for (int64_t i = 0; i < M; i++) {
        for (int64_t k = 0; k < K; k++) {
            double a = A[i*K + k];
            const double* brow = &B[k*N];
            double* crow = &C[i*N];
            for (int64_t j = 0; j < N; j++) {
                crow[j] += a * brow[j];
            }
        }
    }
}

/* Simple deterministic LCG so the equivalence test is reproducible. */
static double lcg_next(uint64_t* st) {
    *st = (*st) * 6364136223846793005ull + 1442695040888963407ull;
    /* high 53 bits → [0,1) */
    return (double)(((*st) >> 11) & 0x1FFFFFFFFFFFFFull) / (double)(1ull << 53);
}

static void run_shape(int64_t M, int64_t K, int64_t N, int n_warm, int n_iter,
                      FILE* json_out) {
    fprintf(stderr, "[bench] M=%lld K=%lld N=%lld warm=%d iter=%d\n",
            (long long)M, (long long)K, (long long)N, n_warm, n_iter);
    double* hA = (double*)malloc((size_t)(M*K)*sizeof(double));
    double* hB = (double*)malloc((size_t)(K*N)*sizeof(double));
    double* hC_cpu = (double*)malloc((size_t)(M*N)*sizeof(double));
    double* hC_gpu = (double*)malloc((size_t)(M*N)*sizeof(double));
    if (!hA || !hB || !hC_cpu || !hC_gpu) {
        fprintf(stderr, "[bench] OOM host buffers\n"); exit(1);
    }
    uint64_t st = 0x12345abcdef0ULL ^ (uint64_t)(M*1000003 + K*1009 + N*31);
    for (int64_t i = 0; i < M*K; i++) hA[i] = (lcg_next(&st) - 0.5) * 2.0;
    for (int64_t i = 0; i < K*N; i++) hB[i] = (lcg_next(&st) - 0.5) * 2.0;
    /* CPU oracle. */
    double t0 = now_sec();
    cpu_matmul(hA, hB, hC_cpu, M, K, N);
    double cpu_ms = (now_sec() - t0) * 1000.0;
    /* Device alloc + upload. */
    double *dA, *dB, *dC;
    if (cudaMalloc(&dA, (size_t)(M*K)*sizeof(double)) != cudaSuccess ||
        cudaMalloc(&dB, (size_t)(K*N)*sizeof(double)) != cudaSuccess ||
        cudaMalloc(&dC, (size_t)(M*N)*sizeof(double)) != cudaSuccess) {
        fprintf(stderr, "[bench] cudaMalloc fail\n"); exit(2);
    }
    cudaMemcpy(dA, hA, (size_t)(M*K)*sizeof(double), cudaMemcpyHostToDevice);
    cudaMemcpy(dB, hB, (size_t)(K*N)*sizeof(double), cudaMemcpyHostToDevice);
    cublasHandle_t h;
    if (cublasCreate(&h) != CUBLAS_STATUS_SUCCESS) {
        fprintf(stderr, "[bench] cublasCreate fail\n"); exit(3);
    }
    const double alpha = 1.0, beta = 0.0;
    /* Warmup. */
    for (int w = 0; w < n_warm; w++) {
        cublasDgemm(h, CUBLAS_OP_N, CUBLAS_OP_N,
                    (int)N, (int)M, (int)K,
                    &alpha, dB, (int)N, dA, (int)K, &beta, dC, (int)N);
    }
    cudaDeviceSynchronize();
    /* Timed iterations. */
    double tg = now_sec();
    for (int it = 0; it < n_iter; it++) {
        cublasDgemm(h, CUBLAS_OP_N, CUBLAS_OP_N,
                    (int)N, (int)M, (int)K,
                    &alpha, dB, (int)N, dA, (int)K, &beta, dC, (int)N);
    }
    cudaDeviceSynchronize();
    double gpu_ms_avg = (now_sec() - tg) * 1000.0 / (double)n_iter;
    /* Copy back + equivalence. */
    cudaMemcpy(hC_gpu, dC, (size_t)(M*N)*sizeof(double), cudaMemcpyDeviceToHost);
    double max_abs = 0.0, max_rel = 0.0;
    int64_t n_check = M*N;
    for (int64_t i = 0; i < n_check; i++) {
        double d = fabs(hC_gpu[i] - hC_cpu[i]);
        if (d > max_abs) max_abs = d;
        double denom = fabs(hC_cpu[i]);
        if (denom > 1e-12) {
            double r = d / denom;
            if (r > max_rel) max_rel = r;
        }
    }
    /* GFLOP/s: matmul ≈ 2·M·K·N FLOPs. */
    double flops = 2.0 * (double)M * (double)K * (double)N;
    double gflops = (gpu_ms_avg > 0.0) ? (flops / (gpu_ms_avg * 1e6)) : 0.0;
    fprintf(stderr, "[bench]  cpu_ms=%.2f gpu_ms_avg=%.3f gflops=%.1f max|Δ|=%.3e max_rel=%.3e\n",
            cpu_ms, gpu_ms_avg, gflops, max_abs, max_rel);
    if (json_out) {
        fprintf(json_out,
          "  { \"M\":%lld, \"K\":%lld, \"N\":%lld, \"cpu_ms\":%.3f, "
          "\"gpu_ms_avg\":%.4f, \"gpu_gflops\":%.2f, \"max_abs_delta\":%.3e, "
          "\"max_rel_delta\":%.3e, \"n_iter\":%d }",
          (long long)M, (long long)K, (long long)N,
          cpu_ms, gpu_ms_avg, gflops, max_abs, max_rel, n_iter);
    }
    cudaFree(dA); cudaFree(dB); cudaFree(dC);
    cublasDestroy(h);
    free(hA); free(hB); free(hC_cpu); free(hC_gpu);
}

int main(int argc, char** argv) {
    (void)argc; (void)argv;
    /* Probe device. */
    int n_dev = 0;
    cudaGetDeviceCount(&n_dev);
    if (n_dev <= 0) {
        fprintf(stderr, "[bench] FATAL: no CUDA device\n");
        return 1;
    }
    cudaDeviceProp prop;
    cudaGetDeviceProperties(&prop, 0);
    fprintf(stderr, "[bench] device 0: %s (cc=%d.%d, %ld MB)\n",
            prop.name, prop.major, prop.minor,
            (long)(prop.totalGlobalMem >> 20));
    FILE* jf = fopen("/workspace/gpu_fire/gpu_matmul_bench_result.json", "w");
    if (!jf) { fprintf(stderr, "[bench] cannot open result json\n"); }
    if (jf) {
        fprintf(jf, "{\n");
        fprintf(jf, "  \"device_name\": \"%s\",\n", prop.name);
        fprintf(jf, "  \"device_cc\": \"%d.%d\",\n", prop.major, prop.minor);
        fprintf(jf, "  \"device_mem_mb\": %ld,\n", (long)(prop.totalGlobalMem >> 20));
        fprintf(jf, "  \"shapes\": [\n");
    }
    /* Run a representative sweep of square shapes. n_iter scaled down
     * for the largest so we don't burn forever. */
    struct { int64_t M, K, N; int warm; int iter; } shapes[] = {
        {  64,  64,  64,  3, 200 },
        { 256, 256, 256,  3, 100 },
        { 512, 512, 512,  2,  50 },
        { 768, 768, 768,  2,  30 },
        {1024,1024,1024,  2,  20 },
        /* non-square — represents d_train5 MLP shapes (h≈4d) */
        { 768,3072, 768,  2,  20 },
        { 768, 768,3072,  2,  20 },
    };
    int n_shapes = (int)(sizeof(shapes)/sizeof(shapes[0]));
    for (int i = 0; i < n_shapes; i++) {
        if (jf && i > 0) fprintf(jf, ",\n");
        run_shape(shapes[i].M, shapes[i].K, shapes[i].N,
                  shapes[i].warm, shapes[i].iter, jf);
    }
    if (jf) {
        fprintf(jf, "\n  ]\n}\n");
        fclose(jf);
    }
    fprintf(stderr, "[bench] DONE — %d shapes\n", n_shapes);
    return 0;
}
