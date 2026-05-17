# 📘 Parte 1 – Fundamentos do LangChain

## 🎯 Objetivo da Parte

Esta primeira parte do estudo tem como objetivo apresentar os **conceitos fundamentais do LangChain**, que servem como base sólida para qualquer aplicação mais avançada envolvendo **LLMs (Large Language Models)** e **Chat Models**.

Ao final desta parte, você será capaz de:

* 🔌 Inicializar e utilizar modelos de linguagem via LangChain
* 🤖 Entender claramente a diferença entre **LLMs tradicionais** e **Chat Models**
* 🧱 Compreender como o LangChain abstrai provedores e modelos
* 🧩 Criar prompts reutilizáveis usando **PromptTemplate** e **ChatPromptTemplate**
* 🧠 Preparar seu código para evoluir para **chains, memory e agents**

Esses fundamentos são **obrigatórios** antes de avançar para aplicações reais.

---

## 🌍 O Papel dos Fundamentos no Ecossistema do LangChain

O LangChain atua como uma **camada de abstração e orquestração** sobre modelos de linguagem.

Antes de construir fluxos complexos, agentes autônomos ou aplicações com memória, é essencial dominar:

* Como conversar com um modelo
* Como estruturar prompts corretamente
* Como separar **lógica de negócio** de **detalhes do modelo**
* Como escrever código desacoplado, reutilizável e sustentável

👉 Os arquivos desta parte mostram uma **progressão pedagógica intencional**, indo do uso mais direto até abstrações mais profissionais.

---

## 📂 Visão Geral dos Arquivos

| Arquivo              | Conceito Principal                | Papel Didático                 |
| -------------------- | --------------------------------- | ------------------------------ |
| `hello-world.py`     | Uso direto de um Chat Model       | Primeiro contato com LangChain |
| `init-chat-model.py` | Inicialização genérica de modelos | Desacoplamento e portabilidade |
| `prompt-template.py` | PromptTemplate                    | Prompts reutilizáveis          |
| `prompt-template.py` | ChatPromptTemplate                | Prompts estruturados para chat |

---

## 1️⃣ hello-world.py

### 📌 O que este código faz?

Realiza a **primeira interação com um Chat Model**, usando diretamente uma classe específica do provedor Google (Gemini).

É o clássico **Hello World do LangChain**.

---

### 📎 Código

```python
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5)
message = model.invoke("Hello, world!")

print(message)
print("=" * 30)
print(message.content)
```

---

### 🧠 Conceitos Demonstrados

* 🔐 Carregamento de variáveis de ambiente (`load_dotenv`)
* 🤖 Uso direto de um Chat Model
* 🔁 Chamada síncrona via `.invoke()`
* 📦 Diferença entre objeto de resposta e texto final

---

### 🔍 Explicação Detalhada por Blocos

#### 1. Configuração do ambiente

```python
load_dotenv()
```

Carrega chaves de API e configurações sensíveis a partir do arquivo `.env`.

---

#### 2. Inicialização do modelo

```python
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.5
)
```

* Classe específica do provedor Google
* `temperature` controla o grau de criatividade

---

#### 3. Chamada ao modelo

```python
message = model.invoke("Hello, world!")
```

* `.invoke()` é a interface padrão do LangChain
* Retorna um **AIMessage**, não apenas uma string

---

#### 4. Acesso ao conteúdo

```python
message.content
```

* Texto puro da resposta
* Essencial para processamento posterior

---

### ✅ Quando usar essa abordagem?

* Estudos iniciais
* Testes rápidos
* Quando o provedor é conhecido e fixo

### ❌ Limitação

Código fortemente **acoplado** ao provedor Google.

---

## 2️⃣ init-chat-model.py

### 📌 O que este código faz?

Inicializa um Chat Model usando uma **fábrica genérica do LangChain**, desacoplando o código do provedor específico.

---

### 📎 Código

```python
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

chat_model = init_chat_model(
    model="gemini-2.5-flash",
    model_provider="google_genai"
)

answer = chat_model.invoke("Hello, world!")

print(answer)
print("=" * 30)
print(answer.content)
```

---

### 🧠 Conceitos Demonstrados

* 🧱 Abstração de provedores
* 🔄 Inicialização genérica de chat models
* ♻️ Código portátil e reutilizável

---

### 🔍 O que muda em relação ao código anterior?

| Aspecto          | hello-world.py | init-chat-model.py |
| ---------------- | -------------- | ------------------ |
| Classe           | Específica     | Genérica           |
| Acoplamento      | Alto           | Baixo              |
| Portabilidade    | Baixa          | Alta               |
| Uso profissional | Limitado       | Recomendado        |

---

### ✅ Quando usar essa abordagem?

* Projetos reais
* Código de produção
* Ambientes com troca de modelo/provedor

💡 **Boa prática**: prefira `init_chat_model` sempre que possível.

---

## 3️⃣ prompt-template.py — PromptTemplate

### 📌 O que este código faz?

Cria **prompts dinâmicos e reutilizáveis**, separando texto de lógica.

---

### 📎 Código

```python
from langchain.prompts import PromptTemplate

template = PromptTemplate(
    input_variables=["name"],
    template="Hi, I'm {name}! Tell me a joke about my name!"
)

text = template.format(name="Aldebaran")
print(text)
```

---

### 🧠 Conceitos Demonstrados

