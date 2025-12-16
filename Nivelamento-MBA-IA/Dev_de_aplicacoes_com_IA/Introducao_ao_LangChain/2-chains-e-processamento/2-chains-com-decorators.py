from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import chain

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5)

@chain
def square(input_dict: dict) -> dict:
    x = input_dict["x"]
    return {"square_result": x * x}

question_template2 = PromptTemplate(
  input_variables=["square_result"],
  template="Tell me abour the number {square_result}!"
)

chain2 = square | question_template2 | model

result2 = chain2.invoke({"x": 10})

print(result2)
print("="*30)
print(result2.content)