import json
import logging
import os
import threading

import gmailer

# import llama_helper
# import llama_helper
from flask import Flask, jsonify, request
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
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


@app.route("/upsert_user", methods=["GET"])
def upsert_user():
    logging.info("in upsert_user")
    # data = request.get_json()
    ip = request.args.get("ip", "No ip received")
    email = request.args.get("email", None)
    name = request.args.get("name", "")
    given_name = request.args.get("given_name", "")
    family_name = request.args.get("family_name", "")
    if given_name == "":
        given_name = name
    if family_name == "":
        family_name = name

    logging.info("data: " + str(request.args))
    # Extract data into variables

    db = PGDB(
        os.getenv("PGHOST"),
        os.getenv("PGUSER"),
        os.getenv("PGPASSWORD"),
        os.getenv("PGDATABASE"),
        "",
    )
    resp = db.upsert_user(email, ip, given_name, family_name)

    if resp:
        json_response = json.dumps({"Success": "true"})
    else:
        json_response = json.dumps({"Success": "false"})

    return json_response


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
    try:
        email = request.args.get("email")
    except Exception:
        email = None

    logging.info("userInfo: " + str(email))
    logging.info("message: " + str(request.args.get("message")))
    logging.info("county: " + str(county))

    db = PGDB(host, user, password, dbname, county)

    question_number = db.update_user_on_new_question(email, ip)
    user = db.get_user_by_info(email, ip)
    logging.info("user: " + str(user))
    logging.info("question_number: " + str(question_number))

    llm = openai_helper(county=county)
    key_words_list = llm.get_key_words_from_message(message)
    db_resp = "No matching data found."
    i = 0
    # do multiple database reads at same time
    threads = []
    results = []
    thread_count = len(key_words_list)
    for i in range(thread_count):
        key_words = key_words_list[i][0].split(" ")
        thread = threading.Thread(
            target=lambda: results.append(
                db.full_text_search_on_key_words(key_words, county)
            )
        )
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete actions
    for thread in threads:
        thread.join()
    context = "No matching data found."
    source = ""
    logging.info("results: " + str(results))
    for i in range(thread_count):
        try:
            if results[i] != "No matching data found.":
                if context == "No matching data found.":
                    context = results[i][2]
                    source = convert_file_name_to_url(results[i][0])
                else:
                    context += results[i][2]
                source += "," + convert_file_name_to_url(results[i][0])
        except Exception as e:
            logging.info("results[i] failed", e)
    response = llm.create_response_message(request.args.get("message"), context)
    # logging.info("response: " + str(response))

    # TODO: figure out how to add many sources

    logging.info("source: " + str(source))
    return jsonify(
        {
            "response": response,
            "sender": "bot",
            "sources": source,
            "pages": db_resp[1],
            "questions_asked": str(question_number),
            "is_paying": user[0][5],
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

    app.debug = True
    http_server = WSGIServer(("", 5002), app)
    http_server.serve_forever()
# app.run(debug=True, host="0.0.0.0", port=5003)
