from __future__ import annotations

import csv
from itertools import product
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "datos" / "recursos.csv"
OUTPUT_DIR = BASE_DIR / "resultados"
OUTPUT_FILE = OUTPUT_DIR / "asignacion_optima.csv"


def load_resources() -> list[dict[str, str]]:
    with DATA_FILE.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def optimize(budget: int = 1800, minimum_benefit: int = 2600) -> tuple[list[int], int, int]:
    resources = load_resources()
    ranges = [
        range(int(row["minimo"]), int(row["maximo"]) + 1)
        for row in resources
    ]

    best_assignment: list[int] = []
    best_cost = 0
    best_benefit = 0

    for quantities in product(*ranges):
        cost = sum(int(row["costo_por_unidad"]) * qty for row, qty in zip(resources, quantities))
        benefit = sum(int(row["beneficio_por_unidad"]) * qty for row, qty in zip(resources, quantities))

        if cost <= budget and benefit >= minimum_benefit and benefit > best_benefit:
            best_assignment = list(quantities)
            best_cost = cost
            best_benefit = benefit

    if not best_assignment:
        raise RuntimeError("No se encontro una asignacion que cumpla las restricciones.")

    return best_assignment, best_cost, best_benefit


def save_results(assignment: list[int], total_cost: int, total_benefit: int) -> None:
    resources = load_resources()
    OUTPUT_DIR.mkdir(exist_ok=True)

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["area", "recurso", "unidades", "costo_total", "beneficio_total"])

        for row, quantity in zip(resources, assignment):
            writer.writerow([
                row["area"],
                row["recurso"],
                quantity,
                quantity * int(row["costo_por_unidad"]),
                quantity * int(row["beneficio_por_unidad"]),
            ])

        writer.writerow(["TOTAL", "", "", total_cost, total_benefit])


def main() -> None:
    assignment, total_cost, total_benefit = optimize()
    save_results(assignment, total_cost, total_benefit)
    print(f"Asignacion optima guardada en {OUTPUT_FILE}")
    print(f"Costo total: {total_cost}")
    print(f"Beneficio total: {total_benefit}")


if __name__ == "__main__":
    main()
