# Adding Models — Quick Guide

This project currently targets **3 online models** (Gemini, GPT-4o-mini, Claude) and **4 local models** (Llama, Qwen, Gemma, DeepSeek-R1 via LM Studio). This guide explains exactly what to change to run any of them or swap in something new.

---

## Running an existing model

### Online models (Gemini / GPT-4o-mini / Claude)

1. **Get your API key** from the provider's developer portal.
2. **Add it to `.env`** (copy `.env.example` to `.env` if you haven't):
   ```
   GEMINI_API_KEY=your-key-here
   OPENAI_API_KEY=your-key-here
   CLAUDE_API_KEY=your-key-here
   ```
3. **Run Experiment 4** — pick the model with `--model`:
   ```bash
   python scripts/run_exp4.py --model claude --language arabic --full
   ```

### Local models (Llama / Qwen / Gemma / DeepSeek-R1 via LM Studio)

1. **Install LM Studio** — download from [lmstudio.ai](https://lmstudio.ai).
2. **Load the model** you want to run.
3. **Start the local server** in LM Studio (default port: `1234`).
4. **Copy the model identifier** shown in LM Studio's "Local Server" tab.
5. **Check the `default_model` value** in [scripts/run_exp4.py](scripts/run_exp4.py) for your model key and update it if the identifier doesn't match:
   ```python
   "llama": {"class": LMStudioProvider, "default_model": "meta-llama-3.1-8b-instruct", ...},
   ```
6. **Run** — no API key or `.env` change needed:
   ```bash
   python scripts/run_exp4.py --model llama --language arabic --full
   ```

---

## Adding a brand new online model

### Step 1 — Create a provider class

Copy the closest existing provider in `src/models/` as a starting point:

```bash
cp src/models/openai_provider.py src/models/myprovider_provider.py
```

Edit `src/models/myprovider_provider.py`:
- Change the class name to `MyProviderProvider`.
- Update `__init__` to use the provider's SDK / base URL.
- Implement `_call_api(self, prompt: str) -> str` — send the prompt, return the raw text.

### Step 2 — Export the class

Add it to [src/models/__init__.py](src/models/__init__.py):

```python
from .myprovider_provider import MyProviderProvider
```

### Step 3 — Add the API key mapping

In [src/config.py](src/config.py), add an entry to `ENV_MAP`:

```python
ENV_MAP = {
    ...
    "myprovider": "MYPROVIDER_API_KEY",   # <-- add this
}
```

Then add the key to your `.env`:

```
MYPROVIDER_API_KEY=your-key-here
```

### Step 4 — Register the model

In [scripts/run_exp4.py](scripts/run_exp4.py), add an entry to the `MODELS` dict:

```python
MODELS = {
    ...
    "myprovider": {"class": MyProviderProvider, "default_model": "model-id-string",
                   "online": True, "workers": 5, "delay": 0.0, "max_tokens": 500},
}
```

That's it — invoke with `--model myprovider`.

---

## Adding a new local model

### Step 1 — Load the model in LM Studio and note its identifier

Start the local server in LM Studio and copy the exact model identifier string.

### Step 2 — Add the model to `run_exp4.py`

```python
MODELS = {
    ...
    "mylocal": {"class": LMStudioProvider, "default_model": "exact-model-id-from-lmstudio",
                "online": False, "workers": 1, "delay": 0.0, "max_tokens": 500},
}
```

### Step 3 — Register it as a local provider (no API key needed)

In [src/config.py](src/config.py), add the key to `LOCAL_PROVIDERS`:

```python
LOCAL_PROVIDERS = {"lmstudio", "llama", "qwen", "mistral", "deepseek-local", "gemma", "mylocal"}
```

---

## File reference

| File | What to change |
|------|----------------|
| `.env` | Add API keys for new online models |
| [src/config.py](src/config.py) | `ENV_MAP` (online) or `LOCAL_PROVIDERS` (local) |
| `src/models/<name>_provider.py` | New provider class (online only) |
| [src/models/__init__.py](src/models/__init__.py) | Export the new class |
| [scripts/run_exp4.py](scripts/run_exp4.py) | `MODELS` dict — one entry per model |
