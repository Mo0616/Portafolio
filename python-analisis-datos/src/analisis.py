from __future__ import annotations

import csv
import math
from collections import Counter, defaultdict
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "data" / "clientes.csv"
OUTPUT_DIR = BASE_DIR / "salidas"
REPORT_FILE = OUTPUT_DIR / "dashboard.html"
TARGET = "satisfecho"


def read_rows() -> list[dict[str, str]]:
    with DATA_FILE.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def entropy(values: list[str]) -> float:
    total = len(values)
    counts = Counter(values)
    return -sum((count / total) * math.log2(count / total) for count in counts.values())


def bucket(value: str) -> str:
    try:
        number = int(value)
    except ValueError:
        return value

    if number <= 2:
        return "bajo"
    if number <= 5:
        return "medio"
    return "alto"


def information_gain(rows: list[dict[str, str]], attribute: str) -> float:
    base_entropy = entropy([row[TARGET] for row in rows])
    groups: dict[str, list[str]] = defaultdict(list)

    for row in rows:
        groups[bucket(row[attribute])].append(row[TARGET])

    weighted_entropy = sum(
        (len(group) / len(rows)) * entropy(group)
        for group in groups.values()
    )
    return base_entropy - weighted_entropy


def build_report(rows: list[dict[str, str]], gains: list[tuple[str, float]]) -> str:
    total = len(rows)
    satisfied = sum(1 for row in rows if row[TARGET] == "Si")
    average_response = sum(int(row["tiempo_respuesta_min"]) for row in rows) / total
    average_purchases = sum(int(row["compras_mensuales"]) for row in rows) / total

    gain_rows = "\n".join(
        f"<tr><td>{attribute}</td><td>{gain:.3f}</td></tr>"
        for attribute, gain in gains
    )

    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Dashboard de analisis de datos</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; color: #1f2933; }}
    main {{ max-width: 920px; margin: auto; }}
    .metrics {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }}
    .metric {{ border: 1px solid #d8dee9; border-radius: 8px; padding: 16px; }}
    .value {{ font-size: 32px; font-weight: 700; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 24px; }}
    th, td {{ border-bottom: 1px solid #d8dee9; padding: 10px; text-align: left; }}
  </style>
</head>
<body>
  <main>
    <h1>Analisis de satisfaccion de clientes</h1>
    <section class="metrics">
      <article class="metric"><p>Registros</p><p class="value">{total}</p></article>
      <article class="metric"><p>Satisfaccion</p><p class="value">{satisfied / total:.0%}</p></article>
      <article class="metric"><p>Respuesta promedio</p><p class="value">{average_response:.1f} min</p></article>
    </section>
    <p>Compras mensuales promedio: {average_purchases:.1f}</p>
    <h2>Seleccion de atributos por Information Gain</h2>
    <table>
      <thead><tr><th>Atributo</th><th>InfoGain</th></tr></thead>
      <tbody>{gain_rows}</tbody>
    </table>
  </main>
</body>
</html>"""


def main() -> None:
    rows = read_rows()
    attributes = [attribute for attribute in rows[0] if attribute not in {"cliente", TARGET}]
    gains = sorted(
        [(attribute, information_gain(rows, attribute)) for attribute in attributes],
        key=lambda item: item[1],
        reverse=True,
    )

    OUTPUT_DIR.mkdir(exist_ok=True)
    REPORT_FILE.write_text(build_report(rows, gains), encoding="utf-8")

    print("Ranking de atributos por Information Gain")
    for attribute, gain in gains:
        print(f"- {attribute}: {gain:.3f}")
    print(f"Dashboard generado en {REPORT_FILE}")


if __name__ == "__main__":
    main()
