from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from utils import print_llm_result

load_dotenv()
msg1 = "What's Brazil's capital?"

msg2 = """
Find the user intent in the following text: 
I'm looking for a restaurant around São Paulo who has a good rating for Japanese food.
"""

msg3 = "What's Brazil's capital? Respond only with the city name."

model_strong = ChatGoogleGenerativeAI(model="gemini-3-flash-preview")
model_mid = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
model_light = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

response1_light = model_light.invoke(msg1)
response1_mid = model_mid.invoke(msg1)
response1_strong = model_strong.invoke(msg1)

print_llm_result(msg1, response1_light)
print_llm_result(msg1, response1_mid)
print_llm_result(msg1, response1_strong)

print("="*70)

response2_light = model_light.invoke(msg2)
response2_mid = model_mid.invoke(msg2)
response2_strong = model_strong.invoke(msg2)

print_llm_result(msg2, response2_light)
print_llm_result(msg2, response2_mid)
print_llm_result(msg2, response2_strong)

print("="*70)

response3_light = model_light.invoke(msg3)
response3_mid = model_mid.invoke(msg3)
response3_strong = model_strong.invoke(msg3)

print_llm_result(msg3, response3_light)
print_llm_result(msg3, response3_mid)
print_llm_result(msg3, response3_strong)