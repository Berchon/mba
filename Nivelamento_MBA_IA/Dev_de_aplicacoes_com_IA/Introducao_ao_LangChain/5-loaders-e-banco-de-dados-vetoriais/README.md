# 📘 Parte 5 – Loaders e Bancos de Dados Vetoriais no LangChain

Este documento faz parte de um estudo introdutório e progressivo sobre **LangChain**, com foco em **carregamento de dados, geração de embeddings e recuperação semântica usando bancos de dados vetoriais**.

O conteúdo foi elaborado para leitores com **conhecimento básico de Python**, mas **iniciantes em LangChain e em arquiteturas de RAG (Retrieval-Augmented Generation)**.

---

## 1. Visão Geral da Parte

### 🎯 Objetivo desta parte

A Parte 5 tem como objetivo ensinar **como transformar dados textuais brutos em uma base vetorial consultável semanticamente**. Para isso, o módulo demonstra um pipeline completo de:

1. **Carregamento de documentos** a partir de diferentes fontes (web e PDF)
2. **Divisão dos textos em chunks** adequados para LLMs
3. **Geração de embeddings de linguagem natural**
4. **Persistência desses vetores em um banco vetorial (PGVector / PostgreSQL)**
5. **Consulta semântica por similaridade**

Esse fluxo representa a espinha dorsal de sistemas modernos de busca semântica, chatbots com memória documental e aplicações RAG.

---

### ❓ Quais problemas esta parte resolve

Sem esse tipo de abordagem, aplicações baseadas em LLMs enfrentam limitações sérias:

* LLMs não “lembram” documentos grandes
* Contexto enviado no prompt é limitado por tokens
* Busca por palavras-chave não captura significado semântico

O uso de **embeddings + banco vetorial** resolve esses problemas ao permitir:

* Indexação de grandes volumes de texto
* Busca baseada em significado, não em palavras exatas
* Recuperação eficiente de trechos relevantes

---

### 🔗 Conexão com as próximas partes

Esta parte prepara o terreno para módulos mais avançados, como:

* **RAG completo** (Retriever + LLM)
* **Chains que combinam busca vetorial com geração de respostas**
* **Agentes que consultam bases de conhecimento externas**
* **Memória de longo prazo baseada em vetores**

Sem dominar loaders, splitters e bancos vetoriais, essas arquiteturas não escalam corretamente.

---

## 2. Explicação Detalhada de Cada Arquivo

---

## 📄 Arquivo 1 – `1-carregamento-usando-WebBaseLoader.py`

### 📌 O que este arquivo faz

Este script demonstra como:

* Carregar conteúdo textual diretamente de uma página web
* Transformar esse conteúdo em documentos do LangChain
* Dividir o texto em chunks menores usando um splitter recursivo

---

### 🧠 Conceito do LangChain demonstrado

* **Document Loaders**
* **WebBaseLoader**
* **RecursiveCharacterTextSplitter**

---

### 🧩 Explicação por blocos

```python
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
```

Importação dos componentes responsáveis por:

* Carregar dados da web
* Dividir textos longos em fragmentos menores

---

```python
loader = WebBaseLoader("https://www.langchain.com/")
docs = loader.load()
```

* O `WebBaseLoader` faz uma requisição HTTP simples
* Extrai o conteúdo textual principal da página
* Retorna uma lista de objetos `Document`

> Cada `Document` contém:
>
> * `page_content`: texto
> * `metadata`: URL, fonte, etc.

---

```python
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = splitter.split_documents(docs)
```

* O splitter quebra o texto em pedaços de até 500 caracteres
* Mantém sobreposição de 100 caracteres entre chunks
* O método recursivo tenta preservar limites semânticos (parágrafos, frases)

---

```python
for chunk in chunks:
    print(chunk)
    print("-"*30)
```

* Apenas visualiza os chunks gerados
* Útil para entender como o texto foi fragmentado

---

### ⚠️ Observação importante

O próprio código comenta corretamente:

> Para casos complexos de crawling e scraping, bibliotecas especializadas (Scrapy, BeautifulSoup, Firecrawl, etc.) são mais adequadas.

O `WebBaseLoader` é **simples e didático**, não um crawler completo.

---

## 📄 Arquivo 2 – `2-carregamento-de-pdf.py`

### 📌 O que este arquivo faz

Este script demonstra como:

* Carregar um documento PDF local
* Converter páginas do PDF em documentos
* Dividir o conteúdo em chunks

---

### 🧠 Conceito do LangChain demonstrado

* **PyPDFLoader**
* **Loaders para arquivos locais**
* **Processamento de documentos estruturados**

---

### 🧩 Explicação por blocos

```python
from pathlib import Path
```

Uso do `Pathlib` para manipulação segura de caminhos de arquivos.

---

```python
BASE_DIR = Path(__file__).resolve().parent
pdf_path = BASE_DIR / "gpt5.pdf"
```

* Garante que o script funcione independentemente do diretório de execução
* Boa prática para scripts reutilizáveis

---

