import os

from mistralai import Mistral

api_key = os.environ["MISTRAL_API_KEY"]
model = "open-mixtral-8x22b"

client = Mistral(api_key=api_key)
text = """ D.   The individual or family has outstanding bills for one or more of the following City utility services: power provided under title 15, chapter15.20 of this Code, water provided under title 13, chapter 13.08 of this Code, sewer provided under title 13, chapter 13.32 of this Code, garbageprovided under section 7.04.030 of this Code, and stormwater provided under title 13, chapter 13.48 of this Code. (Ord. 19-05: Ord. 17-17)
3.04.080: FUNDS AVAILABLE FOR THE CITY'S LIMITED ASSISTANCE HEAT PROGRAM:
   A.   If an individual or family is eligible for the program under section 3.04.060 of this chapter, the eligible individual or family may, subject toavailability and appropriation of funds, be provided City funds to be applied to the outstanding City utility bills of the individual or family based onthe amount of the authorized State HEAT grant as follows: 
HEAT Grant Amount Approved ForIndividual Or Family At Time OfApplicationMaximum Amount Of Funds Available PerFiscal Year From The City To An EligibleIndividual Or Family To Be Applied ToOutstanding City Utility Bills
   $350.00 - $400.00 $50.00   $300.00 - $349.00 45.00   $250.00 - $299.00 40.00   $200.00 - $249.00 35.00   $150.00 - $199.00 30.00   $100.00 - $149.00 25.00   $50.00 - $99.00 20.00   $0.00 - $49.00 15.00
HEAT Grant Amount Approved ForIndividual Or Family At Time OfApplicationMaximum Amount Of Funds Available PerFiscal Year From The City To An EligibleIndividual Or Family To Be Applied ToOutstanding City Utility Bills
   B.   The funds provided to an eligible individual or family as determined in subsection A of this section shall be directly applied to outstandingCity utility bills of the eligible individual or family in the following descending order: power, water, sewer, garbage, stormwater. The fundsprovided under the program shall be applied toward the outstanding City utility bills of the eligible individual or family until the maximum amountprovided in subsection A of this section is expended or the outstanding City utility bills of the eligible individual or family are paid in full.   C.   No funds shall be provided to an eligible individual or family that exceeds the outstanding City utility bills of the eligible individual or family.As an eligible individual or family incurs more City utility charges during a fiscal year, City funds may be applied to future City utility bills in themanner described in this section, provided that the total City funds applied to the City utility bills of the eligible individual or family in the fiscalyear shall not exceed the maximum amount allowed in subsection A of this section. (Ord. 17-17)
3.04.090: APPROPRIATION OF FUNDS FOR THE CITY'S LIMITED ASSISTANCE HEAT PROGRAM:
The funds for this program shall be disbursed from the City's General Fund. The availability of funds for the program shall be subject to annualappropriation by the Murray City Municipal Council. Funds disbursed under the program shall be in addition to funds provided by HEAT orsimilar programs. (Ord. 17-17)
3.04.095: GOVERNMENT OR NONPROFIT UTILITY PAYMENT ASSISTANCE:
   A.   The City is authorized to work with and receive payments from any governmental or nonprofit agency providing utility payment assistancefor low-income households.   B.   The Mayor is approved and authorized to enter into any agreements with governmental or nonprofit agencies providing utility paymentassistance to low-income households that the Mayor determines is in the best interest of the City.   C.   The Director of Finance and Administration is authorized to waive utility account security deposits for low-income households pursuant toany agreement entered into in accordance with section B above, or during the period of time a governmental or nonprofit agency assists suchlow-income household with the payment for utility services. (Ord. 21-26)
3.04.100: INCOME ASSISTANCE FOR IMPROVEMENT DISTRICT ASSESSMENTS; DEFINITIONS:
For the purposes of this chapter, the following definitions shall apply:GRANTEE: A person who receives an abatement under this chapter.HOUSEHOLD: The grantee, the grantee's spouse and any child of the grantee over age eighteen (18) years living in the assessed property.HOUSEHOLD ASSETS: Stocks, bonds, certificates of deposit, savings accounts or other similar liquid assets which can easily be converted tocash, owned by the grantee, the grantee's spouse and any child of the grantee over the age of eighteen (18) years residing in the assessed'
"""
chat_response = client.chat.complete(
    model=model,
    messages=[
        {
            "role": "user",
            "content": f"If the following text is not helpful for understanding laws/ regulations/ and information about a city or municipality respond false, else response true:  {text}",
        },
    ],
)
print(chat_response.choices[0].message.content)
chat_response = client.chat.complete(
    model=model,
    messages=[
        {
            "role": "user",
            "content": f"Trim down the text as needed to get the main points, get rid of any information that is not helpful for understanding municipal code/ city information. {text}",
        },
    ],
)
print(chat_response.choices[0].message.content)
