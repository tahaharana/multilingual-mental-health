# How to Run This Project — Step by Step

A beginner-friendly walkthrough that takes you from a fresh clone all the way through Experiment 4. If you've never touched this repo before, follow the steps in order.

For reference-style docs (prompt list, file formats, how to add a new model), see [README.md](README.md). This file is the runbook.

---

## What You'll Be Doing

The project runs three stages, in order:

| Stage | What it does | Output |
|-------|--------------|--------|
| **Preprocessing** | Builds the 5 000-post evaluation files (2 500 depressed + 2 500 normal per language) | `data/phase2/{arabic,urdu,chinese}_5000samples_seed42.json` |
| **Experiment 4 (few-shot)** | Each model classifies posts from scratch with language-specific in-context examples and writes a written justification | `results/phase2/experiment4_full/` |
| **Experiment 4 (zero-shot)** | Same posts, but with a minimal universal prompt — no examples, no language-specific rules | `results/phase2/experiment4_full_zeroshot/` |

Every stage is **resumable** — kill it mid-run, restart the same command, and it picks up from the last checkpoint.

---

## Step 0 — One-Time Setup

You only need to do this once per machine.

### 0.1 Install Python dependencies

From the project root:

```bash
pip install -r requirements.txt
```

This installs the SDKs for Gemini, OpenAI, Claude, plus `python-dotenv`.

### 0.2 Create your `.env` file

```bash
cp .env.example .env
```

Open `.env` and paste in API keys for the providers you plan to use. **Keys you won't use can be left blank** — the runner just skips that model.

```env
GEMINI_API_KEY=your-key-here
OPENAI_API_KEY=your-key-here
CLAUDE_API_KEY=your-key-here
```

Local models (Llama, Gemma, Qwen, DeepSeek-R1) don't need API keys — see "Running Local Models" below.

### 0.3 (Optional) Start LM Studio for local models

Skip this step if you only plan to use cloud APIs.

1. Install LM Studio.
2. Download the model you want (e.g. `meta-llama-3.1-8b-instruct`).
3. Open the **Local Server** tab and click **Start Server**.
4. Confirm the server is running at `http://localhost:1234`.

The model identifier shown in LM Studio's server tab must match the `default_model` field in [scripts/run_exp4.py](scripts/run_exp4.py). Update it if your ID differs.

---

## Step 1 — Preprocessing (Build the 5 000-Sample Files)

```bash
python scripts/prepare_data.py
```

That's it. The script:

- Reads filtered Arabic + Chinese translation files from [data/phase2/translated/filtered/](data/phase2/translated/filtered/)
- Reads the raw Urdu CSV at [data/raw/urdu/Depression.csv](data/raw/urdu/Depression.csv)
- Stratified-samples **2 500 depressed + 2 500 normal** per language using `seed=42` (deterministic — same output every run)
- Writes `data/phase2/arabic_5000samples_seed42.json`, `urdu_5000samples_seed42.json`, `chinese_5000samples_seed42.json`

### Want just one language?

```bash
python scripts/prepare_data.py --lang arabic
python scripts/prepare_data.py --lang urdu
python scripts/prepare_data.py --lang chinese
```

### Want a smaller eval set for quick testing?

```bash
python scripts/prepare_data.py --n 200   # 100 + 100 per language
```

You should now see three files in `data/phase2/`. **Don't skip this step** — Experiment 4 reads from these files.

---

## Step 2 — Experiment 4: Fresh Classification + Justification

The model classifies posts **from scratch** and writes a short English **justification** for each decision.

Two modes:
- **Few-shot** — the prompt includes language-specific in-context examples
- **Zero-shot** — minimal universal prompt, no examples

Two datasets:
- **Full 5 000-sample dataset** (`--full`) — the main result
- **15-row error-analysis CSVs** (default) — the posts every model got wrong in earlier work; useful for case studies. Inputs live in [data/all_models_wrong/](data/all_models_wrong/).

### Run it

```bash
# Full 5k dataset, few-shot, Claude on Arabic
python scripts/run_exp4.py --model claude --language arabic --full

# Same, but zero-shot
python scripts/run_exp4.py --model claude --language arabic --full --zeroshot

# All models, all languages, full dataset (few-shot)
python scripts/run_exp4.py --models all --languages all --full

# Multiple specific models, specific languages
python scripts/run_exp4.py --models claude,openai --languages arabic,urdu --full

# Smoke test — run just row 42, print everything, write nothing
python scripts/run_exp4.py --model claude --language arabic --debug 42
```

### Useful flags

