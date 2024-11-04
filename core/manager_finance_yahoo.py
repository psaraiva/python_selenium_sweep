import datetime
import inspect
import logging
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

class ManagerFinanceYahoo:
    """
        Essa classe é responsável por extrair dados da página do Yahoo Finance via Selenium.
    """
    __command = [
        'clearRegionFilter',
        'useCountryFilter',
        'executeSearch',
        'extractData',
        'nextPage'
    ]

    def __init__(self, log:logging, project_root:str):
        self.__dataHeader = []
        self.__data = []
        self.__start_time = float(0)
        self.__end_time = float(0)
        self.__logger = log
        self.__projectRoot = project_root

    def initDriver(self) -> 'ManagerFinanceYahoo':
        """
        Inicializa o driver do Selenium e abre a página do Yahoo Finance.
        """
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        #options.add_argument("--headless=new")
        options.add_argument(f"--user-data-dir={self.__projectRoot}/tmp")
        self.__driver = webdriver.Chrome(service=service, options=options)
        self.__driver.get("https://finance.yahoo.com/screener/new")
        return self

    def getHeader(self) -> list:
        return self.__dataHeader

    def getData(self) -> list:
        return self.__data

    def process(self) -> 'ManagerFinanceYahoo':
        """
        Processa todos os passos definidos para extrair informações do Yahoo Finance.
        """
        self.__start_time = time.time()
        self.__logger.info('MFY:Processo iniciado')
        self.initDriver()

        if hasattr(self, self.__command[0]) == False:
            err_str = f"Método {self.__command[0]} não foi encontrado em {self.__class__.__name__}"
            self.__logger.error(err_str)
            raise Exception(err_str)

        self.__logger.info('passo:0')
        getattr(self, self.__command[0])()
        if hasattr(self, self.__command[1]) == False:
            err_str = f"Método {self.__command[1]} não foi encontrado em {self.__class__.__name__}"
            self.__logger.error(err_str)
            raise Exception(err_str)

        self.__logger.info('passo:1')
        getattr(self, self.__command[1])()
        if hasattr(self, self.__command[2]) == False:
            err_str = f"Método {self.__command[2]} não foi encontrado em {self.__class__.__name__}"
            self.__logger.error(err_str)
            raise Exception(err_str)

        self.__logger.info('passo:2')
        getattr(self, self.__command[2])()
        if hasattr(self, self.__command[3]) == False:
            err_str = f"Método {self.__command[3]} não foi encontrado em {self.__class__.__name__}"
            self.__logger.error(err_str)
            raise Exception(err_str)

        self.__logger.info('passo:3')
        getattr(self, self.__command[3])()

        if hasattr(self, self.__command[4]) == False:
            err_str = f"Método {self.__command[4]} não foi encontrado em {self.__class__.__name__}"
            self.__logger.error(err_str)
            raise Exception(err_str)

        cycle=0
        while True:
            cycle += 1
            self.__logger.info('passo:4')
            if getattr(self, self.__command[4])() == False:
                break
            self.__logger.info('passo:3')
            self.__logger.info(f'ciclo:{str(cycle)}')
            getattr(self, self.__command[3])(True)
        
        self.__end_time = time.time()
        current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.__driver.save_screenshot(f'{self.__projectRoot}/output/img/success_{current_time}.png')
        self.__driver.quit()
        self.__logger.info('MFY: Processo finalizado')
        return self

    def clearRegionFilter(self) -> None:
        """
        O comportamento padrão é ao carregar a página o filtro 'region' vir preenchido, esse passo remove o filtro
        """
        self.__driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[5]/div/div/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/ul/li[1]/button').click()

    def useCountryFilter(self) -> None:
        """
        Executa dinâmica com o campo Region da página do Yahoo Finance.

        A dinâmica consiste em abrir o filtro e usar um dos países disponíveis.
        """
        # Abre filtro de setor
        self.__driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[5]/div/div/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/ul/li/button').click()
        # Seleciona o primeiro item, Argentina, por exemplo
        # @TODO isso deve ser parametrizado e adicionar um novo passo intermediário
        self.__driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[5]/div/div/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/div/div/div[2]/div/div[2]/ul/li[1]/label').click()
        time.sleep(3) # delay...
        # Fecha a janela de seleção de filtro
        self.__driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[5]/div/div/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/div/div/div[2]/button').click()

    def executeSearch(self) -> None:
        """
        Executa uma busca na página do Yahoo Finance.

        Apenas executa o borão de busca, usando os filtros preenchidos previamente.
        """
        try:
            self.__driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[5]/div/div/div/div[2]/div[1]/div[3]/button[1]').click()
        except (NoSuchElementException, TimeoutException):
            self.__logger.error('MFY: Processo finalizado')
            current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            self.__driver.save_screenshot(f'{self.__projectRoot}/output/img/error_{current_time}.png')
            self.__driver.quit()
            exit()

    def extractData(self, skip_header=False) -> None:
        """
        Carrega os dados da tabela de resultados da página do Yahoo Finance.

        Guarda as informações de cabeçalho e dados da tabela em variáveis da classe, _dataHeader e _data.
        """
        try:
            el = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[6]/section/div/div[2]/div[1]/table"))
            )
        except (NoSuchElementException, TimeoutException):
            self.__logger.error('Elemento Tabela de Resultados não encontrado.')
            current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            self.__driver.save_screenshot(f'{self.__projectRoot}/output/img/error_{current_time}.png')
            self.__driver.quit()
            exit()

        if skip_header == False:
            self.__logger.info('Extraindo cabeçalho')
            table_head = el.find_element(By.TAG_NAME, "thead")
            for x in table_head.find_element(By.TAG_NAME, "tr").find_elements(By.TAG_NAME, "th"):
                self.__dataHeader.append(x.text)

        self.__logger.info('Extraindo data')
        rows = el.find_element(By.TAG_NAME, "tbody")
        item = 0
        for x in rows.find_elements(By.TAG_NAME, "tr"):
            temp = []
            for y in x.find_elements(By.TAG_NAME, "td"):
                temp.append(y.text)
            self.__data.append(temp)
            item += 1
        self.__logger.info(f'Adicionado {item} itens')

    def nextPage(self) -> bool :
        """
        Navega para a próxima página de resultados.
        """
        m = inspect.currentframe().f_code.co_name
        element = self.__driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[6]/section/div/div[2]/div[2]/button[3]')
        if element.get_attribute("disabled") is not None:
            return False
        element.click()
        return True

    def debug(self) -> 'ManagerFinanceYahoo':
        """
        Estatística para debug.
        """
        duration = self.__end_time - self.__start_time
        self.__logger.debug(f'Duração da execução: {duration:.3f} segundo(s)')
        self.__logger.debug(f'Qtd campos Cabeçalho: {len(self.__dataHeader)}.')
        self.__logger.debug(f'Qtd linhas de dados: {len(self.__data)}.')
        return self
