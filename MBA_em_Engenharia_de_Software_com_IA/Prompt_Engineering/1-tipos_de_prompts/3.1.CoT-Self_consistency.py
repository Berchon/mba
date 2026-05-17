from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from utils import print_llm_result

load_dotenv()

msg1 = """
Question: In an API endpoint that returns a list of users and their posts, the developer wrote:

users := db.FindAllUsers()
for _, u := range users {
    u.Posts = db.FindPostsByUserID(u.ID)
}

How many database queries will this code execute if there are N users?

Generate 3 different reasoning paths step by step.
At the end, summarize the answers and choose the most consistent one, ignoring outliers.
If there are 3 different answers, ONLY reply: "I can't find a consistent answer".
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