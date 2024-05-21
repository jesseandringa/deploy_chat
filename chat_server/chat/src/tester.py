def delete_all_docx_from_folder(folder):
    import os

    for file in os.listdir(folder):
        if file.endswith(".ics"):
            os.remove(os.path.join(folder, file))


delete_all_docx_from_folder("murray-resources")
