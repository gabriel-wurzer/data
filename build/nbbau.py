"""Helper to build a session notebook in two versions (student and solution) from one spec."""
import json
from pathlib import Path

NOTEBOOKS = Path(__file__).resolve().parent.parent / "notebooks"
META = {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.12"}}


class Notebook:
    def __init__(self):
        self.cells = []

    def md(self, text):
        self.cells.append(("markdown", text.strip("\n"), False, None))

    def code(self, text, hidden=False, solution=None):
        self.cells.append(("code", text.strip("\n"), hidden, solution.strip("\n") if solution else None))

    def write(self, stem):
        for name, is_solution in ((f"{stem}.ipynb", False), (f"{stem}_solution.ipynb", True)):
            cells = []
            for kind, text, hidden, solution in self.cells:
                source = solution if (is_solution and solution) else text
                lines = source.split("\n")
                src = [l + "\n" for l in lines[:-1]] + [lines[-1]]
                if kind == "markdown":
                    cells.append({"cell_type": "markdown", "metadata": {}, "source": src})
                else:
                    meta = {"jupyter": {"source_hidden": True}} if hidden else {}
                    cells.append({"cell_type": "code", "execution_count": None, "metadata": meta,
                                  "outputs": [], "source": src})
            nb = {"cells": cells, "metadata": META, "nbformat": 4, "nbformat_minor": 5}
            (NOTEBOOKS / name).write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding="utf-8")
            print("written", name, len(cells), "cells")


# shared pieces -------------------------------------------------------------------------------

DATA_BOX = r'''
<div style="border-left: 5px solid #d8a24a; background-color: #fdf6e3; color: #222; padding: 10px 16px; margin: 6px 0;">

**💡 About the data**

{text}

</div>
'''


def homework_header(title, intro, example_note):
    return f"""## Homework: {title}

{intro}

{example_note}

**How to do it**

1. Fill in the `YOUR TURN` gap above if you have not yet, yourself or from the solution; if from
   the solution, say so in one line at the top of your answers.
2. Below, change only the lines under `# YOUR CHOICE`, and write your answers into the last cell.
3. Choose Kernel, Restart Kernel and Run All Cells, and upload the notebook in TUWEL.

Before you pull updates of the course material, rename this notebook, for example by adding your
name, so your work is not overwritten.

**Points**

- Four for running it, one each: your own data is in, the result is computed, the plot is there,
  and the notebook runs from top to bottom after a restart. Leaving the worked example unchanged
  costs the first point.
- Six for your four answers about your own example. Answers that are about **your** numbers and
  say why get the points. There is no single right answer to hit, and "I cannot tell from my data,
  because ..." is a fine answer. Copied example answers get no points."""


TERMS_FOOTER = """These words are in the flashcard app of this course, together with those of the other sessions
(`webapps/flashcards`, link in TUWEL). Add it to your home screen; it works offline."""


def box(title, text):
    """A set-off note in the style of the data box, with its own title."""
    return f'''<div style="border-left: 5px solid #4c78a8; background-color: #eef3fa; color: #222; padding: 10px 16px; margin: 6px 0;">

**{title}**

{text}

</div>'''
