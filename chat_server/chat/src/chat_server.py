import json
import logging
import os
import threading

import gmailer
import paypalrestsdk

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

DB = PGDB(
    os.getenv("PGHOST"),
    os.getenv("PGUSER"),
    os.getenv("PGPASSWORD"),
    os.getenv("PGDATABASE"),
    "",
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


# Configure the PayPal SDK
paypalrestsdk.configure(
    {
        "mode": "live",  # Use "live" for production
        "client_id": os.getenv("PAYPAL_CLIENT_ID"),
        "client_secret": os.getenv("PAYPAL_CLIENT_SECRET"),
    }
)


@app.route("/unsubscribe", methods=["POST"])
def unsubscribe():
    # Get the subscription ID from the request body
    data = request.get_json()
    email = data.get("email")
    subscription = DB.get_subscription(email)
    subscription_id = subscription.get("subscription_id")

    if not subscription_id:
        return jsonify({"error": "Subscription ID is required"}), 400

    # Retrieve the subscription to confirm it exists
    subscription = paypalrestsdk.BillingAgreement.find(subscription_id)

    if not subscription:
        return jsonify({"error": "Subscription not found"}), 404

    # Cancel the subscription
    cancellation = subscription.cancel({"note": "Unsubscribing from service"})

    if cancellation.success():
        DB.update_user_to_paying(email, False)

        return jsonify({"message": "Successfully unsubscribed"}), 200
    else:
        return jsonify({"error": "Failed to unsubscribe", "details": cancellation}), 500


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


@app.route("/get_user", methods=["GET"])
def get_user():
    logging.info("in get_user")
    email = request.args.get("email", None)

    db = PGDB(
        os.getenv("PGHOST"),
        os.getenv("PGUSER"),
        os.getenv("PGPASSWORD"),
        os.getenv("PGDATABASE"),
        "",
    )
    user = db.get_user_by_email(email)

    if user:
        json_response = json.dumps(user)
    else:
        json_response = json.dumps({"User": None})

    return json_response


@app.route("/subscribe", methods=["GET"])
def subscribe():
    logging.info("in subscribe")
    email = request.args.get("email", None)
    subscription_id = request.args.get("subscription_id", None)
    payment_source = request.args.get("payment_source", None)
    facilitator_access_token = request.args.get("facilitator_access_token", None)
    order_id = request.args.get("order_id", None)

    if (
        not email
        or not subscription_id
        or not payment_source
        or not facilitator_access_token
        or not order_id
    ):
        logging.error("Missing required fields")
        return jsonify({"success": False})
    # Extract data into variables

    db = PGDB(
        os.getenv("PGHOST"),
        os.getenv("PGUSER"),
        os.getenv("PGPASSWORD"),
        os.getenv("PGDATABASE"),
        "",
    )
    resp = db.subscribe(
        email, subscription_id, payment_source, facilitator_access_token, order_id
    )
    if resp:
        # update user to paying
        updated = db.update_user_to_paying(email)

    if resp and updated:
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
    logging.info("Hit 'get-response' endpoint")
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
    user = db.get_user_by_email(email)
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

    # TODO: figure out how to add many sources

    logging.info("source: " + str(source))
    return jsonify(
        {
            "response": response,
            "sender": "bot",
            "sources": source,
            "pages": db_resp[1],
            "questions_asked": str(question_number),
            "is_paying": user.get("is_paying", False),
        }
    )


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
