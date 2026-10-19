/*
 * Independent exhaustive/exact-cardinality subset search for the LRSC v1.1.1
 * benchmark (M=99, k_idx=49, theta=0.08, A=0.50, 50 channels).
 *
 * This program is written from scratch and does NOT call, link against, or reuse
 * any code from the author's exhaustive_search.cpp / audit_k1_to_k10.py. It uses a
 * different enumeration technique: all size-K subsets of {0,...,49} are generated
 * as 64-bit bitmasks via Gosper's hack (a standard bit-trick for iterating combinations
 * in a bitmask representation), not via a recursive lexicographic index tree. For
 * each mask, set bits are extracted with __builtin_ctzll and the quadratic-form
 * objective  const + sum lin[i] + 2*sum_{i<j} gram[i][j]  is evaluated directly from
 * the coefficients written by build_operator.py.
 *
 * Reads channels.bin (produced by build_operator.py). Writes, for each K in
 * [1, KMAX]: the number of masks visited (must equal C(50,K)), the best and
 * second-best objective value and subset, and a self-check comparing the
 * quadratic-form value against a DIRECT reconstruction from the stored complex
 * E and V arrays for the best subset of each K (independent of the quadratic form).
 *
 * Build:  gcc -O3 -std=c11 -o lrsc_independent_search search.c -lm
 * Run:    ./lrsc_independent_search channels.bin KMAX
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>

#define N 50
#define M 99

static double lin[N];
static double gram[N][N];
static double const_term;
static double normE;
static double Ere[M], Eim[M];
static double Vre[N][M], Vim[N][M];

static void load(const char *path) {
    FILE *f = fopen(path, "rb");
    if (!f) { perror("fopen"); exit(1); }
    size_t got;
    got = fread(&normE, sizeof(double), 1, f); if (got != 1) { fprintf(stderr,"short read normE\n"); exit(1);}
    got = fread(&const_term, sizeof(double), 1, f); if (got != 1) { fprintf(stderr,"short read const\n"); exit(1);}
    got = fread(lin, sizeof(double), N, f); if (got != N) { fprintf(stderr,"short read lin\n"); exit(1);}
    double flat[N*N];
    got = fread(flat, sizeof(double), N*N, f); if (got != (size_t)N*N) { fprintf(stderr,"short read gram\n"); exit(1);}
    for (int a=0;a<N;a++) for (int b=0;b<N;b++) gram[a][b]=flat[a*N+b];
    got = fread(Ere, sizeof(double), M, f); if (got != M) { fprintf(stderr,"short read Ere\n"); exit(1);}
    got = fread(Eim, sizeof(double), M, f); if (got != M) { fprintf(stderr,"short read Eim\n"); exit(1);}
    for (int r=0;r<N;r++) {
        got = fread(Vre[r], sizeof(double), M, f); if (got != M) { fprintf(stderr,"short read Vre\n"); exit(1);}
        got = fread(Vim[r], sizeof(double), M, f); if (got != M) { fprintf(stderr,"short read Vim\n"); exit(1);}
    }
    fclose(f);
}

static double direct_residual(const int *idx, int k) {
    double acc = 0.0;
    for (int q = 0; q < M; q++) {
        double re = Ere[q], im = Eim[q];
        for (int t = 0; t < k; t++) { re -= Vre[idx[t]][q]; im -= Vim[idx[t]][q]; }
        acc += re*re + im*im;
    }
    return sqrt(acc) / normE;
}

static unsigned long long comb_count(int n, int k) {
    long double r = 1.0L;
    for (int t = 1; t <= k; t++) r = r * (n - k + t) / t;
    return (unsigned long long) llroundl(r);
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: %s channels.bin KMAX\n", argv[0]); return 1; }
    load(argv[1]);
    int KMAX = atoi(argv[2]);

    for (int K = 1; K <= KMAX; K++) {
        unsigned long long visited = 0;
        double best = 1e300, second = 1e300;
        uint64_t best_mask = 0, second_mask = 0;

        uint64_t x = (K == 0) ? 0 : ((1ULL << K) - 1ULL);
        uint64_t limit = 1ULL << N;
        while (x < limit) {
            /* extract set bits and evaluate quadratic form */
            int idx[16];
            int cnt = 0;
            uint64_t y = x;
            while (y) {
                int b = __builtin_ctzll(y);
                idx[cnt++] = b;
                y &= (y - 1);
            }
            double val = const_term;
            for (int t = 0; t < cnt; t++) val += lin[idx[t]];
            for (int a = 0; a < cnt; a++)
                for (int b = a + 1; b < cnt; b++)
                    val += 2.0 * gram[idx[a]][idx[b]];

            if (val < best) { second = best; second_mask = best_mask; best = val; best_mask = x; }
            else if (val < second) { second = val; second_mask = x; }
            visited++;

            /* Gosper's hack: next bitmask with the same popcount */
            uint64_t c = x & (~x + 1);
            uint64_t r = x + c;
            x = (((r ^ x) >> 2) / c) | r;
        }

        int best_idx[16], second_idx[16];
        int cnt = 0; uint64_t y = best_mask;
        while (y) { int b = __builtin_ctzll(y); best_idx[cnt++] = b; y &= (y-1); }
        cnt = 0; y = second_mask;
        while (y) { int b = __builtin_ctzll(y); second_idx[cnt++] = b; y &= (y-1); }

        double best_direct = direct_residual(best_idx, K);
        double second_direct = direct_residual(second_idx, K);
        double best_quad_err = sqrt(best > 0 ? best : 0.0) / normE;

        unsigned long long expected = comb_count(N, K);

        printf("K=%d expected=%llu visited=%llu best_mask=0x%013llx best_subset=", K, expected, visited, (unsigned long long)best_mask);
        printf("(");
        for (int t=0;t<K;t++) printf("%d%s", best_idx[t], t+1<K?",":"");
        printf(") best_score_hex=%a quad_err=%.17g direct_err=%.17g quad_vs_direct_absdiff=%.3e second_subset=(", best, best_quad_err, best_direct, fabs(best_quad_err-best_direct));
        for (int t=0;t<K;t++) printf("%d%s", second_idx[t], t+1<K?",":"");
        printf(") second_direct_err=%.17g pass_le_0.001=%s\n", second_direct, best_direct<=0.001 ? "YES":"no");
        fflush(stdout);

        if (visited != expected) {
            fprintf(stderr, "FATAL: K=%d visited %llu != expected %llu\n", K, visited, expected);
            return 2;
        }
    }
    return 0;
}
