from pathlib import Path
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService

ROOT_PATH = Path(__file__).parent.parent.parent

CHROMEDRIVER_NAME = 'chromedriver.exe'
CHROMEDRIVER_PATH = ROOT_PATH / 'bin' / CHROMEDRIVER_NAME

FIREFOXDRIVER_NAME = 'geckodriver.exe'
FIREFOXDRIVER_PATH = ROOT_PATH / 'bin' / FIREFOXDRIVER_NAME

EDGEDRIVER_NAME = 'msedgedriver.exe'
EDGEDRIVER_PATH = ROOT_PATH / 'bin' / EDGEDRIVER_NAME


def chrome_browser(*options):
    chrome_options = webdriver.ChromeOptions()

    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    chrome_service = ChromeService(executable_path=CHROMEDRIVER_PATH)
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)

    return browser


def edge_browser(*options):
    edge_options = webdriver.EdgeOptions()

    if options is not None:
        for option in options:
            edge_options.add_argument(option)

    edge_service = EdgeService(executable_path=EDGEDRIVER_PATH)
    browser = webdriver.Edge(service=edge_service, options=edge_options)

    return browser


def firefox_browser(*options):
    firefox_options = webdriver.FirefoxOptions()

    if options is not None:
        for option in options:
            firefox_options.add_argument(option)

    firefox_service = FirefoxService(executable_path=FIREFOXDRIVER_PATH)
    browser = webdriver.Firefox(
        service=firefox_service, options=firefox_options
    )

    return browser


if __name__ == '__main__':
    browser = chrome_browser('--headless')
    browser.get('https://www.google.com')
    sleep(5)
    browser.quit()
