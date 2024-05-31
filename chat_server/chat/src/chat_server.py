import json
import logging
import os

import gmailer

# import llama_helper
# import llama_helper
from flask import Flask, jsonify, request
from flask_cors import CORS
from llm_helper import openai_helper
from util import convert_file_name_to_url

from postgres import PGDB

# LLAMA = None
app = Flask(__name__)
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


def create_app():
    CORS(app)

    return app


@app.route("/")  # This route will match any unmatched URL
def catch_all():
    print("catch_all")


@app.route("/send-email", methods=["POST"])
def send_email():
    print("message:", request.get_json)
    name = request.get_json().get("name", "No name received")
    email = request.get_json().get("email", "No email received")
    message = request.get_json().get("message", "No message received")
    send_message = gmailer.gmail_send_message(
        message_txt=message, name=name, email=email
    )
    worked = json.loads(send_message)
    Sent = worked["labelIds"][1]
    print("Sent:", Sent)
    if Sent == "SENT":
        json_response = json.dumps({"Success": "true"})
    else:
        json_response = json.dumps({"Success": "false"})

    return json_response


@app.route("/login", methods=["GET"])
def login():
    logging.info("message:", request.get_json)
    email = request.get_json().get("email", "No email received")
    password = request.get_json().get("password", "No password received")

    db = PGDB(
        os.getenv("PGHOST"),
        os.getenv("PGUSER"),
        os.getenv("PGPASSWORD"),
        os.getenv("PGDATABASE"),
        "",
    )
    resp = db.login_user(email, password)

    if resp:
        json_response = json.dumps({"Success": "true"})
    else:
        json_response = json.dumps({"Success": "false"})

    return json_response


@app.route("/sign-up", methods=["POST"])
def sign_up():
    logging.info("in sign up")
    data = request.get_json()
    logging.info("data: " + str(data))
    # Extract data into variables
    firstname = data.get("firstname")
    lastname = data.get("lastname")
    email = data.get("email")
    password = data.get("password")
    ip = data.get("ip")

    db = PGDB(
        os.getenv("PGHOST"),
        os.getenv("PGUSER"),
        os.getenv("PGPASSWORD"),
        os.getenv("PGDATABASE"),
        "",
    )
    resp = db.sign_up_user(firstname, lastname, email, password, ip)
    logging.info("resp: " + str(resp))
    if resp:
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


@app.route("/user-data", methods=["GET"])
def get_user_data():
    logging.info("Hit 'user-data' endpoint")
    logging.info("request: " + str(request.args.get("ip")))
    host = os.getenv("PGHOST")
    user = os.getenv("PGUSER")
    password = os.getenv("PGPASSWORD")
    dbname = os.getenv("PGDATABASE")
    db = PGDB(host, user, password, dbname, "")
    result = db.user_query_search(request.args.get("ip"))
    if result is None:
        return jsonify({"success": False})

    return jsonify({"success": True})


@app.route("/get-response", methods=["GET"])
def get_data():
    # logging.debug("This is a debug message hit endpoing")
    logging.info("Hit 'get-response' endpoint")
    # log_text("get_data hit")
    host = os.getenv("PGHOST")
    user = os.getenv("PGUSER")
    password = os.getenv("PGPASSWORD")
    dbname = os.getenv("PGDATABASE")

    county = request.args.get("county", "No county received")
    message = request.args.get("message")
    ip = request.args.get("ip")
    logging.info("ip: " + str(ip))
    logging.info("message: " + str(request.args.get("message")))
    logging.info("county: " + str(county))

    db = PGDB(host, user, password, dbname, county)

    question_number = db.update_user_on_new_question(ip, None)
    logging.info("question_number: " + str(question_number))

    llm = openai_helper(county=county)
    key_words_list = llm.get_key_words_from_message(message)
    db_resp = "No matching data found."
    i = 0
    while db_resp == "No matching data found." and i < 2:  # i < len(key_words_list):
        key_words = key_words_list[i][0].split(" ")
        logging.info("key_words: " + str(key_words))
        db_resp = db.full_text_search_on_key_words(key_words, county)
        logging.info("db_resp: " + str(db_resp))
        i += 1

    # db_resp = db.full_text_search_on_key_words(key_words)
    response = llm.create_response_message(request.args.get("message"), db_resp[2])
    logging.info("response: " + str(response))
    # log_text("db_resp: " + str(db_resp))
    # app.config["LLAMA"].log_text("get_resposnse: " + str(db_resp))
    source = convert_file_name_to_url(db_resp[0])
    return jsonify(
        {
            "response": response,
            "sender": "bot",
            "sources": source,
            "pages": db_resp[1],
            "questions_asked": str(question_number),
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
    # create_database_and_data()
    # user = os.getenv("PGUSER")
    # password = os.getenv("PGPASSWORD")
    # dbname = os.getenv("PGDATABASE")
    # db = PGDB(user, password, dbname)
    # log_text("Starting server...")
    logging.debug("This is a debug message")
    logging.info("This is an info message")
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5002)
