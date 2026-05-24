"""run_all.py — execute the full pipeline end-to-end.

Steps:
  Step 0 — Setup checks (.env present, Python deps importable)
  Step 1 — Preprocessing  (scripts/prepare_data.py)
  Step 2 — Experiment 4   (fresh classification + justification; few-shot AND zero-shot)

Usage:
    python run_all.py                              # full pipeline, every model and language
    python run_all.py --models claude,gemini       # restrict models
    python run_all.py --languages arabic,urdu      # restrict languages
    python run_all.py --limit 10                   # 10 samples per (model, lang) — sanity check
    python run_all.py --skip 1                     # skip Step 1 (preprocessing)
    python run_all.py --only 2                     # run only Step 2 (Exp 4)
    python run_all.py --dry-run                    # print the plan, run nothing

Notes:
    - Every underlying script is resumable — re-running this picks up where it left off.
    - Add --fresh to wipe partial checkpoints and start over.
    - Missing API keys cause that model to be skipped (with a warning) — not a failure.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))

ALL_MODELS = ["gemini", "openai", "claude", "llama", "qwen", "deepseek-local", "gemma"]
ALL_LANGUAGES = ["arabic", "urdu", "chinese"]

STEPS = {
    0: "Setup checks",
    1: "Preprocessing",
    2: "Experiment 4 — Fresh classification + justification",
}


# ── Pretty printing ──────────────────────────────────────────────────────────

def banner(step_num: int, label: str) -> None:
    line = "=" * 78
    print(f"\n{line}")
    print(f"  STEP {step_num} — {label}")
    print(f"{line}")


def run_cmd(cmd: list, check: bool = True) -> int:
    """Run a subprocess, stream output, exit on failure if check=True."""
    print(f"\n  $ {' '.join(str(c) for c in cmd)}\n")
    result = subprocess.run(cmd, cwd=ROOT)
    if check and result.returncode != 0:
        print(f"\n  Step failed with exit code {result.returncode}. Aborting.")
        sys.exit(result.returncode)
    return result.returncode


# ── Step 0: Setup checks ─────────────────────────────────────────────────────

def step0_setup_checks(models: list) -> None:
    banner(0, STEPS[0])
    ok = True

    env_path = ROOT / ".env"
    if not env_path.exists():
        print(f"  [X] .env not found at {env_path}")
        print(f"      Run:  cp .env.example .env   (then fill in API keys)")
        ok = False
    else:
        print(f"  [OK] .env exists")

    for mod in ("dotenv", "google.generativeai", "openai", "anthropic"):
        try:
            __import__(mod)
            print(f"  [OK] import {mod}")
        except ImportError:
            print(f"  [X]  import {mod}  — run: pip install -r requirements.txt")
            ok = False

    if env_path.exists():
        from dotenv import load_dotenv
        load_dotenv(env_path)
        env_map = {
            "gemini": "GEMINI_API_KEY",
            "openai": "OPENAI_API_KEY",
            "claude": "CLAUDE_API_KEY",
        }
        for m in models:
            if m in env_map:
                key = os.environ.get(env_map[m])
                if key and key.strip() and not key.startswith("your-"):
                    print(f"  [OK] {env_map[m]} set ({m})")
                else:
                    print(f"  [!]  {env_map[m]} missing — '{m}' will be skipped")
            else:
                print(f"  [..] {m} is a local model — ensure LM Studio is running")

    if not ok:
        print("\n  Setup checks failed. Fix the issues above, then re-run.")
        sys.exit(1)


# ── Step 1: Preprocessing ────────────────────────────────────────────────────

def step1_preprocess(languages: list, dry_run: bool) -> None:
    banner(1, STEPS[1])
    if set(languages) == set(ALL_LANGUAGES):
        cmd = [sys.executable, "scripts/prepare_data.py"]
        if dry_run:
            print(f"\n  (dry-run) $ {' '.join(cmd)}")
            return
        run_cmd(cmd)
    else:
        for lang in languages:
            cmd = [sys.executable, "scripts/prepare_data.py", "--lang", lang]
            if dry_run:
                print(f"\n  (dry-run) $ {' '.join(cmd)}")
                continue
            run_cmd(cmd)


# ── Step 2: Experiment 4 ─────────────────────────────────────────────────────

def step2_experiment4(models, languages, limit, fresh, dry_run):
    banner(2, STEPS[2])
    models_arg = ",".join(models)
    langs_arg  = ",".join(languages)

    for label, extra in [("few-shot", []), ("zero-shot", ["--zeroshot"])]:
        print(f"\n  -- Experiment 4 ({label}) --")
        cmd = [sys.executable, "scripts/run_exp4.py",
               "--models", models_arg,
               "--languages", langs_arg,
               "--full"] + extra
        if fresh:
            cmd.append("--fresh")
        if limit:
            cmd += ["--limit", str(limit)]
        if dry_run:
            print(f"  (dry-run) $ {' '.join(cmd)}")
            continue
        run_cmd(cmd, check=False)  # keep going even if one mode partially fails


# ── Entry point ──────────────────────────────────────────────────────────────

def _parse_step_list(s: str) -> set:
    return {int(x.strip()) for x in s.split(",") if x.strip()}


def main():
    parser = argparse.ArgumentParser(
        description="Run the full pipeline end-to-end.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--models",    default=",".join(ALL_MODELS),
                        help="Comma-separated model keys (default: all)")
    parser.add_argument("--languages", default=",".join(ALL_LANGUAGES),
                        help="Comma-separated languages (default: arabic,urdu,chinese)")
    parser.add_argument("--limit",   type=int, default=None,
                        help="Process only N samples per (model, lang) — quick sanity check")
    parser.add_argument("--fresh",   action="store_true",
                        help="Discard partial checkpoints; start every step from scratch")
    parser.add_argument("--skip",    default="",
                        help="Comma-separated step numbers to SKIP (e.g. --skip 1)")
    parser.add_argument("--only",    default="",
                        help="Comma-separated step numbers to RUN exclusively (overrides --skip)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print the planned commands without executing them")
    args = parser.parse_args()

    models    = [m.strip() for m in args.models.split(",")    if m.strip()]
    languages = [l.strip() for l in args.languages.split(",") if l.strip()]

    skip = _parse_step_list(args.skip)
    only = _parse_step_list(args.only)
    def should_run(step_num: int) -> bool:
        if only:
            return step_num in only
        return step_num not in skip

    print(f"\n  Pipeline plan")
    print(f"  -------------")
    print(f"  Models:     {', '.join(models)}")
    print(f"  Languages:  {', '.join(languages)}")
    print(f"  Limit:      {args.limit or 'no limit (full dataset)'}")
    print(f"  Fresh:      {args.fresh}")
    print(f"  Steps:      {', '.join(str(s) for s in sorted(STEPS) if should_run(s))}")
    if args.dry_run:
        print(f"  DRY RUN — no commands will execute")

    if should_run(0):
        step0_setup_checks(models)
    if should_run(1):
        step1_preprocess(languages, args.dry_run)
    if should_run(2):
        step2_experiment4(models, languages, args.limit, args.fresh, args.dry_run)

    print(f"\n{'='*78}")
    print(f"  Pipeline complete.")
    print(f"{'='*78}\n")


if __name__ == "__main__":
    main()
