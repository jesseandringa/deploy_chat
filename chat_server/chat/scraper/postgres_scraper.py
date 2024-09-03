import json
import logging
import os
import sys
import threading
from datetime import datetime

import database_vars
import file_reader
import psycopg2

dbname = os.getenv("PGDATABASE")
# conn = psycopg2.connect(

counties_table_names = {
    "gunnison-co": "gunnison_co_pdf_data",
    "sandy-ut": "sandy_ut_pdf_data",
    "millcreek-ut": "millcreek_ut_pdf_data",
    "murray-ut": "murray_ut_pdf_data",
    "king-wa": "king_wa_pdf_data",
    "elko-nv": "elko_nv_pdf_data",
    "cullman-al": "cullman_al_pdf_data",
    "cumberland-nc": "cumberland_nc_pdf_data",
    "summit-ut": "summit_ut_pdf_data",
}


class PGDB:
    def __init__(self, host, user, password, dbname, county=None):
        self.conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            dbname=dbname,
        )
        self.county = county or "Gunnison"

    def check_connection(self):
        try:
            self.conn.cursor().execute("SELECT 1")
        except Exception as e:
            print(f"Error checking connection: {e}")
            return False
        print("Connection successful.")
        return True

    def check_table_has_data(self, table_name):
        cursor = self.conn.cursor()
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            return count
        except Exception as e:
            print(f"Error checking table for data: {e}")
            return False

    def get_just_file_name(self, file_path):
        return file_path.split("/")[-1]

    def create_pdf_text_table(self, table_name):
        cursor = self.conn.cursor()
        try:
            # cursor.execute("DROP TABLE IF EXISTS " + table_name + ";")
            create_table_query = (
                """
            CREATE TABLE IF NOT EXISTS """
                + table_name
                + """ (
            id SERIAL PRIMARY KEY,
            pdf_name VARCHAR(255) NOT NULL,
            page_number INTEGER NOT NULL,
            chunk_text TEXT NOT NULL
            );
            """
            )
            cursor.execute(create_table_query)
            self.conn.commit()
            print(f"Table '{table_name}' created successfully.")
        except Exception as e:
            print(f"Error creating table: {e}")

    def insert_data_into_pdf_text_table(
        self, table_name, pdf_name, page_number, chunk_text
    ):
        cursor = self.conn.cursor()
        text = self.clean_and_trim_text(chunk_text)
        pdf_name = self.get_just_file_name(pdf_name)

        try:
            # Replace with your desired INSERT INTO statement
            insert_query = (
                """
            INSERT INTO """
                + table_name
                + f""" (pdf_name, page_number, chunk_text)
            VALUES ('{pdf_name}', {page_number}, '{text}');
            """
            )
            cursor.execute(insert_query)
            self.conn.commit()
            print("Data inserted successfully.")
        except Exception as e:
            self.conn.rollback()
            print(f"Error inserting data: {e}")
        cursor.close()

    def clean_and_trim_text(self, text):
        text = text.replace("'", "")
        text = text.replace('"', "")
        text = text.replace("\n", " ")
        text = text.replace("\\n", " ")
        text = text.replace("\r\n", " ")
        text = text.replace("\\\n", " ")
        text = text.replace("\r", " ")
        text = text.replace("\t", " ")
        text = text.replace("\b", " ")
        text = text.replace("\f", " ")
        text = text.replace("\v", " ")
        text = text.replace("\a", " ")
        text = text.replace(" the ", " ")
        text = text.replace(" The ", " ")
        text = text.replace(" and ", " ")
        text = text.replace(" And ", " ")
        text = text.replace(" or ", " ")
        text = text.replace(" Or ", " ")
        text = text.replace(" a ", " ")
        text = text.replace("\\", " ")
        return text

    def full_text_search_on_key_words(self, key_words, county, table_name=None):
        """
        Search for key words in the table
        key_words: [str]
        """
        if not table_name:
            table_name = counties_table_names[county]
        try:
            select_query = self.create_full_text_search_query(key_words, table_name)
        except Exception as e:
            print(f"Error searching data: {e}")
            return "No matching data found."
        try:
            first_result_tuple = select_query[0]
        except Exception:
            print("no data: selectquery[0] " + str(select_query))
            return "No matching data found."

        print("select_query: " + str(select_query))
        query_result = str(select_query[0][2])
        if len(query_result) < 50 and len(select_query) > 1:
            query_result = str(select_query[0][2] + ".. " + select_query[1][2])
            # Convert the first result to a list to modify it
            first_result_list = list(select_query[0])
            first_result_list[2] = query_result

            # Convert the list back to a tuple
            first_result_tuple = tuple(first_result_list)
        # select_query[0][2] = query_result
        return first_result_tuple

    def create_full_text_search_query(self, words, table_name):
        """
        words: [str]
        """
        if not words:
            return None  # Handle empty list case
        query = (
            """
            SELECT pdf_name, page_number,chunk_text,
                ts_rank(to_tsvector('english', chunk_text), plainto_tsquery(%s)) AS match_count
            FROM """
            + table_name
            + """ 
            WHERE to_tsvector('english', chunk_text) @@ plainto_tsquery(%s) 
            LIMIT 2;
        """
        )

        search_query = " & ".join(words)
        cursor = self.conn.cursor()
        cursor.execute(query, (search_query, search_query))
        result = cursor.fetchall()
        logging.info("result: " + str(result))
        # for row in result:
        #     print("row: " + str(row))

        return result

    def update_user_on_new_question(self, ip_address, user):
        cursor = self.conn.cursor()
        timestamp = datetime.now()
        try:
            # Replace with your desired DELETE statement
            update_query = f"""
            UPDATE basic_user_info
            SET questions_asked = questions_asked + 1,
            last_question_asked = '{timestamp}'
            WHERE ip_addr = '{ip_address}'
            RETURNING questions_asked;
            """
            cursor.execute(update_query)
            questions_asked = cursor.fetchone()
            logging.info("User updated successfully.", str(questions_asked))

            self.conn.commit()
            return questions_asked[0]
        except Exception as e:
            self.conn.rollback()
            logging.error(f"Error updating data: {e}")
        cursor.close()
        return None

    def user_query_search(self, ip_address=None, username=None, password=None):
        if ip_address:
            query = f"""
            SELECT * FROM basic_user_info WHERE ip_addr = '{ip_address}';
            """
            username = ""
            password = ""

        elif username and password and not ip_address:
            query = f"""
            SELECT * FROM basic_user_info WHERE user_name = '{username}' AND password_hash = '{password}';
            """
            username = ""
            password = ""
        try:
            result = self.execute(query)
        except Exception as e:
            logging.error(f"Error searching data: {e}")
            result = None

        if not result:
            questions_asked = 0
            current_timestamp = datetime.now()
            insert_query = f"""
            INSERT INTO basic_user_info (ip_addr, user_name, password_hash, questions_asked, last_visited)
            VALUES ('{ip_address}', '{username}', '{password}', '{questions_asked}','{current_timestamp}');
            """
            try:
                self.conn.cursor().execute(insert_query)
                self.conn.commit()
            except Exception as e:
                logging.error(f"Error inserting data: {e}")
                result = None
        if result:
            logging.info(f"User found: {result}")

        return result

    def login_user(self, username, password):
        current_timestamp = datetime.now()
        query = f"""
        SELECT * FROM basic_user_info WHERE email = '{username}' AND password_hash = '{password}';
        """
        try:
            result = self.execute(query)
        except Exception as e:
            logging.error(f"Error searching data: {e}")
            result = None
        logging.info(f"User found: {result}")
        return result

    def sign_up_user(self, firstname, lastname, email, password, ip):
        questions_asked = 0
        current_timestamp = datetime.now()
        insert_query = f"""
        INSERT INTO basic_user_info (first_name, last_name, email, password_hash, ip_addr, questions_asked, last_visited, created_at)
        VALUES ('{firstname}', '{lastname}','{email}', '{password}', '{ip}', '{questions_asked}','{current_timestamp}','{current_timestamp}');
        """
        try:
            self.conn.cursor().execute(insert_query)
            self.conn.commit()
        except Exception as e:
            logging.error(f"Error inserting data: {e}")
            return None
        return True

    def execute(self, query):
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def remove_all_data_from_table(self):
        cursor = self.conn.cursor()
        try:
            # Replace with your desired DELETE statement
            delete_query = """
            TRUNCATE TABLE pdf_chunks;
            """
            cursor.execute(delete_query)
            self.conn.commit()
            print("Data removed successfully.")
        except Exception as e:
            self.conn.rollback()
            print(f"Error removing data: {e}")
        cursor.close()
        # self.conn.close()


