from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

model = ChatOpenAI(model="meta-llama/llama-3.3-70b-instruct:free", temperature=0.5)
message = model.invoke("Hello, world!")

print(message)
print("="*30)
print(message.content)