```
--model / --models       Single key or comma-separated. Also: 'online', 'local', 'all'
--language / --languages Same. Also: 'all'
--full                   Use the 5k dataset (otherwise: 15-row error-analysis CSVs)
--zeroshot               Use the universal zero-shot prompt (otherwise: few-shot)
--fresh                  Discard partial results and start over
--limit N                Process only the first N rows
--debug INDEX            Run a single row, print the full LLM response, write nothing
```

### Output

Goes to one of four directories depending on mode + dataset:

| Mode | Dataset | Output dir |
|------|---------|------------|
| Few-shot | 15-row CSVs | `results/phase2/experiment4/` |
| Zero-shot | 15-row CSVs | `results/phase2/experiment4_zeroshot/` |
| Few-shot | Full 5k | `results/phase2/experiment4_full/` |
| Zero-shot | Full 5k | `results/phase2/experiment4_full_zeroshot/` |

Each result entry includes two fields: `exp4_classification` and `exp4_justification`.

### Merge Exp 4 results back into the 15-row CSVs

After the 15-row runs finish, merge each model's predictions/justifications into the error-analysis spreadsheets:

```bash
python scripts/merge_exp4.py             # few-shot → {lang}_all_wrong.csv
python scripts/merge_exp4.py --zeroshot  # zero-shot → {lang}_zeroshot.csv
```

These live in [data/all_models_wrong/](data/all_models_wrong/).

---

## One-Command Pipeline

You can also run the entire pipeline (Step 0 → Step 2) with a single command:

```bash
python run_all.py                                       # full pipeline, every model and language
python run_all.py --models claude,gemini                # restrict models
python run_all.py --languages arabic,urdu               # restrict languages
python run_all.py --limit 5                             # 5 samples per (model, lang) — quick smoke test
python run_all.py --skip 1                              # skip preprocessing if already done
python run_all.py --only 2                              # run only Experiment 4
python run_all.py --fresh                               # ignore partial checkpoints
python run_all.py --dry-run                             # print plan, run nothing
```

---

## Running Local Models

Local models (Llama, Gemma, Qwen, DeepSeek-R1) run through **LM Studio** (or any OpenAI-compatible local server: Ollama, vLLM, llama.cpp).

1. **Start the server** — load the model in LM Studio, click **Start Server** in the Local Server tab.
2. **Check the model ID** — copy the exact identifier shown in the server tab.
3. **Update [scripts/run_exp4.py](scripts/run_exp4.py)** — make sure `default_model` for that key matches.
4. **If you changed the port** (e.g. running Ollama on `11434`), add a `base_url` field to the model entry:

```python
"llama": {"class": LMStudioProvider, "default_model": "llama3.1:8b",
          "online": False, "workers": 1, "delay": 0.0, "max_tokens": 500,
          "base_url": "http://localhost:11434/v1"},
```

5. **Run normally** — `python scripts/run_exp4.py --model llama --language arabic --full`

Default ports: LM Studio `1234`, Ollama `11434`, vLLM `8000`, llama.cpp `8080`.

---

## Common Pitfalls

| Problem | Cause | Fix |
|---------|-------|-----|
| `No prepared data for 'arabic'` | You skipped Step 1 | Run `python scripts/prepare_data.py` |
| API key error | Missing or wrong key in `.env` | Open `.env`, paste the correct key, save |
| Local model "connection refused" | LM Studio server isn't running | Start LM Studio's Local Server |
| Rate-limit errors mid-run | Calling too fast | Reduce `workers` in the `MODELS` dict in [scripts/run_exp4.py](scripts/run_exp4.py) or add delay |
| Run crashes — what now? | Anything | Just rerun the same command. Resume is automatic. Add `--fresh` only if you want to wipe and restart. |
| Want to see what a prompt looks like before running | — | All prompts are defined in [src/evaluation/prompts.py](src/evaluation/prompts.py) |

---

## Recommended Run Order — From a Fresh Clone

```bash
# 0. Setup (once)
pip install -r requirements.txt
cp .env.example .env
# edit .env, paste API keys

# 1. Preprocessing
python scripts/prepare_data.py

# 2. Smoke test first — one model, one language, 5 rows
python scripts/run_exp4.py --model claude --language arabic --full --limit 5

# 3. Full Experiment 4 — few-shot
python scripts/run_exp4.py --models all --languages all --full

# 4. Full Experiment 4 — zero-shot
python scripts/run_exp4.py --models all --languages all --full --zeroshot

# 5. (Optional) Merge into the 15-row error-analysis CSVs
python scripts/merge_exp4.py
python scripts/merge_exp4.py --zeroshot
```

Or just:

```bash
python run_all.py
```
