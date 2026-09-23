#include <algorithm>
#include <array>
#include <cstdint>
#include <limits>
#include <vector>

// Exhaustive lexicographic search over all size-K subsets.
// Objective: ||E - sum_i V_i||_2^2 = c + sum_i f_i + sum_{i,j} Q_ij.
// Inputs are double-precision Gram data generated independently in Python.
extern "C" {
struct Result {
    std::uint64_t count;
    double best;
    double second;
    int best_indices[10];
    int second_indices[10];
};

static int K;
static const int N = 50;
static const double* linear_term;
static const double* gram;
static std::array<int, 10> chosen{};
static Result result;

static void visit(int depth, int first, double partial) {
    if (depth == K) {
        ++result.count;
        if (partial < result.best) {
            result.second = result.best;
            for (int t = 0; t < K; ++t) result.second_indices[t] = result.best_indices[t];
            result.best = partial;
            for (int t = 0; t < K; ++t) result.best_indices[t] = chosen[t];
        } else if (partial < result.second) {
            result.second = partial;
            for (int t = 0; t < K; ++t) result.second_indices[t] = chosen[t];
        }
        return;
    }
    const int remaining = K - depth;
    for (int x = first; x <= N - remaining; ++x) {
        double increment = linear_term[x] + gram[x * N + x];
        for (int t = 0; t < depth; ++t)
            increment += 2.0 * gram[x * N + chosen[t]];
        chosen[depth] = x;
        visit(depth + 1, x + 1, partial + increment);
    }
}

Result exhaustive_search(int cardinality, const double* f, const double* q, double constant) {
    K = cardinality;
    linear_term = f;
    gram = q;
    result = {};
    result.best = std::numeric_limits<double>::infinity();
    result.second = std::numeric_limits<double>::infinity();
    visit(0, 0, constant);
    return result;
}
}
