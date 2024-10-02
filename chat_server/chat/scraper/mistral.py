import ollama

api_key = None  # os.environ["MISTRAL_API_KEY"]
model = None  # "open-mixtral-8x22b"
client = None  # Mistral(api_key=api_key)


def trim_text_using_mistral(text):
    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "user",
                "content": f"Trim down the text as needed to get the main points, get rid of any information that is not helpful for understanding municipal code/ city information. {text}",
            },
        ],
    )
    return chat_response.choices[0].message.content


def check_if_text_is_helpful(text):
    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "user",
                "content": f"If the following text is not helpful for understanding laws/ regulations/ and information about a city or municipality respond only with the word false, else response only the word true. Here is the text:  {text}",
            },
        ],
    )
    # print(chat_response.choices[0].message.content)

    # check if repsonse starts with true or false case insensitive
    if chat_response.choices[0].message.content.lower().startswith("true"):
        return True
    elif chat_response.choices[0].message.content.lower().startswith("false"):
        return False
    else:
        return True


def trim_text_using_ollama(text):
    response = ollama.generate(
        model="llama3.2:1b",
        prompt=f"Trim down the the following text by getting rid of any nonsense chars and strings, also get rid of anything about what languages we can see this in, keep the rest the same: {text}",
    )
    return response["response"]


def check_if_text_is_helpful_using_ollama(text):
    response = ollama.generate(
        model="llama3.2:1b",
        prompt=f"Does the following text contain helpful information about the city rules/regulations/information? respond only with the word true or false if accordingly. Here is the text:  {text}",
    )

    if response["response"].lower().startswith("true"):
        return True
    elif response["response"].lower().startswith("false"):
        return False
    else:
        return True


# text = """
# Chapter 8 - ANIMALS | Code of Ordinances | Cullman, AL | Municode Library Chapter 8 - ANIMALS | Code of Ordinances | Cullman, AL | Municode Library Skip to Sec. 8-28. - Penalty; violator responsible for costs.
# Skip to main content Cullman, AL
# Notifications
# Sign In Help Select KaroBatak SimalungunBatak (Simplified)Chinese (Traditional)ChuukeseChuvashCorsicanCrimean CreoleHakha (Kurmanji)Kurdish (Jawi)MalayalamMalteseMamManxMaoriMarathiMarshalleseMarwadiMauritian CreoleMeadow MariMeiteilon (Manipuri)MinangMizoMongolianMyanmar (Burmese)Nahuatl (Eastern Huasteca)NdauNdebele (South)Nepalbhasa (Newari)NepaliNKoNorwegianNuerOccitanOdia (Oriya)OromoOssetianPangasinanPapiamentoPashtoPersianPolishPortuguese (Brazil)Portuguese (Portugal)Punjabi (Gurmukhi)Punjabi (Shahmukhi)QuechuaQʼeqchiʼRomaniRomanianRundiRussianSami (North)SamoanSangoSanskritSantaliScots GaelicSepediSerbianSesothoSeychellois (Tifinagh)TamilTatarTeluguTetumThaiTibetanTigrinyaTivTok MayaZapotecZuluPowered by Translate Home
# Codes
# Ordinances Documents
# Links
# www.cullmanal.gov
# Municode
# Municode Library
# Order a physical copy
# Terms of use
# Copyright © 2024 Municode.com
# Code of Ordinances Recent Changes
# Previous Versions
# Notifications
# Sign In View Table Close
# Meeting Details
# View All Meetings
# Close
# Meeting Details Close Print or Download Table of Contents Close Add Note Loading, please wait
# Cullman, Alabama - Code of Ordinances Chapter 8 - ANIMALS ARTICLE II. - ADMINISTRATION AND ENFORCEMENT
# Sec. 8-28. - Penalty; violator responsible for costs. Show Changes
# more
# Code of Ordinances Recent Changes Pending Amendments
# Previous Versions MuniPRO My Saved Searches
# My Drafts
# """
# helpful = check_if_text_is_helpful_using_ollama(text)
# cleaned = trim_text_using_ollama(text)
# print(f"helpful is {helpful}")
# print(f"cleaned is {cleaned}")
