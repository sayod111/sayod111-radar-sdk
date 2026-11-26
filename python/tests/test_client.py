import os
import json
from email.message import Message
from unittest.mock import MagicMock, patch
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

    def test_public_requests_offline(self):
        response = MagicMock()
        response.headers = Message()
        response.headers["Content-Type"] = "application/json"
        response.read.return_value = json.dumps({"ok": True, "data": []}).encode()
        response.__enter__.return_value = response
        with patch("urllib.request.urlopen", return_value=response) as transport:
            result = RadarClient().ria_search(q="Vanguard", limit=3)
            request = transport.call_args.args[0]
            self.assertEqual(request.get_method(), "GET")
            self.assertIn("/v1/public/ria-search?", request.full_url)
            self.assertIn("q=Vanguard", request.full_url)
            self.assertIn("limit=3", request.full_url)
            self.assertEqual(result["data"], [])

    @unittest.skipUnless(os.getenv("SAYOD_LIVE_TESTS") == "1", "Live smoke test is opt-in")
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
