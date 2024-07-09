import os
import re

# import fitz
import fitz
import openpyxl
from docx import Document


def chunk_file_into_paragraphs(file_path):
    """Chunks a file into paragraphs."""
    if file_path.endswith(".pdf"):
        return chunk_pdf_into_paragraphs(file_path)
    elif (
        file_path.endswith(".xlsx")
        or file_path.endswith(".xls")
        or file_path.endswith(".xlsm")
        or file_path.endswith(".csv")
    ):
        return chunk_xlsx_into_paragraphs(file_path)
    elif file_path.endswith(".docx") or file_path.endswith(".doc"):
        return chunk_docx_into_paragraphs(file_path)
    else:
        return []


def chunk_xlsx_into_paragraphs(xlsx_path):
    """Chunks an XLSX file into paragraphs."""
    try:
        chunks = []

        # Open the XLSX file
        xlsx_document = openpyxl.load_workbook(xlsx_path)
        sheet = xlsx_document.active

        paragraph_number = 0
        labels = []
        for row in sheet.iter_rows(
            min_row=1, max_row=sheet.max_row, max_col=sheet.max_column
        ):
            paragraph = ""
            for i, cell in enumerate(row):
                if paragraph_number == 0:
                    labels.append(cell.value)
                elif cell.value:
                    paragraph += str(labels[i]) + ": " + str(cell.value) + ", "
            if paragraph_number > 0:
                chunk = [xlsx_path, 1, paragraph_number, paragraph]
                chunks.append(chunk)
            paragraph_number += 1
        return chunks
    except Exception:
        return []


def chunk_pdf_into_paragraphs(pdf_path):
    """Chunks a PDF into paragraphs."""
    chunks = []

    # Open the PDF file
    try:
        pdf_document = fitz.open(pdf_path)
    except Exception:
        return []

    paragraph_number = 0

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text = page.get_text("text")
        # text_length = len(text)
        paragraphs = re.split(r"(?<=[.!?])\s*\n", text)
        # if len(paragraphs) < text_length / 500:
        #     extra_splitted = []
        #     for paragraph in paragraphs:
        #         # split paragraph by single newline but keep paragraphs one list
        #         extra_splitted.extend(paragraph.split("\n"))
        #     paragraphs = extra_splitted

        for paragraph in paragraphs:
            if paragraph.strip():  # Only process non-empty paragraphs
                paragraph_number += 1
                chunk = [pdf_path, page_num, paragraph_number, paragraph.strip()]
                chunks.append(chunk)
                # print("paragraph:", paragraph.strip())
        # print("paragraph_number:", paragraph_number)
    return chunks


def get_all_pdfs(folder_path):
    """Get all PDF files in a folder."""
    # List all files and directories in the given folder
    items = os.listdir(folder_path)

    # Filter out the PDFs
    pdfs = [
        item
        for item in items
        if item.endswith(".pdf") and os.path.isfile(os.path.join(folder_path, item))
    ]

    return pdfs


def get_all_files_with_full_path(folder_path):
    """Get all files in a folder."""
    # List all files and directories in the given folder
    items = os.listdir(folder_path)

    # Filter out the PDFs
    files = [
        os.path.join(folder_path, item)
        for item in items
        if os.path.isfile(os.path.join(folder_path, item))
    ]

    return files


def get_all_xlsx(folder_path):
    """Get all XLSX files in a folder."""
    xlsx_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".xlsx"):
                xlsx_files.append(os.path.join(root, file))
    return xlsx_files


def get_all_docs(folder_path):
    """Get all DOCX files in a folder."""
    doc_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".docx"):
                doc_files.append(os.path.join(root, file))
    return doc_files


def chunk_docx_into_paragraphs(docx_path):
    """Chunks a DOCX file into paragraphs."""
    chunks = []

    # Open the DOCX file
    try:
        doc = Document(docx_path)
    except Exception:
        return []

    paragraph_number = 0

    for para in doc.paragraphs:
        paragraphs = para.text.split("\n")
        for p in paragraphs:
            paragraph_number += 1
            if p.strip():
                cleaned_lines = p.replace("\xa0", " ")
                chunk = [docx_path, 1, paragraph_number, cleaned_lines]
                chunks.append(chunk)
    # print("chunks", chunks)
    return chunks


def check_validity_of_file(file_path, chunks=None):
    if chunks is None:
        if file_path.endswith(".pdf"):
            chunks = chunk_pdf_into_paragraphs(file_path)
        elif file_path.endswith(".xlsx"):
            chunks = chunk_xlsx_into_paragraphs(file_path)
        elif file_path.endswith(".docx"):
            chunks = chunk_docx_into_paragraphs(file_path)

    total_text = ""
    for chunk in chunks:
        total_text += chunk[3]

    if is_mostly_binary(total_text):
        return 0
    if text_is_too_short(total_text):
        return 0
    return len(total_text)


def text_is_too_short(text, threshold=100):
    return len(text) < threshold


def is_mostly_binary(text, threshold=0.5):
    # Count non-printable characters
    non_printable_count = sum(
        1 for char in text if not (32 <= ord(char) <= 126 or char in "\n\r\t")
    )

    # Calculate the proportion of non-printable characters
    if len(text) == 0:
        return True
    binary_ratio = non_printable_count / len(text)

    # Determine if the text is mostly binary
    return binary_ratio > threshold


# Example usage

if __name__ == "__main__":
    pdf_path = "chat_server/chat/file_resources/murray-muni-resources/https:$$$$$$codelibrary.amlegal.com$$$codes$$$murrayut$$$latest$$$murray_ut$$$0-0-0-14#codecontent.pdf"
    pdf_path = "asdfasdf/test.pdf"
    pdf_path = "pathpath/https:$$$$$$www.murray.utah.gov$$$ArchiveCenter$$$ViewFile$$$Item$$$87.pdf"
    pdf_path = "pathpath/https:$$$$$$codelibrary.amlegal.com$$$codes$$$murrayut$$$latest$$$murray_ut$$$0-0-0-4630.pdf"
    pdf_path = "pathpathpath/https:$$$$$$codelibrary.amlegal.com$$$codes$$$murrayut$$$latest$$$murray_ut$$$0-0-0-4630.pdf"
    # Extract text from PDF
    # extracted_text = chunk_docx_into_paragraphs(pdf_path)
    validity = check_validity_of_file(pdf_path)
    # print(validity)
# main()
# chunk_docx_into_paragraphs("test.docx")


# chunk_pdf_into_paragraphs(pdf_path, "end_sentence_newline")
# xl_path = "chat_server/chat/file_resources/gunnison-resources/https:$$$$$$www.gunnisoncounty.org$$$DocumentCenter$$$View$$$14027$$$Public-Data---VALUES-2824.xlsx"
# chunks = chunk_xlsx_into_paragraphs(xl_path)
# for i in range(10):
#     print(chunks[i])
