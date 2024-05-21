import asyncio
import json
import time

# import selenium_async
from base64 import b64decode

import html_helper
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from UniqueList import UniqueList


# Initialize WebDriver
class WebScraper:
    def __init__(
        self,
        base_url,
        pdf_set,
        url_ulist: UniqueList,
        file_resource_path,
        saved_urls_path,
        index_path,
        isMuniCode,
    ):
        self.base_url = base_url
        self.pdf_set = pdf_set
        self.url_ulist = url_ulist
        self.file_resource_path = file_resource_path
        self.saved_urls_path = saved_urls_path
        self.index_path = index_path
        self.isMuniCode = isMuniCode
        self.recursive_depth = 0

    async def scrape(self, url, driver):
        try:
            driver.get(url)
        except Exception as e:
            print("exception getting url: ", url, e)
            return [], []
        if self.recursive_depth == 0:
            sleep_time = 3
        else:
            sleep_time = 3

        time.sleep(sleep_time)

        pdf_links, new_links = self.scrape_links(driver, url)

        self.save_page_as_pdf(driver, url)
        self.save_pdfs(pdf_links)
        self.add_links_to_url_set(new_links)

        write_list_to_json_file(self.url_ulist, self.saved_urls_path)

    def scrape_links(self, driver, url):
        links = driver.find_elements(By.TAG_NAME, "a")
        input_links = []
        # find links that aren't href but <li> tags
        if url.__contains__("#name="):
            base_url_split = url.split("#name=")[0] + "#name="
            input_tags = driver.find_elements(By.TAG_NAME, "input")
            try:
                input_links_endings = [
                    input.get_attribute("value")
                    for input in input_tags
                    if input.get_attribute("value")
                    and input.get_attribute("name") == "checkedNodes"
                ]
                input_links = [
                    base_url_split + input_link for input_link in input_links_endings
                ]
            except Exception as e:
                print("exception getting input links", e)

        # Filter links ending with .pdf
        try:
            pdf_links = [
                link.get_attribute("href")
                for link in links
                if link.get_attribute("href")
                and link.get_attribute("href").__contains__("pdf")
            ]
        except Exception as e:
            pdf_links = []
            print("exception getting pdf links", e)
        try:
            pdf_links.extend(
                [
                    link.get_attribute("href")
                    for link in links
                    if link.get_attribute("href")
                    and link.get_attribute("href").__contains__("xlsx")
                ]
            )
        except:
            print("exception getting pdf links")

        try:
            pdf_links.extend(
                [
                    link.get_attribute("href")
                    for link in links
                    if link.get_attribute("href")
                    and link.get_attribute("href").__contains__("csv")
                ]
            )
        except:
            print("exception getting pdf links")

        try:
            pdf_links.extend(
                [
                    link.get_attribute("href")
                    for link in links
                    if link.get_attribute("href")
                    and link.get_attribute("href").__contains__("ViewFile")
                ]
            )
        except:
            print("exception getting pdf links")

        try:
            pdf_links.extend(
                [
                    link.get_attribute("href")
                    for link in links
                    if link.get_attribute("href")
                    and link.get_attribute("href").__contains__("View/")
                ]
            )
        except:
            print("exception getting pdf links")
        try:
            pdf_links.extend(
                [
                    link.get_attribute("href")
                    for link in links
                    if link.get_attribute("href")
                    and link.get_attribute("href").__contains__("ADID")
                ]
            )
        except:
            print("exception getting pdf links")
        try:
            other_links = [
                link.get_attribute("href")
                for link in links
                if link.get_attribute("href")
                and link.get_attribute("href").startswith(self.base_url)
            ]
            other_links = cut_out_duplicate_urls(other_links)
        except:
            other_links = []
            print("exception getting other links")
        other_links.extend(input_links)

        return pdf_links, other_links

    def save_pdfs(self, pdf_links):
        if pdf_links:
            for link in pdf_links:
                if link not in self.pdf_set:
                    self.pdf_set.add(link)
                    download_file(link, self.file_resource_path)
                    print(" downloading pdf: ", link)

    def add_links_to_url_set(self, links: UniqueList):
        for link in links:
            if link not in self.url_ulist:
                self.url_ulist.append(link)

    async def recursive_search(self, index):
        # Example usage
        print("index: ", index, "of ", len(self.url_ulist))
        write_index_to_json(index, self.index_path)
        if index >= len(self.url_ulist):
            return "Done"

        if len(self.url_ulist) - index > 5:
            range_end = 5
        else:
            range_end = 1

        tasks = []
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless")

        drivers = [webdriver.Chrome(chrome_options) for _ in range(5)]
        for i in range(range_end):
            tasks.append(
                asyncio.create_task(self.scrape(self.url_ulist[index], drivers[i]))
            )
            index += 1
        await asyncio.gather(*tasks)

        for driver in drivers:
            driver.quit()

        self.recursive_depth += 1

        return await self.recursive_search(index)

    def save_page_as_pdf(self, driver, url):
        if self.isMuniCode:
            filename = convert_url_to_file_name(driver.current_url)
            save_path = self.file_resource_path + "/" + filename + ".pdf"
            try:
                html_helper.write_webpage_to_pdf(None, url, save_path)
            except Exception as e:
                print("couldnnt save pdf", e)
                # pass
            return save_path
        else:
            pdf_data = driver.execute_cdp_cmd(
                "Page.printToPDF",
                {
                    "path": self.file_resource_path
                    + "/"
                    + convert_url_to_file_name(url)
                    + ".pdf",
                    "format": "A4",
                },
            )
            with open(
                self.file_resource_path + "/" + convert_url_to_file_name(url) + ".pdf",
                "wb",
            ) as f:
                f.write(b64decode(pdf_data["data"]))


