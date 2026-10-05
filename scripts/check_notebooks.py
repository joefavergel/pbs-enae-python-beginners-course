"""Verificador de los notebooks del curso (solo biblioteca estándar).

Uso:
    python scripts/check_notebooks.py [--strict]

Imprime una tabla notebook x chequeo con OK/WARN/FAIL y termina con
código 1 si hay algún FAIL. Sin ``--strict``, los chequeos C7-C11 que
dependen de las specs 002-006 se reportan como WARN en lugar de FAIL.
"""
import argparse
import json
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent

EXPECTED_NOTEBOOKS = [
    "1-python-introduction.ipynb",
    "2-pydata-stack.ipynb",
    "3-python-data-intake.ipynb",
    "4-python-data-analysis.ipynb",
    "5-python-data-visualization.ipynb",
    "6-python-data-preparation.ipynb",
    "final_project.ipynb",
]

# Sesión de cada notebook (None = proyecto final) y nombre del caso según el syllabus.
SESSIONS = {
    "1-python-introduction": 1,
    "2-pydata-stack": 2,
    "3-python-data-intake": 3,
    "4-python-data-analysis": 3,
    "5-python-data-visualization": 4,
    "6-python-data-preparation": 4,
    "final_project": None,
}
CASE_NAMES = {
    "1-python-introduction": "Introducción a Python",
    "2-pydata-stack": "Introducción al Stack PyData",
    "3-python-data-intake": "Ingesta de Datos",
    "4-python-data-analysis": "Entendimiento y Estadística",
    "5-python-data-visualization": "Visualización de Datos",
    "6-python-data-preparation": "Preparación de Datos",
}

# Las cadenas prohibidas se construyen por partes para que este archivo
# no las contenga literalmente (REQ-001-06).
FORBIDDEN_C5 = [
    "pbs-enae-" + "ml-course",
    "Machine Learning" + " - Tools",
    "vifi" + "cadas",
    "Hals" + "wanter",
    "hei" + "gth",
    "!pip" + " install",
]
FORBIDDEN_C11 = [
    "Prapa" + "ración",
    "can" + "vas",
    "seis" + " sesiones",
    "HERE WE WILL DEVELOP" + " THE CODE IN CLASS",
    "mapbox" + "_style",
    "file_paths" + "[3]",
]

COLAB_RE = re.compile(
    r"https://colab\.research\.google\.com/github/joefavergel/"
    r"pbs-enae-python-beginners-course/blob/main/([^\"'?\s)]+)(\?flush_cache=true)?"
)
HREF_RE = re.compile(r"""href=["']#([^"']+)["']""")
ID_RE = re.compile(r"""\bid=["']([^"']+)["']""")
EXERCISES_RE = re.compile(r"""<a\s+id=["']ejercicios["']""")
DATE_RE = re.compile(r"\b\d{2}/\d{2}/2026\b|Por confirmar")
CASE_TITLE_RE = re.compile(r"""^##\s+\d+\.\s+Caso práctico:\s+["“](.+?)["”]""", re.M)

OK, WARN, FAIL = "OK", "WARN", "FAIL"
CHECKS = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "C11"]
SOFT_CHECKS = {"C7", "C8", "C9", "C10", "C11"}


def cell_text(cell):
    source = cell.get("source", "")
    return "".join(source) if isinstance(source, list) else source


