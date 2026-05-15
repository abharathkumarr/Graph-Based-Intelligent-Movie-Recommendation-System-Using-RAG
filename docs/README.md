# Documentation folder (`docs/`)

These files support the **Software Programs** deliverable (“organized and runnable”) and the **Project Report** (references, reproduction, large artefacts). None of them are strictly *required* by the syllabus wording, but each has a clear purpose.

| File | Keep? | Why |
|------|--------|-----|
| [**MODEL_FILES.md**](./MODEL_FILES.md) | **Yes (recommended)** | The professor explicitly allows large datasets/models **outside** the repo. Your `triplet_*.pkl` files are **gitignored**; this doc tells graders **how to obtain** them so the project is still runnable. |
| [**USAGE.md**](./USAGE.md) | **Yes (recommended)** | Extra run/troubleshooting detail beyond the root `README.md`. Helps a grader run the UI or notebook without email back-and-forth. |
| [**RUBRIC_ALIGNMENT.md**](./RUBRIC_ALIGNMENT.md) | **Optional (nice to have)** | Maps your work to the **Option 2 / evaluation-first** rubric. Not required for credit, but shows intent and makes peer/professor review faster. |
| [CHANGELOG.md](./CHANGELOG.md), [CONTRIBUTING.md](./CONTRIBUTING.md), [DEPLOYMENT.md](./DEPLOYMENT.md) | **Optional** | Standard open-source hygiene; safe to keep. If you want a **minimal** repo for submission only, you could move them to a branch—but **not necessary**. |

**Bottom line:** Keep **MODEL_FILES.md** (and **USAGE.md**) unless you merge that content into the root README. **RUBRIC_ALIGNMENT.md** is optional polish.