# url_save_pdf_path ='murray-url-resources'
# Function to find PDF links on a page
def find_pdf_links(
    url, base_url, driver=None, sleep_time=2, file_resource_path="slco-resources"
):
    print("url: ", url)
    print("base_url: ", base_url)
    # driver = webdriver.Chrome()
    try:
        driver.get(url)
    except Exception as e:
        print("exception getting url: ", url, e)
        return [], []
    # Wait for the page to load. Adjust time as necessary for dynamic content.
    time.sleep(sleep_time)
    # html_helper.write_webpage_to_pdf(driver,url,file_resource_path)
    filename = convert_url_to_file_name(driver.current_url)
    save_path = file_resource_path + "/" + filename + ".pdf"
    try:
        # print('drivere infooo: ',driver.page_source)
        # pdfkit.from_string(driver.page_source,save_path )
        html_helper.write_webpage_to_pdf(None, url, save_path)
    except Exception as e:
        print("couldnnt save pdf", e)
        # pass
    # Find all <a> tags

    links = driver.find_elements(By.TAG_NAME, "a")
    input_links = []
    if url.__contains__("#name="):
        base_url = url.split("#name=")[0] + "#name="
        input_tags = driver.find_elements(By.TAG_NAME, "input")
        try:
            input_links_endings = [
                input.get_attribute("value")
                for input in input_tags
                if input.get_attribute("value")
                and input.get_attribute("name") == "checkedNodes"
            ]
            input_links = [base_url + input_link for input_link in input_links_endings]
            # print('input_links: ',input_links)
        except Exception as e:
            print("exception getting input links", e)

    # Filter links ending with .pdf
    try:
        pdf_links = [
            link.get_attribute("href")
            for link in links
            if link.get_attribute("href")
            and link.get_attribute("href").__contains__("pdf")
        ]
    except Exception as e:
        pdf_links = []
        print("exception getting pdf links", e)
    try:
        pdf_links.extend(
            [
                link.get_attribute("href")
                for link in links
                if link.get_attribute("href")
                and link.get_attribute("href").__contains__("xlsx")
            ]
        )
    except:
        print("exception getting pdf links")

    try:
        pdf_links.extend(
            [
                link.get_attribute("href")
                for link in links
                if link.get_attribute("href")
                and link.get_attribute("href").__contains__("csv")
            ]
        )
    except:
        print("exception getting pdf links")

    try:
        pdf_links.extend(
            [
                link.get_attribute("href")
                for link in links
                if link.get_attribute("href")
                and link.get_attribute("href").__contains__("ViewFile")
            ]
        )
    except:
        print("exception getting pdf links")

    try:
        pdf_links.extend(
            [
                link.get_attribute("href")
                for link in links
                if link.get_attribute("href")
                and link.get_attribute("href").__contains__("View/")
            ]
        )
    except:
        print("exception getting pdf links")
    try:
        pdf_links.extend(
            [
                link.get_attribute("href")
                for link in links
                if link.get_attribute("href")
                and link.get_attribute("href").__contains__("ADID")
            ]
        )
    except:
        print("exception getting pdf links")
    try:
        other_links = [
            link.get_attribute("href")
            for link in links
            if link.get_attribute("href")
            and link.get_attribute("href").startswith(base_url)
        ]
        other_links = cut_out_duplicate_urls(other_links)
    except:
        other_links = []
        print("exception getting other links")
    other_links.extend(input_links)
    # driver.quit()
    return [pdf_links, other_links]


