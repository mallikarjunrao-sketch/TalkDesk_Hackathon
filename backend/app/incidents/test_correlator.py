"""
Unit tests for the PULSE Incident Correlator (Task C4)
Verifies:
1. 4 events -> no incident
2. 6 events -> exactly one incident (INC-0042)
3. Extra events -> update the same incident
4. Non-matching events -> ignored
"""

import unittest
from datetime import datetime, timezone, timedelta
from backend.app.incidents.correlator import (
    IncidentCorrelator,
    IngestedEvent,
    DEFAULT_SIGNATURE,
)


class TestIncidentCorrelator(unittest.TestCase):
    def setUp(self):
        self.correlator = IncidentCorrelator(
            signature=DEFAULT_SIGNATURE,
            window_seconds=120,
            threshold=5,
            incident_id="INC-0042",
        )
        self.base_time = datetime(2026, 11, 4, 10, 30, 0, tzinfo=timezone.utc)

    def test_case_1_four_events_no_incident(self):
        """Case 1: 4 matching events (below threshold of 5) does not open an incident."""
        for i in range(1, 5):
            accepted, inc, opened = self.correlator.ingest({
                "type": DEFAULT_SIGNATURE,
                "payment_ref": f"TX-{100 + i}",
                "ts": (self.base_time + timedelta(seconds=i * 5)).isoformat(),
            })
            self.assertTrue(accepted)
            self.assertFalse(opened)
            self.assertIsNone(inc)

        self.assertIsNone(self.correlator.get_active_incident())

    def test_case_2_six_events_opens_one_incident(self):
        """Case 2: 6 matching events within 120s opens exactly one incident."""
        # 1-4: no incident
        for i in range(1, 5):
            self.correlator.ingest({
                "type": DEFAULT_SIGNATURE,
                "payment_ref": f"TX-{100 + i}",
                "ts": (self.base_time + timedelta(seconds=i * 5)).isoformat(),
            })

        # 5th event opens incident
        _, inc_at_5, opened_at_5 = self.correlator.ingest({
            "type": DEFAULT_SIGNATURE,
            "payment_ref": "TX-105",
            "ts": (self.base_time + timedelta(seconds=25)).isoformat(),
        })
        self.assertTrue(opened_at_5)
        self.assertIsNotNone(inc_at_5)
        self.assertEqual(inc_at_5.id, "INC-0042")
        self.assertEqual(inc_at_5.status, "ACTIVE")
        self.assertEqual(inc_at_5.affected_count, 5)

        # 6th event does not re-open, stays same incident
        _, inc_at_6, opened_at_6 = self.correlator.ingest({
            "type": DEFAULT_SIGNATURE,
            "payment_ref": "TX-106",
            "ts": (self.base_time + timedelta(seconds=30)).isoformat(),
        })
        self.assertFalse(opened_at_6)
        self.assertIsNotNone(inc_at_6)
        self.assertEqual(inc_at_6.id, "INC-0042")
        self.assertEqual(inc_at_6.affected_count, 6)

    def test_case_3_extra_events_update_same_incident(self):
        """Case 3: Extra events update affected references on the existing incident."""
        for i in range(1, 10):
            self.correlator.ingest({
                "type": DEFAULT_SIGNATURE,
                "payment_ref": f"TX-{100 + i}",
                "ts": (self.base_time + timedelta(seconds=i * 2)).isoformat(),
            })

        active = self.correlator.get_active_incident()
        self.assertIsNotNone(active)
        self.assertEqual(active.id, "INC-0042")
        self.assertEqual(active.affected_count, 9)
        self.assertIn("TX-109", active.affected_payment_refs)

    def test_case_4_non_matching_events_ignored(self):
        """Case 4: Non-matching signatures (e.g. PAYMENT_SUCCESS) are ignored and do not count toward threshold."""
        for i in range(1, 15):
            accepted, inc, opened = self.correlator.ingest({
                "type": "PAYMENT_SUCCESS_NORMAL",
                "payment_ref": f"TX-NORMAL-{i}",
                "ts": (self.base_time + timedelta(seconds=i)).isoformat(),
            })
            self.assertTrue(accepted)
            self.assertFalse(opened)
            self.assertIsNone(inc)

        self.assertIsNone(self.correlator.get_active_incident())


if __name__ == "__main__":
    unittest.main()
