import asyncio
import json
import os
import sys
import threading
import time

# import selenium_async
import downloader
import file_reader
from casey_move_pdfs import move_all_pdfs_from_folder_to_folder
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from UniqueList import UniqueList

# from chat_server.chat.src import postgres
# from chat_server.chat.src import localpg


# from UniqueList import UniqueList


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

    def scrape(self, url, driver, thread_num):
        try:
            driver.get(url)
        except KeyboardInterrupt:
            print("\nProgram interrupted with Control-C")
            sys.exit(1)
        except Exception as e:
            if "ERR_INTERNET_DISCONNECTED" in str(e):
                print("Error no internet")
                sys.exit(1)
            print("exception getting url: ", url, e)
            return [], []
        if self.recursive_depth == 0:
            sleep_time = 3
        else:
            sleep_time = 3

        time.sleep(sleep_time)

        pdf_links, new_links = self.scrape_links(driver, url)

        self.save_page_as_pdf(driver, url, self.file_resource_path)
        self.save_pdfs(pdf_links, thread_num)
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
            except KeyboardInterrupt:
                print("\nProgram interrupted with Control-C")
                sys.exit(1)
            except Exception as e:
                print(f"exception getting input links{type(e).__name__}")

        # Filter links ending with .pdf
        try:
            pdf_links = [
                link.get_attribute("href")
                for link in links
                if link.get_attribute("href")
                and link.get_attribute("href").__contains__("pdf")
            ]
        except KeyboardInterrupt:
            print("\nProgram interrupted with Control-C")
            sys.exit(1)
        except Exception as e:
            pdf_links = []
            print(f"exception getting pdf links{type(e).__name__}")
        try:
            pdf_links.extend(
                [
                    link.get_attribute("href")
                    for link in links
                    if link.get_attribute("href")
                    and link.get_attribute("href").__contains__("xlsx")
                ]
            )
        except KeyboardInterrupt:
            print("\nProgram interrupted with Control-C")
            sys.exit(1)
        except Exception as e:
            print(f"exception getting pdf links {type(e).__name__}")

        try:
            pdf_links.extend(
                [
                    link.get_attribute("href")
                    for link in links
                    if link.get_attribute("href")
                    and link.get_attribute("href").__contains__("csv")
                ]
            )
        except KeyboardInterrupt:
            print("\nProgram interrupted with Control-C")
            sys.exit(1)
        except Exception as e:
            print(f"exception getting pdf links {type(e).__name__}")

        try:
            pdf_links.extend(
                [
                    link.get_attribute("href")
                    for link in links
                    if link.get_attribute("href")
                    and link.get_attribute("href").__contains__("ViewFile")
                ]
            )
        except KeyboardInterrupt:
            print("\nProgram interrupted with Control-C")
            sys.exit(1)
        except Exception as e:
            print(f"exception getting pdf links {type(e).__name__}")

        try:
            pdf_links.extend(
                [
                    link.get_attribute("href")
                    for link in links
                    if link.get_attribute("href")
                    and link.get_attribute("href").__contains__("View/")
                ]
            )
        except KeyboardInterrupt:
            print("\nProgram interrupted with Control-C")
            sys.exit(1)
        except Exception as e:
            print(f"exception getting pdf links {type(e).__name__}")
        try:
            pdf_links.extend(
                [
                    link.get_attribute("href")
                    for link in links
                    if link.get_attribute("href")
                    and link.get_attribute("href").__contains__("ADID")
                ]
            )
        except KeyboardInterrupt:
            print("\nProgram interrupted with Control-C")
            sys.exit(1)
        except Exception as e:
            print(f"exception getting pdf links {type(e).__name__}")
        try:
            other_links = [
                link.get_attribute("href")
                for link in links
                if link.get_attribute("href")
                and link.get_attribute("href").startswith(self.base_url)
            ]
            other_links = cut_out_duplicate_urls(other_links)
        except KeyboardInterrupt:
            print("\nProgram interrupted with Control-C")
            sys.exit(1)
        except Exception as e:
            other_links = []
            print(f"exception getting other links {type(e).__name__}")
        other_links.extend(input_links)

        return pdf_links, other_links

    def save_pdfs(self, pdf_links, thread_num):
        threads = []
        threads = []
        results = []
        # if len(pdf_links) > 3:
        #     for i, url in enumerate(
        #         pdf_links
        #     ):  # Example: Perform actions in {range_end} threads
        #         if url not in self.pdf_set:
        #             self.pdf_set.add(url)
        #             # print(" downloading pdf: ", url)
        #             thread = threading.Thread(
        #                 target=lambda: results.append(
        #                     download_file(url, self.file_resource_path, False)
        #                 )
        #             )
        #         threads.append(thread)
        #         thread.start()

        #     # Wait for all threads to complete actions
        #     for thread in threads:
        #         thread.join()
        total_saved = 0
        if pdf_links:
            for url in pdf_links:
                temp_url = convert_file_name_to_url(url)
                if temp_url not in self.pdf_set:
                    if "newsletters#" in url:
                        continue
                    if "/bulletins/" in url:
                        continue
                    if url.endswith("MediaFileFormat=wmv"):
                        continue
                    if url.endswith("MediaFileFormat=mp4"):
                        continue
                    if url.endswith("MediaFileFormat=ismv"):
                        continue

                    # print("trying to downloading pdf in thread : ", thread_num, url)
                    self.pdf_set.add(url)
                    # print(" downloading pdf: ", url)
                    result = download_file(url, self.file_resource_path, False)
                    # print(f"result:{result} in thread {thread_num}")
                    total_saved += result  # 1 if successful, 0 if not

        print("total saved from thread: ", total_saved, thread_num)

    def add_links_to_url_set(self, links: UniqueList):
        for link in links:
            if link not in self.url_ulist:
                self.url_ulist.append(link)

    async def recursive_search(self, index):
        # Example usage
        start_time = time.time()
        print("index: ", index, "of ", len(self.url_ulist))
        write_index_to_json(index, self.index_path)
        if index >= len(self.url_ulist):
            return "Done"

        if len(self.url_ulist) - index > 20:
            range_end = 20
        else:
            range_end = len(self.url_ulist) - index

        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless")

        drivers = [webdriver.Chrome(chrome_options) for _ in range(range_end)]

        threads = []
        results = []
        for i in range(range_end):  # Example: Perform actions in {range_end} threads
            thread = threading.Thread(
                target=lambda: results.append(
                    self.scrape(self.url_ulist[index], drivers[i], i)
                )
            )
            threads.append(thread)
            thread.start()
            index += 1

        # Wait for all threads to complete actions
        for thread in threads:
            thread.join()

        for driver in drivers:
            driver.quit()
        end_time = time.time()
        print("\n\n")
        time_taken = (end_time - start_time) / range_end
        print("Time taken per page: ", time_taken)
        print("\n\n")

        # move all pdfs that are out of place into correct place
        move_all_pdfs_from_folder_to_folder(
            "./", self.file_resource_path, self.pdf_set, True
        )

        self.recursive_depth += 1

        return await self.recursive_search(index)

    def save_page_as_pdf(self, driver, url, directory):
        result = download_file(url, directory, is_html_page=True)
        print(f"result:{bool(result)} for {url}")


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
    except KeyboardInterrupt:
        print("\nProgram interrupted with Control-C")
        sys.exit(1)
    except Exception:
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
    except KeyboardInterrupt:
        print("\nProgram interrupted with Control-C")
        sys.exit(1)
    except Exception:
        return []


