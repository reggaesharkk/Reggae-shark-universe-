"""Post-hoc hybrid-state decomposition of first K36 mass-gate exits."""

import argparse
import json
from pathlib import Path

import numpy as np

import wp16_036_N12_frozen_K36_holdout as hold
from wp16_036_dealiased_trajectory_gate import DealiasedSystem


def ablate(system, a, b, keys):
    n0 = np.linalg.norm(a, axis=1)
    n1 = np.linalg.norm(b, axis=1)
    assert np.all(n0 > 0) and np.all(n1 > 0)
    phase = np.angle(np.einsum('ij,ij->i', np.conj(a), b))
    cases = {
        'initial': a,
        'evolved': b,
        'evolved_magnitudes_initial_directions': a*(n1/n0)[:, None],
        'initial_magnitudes_evolved_directions': b*(n0/n1)[:, None],
        'evolved_scalar_phases_initial_magnitudes_polarizations': a*np.exp(1j*phase[:, None]),
        'evolved_magnitudes_scalar_phases_initial_polarizations':
            a*(n1/n0)[:, None]*np.exp(1j*phase[:, None]),
    }
    out = {}
    for name, state in cases.items():
        row = hold.evaluate_state(system, state, keys)
        out[name] = {k: row[k] for k in ('absolute_mass_fraction', 'signed_share_of_channel_total',
                                        'passes_preregistered_consistency_criteria')}
    out['relative_L2_displacement'] = float(np.linalg.norm(b-a)/np.linalg.norm(a))
    out['relative_magnitude_L2_displacement'] = float(np.linalg.norm(n1-n0)/np.linalg.norm(n0))
    out['anchor_mode_amplitude_ratios'] = {
        str(k): float(n1[system.index[k]]/n0[system.index[k]])
        for k in (hold.P, hold.Q, hold.K)}
    return out


def main():
    p = argparse.ArgumentParser()
    for name in ('n11-json', 'n12-json', 'n13-json', 'source-json', 'crossings-json', 'output'):
        p.add_argument('--'+name, type=Path, required=True)
    args = p.parse_args()
    names = ('n11-json', 'n12-json', 'n13-json', 'source-json', 'crossings-json')
    j11, j12, j13, source, crossings = [
        json.loads(getattr(args, name.replace('-', '_')).read_text()) for name in names]
    hold.System = DealiasedSystem
    keys = hold.frozen_keys(source)
    out = {'status': 'post-hoc hybrid-state ablation at first coarse sampled exit', 'N': {}}
    for N, prev, curr in ((12, hold.get_row(j11, 11), hold.get_row(j12, 12)),
                          (13, hold.get_row(j12, 12), hold.get_row(j13, 13))):
        system, states = hold.reconstruct(prev, curr)
        out['N'][str(N)] = {}
        for name, a in states.items():
            t = crossings['states'][str(N)][name]['coarse_first_fail_time']
            steps = round(t/.0001)
            b = a.copy()
            for _ in range(steps):
                b = system.rk4(b, .0001)
            out['N'][str(N)][name] = {'time': t, **ablate(system, a, b, keys)}
            print('DONE', N, name, flush=True)
    args.output.write_text(json.dumps(out, indent=2)+'\n')


if __name__ == '__main__':
    main()
