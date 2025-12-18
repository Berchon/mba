# 📘 Parte 2 – Chains e Processamento no LangChain

## 🎯 Visão Geral da Parte

A **Parte 2 – Chains e Processamento** marca uma transição fundamental no estudo de LangChain: aqui deixamos de utilizar modelos de linguagem como chamadas isoladas e passamos a **compor fluxos de processamento estruturados**, nos quais múltiplas etapas trabalham em conjunto.

Nesta parte, o foco está em:

* Pensar em **LLMs como transformadores de dados** dentro de um pipeline
* Construir **chains reutilizáveis e declarativas**
* Combinar **prompts, funções Python, modelos e parsers** em fluxos coerentes
* Lidar com **textos longos**, limitações de contexto e estratégias como *map-reduce*

### Problemas que esta parte resolve

* Uso repetitivo e não estruturado de chamadas a LLMs
* Dificuldade de reutilizar lógica de prompts e processamento
* Falta de clareza sobre como encadear múltiplas transformações
* Limitações de contexto ao processar textos longos

### Conexão com as próximas partes

Os conceitos apresentados aqui são **pré-requisitos diretos** para:

* **RAG (Retrieval-Augmented Generation)**: pipelines com recuperação + geração
* **Agents**: chains como etapas internas de tomada de decisão
* **Automação com IA**: fluxos declarativos e reutilizáveis

---

## 🧩 Arquivo 1 – `1-iniciando-com-chains.py`

### O que este arquivo faz

Este arquivo apresenta a forma mais simples de criar uma **chain declarativa** usando o **LCEL (LangChain Expression Language)**, conectando um prompt diretamente a um modelo.

### Conceito demonstrado

* `PromptTemplate`
* Chat Model (`ChatGoogleGenerativeAI`)
* Operador `|` para composição de chains

### Código explicado

```python
question_template = PromptTemplate(
    input_variables=["name"],
    template="Hi, I'm {name}! Tell me a joke about my name!"
)
```

Define um prompt parametrizado. Aqui, o prompt é uma **função declarativa** que recebe dados de entrada.

```python
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5)
```

Inicializa um **Chat Model**, responsável pela geração de texto.

```python
chain = question_template | model
```

Cria uma **chain**: a saída do prompt alimenta diretamente o modelo.

```python
result = chain.invoke({"name": "Aldebaran"})
```

Executa a chain com os dados de entrada.

### Conceitos importantes

* LCEL
* Encadeamento declarativo
* Separação entre prompt e modelo

---

## 🧩 Arquivo 2 – `2-chains-com-decorators.py`

### O que este arquivo faz

Demonstra como **funções Python comuns** podem se tornar etapas de uma chain usando o decorator `@chain`.

### Conceito demonstrado

* `@chain`
* Funções como etapas de processamento
* Integração de lógica determinística com LLMs

### Código explicado

```python
@chain
def square(input_dict: dict) -> dict:
    x = input_dict["x"]
    return {"square_result": x * x}
```

Transforma uma função Python em um **Runnable**, compatível com o LCEL.

```python
chain2 = square | question_template2 | model
```

Aqui temos um pipeline híbrido:

1. Cálculo determinístico
2. Prompt
3. Geração por LLM

### Conceitos importantes

* Runnables
* Pipelines híbridos (Python + LLM)

---

## 🧩 Arquivo 3 – `3-runnable_lambda.py`

### O que este arquivo faz

Mostra como criar um Runnable a partir de uma função usando `RunnableLambda`.

### Conceito demonstrado

* `RunnableLambda`
* Adaptação de funções existentes

### Código explicado

```python
parse_runnable = RunnableLambda(parse_number)
```

Permite encapsular uma função simples como parte de um pipeline LCEL.

### Quando usar

* Funções definidas em outros módulos
* Código legado
* Quando não é possível usar decorators

---

## 🧩 Arquivo 4 – `4-pipeline-de-processamento.py`

