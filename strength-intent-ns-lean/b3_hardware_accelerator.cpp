#include <cmath>

extern "C" {
    // Returns 0 on success and -1 for invalid arguments. The caller must pass
    // arrays with the dimensions implied by fast_dim and slow_dim.
    int execute_b3_block_diagonal_pass(
        const double* x_t,
        const double* W_xh,
        const double* W_fast,
        const double* W_slow,
        const double* h_prev,
        const double* xi_t,
        double* h_next,
        int fast_dim, int slow_dim
    ) {
        if (fast_dim < 0 || slow_dim < 0 || fast_dim > 32 || slow_dim > 32) {
            return -1;
        }
        int total_dim = fast_dim + slow_dim;
        if (total_dim < 1 || total_dim > 32 || x_t == nullptr || W_xh == nullptr ||
            h_prev == nullptr || xi_t == nullptr || h_next == nullptr ||
            (fast_dim > 0 && W_fast == nullptr) ||
            (slow_dim > 0 && W_slow == nullptr)) {
            return -1;
        }

        double input_projected[32] = {0.0};
        for (int j = 0; j < total_dim; ++j) {
            input_projected[j] = x_t[0] * W_xh[j];
        }
        
        for (int j = 0; j < fast_dim; ++j) {
            double sum = 0.0;
            for (int i = 0; i < fast_dim; ++i) {
                sum += h_prev[i] * W_fast[i * fast_dim + j];
            }
            h_next[j] = std::tanh(sum + input_projected[j]) + xi_t[j];
        }
        
        for (int j = 0; j < slow_dim; ++j) {
            double sum = 0.0;
            for (int i = 0; i < slow_dim; ++i) {
                sum += h_prev[fast_dim + i] * W_slow[i * slow_dim + j];
            }
            h_next[fast_dim + j] = std::tanh(sum + input_projected[fast_dim + j]) + xi_t[fast_dim + j];
        }
        return 0;
    }
}

