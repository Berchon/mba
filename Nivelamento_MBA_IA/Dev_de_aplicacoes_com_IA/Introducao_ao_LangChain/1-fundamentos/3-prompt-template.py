from langchain.prompts import PromptTemplate

template = PromptTemplate(
  input_variables=["name"],
  template="Hi, I'm {name}! Tell me a joke about my name!"
)

text = template.format(name="Aldebaran")
print(text)