def write_index_to_json(index, file_path="index.json"):
    # Writing the index to a JSON file
    with open(file_path, "w") as file:
        json.dump(index, file)


def read_index_from_json(file_path="index.json"):
    try:
        # Reading the index from a JSON file
        with open(file_path, "r") as file:
            index = json.load(file)

        return index
    except:
        return 0


def write_urls_to_json(urls, file_path="urls.json"):
    # Example set of URLs
    import json

    # Convert the set to a list
    urls_list = list(urls)

    # Writing the list to a JSON file
    with open(file_path, "w") as file:
        json.dump(urls_list, file)


def convert_url_to_file_name(url):
    path = url.replace("/", "$$$")
    url = path
    return url


def convert_file_name_to_url(path):
    url = path.replace("$$$", "/")
    if url.endswith(".pdf"):
        url = url[:-4]
    if url.endswith(".xlsx"):
        url = url[:-5]
    return url


def read_filenames_from_dir(directory):
    import os

    try:
        file_list = os.listdir(directory)
        return file_list
    except:
        return []


def read_urls_from_json(file_path="urls.json"):
    import json

    try:
        # Reading the URLs from a JSON file
        with open(file_path, "r") as file:
            urls_list = json.load(file)

        return urls_list
    except:
        return []


def download_file(url, directory, extension=".pdf"):
    """Downloads a file (PDF or spreadsheet) from the given URL and saves it to the specified directory.

    Args:
      url: The URL of the file.
      directory: The directory path where the file should be saved.
    """
    import os

    import requests

    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    # Send a HEAD request to get the content type
    # head_response = requests.head(url)
    # content_type = head_response.headers.get('Content-Type', '').lower()

    filename = convert_url_to_file_name(url) + extension

    # Construct the full save path
    save_path = os.path.join(directory, filename)

    # Send a GET request to download the file
    try:
        response = requests.get(url, stream=True)
    except Exception:
        print("exception requesting pdf: ", url)
        return

    # Check for successful response
    if response.status_code == 200:
        # Open the file in binary write mode
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(1024):
                # Write the downloaded data in chunks
                file.write(chunk)
        if not is_valid_pdf(save_path):
            os.remove(save_path)
            filename = convert_url_to_file_name(url) + ".xlsx"
            # Construct the full save path
            save_path = os.path.join(directory, filename)

            # Send a GET request to download the file
            response = requests.get(url, stream=True)
            # Check for successful response
            if response.status_code == 200:
                # Open the file in binary write mode
                with open(save_path, "wb") as file:
                    for chunk in response.iter_content(1024):
                        # Write the downloaded data in chunks
                        file.write(chunk)
                    if not is_valid_xlsx(save_path):
                        os.remove(save_path)
                        print(f"Error downloading file: {response.status_code}")
                        print(save_path)
                        return
        print(f"File downloaded successfully: {save_path}")
    else:
        print(f"Error downloading file: {response.status_code}")


