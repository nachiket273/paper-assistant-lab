# Paper Assistant Lab

A lightweight **Scientific RAG + Evaluation Toolkit** for asking grounded questions over research papers.

The goal is to build a small, transparent system that ingests scientific PDFs, retrieves relevant passages, answers questions using only retrieved evidence, and evaluates retrieval/answer quality.

## Motivation

Scientific papers are dense. General-purpose LLMs often:
- hallucinate details,
- miss technical context,
- ignore equations or methods,
- answer without citations.

This project explores how retrieval-augmented generation can be made more reliable for scientific literature.

## Core Idea

```text
PDF Papers
   ↓
Text Extraction
   ↓
Chunking + Metadata
   ↓
Embeddings
   ↓
Vector Search
   ↓
Retrieved Evidence
   ↓
LLM Answer
   ↓
Citations + Evaluation
```

## Features
### V1
- PDF text extraction
- Page-level metadata
- Fixed-size chunking
- Embedding generation
- FAISS-based vector retrieval
- Citation-aware question answering
- Basic retrieval evaluation

### Planned
- Section-aware chunking
- Comparison of embedding models
- Retrieval metrics: Recall@k, MRR
- Answer faithfulness evaluation
- Scientific-domain benchmark questions
- GraphRAG extension with Neo4j

## Project Structure
```text
paper-assistant-lab/
├── data/
│   ├── papers/
│   └── processed/
├── examples/
│   └── sample_questions.json
├── notebooks/
│   ├── 01_ingestion_demo.ipynb
│   └── 02_retrieval_eval.ipynb
├── src/
│   ├── ingest.py
│   ├── chunk.py
│   ├── embed.py
│   ├── retrieve.py
│   ├── answer.py
│   └── evaluate.py
├── requirements.txt
└── README.md
```

## Initial Scope

This is intentionally a small project.

The first milestone is not a production system. It is a working, inspectable prototype that can answer questions over a small set of scientific papers with explicit evidence.

### Example Questions
- What problem does the paper solve?
- What dataset or simulation setup is used?
- Which model architecture is proposed?
- How is the method evaluated?
- What are the main limitations?
- Which equations or assumptions are central to the method?

## Setup
```bash
git clone https://github.com/nachiket273/paper-assistant-lab.git
cd paper-assistant-lab

python -m venv venv
source venv/bin/activate   # Linux/Mac
# venv\Scripts\activate    # Windows

pip install -r requirements.txt
```

## Usage
1. Add papers
Place PDF files in:
```bash
data/papers/
```

2. Extract text
```bash
python src/ingest.py
```

3. Create chunks
```bash
python src/chunk.py
```

4. Build embeddings
```bash
python src/embed.py
```

5. Ask a question
```bash
python src/retrieve.py --query "What is the main contribution of the paper?"
```

## Evaluation Plan

The project will evaluate both retrieval and generation quality.

### Retrieval
- Top-k retrieved chunks
- Recall@k
- Mean Reciprocal Rank
- Chunking strategy comparison

### Generation
- Groundedness
- Citation correctness
- Answer relevance
- Insufficient-context detection

## Roadmap
### Milestone 1: Basic RAG Pipeline
- [ ] PDF ingestion
- [ ] Text chunking
- [ ] Embedding generation
- [ ] FAISS retrieval
- [ ] CLI query interface
### Milestone 2: Evaluation
- [ ] Add sample questions
- [ ] Add ground-truth evidence
- [ ] Implement retrieval metrics
- [ ] Compare chunking strategies
### Milestone 3: Scientific Extensions
- [ ] Section-aware parsing
- [ ] Equation/context handling
- [ ] Citation-aware answer generation
- [ ] Domain-specific paper collections
### Milestone 4: GraphRAG Extension
- [ ] Extract entities and relationships
- [ ] Store graph in Neo4j
- [ ] Combine graph traversal with vector retrieval
- [ ] Evaluate multi-hop scientific questions


## Why This Project?

This project is designed to demonstrate practical skills in:

- applied LLM systems,
- RAG pipelines,
- scientific document processing,
- ML evaluation,
- Python engineering,
- research-oriented AI tooling.
