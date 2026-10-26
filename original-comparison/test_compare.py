import json
import tempfile
import unittest
from pathlib import Path
from compare import initialize, record


class RecorderTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / 'results.json'
        initialize(self.path, 'Original test question')

    def test_preserves_exact_supplied_output(self):
        # Synthetic test fixture only; never an experiment observation.
        output = 'TEST FIXTURE\n日本語\n'
        record(self.path, 'Original test question', 'test-only', 0.5, output, 'unit test fixture')
        self.assertEqual(json.loads(self.path.read_text())['runs'][0]['output'], output)

    def test_rejects_changed_question_without_modifying_results(self):
        before = self.path.read_bytes()
        with self.assertRaises(ValueError):
            record(self.path, 'Different question', 'test-only', 0, 'fixture', 'test')
        self.assertEqual(before, self.path.read_bytes())

    def test_rejects_invalid_temperature_and_empty_output(self):
        for temperature in [float('nan'), float('inf'), -1, 3]:
            with self.assertRaises(ValueError):
                record(self.path, 'Original test question', 'test-only', temperature, 'fixture', 'test')
        with self.assertRaises(ValueError):
            record(self.path, 'Original test question', 'test-only', 0, '', 'test')
        self.assertEqual(json.loads(self.path.read_text())['runs'], [])

    def test_init_cannot_overwrite_existing_results(self):
        with self.assertRaises(FileExistsError):
            initialize(self.path, 'Replacement')


if __name__ == '__main__':
    unittest.main()