def create_database_and_data():
    user = os.getenv("PGUSER")
    password = os.getenv("PGPASSWORD")
    dbname = os.getenv("PGDATABASE")
    db = PGDB(user, password, dbname)
    db.create_pdf_text_table()
    db.remove_all_data_from_table()
    folder_path = "/app/file_resources/gunnison-resources"
    # pdf_helper.insert_all_file_chunks_to_database(
    #     folder_path,
    #     db,
    # )
    pdf_files = file_reader.get_all_pdfs(folder_path)
    # xlsx_files = pdf_helper.get_all_xlsx(folder_path)
    print("pdf_files:" + str(len(pdf_files)))
    for i, pdf_file in enumerate(pdf_files):
        # if (
        #     "nnisoncounty.org$$$DocumentCenter$$$View$$$12949$$$Genasys-Press-Release-for-Website_English.pdf"
        #     in pdf_file
        # ):
        # if i < 3:
        # print("inserting pdf:")
        try:
            chunks = file_reader.chunk_pdf_into_paragraphs(pdf_file)
        except Exception as e:
            print("failed to chunk pdf" + str(e))
        for i, chunk in enumerate(chunks):
            # if i < 1:
            # print("chunk:" + str(chunk))
            text = chunk[3]
            print("text: " + str(text))
            # print("text: " + str(text))
            # if i < len(chunks) - 1:
            #     if len(str(chunk[3])) < 50:
            #         text = (
            #             str(chunks[i - 1][3])
            #             + " "
            #             + str(chunk[3])
            #             + " "
            #             + str(chunks[i + 1][3])
            #         )
            # print("trying to insert chunk:" + str(text))
            try:
                db.insert_data_into_pdf_text_table(
                    str(chunk[0]), int(chunk[1]), str(text)
                )
            except Exception as e:
                print("failed to insert chunk" + str(e))
    print("finished inserting pdfs")
    # return db


