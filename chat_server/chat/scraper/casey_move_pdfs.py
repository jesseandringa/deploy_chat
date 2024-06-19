import os
import shutil

import file_reader


def move_all_pdfs_from_folder_to_folder(source_folder, destination_folder):
    """Move all PDF files from one folder to another."""
    pdf_files = file_reader.get_all_pdfs(source_folder)
    for pdf_file in pdf_files:
        try:
            shutil.move(pdf_file, destination_folder)
        except shutil.Error:
            delete_pdf_file_from_folder(".", pdf_file)
    return True


def delete_pdf_file_from_folder(folder_path, filename):
    os.remove(filename)


### Casey this is how you move all the pdfs over to the right folder
if __name__ == "__main__":
    source_folder = "."
    ### change this folder name to the folder you want to move the pdfs to
    destination_folder = "chat_server/chat/file_resources/king-wa-resources"
    move_all_pdfs_from_folder_to_folder(source_folder, destination_folder)