### O que este arquivo faz

Cria um **pipeline multi-etapas**, no qual a saída de uma chain alimenta outra.

### Conceito demonstrado

* Pipelines com dicionários
* `StrOutputParser`
* Composição de chains

### Destaque conceitual

```python
pipeline = {"text_to_summarize": translate} | template_summary | model | StrOutputParser()
```

Aqui, o LangChain atua como um **orquestrador de fluxo de dados**.

---

## 🧩 Arquivo 5 – `5-sumarizacao.py`

### O que este arquivo faz

Este arquivo demonstra o uso de uma **cadeia de sumarização pronta** do LangChain utilizando a estratégia **`stuff`**. Ele representa a forma mais direta e simples de resumir um texto usando LangChain.

A ideia central é:

1. Dividir (opcionalmente) um texto longo em partes menores
2. **Juntar todo o conteúdo em um único prompt**
3. Enviar esse prompt completo para o modelo gerar o resumo

Mesmo utilizando um `TextSplitter`, neste exemplo **todas as partes são reunidas novamente** antes da chamada ao modelo. O uso do splitter aqui é apenas didático.

### Estratégia `stuff`: como funciona

Na estratégia `stuff`, o LangChain:

* Pega todos os documentos (chunks)
* "Enfia" (stuff) todo o conteúdo em um único prompt
* Executa **uma única chamada ao LLM**

Fluxo conceitual:

```
Documentos → [concatenação] → Prompt único → LLM → Resumo
```

### Quando usar `stuff`

Esta estratégia é recomendada quando:

* O texto **cabe confortavelmente no contexto do modelo**
* Você quer **simplicidade máxima**
* O custo de múltiplas chamadas ao modelo não se justifica
* O resumo não exige processamento incremental

### Limitações importantes

* Não escala bem para textos grandes
* Pode estourar o limite de tokens do modelo
* Menor controle sobre o processo intermediário

### Conceitos importantes envolvidos

* Cadeias prontas (`load_summarize_chain`)
* Limites de contexto de LLMs
* Trade-off entre simplicidade e escala

---

## 🧩 Arquivo 6 – `6-sumarizacao-com-map-reduce.py`

### O que este arquivo faz

Este arquivo demonstra a mesma tarefa de sumarização, porém utilizando a estratégia **`map_reduce`**, que é mais robusta e escalável para textos longos.

Aqui, o LangChain aplica explicitamente o padrão **Map-Reduce**, muito comum em processamento distribuído.

### Estratégia `map_reduce`: como funciona

A estratégia é dividida em duas fases claras:

#### 1️⃣ Fase Map

* Cada chunk de texto é enviado **individualmente** ao LLM
* O modelo gera um **resumo parcial** para cada parte

#### 2️⃣ Fase Reduce

* Todos os resumos parciais são combinados
* Um novo prompt é enviado ao modelo para gerar o **resumo final**

Fluxo conceitual:

```
Documentos → Map (resumos parciais) → Reduce (resumo final)
```

### Quando usar `map_reduce`

Esta estratégia é recomendada quando:

* O texto é **grande ou potencialmente ilimitado**
* Há risco real de ultrapassar o contexto do modelo
* Você precisa de **robustez e escalabilidade**
* O custo de múltiplas chamadas ao modelo é aceitável

### Vantagens em relação ao `stuff`

* Escala para textos muito grandes
* Evita estouro de contexto
* Processo mais previsível

### Desvantagens

* Mais chamadas ao modelo (maior custo)
* Mais latência
* Menos simples conceitualmente para iniciantes

### Conceitos importantes envolvidos

* Map-Reduce
* Processamento incremental
* Cadeias compostas

---

## 🧩 Arquivo 7 – `7-pipeline-de-sumarizacao.py`

### O que este arquivo faz

Este arquivo reimplementa **manualmente** a estratégia de map-reduce utilizando apenas **LCEL (LangChain Expression Language)**, sem usar cadeias prontas.

