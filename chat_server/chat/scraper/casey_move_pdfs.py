import os
import shutil

import file_reader


def move_all_pdfs_from_folder_to_folder(
    source_folder, destination_folder, pdf_set=None, update_list=False
):
    """Move all PDF files from one folder to another."""
    pdf_files = file_reader.get_all_pdfs(source_folder)
    print(len(pdf_files))
    for pdf in pdf_files:
        source_path = os.path.join(source_folder, pdf)
        destination_path = os.path.join(destination_folder, pdf)
        try:
            shutil.move(source_path, destination_path)
            pdf_set.add(pdf)
        except shutil.Error:
            delete_pdf_file_from_folder(".", source_path)

    pdf_files = file_reader.get_all_pdfs(source_folder)
    return True


def move_all_files_from_folder_to_folder(
    source_folder, destination_folder, extension=".pdf"
):
    """Move all PDF files from one folder to another."""
    files = os.listdir(source_folder)
    print(len(files))
    for file in files:
        if file.endswith(extension):
            source_path = os.path.join(source_folder, file)
            destination_path = os.path.join(destination_folder, file)
            try:
                shutil.move(source_path, destination_path)
            except shutil.Error:
                delete_pdf_file_from_folder(".", source_path)


def delete_pdf_file_from_folder(folder_path, filename):
    os.remove(filename)


def delete_all_crdownloads_from_folder(folder_path):
    items = os.listdir(folder_path)
    for item in items:
        if item.endswith(".crdownload"):
            os.remove(os.path.join(folder_path, item))


### Casey this is how you move all the pdfs over to the right folder
if __name__ == "__main__":
    # destination_folder = "chat_server/chat/file_resources/king-wa-resources"
    # ### change this folder name to the folder you want to move the pdfs to
    # source_folder = "./"
    # move_all_files_from_folder_to_folder(
    #     source_folder, destination_folder, extension=".pdf"
    # )
    # delete_all_crdownloads_from_folder(".")
    path = "chat_server/chat/file_resources/summit-ut-resources/https:$$$$$$codelibrary.amlegal.com$$$codes$$$summitcountyut$$$latest$$$summitcounty_ut$$$0-0-0-293.docx"
    chunks = file_reader.chunk_docx_into_paragraphs(path)
    from website_scraper import convert_file_name_to_url

    strang = ""
    for chunk in chunks:
        strang += chunk[3]
    text = remove_initial_all_caps(strang)
    print(text)
    print(len(strang))
    print(len(text))

    print(convert_file_name_to_url(path))
