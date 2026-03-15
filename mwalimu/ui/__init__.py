"""
mwalimu.ui
----------
Presentation layer — Gradio web interface.

Exports:
    build_interface() -> gr.Blocks
        Constructs and returns the full 5-tab Gradio application.
        Call .launch() on the result to start the server.
"""

from mwalimu.ui.interface import build_interface

__all__ = ["build_interface"]