# def create_table_and_insert_all_data(db, table_name, folder_path):
#     db.create_pdf_text_table(table_name)
#     pdf_files = file_reader.get_all_files_with_full_path(folder_path)
#     print(len(pdf_files))
#     for i, pdf_file in enumerate(pdf_files):
#         try:
#             chunks = file_reader.chunk_file_into_paragraphs(pdf_file, chunk_size=10000)
#             valid = file_reader.check_validity_of_file(file_path=None, chunks=chunks)
#             if valid == 0:
#                 continue
#         except Exception as e:
#             print("failed to chunk pdf" + str(e))
#         j = 0
#         for chunk_index, chunk in enumerate(chunks):
#             if chunk_index < j:
#                 continue
#             text = chunk[1]
#             if chunk_index < len(chunks) - 2:
#                 text = text + " " + chunks[chunk_index + 1][1]
#             if chunk_index > 0:
#                 text = chunks[chunk_index - 1][1] + " " + text

#             if chunk_index % 10 == 0:
#                 print(
#                     "inserting chunk "
#                     + str(j)
#                     + "of "
#                     + str(len(chunks))
#                     + " of pdf : "
#                     + str(i)
#                 )
#                 if (i + 1) % 10 == 0:
#                     print("\n", text)
#             try:
#                 db.insert_data_into_pdf_text_table(
#                     table_name, str(chunk[0]), 0, str(text)
#                 )
#             except Exception as e:
#                 print("failed to insert chunk" + str(e))
#     print("finished inserting pdfs")
# return db


