import json
from pathlib import Path
import unittest

from app import adapt
from jev import normalize
from service import InputError, decide, open_state


class AdapterTests(unittest.TestCase):
    def test_duplicate_flowfile_id_with_changed_text_is_rejected(self):
        policy = json.loads(Path("examples/policy.json").read_text())
        event = json.loads(Path("examples/flowfile.json").read_text())
        with open_state(":memory:") as db:
            decide(
                event, adapt, policy, lambda _: normalize("incident", 0.97, policy), db
            )
            with self.assertRaises(InputError):
                decide(
                    {**event, "text": "Different content"},
                    adapt,
                    policy,
                    lambda _: normalize("routine", 0.97, policy),
                    db,
                )

    def test_non_text_payload_is_rejected(self):
        with self.assertRaises(InputError):
            adapt({"id": "flow-1", "text": None})