def check_notebook(path, notebooks_ok):
    stem = path.stem
    results = {"C1": (OK if notebooks_ok else FAIL, "")}

    try:
        nb = json.loads(path.read_text(encoding="utf-8"))
        assert nb.get("nbformat") == 4, f"nbformat={nb.get('nbformat')}"
    except Exception as e:
        results["C2"] = (FAIL, str(e))
        return results
    results["C2"] = (OK, "")

    cells = nb.get("cells", [])
    texts = [cell_text(c) for c in cells]
    full_text = "\n".join(texts)

    dirty = [
        i for i, c in enumerate(cells)
        if c.get("cell_type") == "code" and (c.get("outputs") or c.get("execution_count") is not None)
    ]
    results["C3"] = (FAIL, f"celdas con salidas: {dirty[:5]}") if dirty else (OK, "")

    kernel = nb.get("metadata", {}).get("kernelspec", {}).get("name")
    results["C4"] = (OK, "") if kernel == "python3" else (FAIL, f"kernelspec.name={kernel}")

    found = [s for s in FORBIDDEN_C5 if s in full_text]
    results["C5"] = (FAIL, ", ".join(found)) if found else (OK, "")

    badges = COLAB_RE.findall(full_text)
    own = [b for b in badges if b[0] == path.name and b[1]]
    others = sorted({b[0] for b in badges if b[0] != path.name})
    if own and not others:
        results["C6"] = (OK, "")
    else:
        results["C6"] = (FAIL, f"badge propio={bool(own)}, otros={others}")

    no_comments = re.sub(r"<!--.*?-->", "", full_text, flags=re.S)
    broken = sorted(set(HREF_RE.findall(no_comments)) - set(ID_RE.findall(no_comments)))
    results["C7"] = (WARN, f"anclas sin destino: {broken}") if broken else (OK, "")

    session = SESSIONS.get(stem)
    header = texts[0] if texts else ""
    expected_header = "Proyecto final" if session is None else f"Sesión {session}"
    results["C8"] = (OK, "") if expected_header in header else (WARN, f"falta '{expected_header}'")

    results["C9"], results["C10"] = check_exercises(stem, texts)

    found = [s for s in FORBIDDEN_C11 if s in full_text]
    results["C11"] = (WARN, ", ".join(found)) if found else (OK, "")

    return results


def check_exercises(stem, texts):
    if stem == "final_project":
        c9 = (OK, "") if "40%" in "\n".join(texts) else (WARN, "no contiene '40%'")
        return c9, (OK, "n/a")

    idx = [i for i, t in enumerate(texts) if EXERCISES_RE.search(t)]
    if len(idx) != 1:
        return (WARN, f'{len(idx)} anclas id="ejercicios"'), (WARN, "sin sección de ejercicios")

    block = "\n".join(texts[idx[0]:idx[0] + 2])
    missing = [s for s in ("Plataforma PBS", "10%") if s not in block]
    if not DATE_RE.search(block):
        missing.append("fecha dd/mm/2026 o 'Por confirmar'")
    c9 = (WARN, f"faltan: {missing}") if missing else (OK, "")

    title = CASE_TITLE_RE.search(texts[idx[0]])
    expected = CASE_NAMES[stem]
    if title and title.group(1) == expected:
        c10 = (OK, "")
    else:
        c10 = (WARN, f"se esperaba 'Caso práctico: \"{expected}\"', hay: {title.group(1) if title else None}")
    return c9, c10


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--strict", action="store_true", help="convierte los WARN de C7-C11 en FAIL")
    args = parser.parse_args()

    present = sorted(p.name for p in REPO_ROOT.glob("*.ipynb"))
    notebooks_ok = present == sorted(EXPECTED_NOTEBOOKS)
    if not notebooks_ok:
        missing = sorted(set(EXPECTED_NOTEBOOKS) - set(present))
        extra = sorted(set(present) - set(EXPECTED_NOTEBOOKS))
        print(f"[FAIL] C1: faltan {missing}, sobran {extra}")

    rows = {}
    for name in present:
        results = check_notebook(REPO_ROOT / name, notebooks_ok)
        if args.strict:
            results = {k: ((FAIL, d) if s == WARN and k in SOFT_CHECKS else (s, d)) for k, (s, d) in results.items()}
        rows[name] = results

    width = max(len(n) for n in present) if present else 10
    print(f"{'notebook':<{width}}  " + "  ".join(f"{c:<4}" for c in CHECKS))
    for name, results in rows.items():
        print(f"{name:<{width}}  " + "  ".join(f"{results.get(c, ('-', ''))[0]:<4}" for c in CHECKS))

    details = [
        (name, c, s, d) for name, results in rows.items() for c in CHECKS
        for s, d in [results.get(c, ("-", ""))] if s in (WARN, FAIL) and d
    ]
    if details:
        print("\nDetalles:")
        for name, c, s, d in details:
            print(f"  [{s}] {name} {c}: {d}")

    failed = not notebooks_ok or any(s == FAIL for r in rows.values() for s, _ in r.values())
    print(f"\nResultado: {'FAIL' if failed else 'OK'}{' (--strict)' if args.strict else ''}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
