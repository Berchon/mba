from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

load_dotenv()

question_template = PromptTemplate(
  input_variables=["name"],
  template="Hi, I'm {name}! Tell me a joke about my name!"
)

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5)

chain = question_template | model

result = chain.invoke({"name": "Aldebaran"})

print(result)
print("="*30)
print(result.content)