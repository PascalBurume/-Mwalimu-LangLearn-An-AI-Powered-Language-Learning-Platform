"""
main.py — Mwalimu-LangLearn entry point
----------------------------------------
Run the application:

    python main.py                        # default: localhost:7860
    python main.py --port 8080            # custom port
    python main.py --share               # create a public Gradio share URL
    python main.py --host 0.0.0.0        # listen on all interfaces

Prerequisites:
    1. Ollama must be running:
           ollama serve
    2. The model must be pulled:
           ollama pull gemma3n:e4b
    3. Python dependencies installed:
           pip install -r requirements.txt

Environment variable overrides (optional):
    OLLAMA_HOST   — Ollama server URL  (default: http://localhost:11434)
    OLLAMA_MODEL  — Model to use       (default: gemma3n:e4b)

Architecture note:
    This file only handles startup concerns (CLI args, connectio
    n check,
    launch).  All business logic lives in mwalimu.features; all inference
    in mwalimu.inference; all UI in mwalimu.ui.
    See CODEBASE_ANALYSIS.md §3.1 for the 3-layer architecture diagram.
"""

import argparse
import os
import sys

# Allow OLLAMA_HOST / OLLAMA_MODEL to be overridden via environment variables
# before the mwalimu package imports its config defaults.
if "OLLAMA_HOST" in os.environ:
    import mwalimu.config as _cfg
    _cfg.OLLAMA_HOST = os.environ["OLLAMA_HOST"]
if "OLLAMA_MODEL" in os.environ:
    import mwalimu.config as _cfg
    _cfg.OLLAMA_MODEL = os.environ["OLLAMA_MODEL"]

from mwalimu.inference import check_connection, HAS_VISION, OLLAMA_MODEL, OLLAMA_HOST
from mwalimu.ui import build_interface


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Mwalimu-LangLearn — AI-powered multilingual language tutor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py
  python main.py --share
  python main.py --host 0.0.0.0 --port 8080
        """,
    )
    parser.add_argument(
        "--host", default="0.0.0.0",
        help="Server host (default: 0.0.0.0). Access via http://127.0.0.1:7860",
    )
    parser.add_argument(
        "--port", type=int, default=7860,
        help="Server port (default: 7860).",
    )
    parser.add_argument(
        "--share", action="store_true",
        help="Create a public Gradio share URL (tunnelled via Gradio servers).",
    )
    return parser.parse_args()


def startup_check() -> None:
    """
    Verify Ollama connectivity and print a clear status summary.
    Exits with a helpful error message if the server is unreachable.
    """
    print("\n" + "=" * 60)
    print("  Mwalimu-LangLearn — startup check")
    print("=" * 60)
    print(f"  Ollama host : {OLLAMA_HOST}")
    print(f"  Model       : {OLLAMA_MODEL}")

    ok, available = check_connection()
    if not ok:
        print("\n  ERROR: Could not connect to Ollama.")
        print(f"  Make sure it is running at {OLLAMA_HOST}")
        print("  Start it with:  ollama serve")
        print("=" * 60 + "\n")
        sys.exit(1)

    print(f"  Status      : connected")
    print(f"  Available   : {', '.join(available) or '(none)'}")

    if OLLAMA_MODEL not in available:
        print(f"\n  WARNING: '{OLLAMA_MODEL}' is not pulled yet.")
        print(f"  Run:  ollama pull {OLLAMA_MODEL}")
        print("  The app will launch but inference will fail until the model is ready.")

    if HAS_VISION:
        print("  Vision      : enabled")
    else:
        print("  Vision      : disabled (text-only model)")
        print("  To enable:  ollama pull llava  then set OLLAMA_MODEL=llava")

    print("=" * 60 + "\n")


def main() -> None:
    args = parse_args()
    startup_check()

    demo = build_interface()

    print(f"  Launching on http://127.0.0.1:{args.port}")
    if args.share:
        print("  Generating public share URL…")
    print()

    demo.launch(
        server_name=args.host,
        server_port=args.port,
        share=args.share,
        show_error=True,
        show_api=False,   # Disable API docs — avoids schema introspection bug on Python 3.9
    )


if __name__ == "__main__":
    main()