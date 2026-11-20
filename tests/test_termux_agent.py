"""Tests for the constrained Termux task runner."""
from pathlib import Path
import importlib.util
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("termux_agent", ROOT / "scripts/termux_agent.py")
AGENT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AGENT)


class AgentSafetyTests(unittest.TestCase):
    def test_only_explicit_task_is_allowed(self):
        self.assertEqual(
            AGENT.ALLOWED_TASKS,
            {"ark_redwood_preflight": "tests/ark_redwood_preflight.py", "ark_redwood_first_pass": "scripts/ark_redwood_first_pass.py"},
        )

    def test_shell_command_is_not_an_allowed_task(self):
        self.assertNotIn("shell", AGENT.ALLOWED_TASKS)
        self.assertNotIn("run_command", AGENT.ALLOWED_TASKS)

    def test_task_script_is_inside_repository(self):
        for relative in AGENT.ALLOWED_TASKS.values():
            self.assertTrue((ROOT / relative).is_file())


if __name__ == "__main__":
    unittest.main()
