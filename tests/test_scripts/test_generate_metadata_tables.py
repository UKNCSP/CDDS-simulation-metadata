import unittest
from pathlib import Path

from scripts.generate_metadata_tables import build_table, generate_html


class TestBuildTable(unittest.TestCase):

    def test_build_table(self):
        table_data = [['Model Workflow ID', 'Model ID', 'Mass Data Class', 'MIP', 'Institution ID', 'Experiment ID',
                       'Variant Label', 'Start Date', 'End Date'],
                       ['u-dv623', 'UKCM2-LL', 'crum', 'CMIP', 'MOHC', '1pctCO2', 'r2i1p1f1', '1850-01-01T00:00:00Z',
                        '2000-01-01T00:00:00Z', 'u-dv623']]
        expected = ('<table border=1, id="table_id", class="display">\n  <thead>\n   <tr bgcolor="#E0EEFF">\n     <th>'
                    'Model Workflow ID</th>\n     <th>Model ID</th>\n     <th>Mass Data Class</th>\n     <th>MIP</th>\n'
                    '     <th>Institution ID</th>\n     <th>Experiment ID</th>\n     <th>Variant Label</th>\n     <th>'
                    'Start Date</th>\n     <th>End Date</th>\n   </tr>\n                          <tr class="filters">'
                    '\n     <th></th>\n     <th></th>\n     <th></th>\n     <th></th>\n     <th></th>\n     <th></th>'
                    '\n     <th></th>\n     <th></th>\n     <th></th>\n   </tr>\n   </thead>\n  <tr bgcolor="#FFFFFF">'
                    '\n     <td><a href="https://github.com/UKNCSP/CDDS-simulation-metadata/tree/main/workflow_metadata'
                    '/u-dv623.cfg">u-dv623</a></td>\n     <td>UKCM2-LL</td>\n     <td>crum</td>\n     <td>CMIP</td>\n  '
                    '   <td>MOHC</td>\n     <td>1pctCO2</td>\n     <td>r2i1p1f1</td>\n     <td>1850-01-01T00:00:00Z'
                    '</td>\n     <td>2000-01-01T00:00:00Z</td>\n  </tr>\n</table>\n')

        table = build_table(table_data)
        self.assertEqual(table, expected, "The html format of the table was not built as expected")


if __name__ == "__main__":
    unittest.main()