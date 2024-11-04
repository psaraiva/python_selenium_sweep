import glob
import logging
import os
import unittest

from core.extractor import Extractor

# @TODO: Gerar caso de teste para cada método que lança exceção.

class TestExtractor(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger('test')
        self.folder = './tests/'
        self.fileNameCSV_1 = self.folder+'test_1.csv'
        self.fileNameCSV_2 = self.folder+'test_2.csv'
        self.fileNameCSV_3 = self.folder+'test_3.csv'

    def tearDown(self):
        files = glob.glob(self.folder+'test*.csv')
        for file in files:
            if os.path.exists(file):
                os.remove(file)

    def test_getFileName(self):
        expected = Extractor(self.logger).getFileName()
        self.assertEqual(expected, '')

    def test_setFileName(self):
        expected = Extractor(self.logger) \
        .setFileName(self.fileNameCSV_1) \
        .getFileName()
        self.assertEqual(expected, self.fileNameCSV_1)

    def test_toCSV(self):
        Extractor(self.logger) \
        .setFileName(self.fileNameCSV_2) \
        .loadDataSet(['field_1', 'field_2'], [['A', 'B']]) \
        .toCSV()
        self.assertTrue(os.path.exists(self.fileNameCSV_2))

    def test_generateMD5(self):
        extractor = Extractor(self.logger)
        extractor.setFileName(self.fileNameCSV_3) \
        .loadDataSet(['A', 'B'], [['100', '200']]) \
        .toCSV()
        self.assertEqual(extractor.getMD5(), '032d835844d3d12ea53778e22c8def73')

if __name__ == '__main__':
    unittest.main()
