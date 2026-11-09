# (C) British Crown Copyright 2026, Met Office.
# Please see LICENSE.md for license details.
import unittest

from scripts.generate_metadata_tables import get_mappings, build_table, generate_html


# This is hand to unit test in its current stage,the function does too much and the naming poorly represents its
# utility. Reading the mappings file in the function makes it hard to test, this should be moved to be a parameter so
# that this can be tested.
class TestGetMappings(unittest.TestCase):
    def test_get_mappings(self):
        pass


class TestBuildTable(unittest.TestCase):
    def test_build_table(self):
        table_data = [
            ['Model Workflow ID', 'Model ID', 'Mass Data Class', 'MIP', 'Institution ID', 'Experiment ID',
             'Variant Label', 'Start Date', 'End Date'],
            ['u-dx055', 'UKCM2-0-LL', 'crum', 'CMIP', 'UKNCSP', 'historical', 'r1i1p1f1', '1850-01-01T00:00:00Z',
             '2022-01-01T00:00:00Z', 'u-dx055']
        ]
        table_html = build_table(table_data)
        expected = ('<table border=1, id="table_id", class="display">\n  <thead>\n   <tr bgcolor="#E0EEFF">\n     '
                    '<th bgcolor="Azure">Model Workflow ID</th>\n     <th bgcolor="Azure">Model ID</th>\n     '
                    '<th bgcolor="Azure">Mass Data Class</th>\n     <th bgcolor="Azure">MIP</th>\n     '
                    '<th bgcolor="Azure">Institution ID</th>\n     <th bgcolor="Azure">Experiment ID</th>\n     '
                    '<th bgcolor="Azure">Variant Label</th>\n     <th bgcolor="Azure">Start Date</th>\n     '
                    '<th bgcolor="Azure">End Date</th>\n   </tr>\n                          <tr class="filters">\n     '
                    '<th bgcolor="Azure"></th>\n     <th bgcolor="Azure"></th>\n     <th bgcolor="Azure"></th>\n     '
                    '<th bgcolor="Azure"></th>\n     <th bgcolor="Azure"></th>\n     <th bgcolor="Azure"></th>\n     '
                    '<th bgcolor="Azure"></th>\n     <th bgcolor="Azure"></th>\n     <th bgcolor="Azure"></th>\n   '
                    '</tr>\n   </thead>\n  <tr bgcolor="#FFFFFF">\n     '
                    '<td bgcolor="Azure"><a href="https://github.com/UKNCSP/CDDS-simulation-metadata/tree/main/'
                    'workflow_metadata/u-dx055.cfg">u-dx055</a></td>\n     <td bgcolor="Azure">UKCM2-0-LL</td>\n     '
                    '<td bgcolor="Azure">crum</td>\n     <td bgcolor="Azure">CMIP</td>\n     '
                    '<td bgcolor="Azure">UKNCSP</td>\n     <td bgcolor="Azure">historical</td>\n     '
                    '<td bgcolor="Azure">r1i1p1f1</td>\n     <td bgcolor="Azure">1850-01-01T00:00:00Z</td>\n     '
                    '<td bgcolor="Azure">2022-01-01T00:00:00Z</td>\n  </tr>\n</table>\n')
        self.assertEqual(table_html, expected, table_html)


# This function should be re written, in its current stage it is nt easily testable.
class TestGenerateHTML(unittest.TestCase):
    def test_generate_html(self):
        pass
