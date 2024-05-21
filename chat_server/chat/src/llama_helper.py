import glob
import json
import logging
import os
from pathlib import Path

# from llama_index.llm_predictor import HuggingFaceLLMPredictor
from llama_index.core import Settings  # , SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.indices import load_indices_from_storage
from llama_index.core.storage import storage_context
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# from llama_index.llms.ollama import Ollama
from llama_index.llms.openai import OpenAI

# from llama_index.readers.web import BeautifulSoupWebReader
from openai_helper import OpenaiClient
from website_scraper import convert_file_name_to_url  # , read_urls_from_json


class LlamaRag:
    def __init__(
        self,
        dir_paths=None,
        storage_paths=["storage"],
        url_json_paths=None,
        is_test=False,
        dynamic_county_load=True,
    ):
        logging.basicConfig(filename="/app/llama.log", level=logging.INFO)
        if is_test:
            return
        self.llmsherpa_api_url = "https://readers.llmsherpa.com/api/document/developer/parseDocument?renderFormat=all"
        self.documents = []
        self.storage_paths = storage_paths
        Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
        # self.llm = Ollama(model="mistral", request_timeout=30.0)
        self.llm = OpenAI()
        self.main_index = None
        self.documents = []
        self.muni_code_index = None
        self.muni_documents = []
        self.indices = []
        self.current_index = None
        self.dynamic_county_load = dynamic_county_load
        self.one_bot = True if len(storage_paths) == 1 else False
        if not self.dynamic_county_load:
            if isinstance(url_json_paths, list):
                self.load_data_to_index(dir_paths, url_json_paths, storage_paths)
            else:
                print("incorrect params")

    def set_county(self, county):
        for i in range(len(self.storage_paths)):
            if county in self.storage_paths[i]:
                self.load_index_from_storage(self.storage_paths[i])

    # def load_data_to_index(self, dir_paths, url_json_paths, storage_paths):
    #     for i in range(len(storage_paths)):
    #         self.documents.append([])

    #         # if vector store exists load it
    #         logging.info("storage paths[i]", storage_paths[i])
    #         print("storage paths[i]", storage_paths[i])
    #         if os.path.exists(storage_paths[i]):
    #             self.load_index_from_storage(storage_paths[i])
    #         else:
    #             print("loading...")
    #             if self.one_bot:  # load all to one index
    #                 print("loading all to one index")
    #                 for path in dir_paths:
    #                     self.load_data_from_dir_path(path, i)
    #                 for path in url_json_paths:
    #                     self.load_data_from_url_path(path, i)
    #             else:
    #                 self.load_data_from_dir_path(dir_paths[i], i)
    #                 if url_json_paths[i] is not None:
    #                     self.load_data_from_url_path(url_json_paths[i], i)

    #             print("creating vector store")
    #             self.indices.append(VectorStoreIndex.from_documents(self.documents[i]))
    #             self.indices[i].storage_context.persist(storage_paths[i])

    # def load_data_from_url_path(self, url_path, i):
    #     print("\n loading web documents from  ", url_path, "\n")
    #     web_loader = BeautifulSoupWebReader()
    #     url_list = []
    #     url_list.extend(read_urls_from_json(url_path))
    #     web_documents = web_loader.load_data(urls=url_list)
    #     self.documents[i].extend(web_documents)

    # def load_data_from_dir_path(self, dir_path, i):
    #     if self.check_folder_path(dir_path):
    #         print("\n Loading files from ", dir_path, "\n")
    #         docs = SimpleDirectoryReader(dir_path).load_data()
    #         self.documents[i].extend(docs)
    #     elif dir_path is not None:
    #         folder_paths = self.get_all_folder_paths(dir_path)
    #         if folder_paths:
    #             for path in folder_paths:
    #                 print("\n Loading file from ", path, "\n")
    #                 if self.check_folder_path(path):
    #                     docs = SimpleDirectoryReader(path).load_data()
    #                     self.documents[i].extend(docs)

    def load_index_from_storage(self, storage_path):
        print("loading from storage", storage_path)
        store = storage_context.StorageContext.from_defaults(persist_dir=storage_path)
        index = load_indices_from_storage(storage_context=store)
        self.indices.append(index)

    # def get_all_folder_paths(self, root_dir):
    #     folder_paths = []
    #     for root, dirs, files in os.walk(root_dir):
    #         for dir in dirs:
    #             folder_path = os.path.join(root, dir)
    #             folder_paths.append(folder_path)
    #     print(folder_paths)
    #     return folder_paths

    def check_folder_path(self, path):
        everything = os.listdir(path)
        files = [f for f in everything if not os.path.isdir(os.path.join(path, f))]
        if files:
            return True
        else:
            return False

    def get_pdf_paths(self, directory_path):
        self.pdf_file_paths = glob.glob(f"{directory_path}/*.pdf")

    def get_csv_paths(self, directory_path):
        file_paths = glob.glob(f"{directory_path}/*.csv")
        self.csv_file_paths = []
        for path in file_paths:
            self.csv_file_paths.append(Path(path))

    # def load_csvs(self):
    #     for file_path in self.csv_file_paths:
    #         print("loading:", file_path)
    #         loaded_csvs = self.csv_loader.load_data(file_path)
    #         self.documents.extend(loaded_csvs)
    #         print("loaded")

    # def load_pdfs(self):
    #     for file_path in self.pdf_file_paths:
    #         print("loading: ", file_path)
    #         loaded_csvs = self.pdf_loader.load_data(file_path)
    #         self.documents.extend(loaded_csvs)
    #         print("loaded")

    def get_general_purpose_response(self, message):
        """
        This function is used to guess at what type of question the user is asking to the prompt the
        correct chat bot model.
        TODO: use function to get correct type of response
        """
        messages = [
            {
                "role": "system",
                "content": "You are asked questions about information that is on a public website.",
            },
            {"role": "user", "content": message},
        ]
        cli = OpenaiClient()
        tools = cli.get_llm_tools()
        api_functions = cli.get_api_functions()

        response = cli.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
            tools=tools,
            tool_choice="auto",  # auto is default, but we'll be explicit
        )
        response_message = response.choices[0].message
        print("response:", response_message)
        tool_calls = response_message.tool_calls
        if tool_calls is None:
            return response_message

        messages.append(response_message)  # extend conversation with assistant's reply

        # call functions if they were used
        for tool_call in tool_calls:
            print("tool call:", tool_call)
            function_name = tool_call.function.name
            function_to_call = api_functions[function_name]
            function_kwargs = json.loads(tool_call.function.arguments)
            try:
                function_response = function_to_call(**function_kwargs)
            except Exception as e:
                function_response = str(e)
        return function_response

    def log_text(self, text):
        data = {"log": text}
        json_string = json.dumps(data)
        with open("logs.json", "a") as f:
            f.write(json_string)

    def get_response(self, message, county):
        self.log_text("getting query")
        for i, path in enumerate(self.storage_paths):
            if county in path:
                index_index = i
                print("using index path:", path)
                break
        try:
            if self.dynamic_county_load:
                self.current_index = self.indices[0][0]
            elif self.one_bot:
                self.current_index = self.indices[0][0]
            else:
                self.current_index = self.indices[index_index][0]
        except Exception as e:
            self.log_text("error in getting index" + str(e))

        self.log_text(str(self.current_index))

        try:
            query_engine = self.current_index.as_query_engine()
        except Exception as e:
            self.log_text("error in query engine" + str(e))
            raise (e)

        self.log_text("query engine created")
        try:
            response = query_engine.query(message)
        except Exception as e:
            self.log_text("error in query" + str(e))
            return "Looks like our LLM is down. Sorry.", "", ""

        self.log_text("query done")

        response_text = str(response)
        source_paths = response.get_formatted_sources()
        print("source path", source_paths)
        source_text = ""
        pages = "Pages: "
        for node in response.source_nodes:
            source = self.get_doc_from_id(node.id_)
            source = convert_file_name_to_url(source)
            page = self.get_page_label_from_id(node.id_)
            print("source", source)
            if page is not None:
                pages = pages + page + ", "
            src_text = source.replace("{", "").replace("}", "")
            source_text += src_text + ", "
        source_text = source_text[:-2]
        pages = pages[:-2]
        if pages == "Pages: " or pages == "Pages":
            pages = ""
        print("\npages:::::\n", pages)

        return response_text, source_text, pages

    def get_page_label_from_id(self, id):
        try:
            doc = self.current_index.docstore.docs[id]
            page_label = doc.metadata.get("page_label")
            return page_label
        except:
            return ""

    def get_doc_from_id(self, id):
        doc = ""
        try:
            doc = self.current_index.docstore.docs[id].metadata["file_name"]
            path = self.current_index.docstore.docs[id].metadata["file_path"]
        except Exception:
            doc = self.current_index.docstore.docs[id].extra_info["URL"]
        print("doc", doc)
        return doc


if __name__ == "__main__":
    llam = LlamaRag(is_test=True)
    response = llam.get_general_purpose_response("When is it legal to water my lawn?")
    print("llama", response)
    print("done")
