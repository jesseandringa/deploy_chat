import asyncio
import time
from base64 import b64decode

from selenium import webdriver

# import b64decode
number = 1


async def open_url(driver, url, index):
    if driver is None:
        return
    # try:
    driver.get(url)
    time.sleep(3)
    # print('driver.pag_source', driver.page_source)
    pdf_data = driver.execute_cdp_cmd(
        "Page.printToPDF", {"path": "output" + str(index) + ".pdf", "format": "A4"}
    )
    # pdf_data = b64decode(driver.print_page())

    # Decode Base64 data and save the PDF

    with open("output" + str(index) + ".pdf", "wb") as f:
        f.write(b64decode(pdf_data["data"]))
        # print("Opened",driver.title)
    # except Exception as e:
    #     print("An error occurred:", e)


async def main():
    tasks = []
    urls = [
        "https://www.murray.utah.gov/349/City-Attorney",
        "https://www.murray.utah.gov/393/Useful-Government-Links",
        "https://www.murray.utah.gov/264/Committee-of-the-Whole",
        "https://www.murray.utah.gov/975/Pay-Court-FinesFees",
        "https://www.murray.utah.gov/140/Senior-Recreation-Center",
        "https://www.murray.utah.gov/266/Council-Messages",
        "https://www.murray.utah.gov/158/Community-Economic-Development",
        "https://www.murray.utah.gov/210/Public-Works",
    ]  # Replace with your URLs
    drivers = [webdriver.Chrome() for _ in urls]  # Launch browsers

    for i in range(len(drivers)):
        # driver = webdriver.Chrome()
        tasks.append(asyncio.create_task(open_url(drivers[i], urls[i], i)))

    await asyncio.gather(*tasks)  # Wait for all tasks to finish

    for driver in drivers:
        driver.quit()  # Close browsers
    return "done"


def actual_main():
    z = asyncio.run(main())
    print(z)
    # print('z', z)


if __name__ == "__main__":
    actual_main()
    # print(z)
