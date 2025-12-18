# 📘 Parte 4 – Gerenciamento de Memória no LangChain

## 1. Visão geral da parte

O módulo **Parte 4 – Gerenciamento de Memória** tem como objetivo introduzir e aprofundar o conceito de **memória conversacional** em aplicações construídas com LangChain. Até aqui, o estudo focou em prompts, chains, modelos e agentes de forma majoritariamente *stateless* — ou seja, cada chamada ao modelo era independente.

Nesta parte, passamos a entender **como e por que manter histórico de conversas**, explorando como o contexto acumulado influencia diretamente o comportamento, a coerência e a utilidade das respostas de um LLM.

### Problemas que esta parte resolve

* Como permitir que o modelo **lembre informações fornecidas anteriormente** pelo usuário
* Como estruturar aplicações conversacionais reais, em vez de chamadas isoladas ao LLM
* Como **controlar o crescimento do histórico**, evitando:

  * Custos excessivos de tokens
  * Vazamento de informações antigas ou irrelevantes
  * Respostas enviesadas por contexto obsoleto

### Conexão com as próximas partes

O gerenciamento de memória é um **pré-requisito fundamental** para:

* Agentes com múltiplos passos e decisões
* Ferramentas que dependem de contexto contínuo
* Aplicações multiusuário (sessions)
* Persistência de memória (bancos de dados, Redis, etc.)

Nas próximas partes, esses conceitos evoluem naturalmente para **agentes**, **tools**, **memória persistente** e **arquiteturas de produção**.

---

## 2. Explicação detalhada dos arquivos

### 📄 1-armazenamento-de-historico.py

#### O que este arquivo faz

Este exemplo demonstra a forma **mais direta e intuitiva** de trabalhar com memória no LangChain:

* Todo o histórico da conversa é armazenado
* O modelo tem acesso completo a todas as mensagens anteriores
* O LLM consegue “lembrar” informações ditas pelo usuário

É o equivalente a uma conversa contínua, sem nenhum tipo de poda ou limitação.

#### Conceito demonstrado

* `InMemoryChatMessageHistory`
* `RunnableWithMessageHistory`
* Uso explícito de `MessagesPlaceholder` em prompts

Esse é o **padrão base de memória conversacional** no LangChain.

---

#### Estrutura do código por blocos

##### 1. Carregamento de dependências e variáveis de ambiente

```python
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory

load_dotenv()
```

* `load_dotenv()` carrega credenciais da API
* O modelo usado é um **chat model**, não um completion model

---

##### 2. Definição do prompt com espaço para histórico

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])
```

Pontos-chave:

* `MessagesPlaceholder` indica ao LangChain **onde inserir o histórico**
* O histórico será uma lista de mensagens (human/assistant/system)
* A ordem importa: histórico vem **antes** do input atual

---

##### 3. Inicialização do modelo

```python
chat_model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.9
)
```

* Modelo de chat
* `temperature` alta favorece respostas mais criativas

---

##### 4. Criação da chain base

```python
chain = prompt | chat_model
```

Aqui ainda **não existe memória**. É apenas uma chain comum.

---

##### 5. Armazenamento de sessões

```python
session_store: dict[str, InMemoryChatMessageHistory] = {}


def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in session_store:
        session_store[session_id] = InMemoryChatMessageHistory()
    return session_store[session_id]
```

* Cada `session_id` possui seu próprio histórico
* Isso permite múltiplos usuários ou conversas paralelas

---

##### 6. Envolvendo a chain com memória

```python
conversational_chain = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)
```

Esse é o **ponto central do exemplo**:

* `RunnableWithMessageHistory` injeta automaticamente:

  * Mensagens do usuário
  * Respostas do modelo
* O histórico cresce a cada interação

---

##### 7. Execução com sessão fixa

```python
config = {"configurable": {"session_id": "demo-session"}}
```

Todas as chamadas usam o mesmo `session_id`, garantindo continuidade.

---

#### Resultado observado

O modelo:

* Aprende o nome do usuário
* Consegue repeti-lo
* Usa a informação em respostas futuras

Isso confirma que o **histórico completo está sendo preservado**.

---

### 📄 2-historico-baseado-em-sliding-window.py

#### O que este arquivo faz

Este exemplo introduz uma estratégia mais avançada:

* O histórico completo **existe**, mas
* Apenas uma **janela limitada** é passada ao modelo

O objetivo é demonstrar **controle fino sobre contexto**.

---

#### Conceito demonstrado

* Sliding window de memória
* `trim_messages`
* Separação entre:

  * Histórico bruto armazenado
  * Histórico efetivamente enviado ao LLM

---

#### Estrutura do código por blocos

##### 1. Prompt com histórico

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that answers with a short joke when possible."),
    MessagesPlaceholder("history"),
    ("human", "{input}"),
])
```

