import logging

from typing import List

from core.manager_finance_yahoo import ManagerFinanceYahoo

class Table:
    def __init__(self, log:logging):
        self.__header = []
        self.__data = []
        self.__fields = []
        self.__logger = log

    def loadDataSetByManagerFinanceYahoo(self, mfy:'ManagerFinanceYahoo') -> 'Table' :
        self.__header = mfy.getHeader()
        self.__data = mfy.getData()
        return self

    def addHeaderField(self, text:str) -> 'Table':
        self.__header.append(text.strip())
        return self

    def setDataRow(self, list_string:List[str]) -> 'Table':
        self.__data.append(list_string)
        return self

    def setFields(self, fields:List[str]) -> 'Table':
        self.__fields = fields
        return self

    def treatment(self) -> 'Table':
        self.__logger.info('Table: processamento de dados iniciado.')
        self.__header = [item.strip() for item in self.__header]
        for i in range(len(self.__data)):
            self.__data[i] = [item.strip() for item in self.__data[i]]
        self.__logger.info('Table: processamento de dados finalizado.')
        return self

    def getHeader(self) -> List[str]:
        return self.__header

    def getData(self) -> List[str]:
        return self.__data

    def getFields(self) -> List[str]:
        return self.__fields

    def countRows(self) -> int:
        return len(self.__data)

    def countFieldsHeader(self) -> int:
        return len(self.__fields)

    def debug(self) -> 'Table':
        self.__logger.debug(f'Table: cabeçalho: {self.__header}')
        self.__logger.debug(f'Table: Qtd dados: {len(self.__data)}')
        return self
