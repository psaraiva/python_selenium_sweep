import datetime
import logging
import os

from core.manager_finance_yahoo import ManagerFinanceYahoo
from core.table import Table
from core.extractor import Extractor

def main():
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

    # DEBUG imprimir muitas mensagens do Selenium.
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(levelname)s] %(message)s')
    logger = logging.getLogger('app')

    mfy = ManagerFinanceYahoo(logger, PROJECT_ROOT) \
    .process() \
    .debug()

    table = Table(logger) \
    .loadDataSetByManagerFinanceYahoo(mfy) \
    .treatment() \
    .debug()

    current_time = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
    Extractor(logger) \
    .setFileName(f'{PROJECT_ROOT}/output/data/{current_time}_result.csv') \
    .loadDataSet(table.getHeader(), table.getData()) \
    .toCSV()

if __name__ == "__main__":
    main()
