import unittest
from pathlib import Path

from scripts.generate_metadata_tables import build_table

TEST_DATA_DIR = Path("tests/test_scripts/data")


class TestBuildTable(unittest.TestCase):

    def test_build_table(self):
        table_data = [['Model Workflow ID', 'Model ID', 'Mass Data Class', 'MIP', 'Institution ID', 'Experiment ID',
                        'Variant Label', 'Start Date', 'End Date'],
                        ['u-dv623', 'UKCM2-LL', 'crum', 'CMIP', 'MOHC', '1pctCO2', 'r2i1p1f1', '1850-01-01T00:00:00Z',
                        '2000-01-01T00:00:00Z', 'u-dv623']]
        with open(Path(TEST_DATA_DIR / "html_table.txt"), "r") as fh:
            expected = fh.read()

        table = build_table(table_data)
        self.assertEqual(table, expected, "The html format of the table was not built as expected.")


if __name__ == "__main__":
    unittest.main()
