from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from intentseal_vrk.canonical import digest_object
from intentseal_vrk.graph import propagate_statuses
from intentseal_vrk.ledger import append_event, verify_ledger
from intentseal_vrk.verify import verify_claim

ROOT = Path(__file__).resolve().parents[1]


class KernelTests(unittest.TestCase):
    def test_lrsc_demo_is_evidence_bound(self):
        result = verify_claim(ROOT / "examples/lrsc_theta07/claim.json")
        self.assertTrue(result["pass"])
        self.assertEqual(result["kernel_status"], "EVIDENCE_BOUND")
        self.assertEqual([c for c in result["checks"] if not c["ok"]], [])

    def test_hash_tamper_fails(self):
        src = ROOT / "examples/lrsc_theta07"
        with tempfile.TemporaryDirectory() as td:
            dst = Path(td) / "x"
            import shutil
            shutil.copytree(src, dst)
            p = dst / "evidence/rigorous_k13.txt"
            p.write_text(p.read_text() + "tamper\n")
            result = verify_claim(dst / "claim.json")
            self.assertFalse(result["pass"])
            self.assertEqual(result["kernel_status"], "UNVERIFIED")

    def test_coverage_plugin_detects_incomplete_search(self):
        src = ROOT / "examples/lrsc_theta07"
        with tempfile.TemporaryDirectory() as td:
            dst = Path(td) / "x"
            import shutil, hashlib
            shutil.copytree(src, dst)
            p = dst / "evidence/rigorous_k11.txt"
            text = p.read_text().replace("covered=37353738800", "covered=37353738799")
            p.write_text(text)
            claim = json.loads((dst / "claim.json").read_text())
            new_hash = hashlib.sha256(p.read_bytes()).hexdigest()
            for ev in claim["evidence"]:
                if ev.get("path") == "evidence/rigorous_k11.txt":
                    ev["sha256"] = new_hash
            (dst / "claim.json").write_text(json.dumps(claim, indent=2) + "\n")
            result = verify_claim(dst / "claim.json")
            self.assertFalse(result["pass"])
            self.assertTrue(any("covered" in c["detail"] for c in result["checks"] if not c["ok"]))

    def test_dependency_falsification_propagates_review(self):
        claims = [
            {"claim_id":"a","dependencies":[]},
            {"claim_id":"b","dependencies":[{"claim_id":"a","relation":"assumes"}]},
            {"claim_id":"c","dependencies":[{"claim_id":"b","relation":"reports"}]},
        ]
        out = propagate_statuses(claims, {"a":"FALSIFIED","b":"CERTIFIED","c":"CERTIFIED"})
        self.assertEqual(out["b"], "REVIEW_REQUIRED")
        self.assertEqual(out["c"], "REVIEW_REQUIRED")

    def test_ledger_tamper_detection(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "ledger.jsonl"
            append_event(p, {"type":"CLAIM_REGISTERED","claim_id":"a"})
            append_event(p, {"type":"CLAIM_CERTIFIED","claim_id":"a"})
            self.assertTrue(verify_ledger(p)[0])
            rows = p.read_text().splitlines()
            row = json.loads(rows[0])
            row["event"]["claim_id"] = "evil"
            rows[0] = json.dumps(row)
            p.write_text("\n".join(rows) + "\n")
            self.assertFalse(verify_ledger(p)[0])

    def test_digest_is_order_independent_for_objects(self):
        self.assertEqual(digest_object({"b":2,"a":1}), digest_object({"a":1,"b":2}))


if __name__ == "__main__":
    unittest.main()