O objetivo aqui não é simplicidade, mas **controle total e compreensão profunda** do fluxo.

### Por que este exemplo é importante

Ele mostra que:

* Cadeias prontas são apenas **abstrações de conveniência**
* Todo o comportamento pode ser reproduzido com LCEL
* LangChain é um **framework de orquestração**, não apenas prompts prontos

### Estrutura detalhada do pipeline

#### 1️⃣ Preparação dos dados (Split)

O texto é dividido em chunks usando `TextSplitter`, assim como nos exemplos anteriores.

#### 2️⃣ Fase Map com LCEL

```python
map_chain = map_prompt | llm | StrOutputParser()
```

Cada chunk passa por:

* Um prompt de resumo
* O modelo
* Um parser de saída

O método `.map()` aplica essa chain a **cada chunk individualmente**.

#### 3️⃣ Preparação para o Reduce

```python
RunnableLambda(lambda summaries: [{"context": "
".join(summaries)}])
```

Aqui ocorre uma transformação puramente Python, preparando os dados para o próximo estágio.

#### 4️⃣ Fase Reduce

Um novo prompt combina todos os resumos parciais em um resumo final.

### Quando usar este tipo de pipeline

Este padrão é recomendado quando:

* Você precisa de **controle fino** sobre cada etapa
* Deseja inserir lógica customizada entre map e reduce
* Quer instrumentar, logar ou validar etapas intermediárias
* Está construindo sistemas complexos (RAG, agents, workflows)

### Comparação com cadeias prontas

| Aspecto       | Cadeias prontas | LCEL manual |
| ------------- | --------------- | ----------- |
| Simplicidade  | Alta            | Média/Baixa |
| Controle      | Baixo           | Alto        |
| Flexibilidade | Limitada        | Máxima      |
| Uso didático  | Início          | Avançado    |

### Conceitos importantes envolvidos

* LCEL avançado
* `map()`
* Pipelines declarativos complexos

### Stuff vs Map_Reduce

|              |                                |               |
| ------------ | ------------------------------ | ------------- |
| `stuff`      | Junta tudo em um único prompt  | Textos curtos |
| `map_reduce` | Resume partes e depois combina | Textos longos |

### Conceitos importantes

* `TextSplitter`
* Limitações de contexto
* Estratégias de redução

---

## 🔍 Comparação entre os arquivos

| Abordagem      | Nível         | Controle | Uso típico         |
| -------------- | ------------- | -------- | ------------------ |
| Chain simples  | Básico        | Baixo    | Introdução         |
| Decorators     | Intermediário | Médio    | Pipelines híbridos |
| Chains prontas | Intermediário | Baixo    | Produtividade      |
| LCEL puro      | Avançado      | Alto     | Sistemas complexos |

---

## ⚙️ Dependência de modelo vs abstração

### Dependente de modelo

* Tipo de saída (`AIMessage`)
* Limitações de contexto
* Parâmetros como `temperature`

### Independente de modelo

* LCEL (`|`, `.map()`)
* Runnables
* Prompts
* Parsers

### Boas práticas

* Use `StrOutputParser` sempre que possível
* Evite acessar `.content` diretamente
* Injete o modelo no nível mais externo possível

---

## ✅ Boas práticas e dicas

* Pense em chains como **funções puras**
* Separe lógica determinística de geração
* Prefira pipelines declarativos
* Use `map_reduce` para escala

---

## 🧠 Resumo Final

### Principais aprendizados

* Chains são pipelines de transformação de dados
* LLMs são apenas uma etapa do fluxo
* LCEL permite composição clara e reutilizável

### Checklist mental

* [x] Sei criar chains simples
* [x] Sei integrar funções Python
* [x] Sei processar textos longos
* [x] Sei escolher entre chains prontas e LCEL puro

✔️ Com isso, você está preparado para avançar para RAG, Agents e aplicações reais.
