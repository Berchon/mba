# 📘 Parte 3 – Agentes e Tools no LangChain

## Visão geral da parte

Esta parte do estudo tem como objetivo demonstrar **como LLMs podem ir além de responder texto**, passando a **executar ações controladas** por meio de ferramentas externas (*tools*). Aqui o LangChain é apresentado como uma **camada de orquestração** entre o modelo de linguagem e funções do mundo real.

### Problemas que essa parte resolve

Antes de agentes e tools, o LLM:

* Apenas gera texto
* Pode “alucinar” respostas
* Não tem como executar código ou consultar fontes externas de forma confiável

Com agentes e tools, passamos a:

* Delegar tarefas específicas para funções determinísticas
* Restringir a fonte de verdade às ferramentas
* Tornar o comportamento do modelo **mais previsível e auditável**

### Conexão com as próximas partes

Esta parte prepara o terreno para:

* **Chains mais complexas** (orquestração multi-etapas)
* **RAG (Retrieval-Augmented Generation)**
* **Agentes mais autônomos e especializados**
* **Aplicações reais com segurança e controle**

---

## Arquivo 1 – `1-agente-react-e-tools.py`

### O que este arquivo faz

Implementa um **agente ReAct (Reason + Act)** usando um *prompt manual*, onde o LLM:

1. Raciocina explicitamente (Thought)
2. Decide qual ferramenta usar (Action)
3. Executa a ferramenta
4. Observa o resultado
5. Repete o ciclo até chegar à resposta final

### Conceito demonstrado

* **Padrão ReAct**
* Agentes baseados em **parsing de texto**
* Forte dependência de prompt

### Estrutura geral do código

#### 1. Carregamento de ambiente

```python
load_dotenv()
```

Carrega variáveis de ambiente, normalmente usadas para chaves de API.

---

#### 2. Definição das tools

```python
@tool("calculator", return_direct=True)
def calculator(expression: str) -> str:
```

Pontos importantes:

* `@tool` transforma uma função Python em uma tool do LangChain
* `return_direct=True` indica que o retorno da tool pode ser usado diretamente como resposta final
* Uso de `eval` **é propositalmente perigoso**, servindo apenas para fins didáticos

A função:

* Avalia uma expressão matemática
* Soma `+3` ao resultado (detalhe importante para mostrar que a tool é a fonte da verdade)

---

```python
@tool("web_search_mock")
def web_search_mock(query: str) -> str:
```

Simula uma busca na web usando um dicionário fixo. Isso permite:

* Testar agentes sem depender de APIs externas
* Demonstrar que o LLM **não sabe as respostas**, apenas usa ferramentas

---

#### 3. Inicialização do modelo

```python
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5)
```

Características:

* Modelo **chat-based**
* Temperatura moderada
* Totalmente substituível por outros modelos compatíveis

---

#### 4. Prompt ReAct manual

```python
prompt = PromptTemplate.from_template("""
...
""")
```

Este é o coração do padrão ReAct:

* Define explicitamente o formato de saída
* Obriga o modelo a seguir o ciclo Thought → Action → Observation
* Proíbe uso de conhecimento prévio

⚠️ **Fragilidade**: qualquer erro de formatação quebra o agente.

---

#### 5. Criação do agente

```python
agent_chain = create_react_agent(llm, tools, prompt)
```

Aqui o LangChain:

* Injeta as tools no prompt
* Controla o ciclo de execução

---

#### 6. Executor

```python
agent_executor = AgentExecutor.from_agent_and_tools(...)
```

Responsabilidades do `AgentExecutor`:

* Executar o loop do agente
* Controlar número máximo de iterações
* Lidar com erros de parsing

---

### Quando usar este padrão

* Ensino e aprendizado
* Demonstração conceitual de agentes
* Depuração de raciocínio do modelo

### Limitações

* Frágil em produção
* Parsing de texto é instável
* Alto acoplamento ao prompt

---

## Arquivo 1.1 – `1.1-agente-tool-calling.py`

### O que este arquivo faz

Implementa um agente usando **Tool Calling**, onde:

* O modelo **não precisa seguir um formato textual rígido**
* O LangChain intercepta chamadas estruturadas às tools

### Conceito demonstrado

* **Tool Calling nativo**
* Abordagem recomendada para aplicações reais

---

### Principais diferenças estruturais

#### Prompt baseado em chat

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "..."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])
```

Vantagens:

* Mais natural para modelos chat
* Menos dependente de formatação manual

---

#### Criação do agente

```python
agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)
```

Aqui:

* O modelo retorna **estruturas internas**, não texto livre
* O LangChain executa a tool automaticamente

---

### Vantagens do Tool Calling

* Maior robustez
* Melhor controle
* Ideal para produção
* Menos erros de parsing

### Quando usar

* Sistemas reais
* APIs
* Backends
* Aplicações com requisitos de confiabilidade

---

## Arquivo 2 – `2-agente-react-usando-prompt-hub.py`

### O que este arquivo faz

Reimplementa o agente ReAct, mas utilizando um **prompt padrão do LangChain Hub**.

```python
prompt = hub.pull("hwchase17/react")
```

---

### Conceito demonstrado

* **Reuso de prompts consolidados**
* Padronização
* Menor esforço manual

---

### Vantagens do Prompt Hub

* Prompt testado pela comunidade
* Menos erros
* Melhor manutenção

### Limitações

* Continua sendo parsing de texto
* Ainda não ideal para produção

---

## Comparação entre os arquivos

| Abordagem    | Arquivo | Robustez | Uso recomendado    |
| ------------ | ------- | -------- | ------------------ |
| ReAct manual | 1       | Baixa    | Ensino             |
| Tool Calling | 1.1     | Alta     | Produção           |
| ReAct Hub    | 2       | Média    | Ensino estruturado |

---

## Aspectos dependentes vs independentes de modelo

### Dependentes de modelo

* Chat models vs completion models
* Suporte a tool calling nativo
* Formato de mensagens

### Independentes (abstrações LangChain)

* `@tool`
* `AgentExecutor`
* Orquestração

### Boas práticas

* Isolar lógica de negócio nas tools
* Trocar modelos sem alterar ferramentas
* Evitar prompts excessivamente rígidos

---

## Boas práticas e erros comuns

### Erros comuns

* Confiar no modelo em vez das tools
* Usar ReAct em produção
* Não limitar iterações

### Padrões recomendados

* Tool Calling para sistemas reais
* ReAct apenas para aprendizado
* Tools pequenas e determinísticas

---

## Resumo final

### Principais aprendizados

* LLMs podem agir, não apenas responder
* Tools são a fonte de verdade
* ReAct é didático, Tool Calling é prático

### Checklist do aluno

* [x] Entender o papel do AgentExecutor
* [x] Criar tools com `@tool`
* [x] Diferenciar ReAct de Tool Calling
* [x] Saber quando usar cada abordagem

---

✅ Ao concluir esta parte, você entende **como transformar raciocínio em ação**, com controle, segurança e clareza arquitetural.
