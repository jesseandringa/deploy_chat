import pdf_helper
import psycopg2
from util import log_text

# dbname = os.getenv("PGDATABASE")
# conn = psycopg2.connect(


class PGDB:
    def __init__(self, user, password, dbname, county=None):
        self.conn = psycopg2.connect(
            user=user,
            password=password,
            dbname=dbname,
        )
        self.county = county or "Gunnison"

    def create_table(self, table_name):
        cursor = self.conn.cursor()
        try:
            create_table_query = (
                """
            CREATE TABLE IF NOT EXISTS """
                + table_name
                + """ (
            id SERIAL PRIMARY KEY,
            ip_addr TEXT NOT NULL,
            user_name VARCHAR(255),
            email VARCHAR(255),
            password_hash VARCHAR(255),
            created_at TIMESTAMP,
            updated_at TIMESTAMP,
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            date_of_birth DATE,
            gender VARCHAR(255),
            age INTEGER,
            state VARCHAR(255),
            questions_asked INTEGER NOT NULL,
            last_question_asked TIMESTAMP,
            last_visited TIMESTAMP
            );
            """
            )
            cursor.execute(create_table_query)
            self.conn.commit()
            print(f"Table '{table_name}' created successfully.")
        except Exception as e:
            print(f"Error creating table: {e}")

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
        # text = text.replace("  ", " ")
        return text

    def get_just_file_name(self, file_path):
        return file_path.split("/")[-1]

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
            WHERE to_tsvector('english', chunk_text) @@ plainto_tsquery(%s);
        """
        )

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

    def remove_all_data_from_table(self, table_name):
        cursor = self.conn.cursor()
        try:
            # Replace with your desired DELETE statement
            delete_query = (
                """
            TRUNCATE TABLE """
                + table_name
                + """;
            """
            )
            cursor.execute(delete_query)
            self.conn.commit()
            print("Data removed successfully.")
        except Exception as e:
            self.conn.rollback()
            print(f"Error removing data: {e}")
        cursor.close()
        # self.conn.close()


def create_database_and_data(table_name, folder_path):
    user = "postgres"  # os.getenv("PGUSER")
    password = "guru"  # os.getenv("PGPASSWORD")
    dbname = "postgres"  # os.getenv("PGDATABASE")
    db = PGDB(user, password, dbname)
    db.create_pdf_text_table(table_name)
    # db.remove_all_data_from_table(table_name)
    # folder_path = "chat_server/chat/file_resources/gunnison-resources"
    pdf_files = pdf_helper.get_all_pdfs(folder_path)
    # xlsx_files = pdf_helper.get_all_xlsx(folder_path)
    # log_text("pdf_files:" + str(len(pdf_files)))
    for i, pdf_file in enumerate(pdf_files):
        try:
            chunks = pdf_helper.chunk_pdf_into_paragraphs(pdf_file)
        except Exception as e:
            print("failed to chunk pdf" + str(e))
        for j, chunk in enumerate(chunks):
            if j > 0 and j % 10 == 0:
                print("inserting chunk " + str(j) + " of pdf : " + str(i))
            text = chunk[3]
            if len(text) < 300 and j < len(chunks) - 1:
                text = str(chunks[j - 1][3]) + " " + text + " " + str(chunks[j + 1][3])
            if len(text) < 500 and j < len(chunks) - 2:
                text = (
                    str(chunks[j - 2][3])
                    + " "
                    + str(chunks[j - 1][3])
                    + " "
                    + text
                    + " "
                    + str(chunks[j + 1][3])
                    + " "
                    + str(chunks[j + 2][3])
                )
            if len(text) < 15:
                continue
            # print("text: " + str(text))
            try:
                db.insert_data_into_pdf_text_table(
                    table_name, str(chunk[0]), int(chunk[1]), str(text)
                )
            except Exception as e:
                print("failed to insert chunk" + str(e))
    print("finished inserting pdfs")
    # return db


if __name__ == "__main__":
    # pdf_path = "chat_server/chat/file_resources/sandy_muni_url_pdfs"
    # table_name = "sandy_ut_pdf_data"
    # create_database_and_data(table_name, pdf_path)
    user = "postgres"  # os.getenv("PGUSER")
    password = "guru"  # os.getenv("PGPASSWORD")
    dbname = "postgres"  # os.getenv("PGDATABASE")
    db = PGDB(user, password, dbname)
    db.create_table("basic_user_info")
