"""Prueba de humo: ejecuta notebooks completos sin escribir el resultado en el repo.

Uso:
    python scripts/smoke_test.py [notebook ...] [--timeout 900]

Sin notebooks, ejecuta todos los ``*.ipynb`` de la raíz. Cada notebook se
ejecuta en memoria con ``nbclient`` y con el directorio de trabajo en la raíz
del repo, para reutilizar la caché de ``datasets/``.

Si la variable de entorno ``SMOKE_SKIP_NETWORK=1`` está definida, se omiten
las celdas con la etiqueta de metadatos ``"network"``.
"""
import argparse
import os
import sys
import time
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError


REPO_ROOT = Path(__file__).resolve().parent.parent


def run(path, timeout, skip_network):
    nb = nbformat.read(path, as_version=4)
    if skip_network:
        nb.cells = [c for c in nb.cells if "network" not in c.get("metadata", {}).get("tags", [])]
    # Celda auxiliar (solo en memoria) para reportar el intérprete del kernel.
    nb.cells.append(nbformat.v4.new_code_cell("import sys; print(sys.executable)"))

    client = NotebookClient(
        nb,
        timeout=timeout,
        kernel_name="python3",
        resources={"metadata": {"path": str(REPO_ROOT)}},
    )
    start = time.time()
    try:
        client.execute()
    except CellExecutionError as e:
        failed = next(
            (
                (i, c)
                for i, c in enumerate(nb.cells)
                if c.cell_type == "code" and any(o.get("output_type") == "error" for o in c.get("outputs", []))
            ),
            (None, None),
        )
        idx, cell = failed
        cell_id = cell.get("id") if cell is not None else "?"
        summary = str(e).strip().splitlines()[-1] if str(e).strip() else repr(e)
        return False, f"celda {idx} (id={cell_id}): {summary}", time.time() - start
    except Exception as e:
        return False, f"{type(e).__name__}: {e}", time.time() - start
    kernel_python = "".join(o.get("text", "") for o in nb.cells[-1].get("outputs", [])).strip()
    return True, f"kernel: {kernel_python}", time.time() - start


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("notebooks", nargs="*", help="notebooks a ejecutar (por defecto, todos)")
    parser.add_argument("--timeout", type=int, default=900, help="timeout por celda, en segundos")
    args = parser.parse_args()

    skip_network = os.environ.get("SMOKE_SKIP_NETWORK") == "1"
    paths = [Path(p).resolve() for p in args.notebooks] or sorted(REPO_ROOT.glob("*.ipynb"))

    print(f"[INFO] Python del entorno: {sys.executable}")
    if skip_network:
        print("[INFO] SMOKE_SKIP_NETWORK=1: se omiten las celdas con la etiqueta 'network'.")

    failures = 0
    for path in paths:
        ok, detail, elapsed = run(path, args.timeout, skip_network)
        status = "OK" if ok else "FAIL"
        print(f"[{status}] {path.name} ({elapsed:.0f} s){' — ' + detail if detail else ''}")
        failures += not ok

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
