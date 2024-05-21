def get_response_message(question, county, llama):
    response_text, sources, pages = llama.get_response(question, county)

    # openai_client = openai_helper.OpenAI()
    # roles = ['system','user']
    # contents = [response_text,input]
    # messages = openai_client.compose_messages(roles,contents)
    # response = openai_client.get_openai_response_to_message(messages)

    print("resposne_text", str(response_text))
    print("")
    # print('open response: ', str(response))

    return {
        "response": str(response_text),
        "sources": str(sources),
        "pages": str(pages),
        "sender": "bot",
    }