* 🧩 Separação entre prompt e lógica
* 🔁 Parametrização de prompts
* ♻️ Reutilização em múltiplos contextos

---

### 🔍 Explicação Detalhada

* `input_variables`: define os parâmetros obrigatórios
* `{name}`: placeholder dinâmico
* `format()`: gera o prompt final

---

### ✅ Quando usar PromptTemplate?

* Sempre que houver variáveis
* Em chains e agents
* Em qualquer aplicação real

❌ Evite prompts hardcoded em produção.

---

## 4️⃣ ChatPromptTemplate — Prompt para Chat Models

### 📌 O que este código faz?

Cria prompts **estruturados por papéis**, próprios para Chat Models.

---

### 📎 Código

```python
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate

load_dotenv()

system = ("system", "you are an assistant that answers questions in a {style} style")
user = ("user", "{question}")

chat_prompt = ChatPromptTemplate([system, user])

messages = chat_prompt.format_messages(
    style="funny",
    question="Who is Alan Turing?"
)

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5)
result = model.invoke(messages)

print(result.content)
```

---

### 🧠 Conceitos Demonstrados

* 🎭 Papéis explícitos (`system`, `user`)
* 📬 Lista de mensagens como entrada
* 🔄 `format_messages()` vs `format()`

---

## 🧩 PromptTemplate vs ChatPromptTemplate

### Qual a diferença e quando usar cada um?

Entender a diferença entre **PromptTemplate** e **ChatPromptTemplate** é essencial para escrever prompts corretos, reutilizáveis e alinhados com o tipo de modelo que você está utilizando.

Embora ambos sirvam para **construir prompts dinâmicos**, eles atendem a **estruturas de entrada diferentes** e representam **paradigmas distintos de interação** com modelos de linguagem.

---

### 🧠 Visão Geral

| Aspecto                        | PromptTemplate | ChatPromptTemplate |
| ------------------------------ | -------------- | ------------------ |
| Tipo de saída                  | `str` (texto)  | Lista de mensagens |
| Paradigma                      | Texto linear   | Conversacional     |
| Papéis (system/user/assistant) | ❌ Não          | ✅ Sim              |
| Compatível com Chat Models     | ⚠️ Parcial     | ✅ Total            |
| Uso em chains modernas         | ⚠️ Limitado    | ✅ Recomendado      |
| Uso em agents                  | ❌ Raro         | ✅ Padrão           |
| Nível de controle              | Médio          | Alto               |

---

### 📝 PromptTemplate

**O que é?**
Gera uma única string de texto a partir de um template parametrizável.

```python
from langchain.prompts import PromptTemplate

template = PromptTemplate(
    input_variables=["topic"],
    template="Explique o conceito de {topic} para um iniciante."
)

prompt = template.format(topic="LangChain")
```

**Quando usar:**

* Texto simples
* Sem contexto conversacional
* Estudos iniciais

**Limitações:**

* Não possui papéis
* Menor controle de comportamento

---

### 💬 ChatPromptTemplate

**O que é?**
Cria uma lista estruturada de mensagens, adequada a Chat Models.

```python
from langchain.prompts import ChatPromptTemplate

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é um professor de programação."),
    ("human", "Explique o conceito de {topic} para um iniciante.")
])

messages = chat_prompt.format_messages(topic="LangChain")
```

**Quando usar:**

* Chat Models (Gemini, GPT, Claude)
* System prompt
* Chains, memory e agents

**Vantagens:**

* Controle fino
* Escalável
* Padrão moderno

---

### 🎯 Regra de Ouro

> **Texto simples → PromptTemplate**
> **Conversas e comportamento → ChatPromptTemplate**

---

## 🔄 Comparação Geral das Abordagens

| Tema           | Simples           | Abstraído        |
| -------------- | ----------------- | ---------------- |
| Modelo         | Classe específica | Fábrica genérica |
| Prompt         | String literal    | Templates        |
| Escalabilidade | Baixa             | Alta             |

---

## 🤖 Dependência de Modelo

### 🔒 Dependente de Chat Models

* Estrutura de mensagens
* Papéis (system, user)
* `.content`

### 🔓 Independente (LangChain)

* `.invoke()`
* PromptTemplate
* Chains
* Memory
* Agents

💡 O LangChain protege seu código contra mudanças de modelo.

---

## ✅ Boas Práticas Introduzidas

* 🔐 Uso de `.env`
* 🧱 Inicialização genérica de modelos
* 🧩 Separação de prompts e lógica
* ♻️ Reutilização desde o início

---

## 🧠 Resumo Final — Parte 1

### 📚 Conceitos Aprendidos

* O papel do LangChain
* Inicialização de Chat Models
* Uso de `.invoke()`
* PromptTemplate vs ChatPromptTemplate
* Abstração de provedores

---

### ✔️ Checklist Completo de Conhecimento

* [x] Sei explicar a diferença entre LLM e Chat Model
* [x] Sei inicializar modelos direta e genericamente
* [x] Entendo o papel do `load_dotenv`
* [x] Sei o que `.invoke()` retorna
* [x] Sei acessar `message.content`
* [x] Sei criar PromptTemplate
* [x] Sei criar ChatPromptTemplate
* [x] Sei quando usar string vs mensagens
* [x] Entendo o que é dependente de modelo
* [x] Estou pronto para avançar para Chains

---

🚀 Com esses fundamentos dominados, você está pronto para avançar no LangChain.
