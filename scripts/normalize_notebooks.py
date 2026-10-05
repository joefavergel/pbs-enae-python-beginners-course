"""Normaliza los notebooks del curso: salidas limpias y kernelspec homogéneo.

Uso:
    python scripts/normalize_notebooks.py [notebook ...]

Sin argumentos, procesa todos los ``*.ipynb`` de la raíz del repositorio.
"""
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
KERNELSPEC = {
    "display_name": "Python 3 (ipykernel)",
    "language": "python",
    "name": "python3",
}


def normalize(path):
    nb = json.loads(path.read_text(encoding="utf-8"))

    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            cell["outputs"] = []
            cell["execution_count"] = None

    metadata = nb.setdefault("metadata", {})
    metadata["kernelspec"] = dict(KERNELSPEC)
    metadata.get("language_info", {}).pop("version", None)

    with path.open("w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
        f.write("\n")


def main(argv):
    paths = [Path(p) for p in argv] or sorted(REPO_ROOT.glob("*.ipynb"))
    for path in paths:
        normalize(path)
        print(f"[INFO] Normalizado: {path.name}")


if __name__ == "__main__":
    main(sys.argv[1:])
