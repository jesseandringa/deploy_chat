# import hashlib
# import os

# from PyPDF2 import PdfReader


# def get_pdf_content(pdf_path):
#     with open(pdf_path, "rb") as file:
#         reader = PdfReader(file)
#         text = ""
#         for page_num in range(len(reader.pages)):
#             text += reader.pages[page_num].extract_text()
#         return text


# def remove_duplicate_pdfs(folder_path):
#     unique_pdfs = {}
#     duplicate_files = []

#     for filename in os.listdir(folder_path):
#         if filename.endswith(".pdf"):
#             file_path = os.path.join(folder_path, filename)
#             content = get_pdf_content(file_path)
#             hash_value = hashlib.md5(content.encode()).hexdigest()

#             if hash_value in unique_pdfs:
#                 duplicate_files.append(file_path)
#                 print(f"Duplicate file found: {file_path}")
#             else:
#                 unique_pdfs[hash_value] = file_path

#     for duplicate_file in duplicate_files:
#         print(f"Removing duplicate file: {duplicate_file}")
#         os.remove(duplicate_file)


# # Usage
# folder_path = "sandy_muni_url_pdfs"
# remove_duplicate_pdfs(folder_path)