def read_urls_from_json(file_path="urls.json"):
    try:
        # Reading the URLs from a JSON file
        with open(file_path, "r") as file:
            urls_list = json.load(file)
        # print("urls_list: ", urls_list)
        return urls_list
    except KeyboardInterrupt:
        print("\nProgram interrupted with Control-C")
        sys.exit(1)
    except Exception:
        return []


def download_file(url, directory, is_html_page=False):
    file_path = downloader.trim_filename(url)
    file_path = directory + "/" + convert_url_to_file_name(file_path)
    # print("file_path: ", file_path)
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options)

    os.makedirs(directory, exist_ok=True)
    # filename = convert_url_to_file_name(url) + extension
    validity = []
    if is_html_page:
        funcs = [
            # downloader.download_page_with_requests,
            downloader.download_page_using_chrome_print,
            # downloader.download_page_using_wkhtmltopdf,
            downloader.download_page_using_pagesource_to_docx,
        ]
    else:
        funcs = [
            downloader.download_page_with_requests,
            downloader.download_page_using_chrome_print,
            # downloader.download_page_using_wkhtmltopdf,
            downloader.download_page_using_pagesource_to_docx,
            downloader.download_as_xlsl,
        ]
    pdfs = file_reader.get_all_pdfs(".")
    num_pdfs_before = len(pdfs)
    for i in range(len(funcs)):
        # print("trying: ", str(funcs[i]))
        try:
            extension = funcs[i](driver, url, directory)
        except KeyboardInterrupt:
            print("\nProgram interrupted with Control-C")
            sys.exit(1)
        except Exception:
            extension = ".xlsx"
        temp_file = file_path + extension
        try:
            validity.append(file_reader.check_validity_of_file(temp_file))
        except KeyboardInterrupt:
            print("\nProgram interrupted with Control-C")
            sys.exit(1)
        except Exception:
            validity.append(0)
    # print("validity: ", validity)
    max_value = max(validity)
    delete_file(file_path + ".pdf")
    delete_file(file_path + ".docx")
    delete_file(file_path + ".xlsx")

    pdfs = file_reader.get_all_pdfs(".")
    num_pdfs_after = len(pdfs)
    if num_pdfs_after > num_pdfs_before:
        found = False
        for i in range(num_pdfs_after):
            if pdfs[i].lower() in file_path.lower():
                file_path = downloader.trim_filename(pdfs[i])
                dir_name = os.path.dirname(pdfs[i])
                new_path = os.path.join(dir_name, file_path + ".pdf")
                os.rename(pdfs[i], new_path)
                found = True
        if found:
            return 1
    index = 0
    if max_value > 0:
        index = validity.index(max_value)
        funcs[index](driver, url, directory)
        return 1
    return 0


