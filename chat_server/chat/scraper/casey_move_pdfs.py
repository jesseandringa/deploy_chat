import os
import shutil

import file_reader


def move_all_pdfs_from_folder_to_folder(source_folder, destination_folder):
    """Move all PDF files from one folder to another."""
    pdf_files = file_reader.get_all_pdfs(source_folder)
    print(len(pdf_files))
    for pdf in pdf_files:
        source_path = os.path.join(source_folder, pdf)
        destination_path = os.path.join(destination_folder, pdf)
        try:
            shutil.move(source_path, destination_path)
        except shutil.Error:
            delete_pdf_file_from_folder(".", source_path)
    return True


def delete_pdf_file_from_folder(folder_path, filename):
    os.remove(filename)


### Casey this is how you move all the pdfs over to the right folder
if __name__ == "__main__":
    destination_folder = "chat_server/chat/file_resources/murray-muni-resources"
    ### change this folder name to the folder you want to move the pdfs to
    source_folder = "chat_server/chat/file_resources/king-wa-resources"
    move_all_pdfs_from_folder_to_folder(source_folder, destination_folder)
