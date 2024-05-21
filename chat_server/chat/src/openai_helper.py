import json
import os

from openai import OpenAI


class OpenaiClient:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = "gpt-3.5-turbo"
        self.client = OpenAI(api_key=self.api_key)

    def get_openai_response_to_message(self, messages):
        completion = self.client.chat.completions.create(
            model=self.model, messages=messages
        )
        return completion.choices[0].message

    def get_api_key(self, filepath):
        file_path = "../resources/text.json"

        # Open the JSON file and load its contents into a Python object
        with open(file_path, "r") as file:
            data = json.load(file)

            # Now, `data` is a Python dictionary or list that represents the JSON structure
            print(data)
            return data

    def compose_messages(self, roles, contents):
        messages = []
        for i in range(len(roles)):
            msg = {"role": roles[i], "content": contents[i]}
            messages.append(msg)

        return messages

    def get_llm_tools(
        self,
    ):
        # docs: https://platform.openai.com/docs/guides/function-calling
        return [
            {
                "type": "function",
                "function": {
                    "name": "municipal_code",
                    "descrtipion": "Check whether a question is about laws, codes, regulations, or legal documents",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "is_municipal_code_related": {
                                "type": "string",
                                "description": "true or false if the question is about laws, codes, regulations, or legal documents",
                            },
                        },
                    },
                    "required": ["is_municipal_code_related"],
                },
            },
        ]

    def get_api_functions(
        self,
    ):
        def municipal_code(is_municipal_code_related=None):
            print(
                "in municipal code with is_municipal_code_related:",
                is_municipal_code_related,
            )
            if is_municipal_code_related:
                return True
            if (
                is_municipal_code_related == "true"
                or is_municipal_code_related == "True"
                or is_municipal_code_related == "TRUE"
            ):
                return True
            return False

        return {
            "municipal_code": municipal_code,
        }


if __name__ == "__main__":
    openaiClient = OpenaiClient()
    contents = [
        "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair.",
        "Compose a haiku that explains the concept of recursion in programming.",
    ]
    roles = ["system", "user"]
    messages = openaiClient.compose_messages(roles, contents)
    response = openaiClient.get_openai_response_to_message(messages)
    print("resposne", response)
