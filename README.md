# RAG Resilience Lab

A research-oriented framework for evaluating how Retrieval-Augmented Generation (RAG) systems fail under adversarial conditions.

This project focuses on identifying, measuring, and mitigating failure modes in RAG pipelines where external data can influence model outputs.

---

## Overview

RAG systems rely on retrieved external context to generate responses. This creates a new attack surface: the retrieval layer.

This project builds a minimal RAG pipeline and uses it as a controlled testbed to study:

- how adversarial documents influence model outputs  
- when retrieved content overrides system-level intent  
- how retrieval quality degrades under contamination  
- how simple defenses can restore alignment  

---

## Threat Model

We assume an attacker cannot modify model weights, but can influence retrieved data.

### Attacker capabilities
- inject misleading or conflicting documents into the corpus  
- craft queries that increase the likelihood of adversarial retrieval  
- exploit the model’s tendency to trust retrieved context  

### Defender assumptions
- base model and embeddings are fixed  
- behavior is observable via outputs and logs  
- defenses operate at the retrieval / data layer  

### Security objective
Measure whether the system remains aligned with intended behavior under adversarial context.

---

## System Design

The pipeline consists of:

- document ingestion and embedding (Sentence Transformers)  
- vector similarity search (FAISS)  
- retrieval → answer generation  
- structured evaluation using benchmark queries  

---

## Project Structure

rag-resilience-lab/
├── app/
│   ├── ingest.py
│   ├── retrieve.py
│   ├── answer.py
│   └── main.py
├── attacks/
│   └── context_poisoning.py
├── data/
│   ├── clean/
│   └── contaminated/
├── eval/
│   ├── benchmark.json
│   ├── evaluate.py
│   ├── run_contaminated.py
│   ├── run_defended.py
│   └── results_*.json
├── logs/
│   └── log.json

---

## Evaluation Scenarios

### 1. Clean Baseline
System operates on trusted data only.

Expected behavior:
- correct document retrieval  
- correct answer generation  

---

### 2. Context Poisoning (Attack)

A conflicting document is injected:

refund_policy_fake.txt → “refund within 90 days without proof”

Effect:
- retrieval selects incorrect document  
- answer deviates from intended policy  

---

### 3. Defended Retrieval

Defense: restrict retrieval to trusted sources (`data/clean`)

Effect:
- adversarial documents excluded  
- correct behavior restored  

---

## Results

| Scenario       | Retrieval Accuracy | Answer Accuracy | Attack Success Rate |
|---------------|------------------|-----------------|---------------------|
| Clean         | 1.0              | 1.0             | 0.0                 |
| Contaminated  | 0.0              | 0.0             | 1.0                 |
| Defended      | 1.0              | 1.0             | 0.0                 |

These results demonstrate:

- RAG systems can be fully compromised via data-layer attacks  
- simple retrieval constraints can restore alignment  
- robustness depends heavily on data trust boundaries  

---

## Reproducibility Note

The evaluation pipeline is currently in a prototype stage.

- benchmark structure and adversarial scenarios are implemented  
- output formats and metrics reflect intended evaluation design  
- environment-specific execution issues are being resolved  

---

## Usage

python -m venv venv  
.\venv\Scripts\Activate.ps1  
pip install faiss-cpu sentence-transformers numpy  

Run evaluations:

python eval/run_defended.py  
python eval/run_contaminated.py  

---

## Key Insight

RAG systems introduce a critical security tradeoff:

The model becomes only as trustworthy as the data it retrieves.

This project demonstrates that:
- attacks can succeed without modifying the model  
- defenses can succeed without retraining the model  

---

## Future Work

- ranking-time adversarial filtering  
- source credibility scoring  
- multi-document consistency checks  
- detection of conflicting evidence  
- integration with LLM-based guardrails  

---

## Purpose

This repository is designed as a minimal, inspectable environment for studying AI system robustness at the retrieval layer, with a focus on adversarial behavior and defensive strategies.
