![CI](https://github.com/nachiket273/paper-assistant-lab/actions/workflows/ci.yml/badge.svg)

# Paper Assistant Lab

> **A Research Engineering Toolkit for Scientific Retrieval-Augmented Generation (RAG)**

Paper Assistant Lab is an experimental framework for building and evaluating Retrieval-Augmented Generation (RAG) systems for scientific literature.

Unlike generic document chatbots, this project focuses on **grounded scientific question answering**, emphasizing transparent retrieval, citation-aware responses, reproducible evaluation, and modular experimentation.

The repository is designed both as a practical RAG implementation and as a research platform for studying retrieval strategies on scientific documents.

---

# Motivation

Large Language Models are increasingly used to summarize and answer questions about scientific papers. However, scientific documents present unique challenges:

- dense technical language
- mathematical notation
- domain-specific terminology
- long contextual dependencies
- multiple sections containing similar concepts
- high cost of factual mistakes

Traditional LLM-based question answering often produces:

- hallucinated claims
- unsupported conclusions
- incorrect citations
- incomplete methodological explanations

Paper Assistant Lab explores how retrieval-augmented generation can improve reliability by grounding every answer in retrieved evidence while providing measurable retrieval and generation quality.

Rather than optimizing for chatbot interactions, the project emphasizes:

- reproducibility
- interpretability
- modular experimentation
- scientific evaluation

---

# Design Principles

The repository follows five guiding principles.

### Transparent Retrieval

Every answer should be traceable back to the original paper.

### Modular Architecture

Each pipeline stage can be replaced independently for experimentation.

### Reproducible Evaluation

Experiments should produce repeatable retrieval metrics.

### Scientific-First Processing

Scientific papers are treated differently from generic PDFs by preserving metadata such as sections, page numbers, and references.

### Research-Friendly

The project should make it easy to compare embedding models, chunking methods, rerankers, and prompting strategies.

---

# Architecture

```text
                    PDF Papers
                         │
             Text + Metadata Extraction
                         │
        Section-aware Document Processing
                         │
               Chunking Strategies
      (Fixed / Recursive / Semantic)
                         │
               Embedding Models
        (MiniLM / BGE / E5 / etc.)
                         │
                  Vector Database
                      (FAISS)
                         │
               Dense Retrieval
                         │
          (Future: Hybrid Retrieval)
                         │
              Evidence Selection
                         │
            Prompt + Retrieved Context
                         │
                 LLM Generation
                         │
        Citation-aware Scientific Answer
                         │
            Retrieval & QA Evaluation
```

---

# Features

## Current (Version 1)

- PDF text extraction
- Metadata preservation
- Fixed-size chunking
- Sentence-transformer embeddings
- FAISS vector search
- Citation-aware question answering
- CLI interface
- Basic retrieval evaluation

---

## Planned

### Document Processing

- Section-aware chunking
- Recursive chunking
- Semantic chunking
- Figure and table references
- Equation-aware parsing

### Retrieval

- Multiple embedding backends
- Hybrid retrieval (BM25 + Dense)
- Cross-encoder reranking
- Metadata filtering

### Generation

- Better prompting
- Multi-document QA
- Context compression
- Self-verification
- Evidence ranking

### Evaluation

- Recall@k
- Precision@k
- Mean Reciprocal Rank (MRR)
- nDCG
- Citation accuracy
- Faithfulness
- Hallucination detection
- Groundedness scoring

### Scientific Extensions

- GraphRAG
- Neo4j knowledge graph
- Entity extraction
- Citation graph analysis
- Multi-hop scientific reasoning

---

# Repository Structure

```text
paper-assistant-lab/

├── configs/
│   ├── embedding.yaml
│   ├── retrieval.yaml
│   └── generation.yaml
│
├── data/
│   ├── papers/
│   ├── processed/
│   ├── chunks/
│   └── embeddings/
│
├── notebooks/
│   ├── 01_ingestion_demo.ipynb
│   ├── 02_chunking_experiments.ipynb
│   ├── 03_embedding_comparison.ipynb
│   ├── 04_retrieval_evaluation.ipynb
│   └── 05_generation_evaluation.ipynb
│
├── src/
│   ├── ingestion/
│   │   ├── ingest.py
│   │   ├── parser.py
│   │   └── metadata.py
│   │
│   ├── chunking/
│   │   ├── fixed.py
│   │   ├── recursive.py
│   │   └── semantic.py
│   │
│   ├── embeddings/
│   │   ├── embed.py
│   │   └── models.py
│   │
│   ├── retrieval/
│   │   ├── faiss.py
│   │   ├── search.py
│   │   └── rerank.py
│   │
│   ├── generation/
│   │   ├── answer.py
│   │   └── prompts.py
│   │
│   ├── evaluation/
│   │   ├── retrieval.py
│   │   ├── generation.py
│   │   └── benchmark.py
│   │
│   └── utils/
│
├── examples/
│   ├── sample_questions.json
│   └── benchmark_dataset.json
│
├── requirements.txt
├── README.md
└── LICENSE
```

---

# Installation

```bash
git clone https://github.com/nachiket273/paper-assistant-lab.git

cd paper-assistant-lab

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

---

# Quick Start

## Step 1

Add PDF files

```
data/papers/
```

---

## Step 2

Extract text

```bash
python src/ingestion/ingest.py
```

---

## Step 3

Generate chunks

```bash
python src/chunking/fixed.py
```

---

## Step 4

Generate embeddings

```bash
python src/embeddings/embed.py
```

---

## Step 5

Build FAISS index

```bash
python src/retrieval/faiss.py
```

---

## Step 6

Ask questions

```bash
python main.py \
--query "What problem does the paper solve?"
```

Example output

```text
Question

What problem does the paper solve?

----------------------------------

Retrieved Evidence

[Page 3]

"The proposed method addresses..."

[Page 5]

"Our primary contribution..."

----------------------------------

Answer

The paper proposes...

----------------------------------

Sources

Page 3

Page 5
```

---

# Example Questions

General

- What problem does the paper solve?
- What are the main contributions?
- What assumptions are made?
- What are the limitations?

Methods

- Which architecture is proposed?
- How are embeddings generated?
- Which optimization method is used?
- Which hyperparameters are important?

Experiments

- Which datasets are used?
- How is the model evaluated?
- Which baselines are compared?
- What metrics are reported?

Scientific

- Which equations define the method?
- What approximations are introduced?
- Which physical assumptions are made?
- Which theoretical model is used?

---

# Supported Embedding Models

Initial support

- all-MiniLM-L6-v2
- BAAI/bge-small-en
- BAAI/bge-base-en
- intfloat/e5-base

Future

- Instructor XL
- NV-Embed
- GTE
- Jina Embeddings

---

# Evaluation

A central goal of this project is measuring retrieval quality rather than relying solely on subjective answer quality.

## Retrieval Metrics

- Recall@k
- Precision@k
- MRR
- nDCG
- Hit Rate
- Retrieval latency

---

## Generation Metrics

- Faithfulness
- Citation correctness
- Groundedness
- Hallucination rate
- Answer relevance
- Context utilization

---

# Research Questions

The repository is intended to support experiments such as

### RQ1

Does section-aware chunking improve retrieval?

### RQ2

How sensitive is retrieval to chunk size?

### RQ3

Which embedding model performs best for scientific papers?

### RQ4

Does reranking improve citation quality?

### RQ5

Can LLMs reliably detect insufficient evidence?

### RQ6

How does GraphRAG compare with dense retrieval?

---

# Roadmap

## Milestone 1

Basic Scientific RAG

- [X] PDF ingestion
- [ ] Chunking
- [ ] Embeddings
- [ ] FAISS retrieval
- [ ] Citation-aware QA

---

## Milestone 2

Evaluation Framework

- [ ] Benchmark dataset
- [ ] Ground-truth evidence
- [ ] Retrieval metrics
- [ ] Answer evaluation
- [ ] Experiment logging

---

## Milestone 3

Advanced Retrieval

- [ ] Semantic chunking
- [ ] Hybrid retrieval
- [ ] Cross-encoder reranking
- [ ] Metadata filtering

---

## Milestone 4

Scientific Extensions

- [ ] Equation-aware parsing
- [ ] Figure references
- [ ] Citation graph
- [ ] Multi-document QA

---

## Milestone 5

GraphRAG

- [ ] Entity extraction
- [ ] Neo4j integration
- [ ] Multi-hop retrieval
- [ ] Knowledge graph evaluation

---

# Future Directions

Possible research directions include

- Scientific document parsing
- Domain-specific embedding models
- Retrieval benchmarks
- Citation graph reasoning
- GraphRAG
- Agentic literature review
- Scientific knowledge discovery

---

# Why This Project?

Paper Assistant Lab is intended to demonstrate practical skills in

- Retrieval-Augmented Generation
- Information Retrieval
- Scientific NLP
- Large Language Models
- Python software engineering
- Experiment design
- Retrieval evaluation
- AI research tooling

The long-term vision is to evolve this repository into a reproducible research platform for experimenting with scientific retrieval systems rather than a simple "chat with PDFs" application.

---

# License

Apache License
