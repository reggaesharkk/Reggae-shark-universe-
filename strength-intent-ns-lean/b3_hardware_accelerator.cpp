#include <cmath>

extern "C" {
    void execute_b3_block_diagonal_pass(
        const double* __restrict__ x_t,       
        const double* __restrict__ W_xh,      
        const double* __restrict__ W_fast,    
        const double* __restrict__ W_slow,    
        const double* __restrict__ h_prev,    
        const double* __restrict__ xi_t,      
        double* __restrict__ h_next,          
        int fast_dim, int slow_dim
    ) {
        int total_dim = fast_dim + slow_dim;
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
    }
}
