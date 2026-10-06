"""Ejecuta un notebook y lo exporta a HTML, junto con el enunciado de su caso práctico.

Uso:
    python scripts/export_html.py <notebook.ipynb> [--out DIR] [--no-execute] [--timeout 900]

Genera en ``--out``:
- ``<nombre>.html``: el notebook ejecutado (con salidas);
- ``<nombre>-caso-practico.html``: el enunciado del caso práctico, tomado de
  ``casos/<nombre>.md``, con los estilos de ``styles/custom.css``. Los enunciados
  se publican en el Moodle del curso (Plataforma PBS), no en el notebook.

El notebook se ejecuta en memoria con el directorio de trabajo en la raíz del repo
(para reutilizar ``datasets/``); el ``.ipynb`` del repositorio no se modifica.
"""
import argparse
import html
import re
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbconvert import HTMLExporter


REPO_ROOT = Path(__file__).resolve().parent.parent
CASES_DIR = REPO_ROOT / "casos"
TITLE_RE = re.compile(r"^##\s+(.+)$", re.M)
FULL_PAGE_RE = re.compile(r"<html[\s>]|<!doctype html", re.I)


def isolate_html_documents(nb):
    """Muestra en un iframe las salidas que son páginas HTML completas.

    Así su CSS (p. ej. ``body{max-width:...}``) no altera el diseño del HTML exportado.
    """
    for cell in nb.cells:
        for output in cell.get("outputs", []):
            page = output.get("data", {}).get("text/html")
            if isinstance(page, list):
                page = "".join(page)
            if page and FULL_PAGE_RE.search(page):
                output["data"]["text/html"] = (
                    f'<iframe srcdoc="{html.escape(page, quote=True)}" '
                    'style="width:100%; height:320px; border:1px solid #ddd;"></iframe>'
                )


def case_notebook(source, metadata):
    # Celda de estilos: solo su salida HTML aparece en la exportación (el código se oculta).
    css = (REPO_ROOT / "styles" / "custom.css").read_text(encoding="utf-8")
    styles = nbformat.v4.new_code_cell(
        "# estilos",
        outputs=[nbformat.v4.new_output("display_data", data={"text/html": css})],
    )
    title = TITLE_RE.search(source)
    nb = nbformat.v4.new_notebook(cells=[styles, nbformat.v4.new_markdown_cell(source)])
    nb.metadata = {**metadata, "title": title.group(1).replace('"', "") if title else "Caso práctico"}
    return nb


def export(nb, target, name, **options):
    body, _ = HTMLExporter(template_name="lab", **options).from_notebook_node(
        nb, resources={"metadata": {"name": name}}
    )
    target.write_text(body, encoding="utf-8")
    print(f"[OK] {target}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("notebook", type=Path)
    parser.add_argument("--out", type=Path, default=Path("."), help="carpeta de salida")
    parser.add_argument("--no-execute", action="store_true", help="exporta sin ejecutar el notebook")
    parser.add_argument("--timeout", type=int, default=900, help="timeout por celda, en segundos")
    args = parser.parse_args()

    stem = args.notebook.stem
    nb = nbformat.read(args.notebook, as_version=4)
    if not args.no_execute:
        NotebookClient(
            nb,
            timeout=args.timeout,
            kernel_name="python3",
            resources={"metadata": {"path": str(REPO_ROOT)}},
        ).execute()

    isolate_html_documents(nb)
    args.out.mkdir(parents=True, exist_ok=True)
    export(nb, args.out / f"{stem}.html", stem)

    case_source = CASES_DIR / f"{stem}.md"
    if case_source.is_file():
        export(
            case_notebook(case_source.read_text(encoding="utf-8"), nb.metadata),
            args.out / f"{stem}-caso-practico.html",
            stem,
            exclude_input=True,
            exclude_input_prompt=True,
            exclude_output_prompt=True,
        )
    else:
        print(f"[WARN] {stem}: no existe {case_source.relative_to(REPO_ROOT)}; no se genera el HTML del caso.")


if __name__ == "__main__":
    main()
