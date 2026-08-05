import subprocess
import sys
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "schemas.py"


class SchemasCompatibilityTests(unittest.TestCase):
    def test_schemas_module_imports_with_current_pandera(self):
        completed = subprocess.run(
            [sys.executable, str(SCRIPT_PATH)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)

    def test_user_schema_validates(self):
        probe = f"""
import importlib.util
import pandas as pd

spec = importlib.util.spec_from_file_location('pandera_validation_schemas', {str(SCRIPT_PATH)!r})
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
frame = pd.DataFrame({{
    'id': [1],
    'email': ['user@example.com'],
    'age': [42],
    'status': ['active'],
}})
module.UserSchema.validate(frame)
"""
        completed = subprocess.run(
            [sys.executable, "-c", probe],
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)


if __name__ == "__main__":
    unittest.main()
