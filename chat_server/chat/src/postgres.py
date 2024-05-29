import os

import pdf_helper
import psycopg2
from util import log_text

dbname = os.getenv("PGDATABASE")
# conn = psycopg2.connect(


class PGDB:
    def __init__(self, user, password, dbname, county=None):
        self.conn = psycopg2.connect(
            user=user,
            password=password,
            dbname=dbname,
        )
        self.county = county or "Gunnison"

    def create_pdf_text_table(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("DROP TABLE IF EXISTS pdf_chunks;")
            # Replace with your desired CREATE TABLE statement
            table_name = "PDF_TEXT"
            create_table_query = """
            CREATE TABLE IF NOT EXISTS pdf_chunks (
            id SERIAL PRIMARY KEY,
            pdf_name VARCHAR(255) NOT NULL,
            page_number INTEGER NOT NULL,
            chunk_text TEXT NOT NULL
            );
            """
            cursor.execute(create_table_query)
            self.conn.commit()
            print(f"Table '{table_name}' created successfully.")
        except Exception as e:
            print(f"Error creating table: {e}")

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

    def insert_data_into_pdf_text_table(self, pdf_name, page_number, chunk_text):
        cursor = self.conn.cursor()
        text = self.clean_and_trim_text(chunk_text)
        try:
            # Replace with your desired INSERT INTO statement
            insert_query = f"""
            INSERT INTO pdf_chunks (pdf_name, page_number, chunk_text)
            VALUES ('{pdf_name}', {page_number}, '{text}');
            """
            cursor.execute(insert_query)
            self.conn.commit()
            log_text("Data inserted successfully.")
            # print("Data inserted successfully.")
        except Exception as e:
            self.conn.rollback()
            log_text(f"Error inserting data: {e}")
        cursor.close()
        # self.conn.close()

    def full_text_search_on_key_words(self, key_words):
        """
        Search for key words in the table
        key_words: [str]
        """
        try:
            select_query = self.create_full_text_search_query(key_words)
        except Exception as e:
            log_text(f"Error searching data: {e}")
            return "No matching data found."
        try:
            first_result_tuple = select_query[0]
        except Exception:
            log_text("no data: selectquery[0] " + str(select_query))
            return "No matching data found."

        log_text("select_query: " + str(select_query))
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

    def create_full_text_search_query(self, words):
        """
        words: [str]
        """
        if not words:
            return None  # Handle empty list case
        query = """
            SELECT pdf_name, page_number,chunk_text,
                ts_rank(to_tsvector('english', chunk_text), plainto_tsquery(%s)) AS match_count
            FROM pdf_chunks
            WHERE to_tsvector('english', chunk_text) @@ plainto_tsquery(%s);
        """

        search_query = " & ".join(words)
        cursor = self.conn.cursor()
        cursor.execute(query, (search_query, search_query))
        result = cursor.fetchall()
        # for row in result:
        #     log_text("row: " + str(row))

        return result

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
    # db.insert_data_into_pdf_text_table("test.pdf", 1, "Hello, World!")
    # db.insert_data_into_pdf_text_table("test.pdf", 2, "This is a test.")
    folder_path = "/app/file_resources/gunnison-resources"
    # pdf_helper.insert_all_file_chunks_to_database(
    #     folder_path,
    #     db,
    # )
    pdf_files = pdf_helper.get_all_pdfs(folder_path)
    # xlsx_files = pdf_helper.get_all_xlsx(folder_path)
    log_text("pdf_files:" + str(len(pdf_files)))
    for i, pdf_file in enumerate(pdf_files):
        # if (
        #     "nnisoncounty.org$$$DocumentCenter$$$View$$$12949$$$Genasys-Press-Release-for-Website_English.pdf"
        #     in pdf_file
        # ):
        # if i < 3:
        # log_text("inserting pdf:")
        try:
            chunks = pdf_helper.chunk_pdf_into_paragraphs(pdf_file)
        except Exception as e:
            log_text("failed to chunk pdf" + str(e))
        for i, chunk in enumerate(chunks):
            # if i < 1:
            # log_text("chunk:" + str(chunk))
            text = chunk[3]
            log_text("text: " + str(text))
            # log_text("text: " + str(text))
            # if i < len(chunks) - 1:
            #     if len(str(chunk[3])) < 50:
            #         text = (
            #             str(chunks[i - 1][3])
            #             + " "
            #             + str(chunk[3])
            #             + " "
            #             + str(chunks[i + 1][3])
            #         )
            # log_text("trying to insert chunk:" + str(text))
            try:
                db.insert_data_into_pdf_text_table(
                    str(chunk[0]), int(chunk[1]), str(text)
                )
            except Exception as e:
                log_text("failed to insert chunk" + str(e))
    log_text("finished inserting pdfs")
    # return db
