import csv
import hashlib
import logging
import os

from typing import List

class Extractor:
    def __init__(self, log:logging) -> None:
        self.__fileName = ''
        self.__dataHeader = []
        self.__data = []
        self.__logger = log
        self.__md5 = ''

    def loadDataSet(self, datHeader:List[str], data:List[str]) -> 'Extractor':
        self.__dataHeader = datHeader
        self.__data = data
        return self

    def getFileName(self) -> str:
        return self.__fileName

    def getMD5(self) -> str:
        return self.__md5

    # @TODO criar regra para criar nome do arquivo.
    def setFileName(self, fileName:str) -> 'Extractor':
        self.__fileName = fileName
        return self

    def generateMD5(self) -> 'Extractor':
        if os.path.exists(self.__fileName) == False:
            raise Exception(f"Extractor: O arquivo '{self.__fileName}' não existe.")

        md5_hash = hashlib.md5()
        with open(self.__fileName, 'rb') as file:
            md5_hash.update(file.read())
        self.__md5 = md5_hash.hexdigest()
        return self

    def generateFile(self) -> bool:
        """
        Gera um arquivo vazio.

        Raises:
            Exception: Se o nome do arquivo não foi definido ou se ocorrer um erro ao gerar o arquivo.

        Returns:
            bool: Representando a ação de criar o arquivo.
        """
        try:
            with open(self.__fileName, 'x') as _:
                return True
        except IOError as e:
            raise Exception(f"Um erro ocorreu enquanto gerava o arquivo: {e}")
        return False

    def toCSV(self) -> None:
        """
        Gera um arquivo CSV.
        """
        self.__logger.info('Extractor: Gerando arquivo CSV vazio.')
        if self.generateFile() == False:
            self.__logger.error('Extractor: Erro ao gerar arquivo CSV.')
            return
        self.__logger.info('Extractor: Arquivo CSV gerado.')

        with open(self.__fileName, 'w+', newline='\n') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(self.__dataHeader)
            csvwriter.writerows(self.__data)

        self.generateMD5()
        self.__logger.info(f'Arquivo CSV {self.__fileName} preenchido com sucesso.')
        self.__logger.info(f'Hash MD5 {self.__md5}')
