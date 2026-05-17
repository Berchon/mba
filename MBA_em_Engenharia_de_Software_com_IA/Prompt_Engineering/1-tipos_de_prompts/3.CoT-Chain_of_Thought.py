from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from utils import print_llm_result

load_dotenv()

msg1 = """
Classify the log severity.

Input: "Disk usage at 85%."
Answer only with INFO, WARNING, or ERROR.
"""

msg2 = """
Classify the log severity.

Input: "Disk usage at 85%."
Think step by step about why this is INFO, WARNING, or ERROR. 
At the end, give only the final answer after "Answer:".
"""

msg3 = """
Question: How many "r" are in the word "strawberry"?
Answer only with the number of "r".
"""

msg4 = """
Question: How many "r" are in the word "strawberry"?
Explain step by step by breaking down each letter in bullet points, pointing out the "r" before giving the final answer. 
Give the final result after "Answer:".
"""

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

print("="*70)

response4_light = model_light.invoke(msg4)
response4_mid = model_mid.invoke(msg4)
response4_strong = model_strong.invoke(msg4)

print_llm_result(msg4, response4_light)
print_llm_result(msg4, response4_mid)
print_llm_result(msg4, response4_strong)