# How This Project Maps to “Option 2 — LLMs + AI Agent System (Evaluation-First)”

This document is for instructors and teammates. It separates **what the codebase does today** from **rubric extras** that may still be partial.

## You are not “missing AI”

The system is a standard **applied AI stack**:

- **Knowledge graph → natural-language facts → embeddings → vector retrieval (FAISS) → LLM (Groq)**  
  That is **Retrieval-Augmented Generation (RAG)** on **graph-derived knowledge**, i.e. **Knowledge-Graph RAG / GraphRAG-style grounding** (facts originate from Neo4j triplets, not arbitrary web text).

## Section A — Problem formulation

**Met.** Vertical use case: **intelligent movie recommendations** grounded in structured movie-domain knowledge.

## Section B — Data & evaluation set

| Item | Status |
|------|--------|
| Few-shot prompting | **Partial → improved in UI:** `app_full.py` prompt now includes **in-prompt few-shot** examples. The notebook may add more. |
| **≥ 50 test cases** | **Documented artifact:** `data/eval_queries.json` contains **50** natural-language queries for benchmarking. **Ground-truth labels** per query (if required) still come from your notebook / Neo4j Cypher exports — wire those the same way you already compute Precision@k. |

## Section C — Multi-model comparison (3 LLMs, ≥1 open-source, same eval set)

| Item | Status |
|------|--------|
| 3 models | **Partial → improved in UI:** sidebar lets you run the **same query** with **three Groq models** (e.g. Llama 3.3 70B, Llama 3.1 8B, Mixtral). Compare **latency** live; for **scores**, log runs over `data/eval_queries.json` in the notebook. |
| Same evaluation set | Use **`data/eval_queries.json`** for every model run. |
| Cost / latency | **Latency** is shown in the UI per request; **cost** is best summarized from Groq pricing + token counts (add in report if needed). |

## Section D — Non-trivial capability

### Advanced RAG

| Item | Status |
|------|--------|
| Real vector store | **Yes** — FAISS over MiniLM embeddings of KG sentences. |
| Chunking strategy | **Yes (domain-specific)** — **one triplet → one “chunk” sentence**, not generic PDF chunking. Say this explicitly in slides. |
| Citation / grounding | **Partial → improved:** UI shows **retrieved fact snippets**; **grounding score** = lexical overlap of answer with retrieved text (simple **critic** signal). |
| Advanced feature | **Yes** — **Knowledge-Graph RAG** (facts from Neo4j, then retrieval + LLM). |

### Planner–Executor–Critic agent with 2+ tools

**Honest framing:** this is **not** a full LangChain “ReAct” agent with arbitrary tools.  
**What we ship:** a **fixed pipeline** that matches the *spirit* of stages:

1. **Plan** — fixed policy: retrieve top-k KG facts, then answer with facts-only prompt.  
2. **Execute** — **Tool 1:** FAISS retriever; **Tool 2:** Groq chat completion.  
3. **Critic** — **Tool 3:** token overlap grounding check (+ optional user-visible guardrail).

Structured **JSONL logging** records these stages (see `logs/rag_pipeline.jsonl` after running the app).

### Stateful / long-horizon memory

**Partial:** Streamlit **session memory** (last turns) in the sidebar. This is **not** full long-horizon summarised memory; call that **future work** unless you add summarisation + retrieval of past sessions.

## Section E — UI + engineering + evaluation

| Item | Status |
|------|--------|
| Web UI | **Yes** — Streamlit. |
| Session state | **Yes** — query + last turns. |
| Guardrails | **Partial** — facts-only prompt + low-grounding warning. |
| Structured logging | **Yes** — append-only JSONL (`logs/rag_pipeline.jsonl`). |
| Evaluation on set | **Notebook** already has Precision / Recall / F1 machinery; run it over the **50 queries** (+ your ground truth) for the report. |

## Suggested one-liner for Q&A

> “We implement **Knowledge-Graph RAG** with **FAISS retrieval**, **few-shot prompting**, **retrieved-fact citations**, a **lightweight grounding critic**, **structured logging**, and **multi-model runs** via Groq. Full formal **50-case labeled scores for three models** belong in the **evaluation notebook + report** using `data/eval_queries.json` as the shared query set.”
