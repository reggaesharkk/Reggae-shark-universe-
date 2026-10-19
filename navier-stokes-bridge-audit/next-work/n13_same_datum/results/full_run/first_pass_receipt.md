# N13 same-datum first-pass checkpoint

- This file records the intermediate checkpoint before independent replay.
- Final status: PASS; all 120 segments independently rechecked. See
  `n13_same_datum_certificate.json` and `replay.log`.
- Cutoff: N=13; viscosity 0.1; interval [0, 0.003]; 120 segments.
- Exact witness SHA-256: 4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624.
- K36 key SHA-256: 7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47.
- Terminal trajectory error upper bound: 0.000012244529.
- True endpoint F interval: [-87.154087422, -83.563901281].
- Whole-path normalizer lower bound: 48869.38355689.
- At the checkpoint, the certificate JSON had `independent_arb_segment_replay=false`.
  The final certificate now has `independent_arb_segment_replay=true`.
