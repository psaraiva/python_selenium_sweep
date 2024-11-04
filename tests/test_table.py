import logging
import unittest

from core.table import Table

# @TODO criar testes para saídas de log
# capturar saída de log e comparar com a mensagem esperada

class TestTable(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger('test')

    def test_getData(self):
        expected = Table(self.logger).getData()
        self.assertEqual(expected, [])

    def test_getHeader(self):
        expected = Table(self.logger).getHeader()
        self.assertEqual(expected, [])

    def test_addHeaderField(self):
        expected = Table(self.logger) \
        .addHeaderField('A') \
        .addHeaderField('B') \
        .getHeader()
        self.assertEqual(expected, ['A','B'])

    def test_setDataRow(self):
        expected = Table(self.logger) \
        .setDataRow(['a', 'b', 'c']) \
        .getData()
        self.assertEqual(expected, [['a', 'b', 'c']])

    def test_countRows(self):
        expected = Table(self.logger) \
        .setDataRow(['a', 'b', 'c', 'd']) \
        .setDataRow(['a', 'b', 'c', 'd']) \
        .setDataRow(['a', 'b', 'c', 'd']) \
        .countRows()
        self.assertEqual(expected, 3)

    def test_getFields(self):
        expected = Table(self.logger) \
        .setFields(['A', 'B', 'C']) \
        .getFields()
        self.assertEqual(expected, ['A', 'B', 'C'])

    def test_countFieldsHeader(self):
        expected = Table(self.logger) \
        .setFields(['A', 'B', 'C']) \
        .countFieldsHeader()
        self.assertEqual(expected, 3)

    def test_treatment(self):
        expected = Table(self.logger) \
        .setDataRow([' a ', 'b ', ' c', 'd']) \
        .treatment()
        self.assertEqual(expected.getData(), [['a', 'b', 'c', 'd']])
        self.assertEqual(expected.getHeader(), [])

if __name__ == '__main__':
    unittest.main()
