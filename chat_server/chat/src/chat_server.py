import json
import logging
import os

import gmailer
import llama_helper
from chat_client import get_response_message
from flask import Flask, current_app, jsonify, request
from flask_cors import CORS

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
        app.config["LLAMA"] = llama_helper.LlamaRag(
            dir_paths=dir_paths,
            storage_paths=storage_paths,
            url_json_paths=url_json_paths,
        )
        print("Made LLAMA.")
        logging.info("Made LLAMA2.")


def get_storage_paths():
    resources_path = "/app/storage_resources"
    entries = os.listdir(resources_path)
    storage_paths = [
        resources_path + "/" + entry
        for entry in entries
        if os.path.isdir(os.path.join(resources_path, entry))
    ]
    storage_paths = storage_paths[1:-2]
    print("storage_pathss:", storage_paths)
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
    logging.error("Received a request.")


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


@app.route("/get-response", methods=["GET"])
def get_data():
    data = {"in": "get-response", "age": 25}

    # Convert data to JSON string
    json_string = json.dumps(data)

    # Open the file in write mode
    with open("logs.json", "a") as f:
        # Write the JSON string to the file
        f.write(json_string)
    print("message:", request.get_json)
    # app.logger.info("received a request.")
    # print("message:", request.get_json)
    # print("messageee", request.args.get("message", "No message received"))
    county = request.args.get("county", "No county received")
    # print("county:", county)
    message = request.args.get("message", "No message received")
    llama = current_app.config["LLAMA"]
    try:
        response_message = get_response_message(message, county, llama=llama)
    except Exception as e:
        logging.info(f"Failed to get response, {e}")
        response_message = {"sender": "bot", "response": "Sorry, I couldn't find that."}
    # Process the data (this example just echoes back the received message)
    # print("resepos", response_message)
    logging.info(f"Response: {response_message}")
    # Return the processed data as JSON
    return jsonify(response_message)


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5002)
