import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from sayod111_radar import RadarClient

class TestRadarClient(unittest.TestCase):
    def test_requires_key_for_paid(self):
        c = RadarClient()
        with self.assertRaises(ValueError):
            c.me()

    def test_live_public_health_and_audit(self):
        c = RadarClient()
        h = c.health()
        self.assertTrue(h.get("ok"))
        self.assertIn("datasets", h)
        ria = c.ria_search(q="vanguard", limit=3)
        self.assertTrue(ria.get("ok"))
        self.assertGreaterEqual(ria.get("count", 0), 1)
        bio = c.biotech_search(limit=3)
        self.assertTrue(bio.get("ok"))

if __name__ == "__main__":
    unittest.main()
