# CMPE 258 Final Submission Map (Group 19)

This file maps the professor’s **three deliverables** to concrete paths in this repository so a grader can verify everything in one pass.

**Demo video (Google Drive):** [CMPE258_Group19_Demo_Video.mp4](https://drive.google.com/file/d/1EjjEb7zk4U2X9u1einyf2kfJwKbFtY-E/view?usp=sharing)

## 1. Project Report (Document)

| Item | Location | Notes |
|------|----------|--------|
| **PDF for Canvas (Turnitin)** | [`report/ProjectReport.pdf`](./report/ProjectReport.pdf) | Upload this file directly to Canvas. |
| Editable report (Word) | *(optional)* Add `report/ProjectReport.docx` if you have it | Professor asked for editable + PDF in the same Drive or repo. |
| Slides | [`report/CMPE258_Project.pptx`](./report/CMPE258_Project.pptx) | Supporting presentation. |
| Proposal | [`report/CMPE258_ProjectProposal.pdf`](./report/CMPE258_ProjectProposal.pdf) | Earlier course artifact. |

## 2. Software Programs (Code + Supporting Files)

| Item | Location | Notes |
|------|----------|--------|
| **Public repo (submit this link in Canvas)** | https://github.com/abharathkumarr/Graph-Based-Intelligent-Movie-Recommendation-System-Using-RAG | Must stay **public** and accessible. |
| Main notebook | [`CMPE258_Project_Code.ipynb`](./CMPE258_Project_Code.ipynb) | Includes **Option 2** evaluation cells. |
| Demo application | [`app_full.py`](./app_full.py), [`run_app.sh`](./run_app.sh), [`requirements_ui.txt`](./requirements_ui.txt) | Run after setting `GROQ_API_KEY`; see root [`README.md`](./README.md). |
| Evaluation set + artefacts | [`data/eval_queries.json`](./data/eval_queries.json), [`evaluation/`](./evaluation/) | CSVs and PNGs must **match** tables/figures in the report. |
| Large pickles (not in git) | *(local / Drive)* `triplet_sentences.pkl`, `triplet_embeddings.pkl` | **Not** committed (size). Obtain per [`docs/MODEL_FILES.md`](./docs/MODEL_FILES.md). |

**Security:** No API keys in the repo—use `.env.example` and environment variables only.

## 3. Video Demo

| Item | Location | Notes |
|------|----------|--------|
| **Team demo video** | In repo: [`demo/CMPE258_Group19_Demo_Video.mp4`](./demo/CMPE258_Group19_Demo_Video.mp4) — [Google Drive copy](https://drive.google.com/file/d/1EjjEb7zk4U2X9u1einyf2kfJwKbFtY-E/view?usp=sharing) | **Landscape** recording; include **all members** (face + voice); show **live demo + repo**, not only portrait PPT slides (per rubric). |

## Rubric cross-check (100 pts)

| Rubric criterion | Evidence in this repo |
|------------------|------------------------|
| **Project Document (20)** | `report/ProjectReport.pdf` — architecture, techniques, task split, references, **evaluation + model comparison**. |
| **Software + implementation (60)** | Runnable layout, `README.md`, notebook + `evaluation/` artefacts aligned with the report, non-trivial KG+RAG+FAISS+multi-model eval. |
| **Video demo (20)** | `demo/CMPE258_Group19_Demo_Video.mp4` and [Google Drive](https://drive.google.com/file/d/1EjjEb7zk4U2X9u1einyf2kfJwKbFtY-E/view?usp=sharing) — must satisfy format/content requirements when you record. |

## “Finished implementation” rule (from assignment)

Each claimed feature should appear in **code**, **report**, **video**, and **evaluation** where applicable. This repo is organized so those four line up: implementation (`app_full.py`, notebook), write-up (`ProjectReport.pdf`), evidence (`evaluation/`), and demo (`demo/`).
