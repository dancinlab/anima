/*
 * sgemm_ref_runeq_small.c — fast subset of sgemm_ref_runeq.c (16^3 cases
 * + an 8x12x20 non-square), used to verify the C reference side quickly
 * while the full 128^3 set is also available in sgemm_ref_runeq.c. Output
 * format matches sgemm_ref_native.hexa line-for-line. The hexa side of
 * this RUNEQ is currently BLOCKED by two hexa 0.1.0-dispatch toolchain
 * defects (see .verdicts/c-port/M3-sgemm_ref.txt + training/native/repro/).
 * Build:  cc -O2 -o sgemm_ref_runeq_small sgemm_ref_runeq_small.c -lm
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
static char* fmtf(float v){static char b[64];snprintf(b,sizeof(b),"%g",(double)v);return b;}
static void run_case(int M,int N,int K,int transA,int transB){
    int rowsA=transA?K:M,colsA=transA?M:K,rowsB=transB?N:K,colsB=transB?K:N;
    float *A=calloc(rowsA*colsA,sizeof(float)),*B=calloc(rowsB*colsB,sizeof(float)),*Cref=calloc(M*N,sizeof(float));
    for(int i=0;i<rowsA*colsA;i++)A[i]=0.02f*(float)((i*37)%131-65);
    for(int i=0;i<rowsB*colsB;i++)B[i]=0.02f*(float)((i*53)%127-63);
    for(int i=0;i<M;i++)for(int j=0;j<N;j++){float s=0.0f;
        for(int k=0;k<K;k++){float a=transA?A[k*M+i]:A[i*K+k];float b=transB?B[j*K+k]:B[k*N+j];s+=a*b;}
        Cref[i*N+j]=s;}
    float sum=0.0f,maxabs=0.0f;
    for(int idx=0;idx<M*N;idx++){float v=Cref[idx];sum+=v;float av=fabsf(v);if(av>maxabs)maxabs=av;}
    printf("[%dx%dx%d tA=%d tB=%d] sum=%s ",M,N,K,transA,transB,fmtf(sum));
    printf("maxabs=%s\n",fmtf(maxabs));
    free(A);free(B);free(Cref);
}
int main(void){
    run_case(16,16,16,0,0);run_case(16,16,16,1,0);run_case(16,16,16,0,1);run_case(16,16,16,1,1);
    run_case(8,12,20,0,0);run_case(8,12,20,1,1);
    printf("[sgemm_ref] DONE\n");return 0;
}