Semelhante ao exemplo anterior, mas com um comportamento de sistema diferente.

---

##### 2. Função de preparação de inputs

```python
def prepare_inputs(payload: dict) -> dict:
    raw_history = payload.get("raw_history", [])
    trimmed = trim_messages(
        raw_history,
        token_counter=len,
        max_tokens=2,
        strategy="last",
        start_on="human",
        include_system=True,
        allow_partial=False,
    )
    return {
        "input": payload.get("input", ""),
        "history": trimmed
    }
```

Aqui está o **coração da sliding window**:

* `raw_history`: histórico completo armazenado
* `trim_messages`: reduz o histórico
* Apenas as últimas mensagens relevantes são mantidas

Importante:

* O modelo **não vê tudo**
* Ele só responde com base na janela ativa

---

##### 3. Uso de RunnableLambda

```python
prepare = RunnableLambda(prepare_inputs)
chain = prepare | prompt | llm
```

* Permite pré-processamento antes do prompt
* Padrão extremamente comum em pipelines reais

---

##### 4. Memória com chave diferente

```python
conversational_chain = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="raw_history"
)
```

Diferente do primeiro exemplo:

* O histórico armazenado chama-se `raw_history`
* O histórico enviado ao prompt chama-se `history`

Essa separação é **intencional e poderosa**.

---

#### Resultado observado

Quando o usuário pergunta seu nome:

* O modelo **não sabe responder**
* A informação foi descartada pela sliding window

Isso demonstra claramente:

> Memória armazenada ≠ memória usada pelo modelo

---

## 3. Comparação entre os arquivos

| Aspecto                   | Histórico Completo   | Sliding Window    |
| ------------------------- | -------------------- | ----------------- |
| Simplicidade              | Alta                 | Média             |
| Controle de contexto      | Nenhum               | Alto              |
| Custo de tokens           | Crescente            | Controlado        |
| Risco de info irrelevante | Alto                 | Baixo             |
| Casos de uso              | Demos, chats simples | Produção, agentes |

### Quando usar cada abordagem

* **Histórico completo**:

  * Tutoriais
  * Prototipação
  * Conversas curtas

* **Sliding window**:

  * Chats longos
  * Sistemas multiusuário
  * Agentes autônomos

---

## 4. Aspectos dependentes vs independentes de modelo

### Dependentes de modelo

* Uso de `ChatPromptTemplate`
* Mensagens estruturadas (human/system/assistant)
* Necessidade de modelos do tipo *chat*

### Independentes de modelo (abstrações LangChain)

* `RunnableWithMessageHistory`
* Estratégias de memória
* Pipelines com `RunnableLambda`

### Boas práticas de desacoplamento

* Isolar prompts
* Isolar memória
* Trocar modelos sem reescrever lógica

---

## 5. Boas práticas e dicas

### Erros comuns

* Não limitar histórico
* Confiar que o modelo “vai lembrar” sem memória
* Misturar histórico bruto com histórico de prompt

### Padrões recomendados

* Sempre separar:

  * Armazenamento
  * Contexto ativo
* Usar sliding window por padrão
* Aumentar janela apenas quando necessário

### Evolução para aplicações reais

* Substituir `InMemoryChatMessageHistory`
* Persistir em banco ou cache
* Combinar com ferramentas e agentes

---

## 6. Resumo final

### Principais aprendizados

* Memória não é automática em LLMs
* LangChain fornece abstrações claras para isso
* Histórico completo é simples, mas perigoso
* Sliding window equilibra contexto, custo e relevância

### Checklist mental do aluno

* [x] Sei o que é memória conversacional
* [x] Sei usar `RunnableWithMessageHistory`
* [x] Sei controlar histórico com sliding window
* [x] Sei quando descartar contexto antigo
* [x] Estou pronto para agentes com memória
