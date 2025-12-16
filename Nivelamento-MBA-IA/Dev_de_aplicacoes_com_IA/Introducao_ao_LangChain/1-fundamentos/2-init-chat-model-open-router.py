from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

openRouter = init_chat_model(model="meta-llama/llama-3.3-70b-instruct:free", model_provider="openai")
answer = openRouter.invoke("Hello, world!")

print(answer)
print("="*30)
print(answer.content)