def delete_file(filepath):
    try:
        os.remove(filepath)
    except FileNotFoundError:
        pass
    except PermissionError:
        pass
    except KeyboardInterrupt:
        print("\nProgram interrupted with Control-C")
        sys.exit(1)


# def download_file(url, directory, extension=".pdf"):
#     """Downloads a file (PDF or spreadsheet) from the given URL and saves it to the specified directory.

#     Args:
#       url: The URL of the file.
#       directory: The directory path where the file should be saved.
#     """
#     import os

#     import requests

#     # Create the directory if it doesn't exist
#     os.makedirs(directory, exist_ok=True)

#     # Send a HEAD request to get the content type
#     # head_response = requests.head(url)
#     # content_type = head_response.headers.get('Content-Type', '').lower()

#     filename = convert_url_to_file_name(url) + extension

#     # Construct the full save path
#     save_path = os.path.join(directory, filename)

#     # Send a GET request to download the file
#     try:
#         response = requests.get(url, stream=True)
#     except Exception:
#         print("exception requesting pdf: ", url)
#         return

#     # Check for successful response
#     if response.status_code == 200:
#         # Open the file in binary write mode
#         with open(save_path, "wb") as file:
#             for chunk in response.iter_content(1024):
#                 # Write the downloaded data in chunks
#                 file.write(chunk)
#         if not is_valid_pdf(save_path):
#             os.remove(save_path)
#             filename = convert_url_to_file_name(url) + ".xlsx"
#             # Construct the full save path
#             save_path = os.path.join(directory, filename)

#             # Send a GET request to download the file
#             response = requests.get(url, stream=True)
#             # Check for successful response
#             if response.status_code == 200:
#                 # Open the file in binary write mode
#                 with open(save_path, "wb") as file:
#                     for chunk in response.iter_content(1024):
#                         # Write the downloaded data in chunks
#                         file.write(chunk)
#                     if not is_valid_xlsx(save_path):
#                         os.remove(save_path)
#                         print(f"Error downloading file: {response.status_code}")
#                         print(save_path)
#                         return
#         print(f"File downloaded successfully: {save_path}")
#     else:
#         print(f"Error downloading file: {response.status_code}")


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
    except KeyboardInterrupt:
        print("\nProgram interrupted with Control-C")
        sys.exit(1)
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
    except KeyboardInterrupt:
        print("\nProgram interrupted with Control-C")
        sys.exit(1)
    except Exception:
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
    except KeyboardInterrupt:
        print("\nProgram interrupted with Control-C")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        # print("eeee", e.args[0])
        error_message = str(e.args[0])  # Convert the first argument to a string
        host = error_message.split("'")[1]  # Split by single quotes to extract the host
        start_of_text = error_message.find("url: ") + 5
        subset_of_url_text = error_message[start_of_text:]
        end_of_text = subset_of_url_text.find(" (")
        url = subset_of_url_text[:end_of_text]
        # url = error_message.split("'")[3].split("(")[0].strip()  # Extract URL
        # print(f"Host: {host}")
        # print(f"URL: {url}")
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
    ############ CASEY change these ##################
    url = "https://library.municode.com/al/cullman/codes/code_of_ordinances"
    saved_urls_path = "chat_server/chat/cullman-al.json"
    resource_path = "chat_server/chat/file_resources/cullman-al-resources"
    index_path = "chat_server/chat/muni_index.json"
    isMuniCode = True
    ##################################################

    url_list = read_urls_from_json(saved_urls_path)
    # print("url_list", url_list)
    if not url_list:
        url_list.append(url)
    url_ulist = UniqueList(url_list)
    # print(url_list)
    pdf_set = set()
    pdf_list = read_filenames_from_dir(resource_path)
    print("pdf_list: ", pdf_list)
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
        except KeyboardInterrupt:
            print("\nProgram interrupted with Control-C")
            sys.exit(1)
        except RecursionError as e:
            start_index = read_index_from_json(index_path)
            print("recursion error", e)
            pass
    write_index_to_json(0, index_path)
    print(done)


if __name__ == "__main__":
    main()
