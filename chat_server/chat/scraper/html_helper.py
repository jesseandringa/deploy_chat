import base64
import json
import logging
import time
from io import BytesIO
from typing import List

import pdfkit
import website_scraper
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(
    filename="error.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class PdfGenerator:
    """
    Simple use case:
       pdf_file = PdfGenerator(['https://google.com']).main()
       with open('new_pdf.pdf', "wb") as outfile:
           outfile.write(pdf_file[0].getbuffer())
    """

    driver = None
    sleep_time = 4
    # https://chromedevtools.github.io/devtools-protocol/tot/Page#method-printToPDF
    print_options = {
        "landscape": False,
        "displayHeaderFooter": True,
        "printBackground": True,
        "preferCSSPageSize": False,
        "paperWidth": 6.97,
        "paperHeight": 16.5,
    }

    def __init__(self, urls: List[str]):
        self.urls = urls

    def _get_pdf_from_url(self, url, *args, **kwargs):
        self.driver.get(url)
        time.sleep(self.sleep_time)
        # pdfkit.from_url(url, 'url.pdf')
        try:
            pdfkit.from_string(
                self.driver.page_source, "millcreek-muni-resources/page_source.pdf"
            )
        except Exception as e:
            print("eeeeerrrrrroooooorrrrrr", e)
        print_options = self.print_options.copy()
        result = self._send_devtools(self.driver, "Page.printToPDF", print_options)
        return base64.b64decode(result["data"])

    @staticmethod
    def _send_devtools(driver, cmd, params):
        """
        Works only with chromedriver.
        Method uses cromedriver's api to pass various commands to it.
        """
        resource = (
            "/session/%s/chromium/send_command_and_get_result" % driver.session_id
        )
        url = driver.command_executor._url + resource
        body = json.dumps({"cmd": cmd, "params": params})
        response = driver.command_executor._request("POST", url, body)
        # print('response',response.get('value'))
        return response.get("value")

    def _generate_pdfs(self):
        pdf_files = []

        for url in self.urls:
            result = self._get_pdf_from_url(url)
            file = BytesIO()
            file.write(result)
            pdf_files.append(file)

        return pdf_files

    def main(self, driver=None) -> List[BytesIO]:
        self.sleep_time = 5
        if driver is None:
            webdriver_options = ChromeOptions()

            webdriver_options.add_argument("--headless")
            # webdriver_options.add_argument('--window-size=1920,1080')
            # webdriver_options.add_argument('--disable-gpu')
            self.driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=webdriver_options,
            )
        else:
            self.driver = driver
        try:
            result = self._generate_pdfs()
        except Exception as e:
            print("an error occured using driver", e)
            logging.error("An error occurred: %s", e, exc_info=True)
        self.driver.quit()
        return result


def write_webpage_to_pdf(driver, url, save_path):
    try:
        # url = driver.current_url
        pdf_file = PdfGenerator([url]).main(driver)
        filename = website_scraper.convert_url_to_file_name(url)

        print("path", save_path)
        with open(save_path, "wb") as outfile:
            outfile.write(pdf_file[0].getbuffer())
    except Exception as e:
        logging.error("An error occurred: %s", e, exc_info=True)
        logging.error(f"Could not convert {url} to pdf")


if __name__ == "__main__":
    driver = webdriver.Chrome()
    file = "https://codelibrary.amlegal.com/codes/murrayut/latest/"
    driver.get(file)
    file = driver.current_url
    try:
        pdf_file = PdfGenerator([file]).main(driver)
        filename = website_scraper.convert_url_to_file_name(file)
        with open("xxxxxx/" + filename + ".pdf", "wb") as outfile:
            outfile.write(pdf_file[0].getbuffer())
            print("written pdf with index")
    except Exception as e:
        print("error", e)