def read_index_from_json(file_path="index.json"):
    try:
        # Reading the index from a JSON file
        with open(file_path, "r") as file:
            index = json.load(file)

        return index
    except KeyboardInterrupt:
        print("\nProgram interrupted with Control-C")
        sys.exit(1)
    except Exception:
        return 0


def write_index_to_json(index, file_path="index.json"):
    # Writing the index to a JSON file
    with open(file_path, "w") as file:
        json.dump(index, file)


def chunk_text_and_insert(pdf_files, i, db, table_name):
    try:
        chunks = file_reader.chunk_file_into_paragraphs(pdf_files[i], chunk_size=10000)
        valid = file_reader.check_validity_of_file(file_path=None, chunks=chunks)
        if valid == 0:
            return 1
    except Exception as e:
        print("failed to chunk pdf" + str(e))

    for chunk_index, chunk in enumerate(chunks):
        text = chunk[1]
        if chunk_index < len(chunks) - 2:
            text = text + " " + chunks[chunk_index + 1][1]
        if chunk_index > 0:
            text = chunks[chunk_index - 1][1] + " " + text

        if chunk_index % 10 == 0:
            print(
                "inserting chunk "
                + str(chunk_index)
                + "of "
                + str(len(chunks))
                + " of pdf : "
                + str(i)
            )
        try:
            db.insert_data_into_pdf_text_table(table_name, str(chunk[0]), 0, str(text))
        except Exception as e:
            print("failed to insert chunk" + str(e))


def create_table_and_insert_all_data(db, table_name, folder_path):
    db.create_pdf_text_table(table_name)
    pdf_files = file_reader.get_all_files_with_full_path(folder_path)
    print(len(pdf_files))
    index_path = "chat_server/chat/scraper/database_index.json"
    i = read_index_from_json(index_path)
    while i < len(pdf_files):
        threads = []
        results = []
        for j in range(6):  # Example: Perform actions in {range_end} threads
            thread = threading.Thread(
                target=lambda: results.append(
                    chunk_text_and_insert(pdf_files, i + j, db, table_name)
                )
            )
            threads.append(thread)
            thread.start()
            i += 1

        # Wait for all threads to complete actions
        for thread in threads:
            thread.join()

        write_index_to_json(i, index_path)
    write_index_to_json(0, index_path)

    print("finished inserting pdfs")


if __name__ == "__main__":
    dbvars = database_vars.get_db_vars()
    db = PGDB(
        dbvars["PGHOST"],
        dbvars["PGUSER"],
        dbvars["PGPASSWORD"],
        dbvars["PGDATABASE"],
    )
    # # start timer:
    # import time

    # start_time = time.time()
    # text = db.full_text_search_on_key_words(
    #     ["governing", "annual", "delegates"], "g", "test_10000"
    # )
    # end_time = time.time()
    # print("text: " + str(text))
    # execution_time = end_time - start_time
    # print(f"Execution time: {execution_time} seconds")

    ###########CASEY change table_name and folder_path to match your data#############################
    # table names follow the format: county_state_pdf_data
    # ex.      murray_ut_pdf_data
    # folder path to the pdfs you want to upsert (control click folder copy and paste 'relatitve path')
    # ex.      chat_server/chat/file_resources/murray-muni-resources
    table_name = "test_10000"
    folder_path = "chat_server/chat/file_resources/summit-ut-resources"
    ##################################################################################################
    create_table_and_insert_all_data(db, table_name, folder_path)
    # user
