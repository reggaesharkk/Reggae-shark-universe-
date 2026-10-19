// Independent exact-minimum search:  min_{|S|=K} || E - sum_{i in S} V_i ||^2
// Branch and bound over increasing index tuples (in a chosen channel order).
// Lower bound at a node: for an orthonormal basis e_d, each coordinate of any completion
// sum lies in [sum of r smallest, sum of r largest] of the remaining channels' coordinates,
// so ||residual||^2 >= sum_d dist(E_d - P_d, [lo_d, hi_d])^2.  Coverage is counted exactly.
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <algorithm>
#include <cmath>
typedef unsigned long long u64;
typedef __int128 i128;

int n, D, K;
std::vector<double> E, V;
std::vector<int> orig;
std::vector<double> LO, HI;
double best; std::vector<int> bestSet, cur;
u64 nodes = 0, leaves = 0; i128 covered = 0;
u64 binom[64][64];

static inline double lb(const double* P, int f, int r) {
    const double* lo = &LO[((size_t)f * (K + 1) + r) * D];
    const double* hi = &HI[((size_t)f * (K + 1) + r) * D];
    double s = 0;
    for (int d = 0; d < D; ++d) {
        double a = E[d] - P[d], g = 0;
        if (a < lo[d]) g = lo[d] - a; else if (a > hi[d]) g = a - hi[d];
        s += g * g;
    }
    return s;
}

static inline double exact(const double* P) {
    double s = 0; for (int d = 0; d < D; ++d) { double a = E[d] - P[d]; s += a * a; } return s;
}

void rec(int depth, int start, std::vector<double>& P) {
    int r = K - depth;
    std::vector<double> Q(D);
    for (int i = start; i <= n - r; ++i) {
        ++nodes;
        for (int d = 0; d < D; ++d) Q[d] = P[d] + V[(size_t)i * D + d];
        cur[depth] = i;
        if (r == 1) {
            ++leaves; ++covered;
            double v = exact(Q.data());
            if (v < best) { best = v; bestSet.assign(cur.begin(), cur.begin() + K); }
            continue;
        }
        double b = lb(Q.data(), i + 1, r - 1);
        if (b > best * (1 + 1e-12)) { covered += binom[n - i - 1][r - 1]; continue; }
        rec(depth + 1, i + 1, Q);
    }
}

int main(int argc, char** argv) {
    FILE* fp = fopen(argv[1], "r");
    double ub0;
    if (fscanf(fp, "%d %d %d %lf", &n, &D, &K, &ub0) != 4) return 1;
    E.resize(D); V.resize((size_t)n * D); orig.resize(n);
    for (auto& x : E) if (fscanf(fp, "%lf", &x) != 1) return 1;
    for (auto& x : V) if (fscanf(fp, "%lf", &x) != 1) return 1;
    for (auto& x : orig) if (fscanf(fp, "%d", &x) != 1) return 1;
    fclose(fp);
    for (int a = 0; a < 64; ++a) for (int b = 0; b < 64; ++b)
        binom[a][b] = (b == 0) ? 1 : (a == 0 ? 0 : binom[a - 1][b - 1] + binom[a - 1][b]);
    LO.assign((size_t)(n + 1) * (K + 1) * D, 0); HI = LO;
    std::vector<double> col;
    for (int f = 0; f <= n; ++f) for (int d = 0; d < D; ++d) {
        col.clear(); for (int i = f; i < n; ++i) col.push_back(V[(size_t)i * D + d]);
        std::sort(col.begin(), col.end());
        int m = col.size();
        for (int r = 0; r <= K; ++r) {
            double lo = 0, hi = 0;
            if (r > m) { lo = 1e300; hi = -1e300; }
            else { for (int q = 0; q < r; ++q) { lo += col[q]; hi += col[m - 1 - q]; } }
            LO[((size_t)f * (K + 1) + r) * D + d] = lo;
            HI[((size_t)f * (K + 1) + r) * D + d] = hi;
        }
    }
    best = ub0; cur.assign(K, -1);
    std::vector<double> P(D, 0.0);
    rec(0, 0, P);
    u64 expect = binom[n][K];
    printf("K=%d nodes=%llu leaves=%llu covered=%llu expected=%llu complete=%s\n", K,
           (unsigned long long)nodes, (unsigned long long)leaves, (unsigned long long)covered,
           (unsigned long long)expect, (covered == (i128)expect) ? "yes" : "NO");
    if (bestSet.empty()) { printf("min >= initial UB %.17g (no subset improved it)\n", ub0); return 0; }
    std::vector<int> lab; for (int i : bestSet) lab.push_back(orig[i]);
    std::sort(lab.begin(), lab.end());
    printf("min_R2=%.17g subset=", best);
    for (size_t q = 0; q < lab.size(); ++q) printf("%s%d", q ? "," : "", lab[q]);
    printf("\n");
    return 0;
}
