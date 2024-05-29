import json
import logging
import os

import gmailer

# import llama_helper
# import llama_helper
from flask import Flask, jsonify, request
from flask_cors import CORS
from llm_helper import openai_helper
from util import convert_file_name_to_url, log_text

from postgres import PGDB, create_database_and_data

# LLAMA = None
app = Flask(__name__)
logging.basicConfig(filename="/app/llama.log", level=logging.INFO)


# CORS(app)
def init_llama(app):
    with app.app_context():
        print("Making LLAMA...")
        dir_paths = []
        storage_paths = get_storage_paths()
        url_json_paths = []
        # app.config["LLAMA"] = None
        app.config["LLAMA"] = None
        # llama_helper.LlamaRag(
        #     dir_paths=dir_paths,
        #     storage_paths=storage_paths,
        #     url_json_paths=url_json_paths,
        #     dynamic_county_load=True,
        # )
        print("Made LLAMA.")
        # logging.info("Made LLAMA2.")


def get_storage_paths():
    resources_path = "/app/storage_resources"
    entries = os.listdir(resources_path)
    storage_paths = [
        resources_path + "/" + entry
        for entry in entries
        if os.path.isdir(os.path.join(resources_path, entry))
    ]
    # storage_paths = [storage_paths[2]]
    # print("storage_pathss:", storage_paths)
    return storage_paths


def create_app():
    CORS(app)
    # handler = logging.StreamHandler()  # Create a StreamHandler
    # handler.setLevel(logging.DEBUG)  # Set the logging level for the handler

    # app.logger.addHandler(handler)
    init_llama(app)

    return app


@app.route("/")  # This route will match any unmatched URL
def catch_all():
    print("catch_all")
    # logging.error("Received a request.")


@app.route("/send-email", methods=["POST"])
def send_email():
    print("message:", request.get_json)
    name = request.get_json().get("name", "No name received")
    email = request.get_json().get("email", "No email received")
    message = request.get_json().get("message", "No message received")
    send_message = gmailer.gmail_send_message(
        message_txt=message, name=name, email=email
    )
    logging.info(f"Message: {message}")
    logging.info(f"Send Message: {send_message}")
    worked = json.loads(send_message)
    Sent = worked["labelIds"][1]
    print("Sent:", Sent)
    if Sent == "SENT":
        json_response = json.dumps({"Success": "true"})
    else:
        json_response = json.dumps({"Success": "false"})

    return json_response


@app.route("/change-county", methods=["GET"])
def change_county():
    app.config["SERVER_TIMEOUT"] = 50
    county = request.args.get("county", "No county received")
    # current_app.config["LLAMA"].set_county(county)
    # current_app.config["LLAMA"].log_text("Changed county to " + county)
    return jsonify({"success": True})


@app.route("/get-response", methods=["GET"])
def get_data():
    user = os.getenv("PGUSER")
    password = os.getenv("PGPASSWORD")
    dbname = os.getenv("PGDATABASE")

    county = request.args.get("county", "No county received")
    db = PGDB(user, password, dbname, county)
    # key_words = request.args.get("message").split(" ")

    llm = openai_helper(county=county)
    key_words_list = llm.get_key_words_from_message(request.args.get("message"))
    db_resp = "No matching data found."
    i = 0
    while db_resp == "No matching data found." and i < len(key_words_list):
        key_words = key_words_list[i][0].split(" ")
        log_text("key_words: " + str(key_words))
        db_resp = db.full_text_search_on_key_words(key_words)
        log_text("db_resp: " + str(db_resp))
        i += 1

    # db_resp = db.full_text_search_on_key_words(key_words)
    response = llm.create_response_message(request.args.get("message"), db_resp[2])

    log_text("db_resp: " + str(db_resp))
    # app.config["LLAMA"].log_text("get_resposnse: " + str(db_resp))
    source = convert_file_name_to_url(db_resp[0])
    return jsonify(
        {
            "response": response,
            "sender": "bot",
            "sources": source,
            "pages": db_resp[1],
        }
    )
    # app.config["SERVER_TIMEOUT"] = 120
    # current_app.config["LLAMA"].log_text(
    #     "get_resposnse: " + str(request.args.get("message"))
    # )

    # county = request.args.get("county", "No county received")
    # # print("county:", county)
    # message = request.args.get("message", "No message received")
    # llama = current_app.config["LLAMA"]
    # try:
    #     response_message = get_response_message(message, county, llama=llama)
    # except Exception as e:
    #     logging.info(f"Failed to get response, {e}")
    #     response_message = {"sender": "bot", "response": "Sorry, I couldn't find that."}
    # # Process the data (this example just echoes back the received message)
    # # print("resepos", response_message)
    # logging.info(f"Response: {response_message}")
    # # Return the processed data as JSON
    # return jsonify(response_message)


if __name__ == "__main__":
    # create database then create server
    create_database_and_data()
    # user = os.getenv("PGUSER")
    # password = os.getenv("PGPASSWORD")
    # dbname = os.getenv("PGDATABASE")
    # db = PGDB(user, password, dbname)

    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5002)
