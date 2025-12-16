# RunnableLambda: permite criar um Runnable a partir de uma função lambda 
# ou função normal em Python.
# Ele é util quando você não pode usar decoradores/anotações diretamente, 
# como quando a função é definida em outro módulo, biblioteca ou tem um 
# contrato prévio.

from langchain_core.runnables import RunnableLambda

def parse_number(text:str) -> int:
    return int(text.strip())

parse_runnable = RunnableLambda(parse_number)

number = parse_runnable.invoke("10")

print(number)
print("="*30)
print(type(number))