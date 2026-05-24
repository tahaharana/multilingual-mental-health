# Multilingual Mental Health — LLM Evaluation Framework

Evaluates LLM depression detection across Arabic, Urdu, and Chinese social media posts via **Experiment 4**: fresh classification + written justification, in either few-shot or zero-shot mode. Supports both cloud APIs and local models via LM Studio.

For a step-by-step walkthrough from a fresh clone, see [INSTRUCTIONS.md](INSTRUCTIONS.md).

---

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
python scripts/prepare_data.py   # creates the 5 000-post eval files
```

Open `.env` and fill in the keys for the models you want to use:

```
GEMINI_API_KEY=your-gemini-key-here
OPENAI_API_KEY=your-openai-key-here
CLAUDE_API_KEY=your-claude-key-here
```

Keys for models you don't use can be left blank. Local models (Llama, Gemma, Qwen, DeepSeek-R1) run via LM Studio and need no API key.

---

## Running Experiment 4

Experiment 4 reclassifies each post from scratch and asks the model to write a 2-4 sentence justification.

```bash
# Few-shot, specific models and languages
python scripts/run_exp4.py --models claude,openai --languages arabic,urdu --full

# Full 5k dataset (checkpoints every 50 rows, auto-resumes on restart)
python scripts/run_exp4.py --model claude --language arabic --full

# Zero-shot mode
python scripts/run_exp4.py --model claude --language arabic --full --zeroshot

# Smoke test one row
python scripts/run_exp4.py --model claude --language arabic --debug 42

# All models, all languages
python scripts/run_exp4.py --models all --languages all --full
```

```
Flags:
  --model / --models      Single key or comma-separated; also: online, local, all
  --language / --languages
  --full                  Use 5k dataset instead of 15-row error-analysis CSVs
  --zeroshot              Use universal zero-shot prompt
  --fresh                 Discard existing results and start over
  --limit N               Process first N rows only
  --debug INDEX           Run one row, print full response, write nothing
```

Or run the entire pipeline (preprocessing + Experiment 4 in both modes) in one shot:

```bash
python run_all.py                          # full pipeline
python run_all.py --limit 5                # quick smoke test
python run_all.py --models claude,gemini   # restrict models
```

---

## Utility Scripts

```bash
# Merge Exp 4 classifications into the error-analysis CSVs
python scripts/merge_exp4.py             # few-shot → {lang}_all_wrong.csv
python scripts/merge_exp4.py --zeroshot  # zero-shot → {lang}_zeroshot.csv
```

---

## Models

| Key | Model | Type |
|-----|-------|------|
| `gemini` | Gemini 3.1 Flash Lite | API |
| `openai` | GPT-4o-mini | API |
| `claude` | Claude Haiku 4.5 | API |
| `llama` | Llama 3.3 8B | Local (LM Studio) |
| `gemma` | Gemma 4 E2B | Local (LM Studio) |
| `qwen` | Qwen 3.5 9B | Local (LM Studio) |
| `deepseek-local` | DeepSeek-R1 0528 Qwen3 8B | Local (LM Studio) |

**Adding a model:** Create a provider class in `src/models/`, add the API key mapping to `src/config.py` and `.env`, then add an entry to the `MODELS` dict in `scripts/run_exp4.py`.

**Local models:** Any OpenAI-compatible local inference server works — LM Studio, Ollama, vLLM, llama.cpp, etc. Start the server, then update `"default_model"` for the relevant key in the `MODELS` dict. If the server runs on a different port, add a `"base_url"` field to the entry:

```python
"llama": {"class": LMStudioProvider, "default_model": "llama3.3:8b",
          "online": False, "workers": 1, "delay": 0.0, "max_tokens": 500,
          "base_url": "http://localhost:11434/v1"},
```

Default ports: LM Studio → `1234`, Ollama → `11434`, vLLM → `8000`, llama.cpp → `8080`.

---

## Prompt Versions

| Key | Used for |
|-----|----------|
| `v3_exp4` | Urdu — few-shot (default) |
| `v3_arabic_exp4` | Arabic — few-shot (default) |
| `v3_chinese_exp4` | Chinese — few-shot (default) |
| `v3_exp4_zeroshot` | Universal zero-shot (all languages) |

All prompts are defined in [src/evaluation/prompts.py](src/evaluation/prompts.py).

---

## Repository Structure

```
├── scripts/
│   ├── prepare_data.py         # Build 5k eval files from raw datasets
│   ├── run_exp4.py             # Experiment 4 — fresh classification + justification
│   └── merge_exp4.py           # Merge Exp 4 results into error-analysis CSVs
│
├── src/                         # Library code (imported by scripts)
│   ├── evaluation/
│   │   ├── prompts.py          # All prompt definitions
│   │   └── parsers.py          # Dataset parsers per language
│   ├── models/                 # One provider class per LLM
│   └── config.py               # API key loader (reads from .env)
│
├── data/
│   ├── raw/                    # Original raw datasets (Arabic + Urdu)
│   ├── phase2/                 # 5k-post eval files (created by prepare_data.py)
│   └── all_models_wrong/       # 15-row error-analysis CSVs (Exp 4 input)
│
├── results/phase2/              # Experiment 4 outputs (timestamped JSONs)
│   ├── experiment4/                  # 15-row few-shot
│   ├── experiment4_zeroshot/         # 15-row zero-shot
│   ├── experiment4_full/             # 5k few-shot
│   └── experiment4_full_zeroshot/    # 5k zero-shot
│
├── run_all.py                  # One-command pipeline (preprocessing + Exp 4)
├── INSTRUCTIONS.md             # Step-by-step runbook
└── .env                        # API keys (not committed)
```

---

## Result File Format

Each Exp 4 run writes a timestamped JSON to its results directory:

```json
{
  "metadata": { "model": "claude", "language": "arabic", "timestamp": "..." },
  "results":  [
    {
      "index": 0,
      "conversation": "...",
      "translation": "...",
      "actual_value": "depressed",
      "exp4_classification": "depressed",
      "exp4_justification": "..."
    }
  ]
}
```
