import json


def log_text(text):
    data = {"log": text}
    json_string = json.dumps(data)
    with open("logs.json", "a") as f:
        f.write("\n")
        f.write(json_string)


def convert_file_name_to_url(path):
    url = path.replace("$$$", "/")
    if url.endswith(".pdf"):
        url = url[:-4]
    if url.endswith(".xlsx"):
        url = url[:-5]
    return url
