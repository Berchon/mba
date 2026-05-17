from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from utils import print_llm_result

load_dotenv()

msg1 = """
You are a senior software engineer. 
A user reports that an API request to the endpoint `/users` is taking 5 seconds to respond, which is too slow. 
Think in a Tree of Thought manner: 
- Generate at least 3 different possible causes for this latency. 
- For each cause, reason step by step about how likely it is and how you would verify it. 
- Then compare the branches and choose the most plausible one as the primary hypothesis. 
- Finish with a recommended next action to debug or fix the issue.
"""

msg2 = f"""
You are designing a service that processes millions of images daily. 
Think in a Tree of Thought manner: 
- Generate at least 3 different architecture options. 
- For each option, reason step by step about scalability, cost, and complexity. 
- Compare the options. 
- Choose the best trade-off and explain why it is superior to the others.
- Finish with "Final Answer: " + the chosen option.
"""

msg3 = f"""
You are designing a service that processes millions of images daily. 
Think in a Tree of Thought manner: 
- Think about at least 3 different architecture options. 
- For each option, reason step by step about scalability, cost, and complexity. 
- Compare the options. 
- Choose the best trade-off and explain why it is superior to the others.
- Finish with "Final Answer: " + the chosen option with 6 words or less.

- OUTPUT ONLY THE FINAL ANSWER, WITHOUT ANY OTHER TEXT.
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