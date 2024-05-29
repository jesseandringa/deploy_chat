import json

from openai import OpenAI
from util import log_text


class openai_helper:
    def __init__(self, county):
        self.key = self.get_key_from_json_file("/app/openaikey.json")
        self.client = OpenAI(api_key=self.key["key"])
        self.county = county

    def get_key_from_json_file(self, filepath):
        with open(filepath, "r") as file:
            return json.load(file)

    def get_key_words_from_message(self, question):
        prompt = (
            f'Given the user query "{question}", return a short list of specific, short, concise document search terms designed to find and expand on the most relevant documents for answering the user query to be given to a postgres database. Consider search queries in the form of potential answers to the question in order to increase the accuracy of results. Return up to 8 items. Each search query should have a MAX of 32 characters. Answer ONLY IN THE FOLLOWING JSON FORMAT:'
            + """[["short search query 1", "weight of search query in (0, 1)"],["short search query 2", "weight of search query in (0, 1)"]]"""
        )
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )
        resp = str(completion.choices[0].message.content)

        """
        example response: 
        "key words to search[\n[\"Gunnison County Juvenile Services overview\", 0.9],\n[\"youth programs in Gunnison County\", 0.7],\n[\"juvenile justice resources Gunnison\", 0.8],\n[\"Gunnison County youth rehabilitation\", 0.6],\n[\"juvenile offenders support services\", 0.7],\n[\"alternative sentencing for juveniles\", 0.6],\n[\"Gunnison County juvenile court process\", 0.8],\n[\"community programs for at-risk youth\", 0.7]\n]"
        """
        # log_text("key words to search " + resp)
        resp = resp.replace("\n", "")
        json_resp = json.loads(resp)
        return json_resp

    def create_response_message(self, question, context):
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Answer the following question given following information from the"
                    + self.county
                    + " website ",
                },
                {
                    "role": "user",
                    "content": "question: " + question + " context: " + context,
                },
            ],
        )
        resp = str(completion.choices[0].message.content)
        log_text("completed answer: " + resp)
        return resp