def is_valid_pdf(file_path):
    import PyPDF2

    """Check if the file at `file_path` is a valid PDF.
    
    Args:
        file_path (str): The path to the PDF file to check.
        
    Returns:
        bool: True if the file is a valid PDF, False otherwise.
    """

    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)

            # Check for basic validity and readability:
            if len(reader.pages) > 0:
                return True
            else:
                return False

    except PyPDF2.errors.PdfReadError as e:
        print(f"Error reading PDF: {e}")  # Specific error message
        return False

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return False

    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


def write_list_to_json_file(url_ulist: UniqueList, file_path):
    """
    Writes a list to a JSON file.

    Args:
      lst: The list to be written.
      file_path: The path of the JSON file.
    """
    with open(file_path, "w") as file:
        json.dump(url_ulist.lst, file)


def is_valid_xlsx(file_path):
    import openpyxl

    """Check if the file at `file_path` is a valid XLSX file.
    
    Args:
        file_path (str): The path to the XLSX file to check.
        
    Returns:
        bool: True if the file is a valid XLSX file, False otherwise.
    """
    try:
        workbook = openpyxl.load_workbook(file_path)
        return True
    except:
        return False


def get_final_url(url):
    import requests

    """
  Fetches the final URL after following redirects.

  Args:
      url: The initial URL to follow.

  Returns:
      The final URL after following redirects.
  """
    try:
        response = requests.get(url, allow_redirects=True)
    except requests.exceptions.RequestException as e:
        print("eeee", e.args[0])
        error_message = str(e.args[0])  # Convert the first argument to a string
        host = error_message.split("'")[1]  # Split by single quotes to extract the host
        start_of_text = error_message.find("url: ") + 5
        subset_of_url_text = error_message[start_of_text:]
        end_of_text = subset_of_url_text.find(" (")
        url = subset_of_url_text[:end_of_text]
        # url = error_message.split("'")[3].split("(")[0].strip()  # Extract URL
        print(f"Host: {host}")
        print(f"URL: {url}")
        return host + url
    return response.url


def take_out_all_contentid(url):
    if url.__contains__("?contentId="):
        url = url.split("?contentId=")[0]
    return url


def cut_out_duplicate_urls(url_list):
    for i in range(len(url_list)):
        url_list[i] = take_out_all_contentid(url_list[i])
    url_list = list(set(url_list))
    return url_list


def main():
    url = "https://www.murray.utah.gov/"
    saved_urls_path = "murray.json"
    resource_path = "murray-resources"
    index_path = "index.json"
    isMuniCode = False

    url = "https://codelibrary.amlegal.com/codes/murrayut/latest/"
    saved_urls_path = "murray_muni.json"
    resource_path = "murray-muni-resources"
    index_path = "muni_index.json"
    isMuniCode = True

    url_list = read_urls_from_json(saved_urls_path)
    if not url_list:
        url_list.append(url)
    url_ulist = UniqueList(url_list)
    # url_set = set(url_list)
    pdf_set = set()
    pdf_list = read_filenames_from_dir(resource_path)
    pdf_set = set(pdf_list)

    web_scraper = WebScraper(
        base_url=url,
        pdf_set=pdf_set,
        url_ulist=url_ulist,
        file_resource_path=resource_path,
        saved_urls_path=saved_urls_path,
        index_path=index_path,
        isMuniCode=isMuniCode,
    )

    start_index = read_index_from_json(index_path)
    done = None

    while done is None:
        try:
            done = asyncio.run(web_scraper.recursive_search(start_index))
        except RecursionError as e:
            start_index = read_index_from_json(index_path)
            print("recursion error", e)
            pass

    print(done)


if __name__ == "__main__":
    main()
