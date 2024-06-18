import os
import re
import time
from base64 import b64decode

import html_helper
import requests
import website_scraper
from bs4 import BeautifulSoup
from docx import Document


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


def convert_url_to_file_name(url):
    path = url.replace("/", "$$$")
    url = path
    return url


def download_as_xlsl(driver, url, file_path):
    filename = convert_url_to_file_name(url) + ".xlsx"
    # Construct the full save path
    save_path = os.path.join(file_path, filename)

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
                # print(f"Error downloading file: {response.status_code}")
                # print(save_path)

    return ".xlsx"


def download_page_with_requests(driver, url, file_path):
    response = requests.get(url)
    filename = file_path + "/" + website_scraper.convert_url_to_file_name(url) + ".pdf"
    with open(filename, "wb") as file:
        file.write(response.content)
    return ".pdf"


def download_page_using_wkhtmltopdf(driver, url, file_path):
    filename = website_scraper.convert_url_to_file_name(url)
    try:
        html_helper.write_webpage_to_pdf(driver, url, file_path)
        # print("saved pdf")
    except Exception:
        # print("couldnnt save pdf", e)
        pass
    return ".pdf"


def download_page_using_chrome_print(driver, url, file_path):
    driver.get(url)
    pdf_data = driver.execute_cdp_cmd(
        "Page.printToPDF",
        {
            "path": file_path
            + "/"
            + website_scraper.convert_url_to_file_name(url)
            + ".pdf",
            "format": "A4",
        },
    )
    with open(
        file_path + "/" + website_scraper.convert_url_to_file_name(url) + ".pdf",
        "wb",
    ) as f:
        f.write(b64decode(pdf_data["data"]))
    return ".pdf"


def download_page_using_pagesource_to_docx(
    driver,
    url,
    filepath,
):
    driver.implicitly_wait(10)
    # Load the page
    driver.get(url)
    time.sleep(3)
    # Get the page source
    html = driver.page_source

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Extract all the text
    page_text = soup.get_text()
    print(page_text)
    text = clean_text(page_text)
    filename = filepath + "/" + website_scraper.convert_url_to_file_name(url) + ".docx"
    # print(text)
    create_docx(str(text), filename)

    # Close the browser
    driver.quit()
    return ".docx"


def clean_text(text, max_length=100):
    # Define a regex pattern to find long continuous strings without spaces
    pattern = r"\S{%d,}" % max_length
    # Replace matched patterns with empty string
    cleaned_text = re.sub(pattern, "", text)
    return cleaned_text


def create_docx(text, filename):
    doc = Document()
    p = doc.add_paragraph()
    p.add_run(text)
    doc.save(filename)
