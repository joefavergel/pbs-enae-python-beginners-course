<img height="8" src="https://i.imgur.com/826AqJI.png" alt="pbs-enae">

<h1 align="center">Introducción a Python</h1>

<p align="center"><i>Curso Práctico e Interactivo de Introducción al Lenguaje de Programación Python</i></p>

<p align="center">
  <a href="https://joefaver.dev/">Joseph F. Vergel-Becerra</a> 
  <a href="#estructura-del-curso">Estructura del curso</a> •
  <a href="#referencias">Referencias</a> •
  <a href="#contribuir">Contribuir</a>
  <br><br>
  <a href="https://img.shields.io/badge/version-2026.10-blue.svg?cacheSeconds=2592000"><img src="https://img.shields.io/badge/version-2026.10-blue.svg?cacheSeconds=2592000" alt="Version" height="18">
  </a>
  <a href="https://colab.research.google.com/" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Running on Colab"/>
  </a>
  <a href="https://github.com/joefavergel/pbs-enae-python-beginners-course" target="_parent"><img src="https://img.shields.io/github/forks/joefavergel/pbs-enae-python-beginners-course?style=social" alt="Fork"/>
  </a>
</p>

---

<a id="descripcion"></a>
## Descripción

Curso práctico de introducción a `Python`, del módulo **Introducción a Python** de la Especialización en Advanced Analytics and Data Science de la Panamerican Business School (octubre 2026). Su objetivo es que los participantes adquieran las habilidades necesarias para analizar datos con las bibliotecas más comunes en la industria; los conceptos teóricos se presentan junto con su implementación directa. El temario va desde la sintaxis básica hasta la manipulación de datos con `pandas`, la visualización con `matplotlib`/`seaborn` y la preparación de datos.

---

<a id="estructura-del-curso"></a>
## Estructura del curso

Sesiones los lunes de 6:00 p. m. a 9:00 p. m. (hora de Guatemala), 3 horas cada una (12 horas en total).

| Sesión | Fecha | Módulo | Notebook | Caso práctico | Ponderación | Entrega |
|---|---|---|---|---|---|---|
| 1 | lun 05/10/2026 | M1 Fundamentos de Programación en Python | `1-python-introduction.ipynb` <a href="https://colab.research.google.com/github/joefavergel/pbs-enae-python-beginners-course/blob/main/1-python-introduction.ipynb?flush_cache=true" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | Caso 1 "Introducción a Python" | 10% | 12/10/2026 |
| 2 | lun 12/10/2026 | M2 Introducción al Stack PyData (NumPy y Pandas) | `2-pydata-stack.ipynb` <a href="https://colab.research.google.com/github/joefavergel/pbs-enae-python-beginners-course/blob/main/2-pydata-stack.ipynb?flush_cache=true" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | Caso 2 "Introducción al Stack PyData" | 10% | 19/10/2026 |
| 3 | lun 19/10/2026 | M3 Ingesta, Entendimiento y Estadística Descriptiva | `3-python-data-intake.ipynb` <a href="https://colab.research.google.com/github/joefavergel/pbs-enae-python-beginners-course/blob/main/3-python-data-intake.ipynb?flush_cache=true" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a><br>`4-python-data-analysis.ipynb` <a href="https://colab.research.google.com/github/joefavergel/pbs-enae-python-beginners-course/blob/main/4-python-data-analysis.ipynb?flush_cache=true" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | Caso 3 "Ingesta de Datos"<br>Caso 4 "Entendimiento y Estadística" | 10% + 10% | 26/10/2026 |
| 4 | lun 26/10/2026 | M4 Visualización de Datos<br>M5 Preparación y Limpieza Avanzada de Datos | `5-python-data-visualization.ipynb` <a href="https://colab.research.google.com/github/joefavergel/pbs-enae-python-beginners-course/blob/main/5-python-data-visualization.ipynb?flush_cache=true" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a><br>`6-python-data-preparation.ipynb` <a href="https://colab.research.google.com/github/joefavergel/pbs-enae-python-beginners-course/blob/main/6-python-data-preparation.ipynb?flush_cache=true" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | Caso 5 "Visualización de Datos"<br>Caso 6 "Preparación de Datos" | 10% + 10% | Por confirmar |
| — | — | Proyecto final | `final_project.ipynb` <a href="https://colab.research.google.com/github/joefavergel/pbs-enae-python-beginners-course/blob/main/final_project.ipynb?flush_cache=true" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | Caso práctico final | 40% | Por confirmar |

---

<a id="como-usar"></a>
## Cómo usar los notebooks

**En Google Colab (recomendado):** abra cada notebook con su badge *Open In Colab* de la tabla anterior. Los datasets se descargan automáticamente en la carpeta `datasets/` la primera vez que se ejecutan las celdas correspondientes.

**En local:** con Python 3.9 o superior (se recomienda 3.11 o 3.12):

```bash
python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && jupyter lab
```

En Windows, active el entorno con `.venv\Scripts\activate`.

---

<a id="evaluacion"></a>
## Evaluación y entregas

- **60% acumulativo:** 6 casos prácticos, cada uno con un 10% de la nota final.
- **40% proyecto final:** caso práctico final que integra ingesta, limpieza, análisis exploratorio y visualización en un problema de negocio.

Todas las entregas se realizan únicamente a través de la Plataforma PBS.

---

<a id="referencias"></a>
## Referencias

- Matthes, E. (2019). *Python crash course: A hands-on, project-based introduction to programming.* No Starch Press.
- Johansson, R. (2019). *Numerical Python: Scientific Computing and Data Science Applications with Numpy, SciPy and Matplotlib.* Apress, Berkeley.
- VanderPlas, J. (2016). *Python data science handbook: Essential tools for working with data.* O'Reilly Media, Inc.
- Haslwanter, T. (2016). *An Introduction to Statistics with Python: With Applications in the Life Sciences.* Springer.
- Downey, A. (2015). *Think Python: How to Think Like a Computer Scientist.* O'Reilly Media, Inc.
- Aggarwal, C. C. (2015). *Data mining: The textbook* (Vol. 1). New York: Springer.

---

<a id="contribuir"></a>
## Contribuir

Para correcciones, *bugs* o sugerencias, por favor escribe a [joefavergel@gmail.com](mailto:joefavergel@gmail.com) o directamente en el repositorio.

---

## License

All code in this repository is licensed under MIT. Copyright 2023–2026 © Joseph F. Vergel-Becerra.
