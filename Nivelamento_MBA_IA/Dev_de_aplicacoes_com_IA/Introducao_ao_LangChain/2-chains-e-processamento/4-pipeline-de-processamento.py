from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

template_translate = PromptTemplate(
  input_variables=["initial_text", "target_language"],
  template="Translate the following text to {target_language}\n ```{initial_text}```"
)

template_summary = PromptTemplate(
  input_variables=["text_to_summarize"],
  template="Summarize the following text in 4 words:\n ```{text_to_summarize}```"
)

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5)

translate = template_translate | model | StrOutputParser()
pipeline = {"text_to_summarize": translate} | template_summary | model | StrOutputParser()

result = pipeline.invoke({
  "initial_text": "LangChain é um framework de desenvolvimento de aplicações de IA",
  "target_language": "English"
})

print(result)
print("="*30)
print(type(result))