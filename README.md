\# RAG Resilience Lab

A research-oriented framework for systematically evaluating how retrieval-augmented generation (RAG) systems fail under adversarial conditions.

This project investigates failure modes including:
- prompt injection via retrieved documents
- context poisoning within the knowledge base
- retrieval manipulation that surfaces adversarial or misleading content

The goal is to quantify when and how a RAG pipeline deviates from intended behavior under adversarial influence.


## Overview

This project builds a retrieval-augmented generation (RAG) pipeline and uses it as a controlled environment to study adversarial behavior.

The system includes:
- document ingestion and embedding (Sentence Transformers)
- vector search (FAISS)
- retrieval + answer generation pipeline
- logging and experiment tracking

On top of this pipeline, the project runs structured adversarial experiments to evaluate:

- how injected or poisoned context influences model outputs
- when retrieved information overrides system-level instructions
- how retrieval quality degrades under adversarial conditions

The objective is not only to build a RAG system, but to analyze its failure modes through repeatable experiments and measurable outcomes.

## Threat Model

This project evaluates RAG failures under an adversarial setting where an attacker can influence retrieved context without modifying model weights.

**Attacker capabilities**
- inject malicious or misleading documents into the retrieval corpus
- craft queries that increase the chance of retrieving adversarial content
- exploit the model’s tendency to prioritize retrieved instructions over intended behavior

**Defender assumptions**
- the base model and embeddings are fixed
- retrieval pipeline behavior can be observed through logs and outputs
- attacks are evaluated at the application layer rather than through model fine-tuning

**Security objective**
- measure whether the pipeline remains aligned with intended behavior when exposed to adversarial context


\## Project Structure



rag-resilience-lab/

│

├── app/

│ ├── ingest.py

│ ├── retrieve.py

│ ├── answer.py

│ └── main.py

│

├── data/

│ └── clean/

│

├── eval/

│ ├── benchmark.json

│ ├── evaluate.py

│ └── results.json

│

├── logs/

│ └── log.json





\## Tech Stack

Python, FAISS (vector similarity search), and Sentence Transformers (embeddings)



\## Usage

Create a virtual environment and activate it, install dependencies, then run the system or evaluation:





python -m venv venv

.\\venv\\Scripts\\Activate.ps1

python -m pip install faiss-cpu sentence-transformers

cd app

python main.py

cd ../eval

python evaluate.py





\## Example

Query:



What is the refund policy?





Output:



Retrieved documents:

\['refund\_policy.txt']



Answer:

Customers can request a refund within 30 days of purchase with proof of payment.





\## Evaluation

On a clean baseline dataset, the system achieves:

\- Retrieval Accuracy: 1.0

\- Answer Accuracy: 1.0



\## Progress

The project progresses through three stages: Stage 1 builds a baseline FAISS-based retrieval system, Stage 2 introduces answer generation and logging for full traceability, and Stage 3 adds benchmark evaluation with measurable accuracy metrics.



\## Next Steps

The next phase introduces controlled document contamination, measures its impact on retrieval accuracy, and explores defense strategies to improve system robustness.



\## Purpose

This project investigates how RAG systems respond to corrupted or adversarial data and provides a structured framework to evaluate and improve their reliability.

\## Stage 4 — Controlled Contamination

To test robustness, a conflicting document was added under `data/contaminated/`:



`refund\_policy\_fake.txt` → “Customers can request a refund within 90 days without proof of payment.”



This stage is used to simulate how conflicting or low-quality documents can degrade retrieval quality and lead to incorrect answers.

\## Before vs After



| Condition | Retrieval Accuracy | Answer Accuracy |

|-----------|--------------------|-----------------|

| Clean      | 1.0                | 1.0             |

| Contaminated | 0.0              | 0.0             |

\## Stage 5 — Defense (Trusted Source Filtering)



A simple defense was introduced by restricting retrieval to trusted data sources (`data/clean`).



This prevents malicious or low-quality documents from influencing the retrieval pipeline.



\### Results



| Condition    | Retrieval Accuracy | Answer Accuracy |

|--------------|--------------------|-----------------|

| Clean        | 1.0                | 1.0             |

| Contaminated | 0.0                | 0.0             |

| Defended     | 1.0                | 1.0             |

\## Threat Model



This project assumes an adversary can introduce conflicting or low-quality documents into the retrieval corpus. The attack goal is to influence retrieval rankings so that incorrect documents are selected and misleading answers are returned. The defense assumes trusted and untrusted data can be separated at retrieval time.

\## Why the Defense Works



The failure occurs because the retriever treats all documents as equally eligible for retrieval. By restricting retrieval to trusted sources, the system removes the attack path where conflicting documents can influence similarity search and downstream answers.