```python
loader = PyPDFLoader(str(pdf_path))
docs = loader.load()
```

* Cada página do PDF vira um objeto `Document`
* Metadados incluem número da página e origem

---

```python
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = splitter.split_documents(docs)
```

* Mesma estratégia usada para conteúdo web
* Reforça que **splitters são independentes da fonte**

---

```python
print(len(chunks))
```

* Apenas valida o volume de fragmentos gerados

---

## 📄 Arquivo 3 – `3-ingestion-pgvector.py`

### 📌 O que este arquivo faz

Este é o script mais importante da parte. Ele implementa a **ingestão completa em um banco vetorial**:

* Carrega um PDF
* Divide em chunks
* Gera embeddings
* Persiste os vetores no PostgreSQL usando PGVector

---

### 🧠 Conceitos demonstrados

* **Embeddings**
* **Vector Stores**
* **PGVector**
* **Integração com serviços externos**

---

### 🧩 Explicação por blocos

```python
from dotenv import load_dotenv
load_dotenv()
```

Carrega variáveis sensíveis a partir de `.env` — prática essencial em projetos reais.

---

```python
for k in ["GOOGLE_API_KEY", "PGVECTOR_URL", "PGVECTOR_COLLECTION"]:
    if k not in os.environ:
        raise RuntimeError(...)
```

* Validação explícita de dependências de ambiente
* Falha rápida (fail fast)

---

```python
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150,
)
```

* Chunks maiores para embeddings
* Overlap maior preserva contexto semântico

---

```python
enriched = [Document(
    page_content=doc.page_content,
    metadata={k: v for k, v in doc.metadata.items() if v not in ("", None)},
) for doc in splits]
```

* Limpa metadados inválidos
* Prepara documentos para persistência

---

```python
embeddings = GoogleGenerativeAIEmbeddings(
    model="text-embedding-004",
)
```

* Define explicitamente o modelo de embeddings
* Abstração permite trocar o provedor futuramente

---

```python
store = PGVector(
    embeddings=embeddings,
    collection_name=...,
    connection=...,
    use_jsonb=True,
)
```

* Inicializa o banco vetorial
* `use_jsonb=True` melhora performance e flexibilidade

---

```python
store.add_documents(documents=enriched, ids=ids)
```

* Persiste vetores + metadados
* Conclui o pipeline de ingestão

---

## 📄 Arquivo 4 – `4-search-vector.py`

### 📌 O que este arquivo faz

Este script demonstra como:

* Consultar um banco vetorial existente
* Realizar busca por similaridade semântica
* Recuperar documentos relevantes

---

### 🧠 Conceitos demonstrados

* **Similarity Search**
* **Embeddings de consulta**
* **Scoring semântico**

---

### 🧩 Explicação por blocos

```python
query = "Tell me more about the gpt-5 thinking evaluation..."
```

Consulta em linguagem natural — não precisa coincidir com o texto original.

---

```python
results = store.similarity_search_with_score(query, k=3)
```

* Retorna os 3 documentos mais similares
* Cada resultado inclui um score de distância

---

```python
for doc, score in results:
    print(doc.page_content)
```

* Visualiza texto recuperado
* Metadados ajudam no rastreamento da origem

---

## 3. Comparação Entre os Arquivos

| Arquivo            | Papel        | Persistência | Complexidade |
| ------------------ | ------------ | ------------ | ------------ |
| WebBaseLoader      | Coleta web   | Não          | Baixa        |
| PyPDFLoader        | Coleta local | Não          | Baixa        |
| Ingestion PGVector | Indexação    | Sim          | Alta         |
| Search Vector      | Recuperação  | Sim          | Média        |

---

## 4. Aspectos Dependentes vs Independentes de Modelo

### 🔒 Dependentes de modelo

* Classe `GoogleGenerativeAIEmbeddings`
* Nome do modelo (`text-embedding-004`)

### 🔓 Independentes de modelo

* Loaders
* Splitters
* VectorStore API
* Interface `Document`

> O LangChain abstrai o modelo, permitindo troca futura por OpenAI, Cohere, HuggingFace, etc.

---

## 5. Boas Práticas e Dicas

### ✅ Boas práticas

* Sempre usar `.env`
* Validar variáveis de ambiente
* Usar splitters adequados ao caso
* Persistir metadados úteis

### ❌ Erros comuns

* Chunks grandes demais
* Ignorar overlap
* Misturar ingestão e busca no mesmo script

---

## 6. Resumo Final

### 📌 Principais aprendizados

* Loaders transformam dados brutos em documentos
* Splitters preparam dados para LLMs
* Embeddings capturam significado
* Bancos vetoriais permitem busca semântica

---

### ✅ Checklist mental do aluno

* [x] Sei carregar dados de web e PDF
* [x] Sei dividir textos corretamente
* [x] Entendo embeddings
* [x] Sei ingerir dados em banco vetorial
* [x] Sei consultar por similaridade semântica

---

📘 **Conclusão:** esta parte estabelece a base técnica necessária para qualquer aplicação séria de RAG com LangChain.
