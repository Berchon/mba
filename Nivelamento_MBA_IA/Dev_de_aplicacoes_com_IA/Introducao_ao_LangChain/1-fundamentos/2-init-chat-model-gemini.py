from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

openRouter = init_chat_model(model="gemini-2.5-flash", model_provider="google_genai")
answer = openRouter.invoke("Hello, world!")

print(answer)
print("="*30)
print(answer.content)