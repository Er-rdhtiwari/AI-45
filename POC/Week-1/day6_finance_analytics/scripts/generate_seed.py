from __future__ import annotations

import csv
import random
from calendar import monthrange
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
SEED = 20250806

DEPARTMENTS = [
    ("FIN", "Finance"),
    ("ENG", "Engineering"),
    ("SALES", "Sales"),
    ("MKT", "Marketing"),
    ("HR", "Human Resources"),
    ("OPS", "Operations"),
    ("IT", "Information Technology"),
    ("LEGAL", "Legal and Compliance"),
]

COST_CENTRE_NAMES = {
    "FIN": ["Controllership", "Treasury", "FP&A"],
    "ENG": ["Platform", "Data Products", "Quality Engineering"],
    "SALES": ["Enterprise Sales", "Channel Sales", "Sales Operations"],
    "MKT": ["Brand", "Demand Generation", "Events"],
    "HR": ["Talent Acquisition", "Learning", "People Operations"],
    "OPS": ["Facilities", "Procurement", "Business Operations"],
    "IT": ["End User Computing", "Cloud Infrastructure", "Security"],
    "LEGAL": ["Commercial Legal", "Privacy", "Compliance"],
}

VENDOR_PREFIXES = [
    "Apex", "BluePeak", "Crest", "Delta", "Evergreen", "Fusion", "Granite", "Helix",
    "Ion", "Jupiter", "Keystone", "Lumina", "Metro", "Nimbus", "Orion", "Pinnacle",
    "Quantum", "Redwood", "Summit", "Titan", "Unity", "Vertex", "Willow", "Xenon",
    "Yellowfin", "Zenith", "Acorn", "Beacon", "Cloudline", "Databridge",
]
VENDOR_SUFFIXES = ["Consulting", "Systems", "Services", "Solutions", "Supplies"]
DESCRIPTIONS = [
    "Professional services",
    "Software subscription",
    "Cloud infrastructure usage",
    "Office and facility services",
    "Travel and accommodation",
    "Marketing campaign services",
    "Recruitment services",
    "Training and certification",
    "Security assessment",
    "Data and research subscription",
]


def write_csv(path: Path, headers: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def generate() -> dict[str, int]:
    rng = random.Random(SEED)
    DATA_DIR.mkdir(exist_ok=True)

    departments = [
        {"code": code, "name": name} for code, name in DEPARTMENTS
    ]
    cost_centres: list[dict[str, object]] = []
    for department_code, _ in DEPARTMENTS:
        for index, name in enumerate(COST_CENTRE_NAMES[department_code], start=1):
            cost_centres.append(
                {
                    "department_code": department_code,
                    "code": f"{department_code}-{index:02d}",
                    "name": name,
                }
            )

    vendors: list[dict[str, object]] = []
    for index, prefix in enumerate(VENDOR_PREFIXES, start=1):
        risk_tier = "HIGH" if index % 10 == 0 else "MEDIUM" if index % 4 == 0 else "LOW"
        vendors.append(
            {
                "vendor_code": f"V{index:03d}",
                "name": f"{prefix} {VENDOR_SUFFIXES[index % len(VENDOR_SUFFIXES)]}",
                "risk_tier": risk_tier,
            }
        )

    department_multipliers = {
        "ENG": 1.55,
        "IT": 1.40,
        "SALES": 1.25,
        "MKT": 1.15,
        "OPS": 1.05,
        "FIN": 0.90,
        "HR": 0.75,
        "LEGAL": 0.70,
    }
    budgets: list[dict[str, object]] = []
    expenses: list[dict[str, object]] = []
    expense_counter = 1

    for cc_index, cost_centre in enumerate(cost_centres, start=1):
        department_code = str(cost_centre["department_code"])
        base_budget = rng.randint(75_000, 180_000) * department_multipliers[department_code]
        for month in range(1, 13):
            period = date(2025, month, 1)
            seasonal = 1.18 if month in {3, 6, 9, 12} else 1.0
            budget_amount = round(base_budget * seasonal * rng.uniform(0.94, 1.06), 2)
            budgets.append(
                {
                    "cost_centre_code": cost_centre["code"],
                    "period": period.isoformat(),
                    "amount": f"{budget_amount:.2f}",
                }
            )

            transaction_count = rng.randint(5, 11)
            actual_ratio = rng.uniform(0.78, 1.18)
            if (cc_index + month) % 11 == 0:
                actual_ratio += rng.uniform(0.18, 0.35)
            actual_total = budget_amount * actual_ratio
            weights = [rng.gammavariate(1.4, 1.0) for _ in range(transaction_count)]
            weight_total = sum(weights)

            for tx_index, weight in enumerate(weights, start=1):
                amount = round(max(500.0, actual_total * weight / weight_total), 2)
                if expense_counter % 97 == 0:
                    amount = round(amount * 2.6, 2)
                vendor = rng.choice(vendors)
                share = amount / budget_amount
                pending_probability = min(0.42, 0.07 + share * 0.65)
                rejected_probability = min(0.18, 0.02 + share * 0.22)
                draw = rng.random()
                if draw < rejected_probability:
                    approval = "REJECTED"
                elif draw < rejected_probability + pending_probability:
                    approval = "PENDING"
                else:
                    approval = "APPROVED"
                if vendor["risk_tier"] == "HIGH" and rng.random() < 0.28:
                    approval = "PENDING"

                last_day = monthrange(2025, month)[1]
                transaction_day = rng.randint(1, last_day)
                transaction_date = date(2025, month, transaction_day)
                expenses.append(
                    {
                        "source_system": "ERP",
                        "source_record_id": f"ERP-{expense_counter:06d}",
                        "cost_centre_code": cost_centre["code"],
                        "vendor_code": vendor["vendor_code"],
                        "period": period.isoformat(),
                        "transaction_date": transaction_date.isoformat(),
                        "invoice_number": f"INV-{2025}{month:02d}-{expense_counter:06d}",
                        "amount": f"{amount:.2f}",
                        "approval_status": approval,
                        "description": rng.choice(DESCRIPTIONS),
                    }
                )
                expense_counter += 1

    write_csv(DATA_DIR / "departments.csv", ["code", "name"], departments)
    write_csv(
        DATA_DIR / "cost_centres.csv",
        ["department_code", "code", "name"],
        cost_centres,
    )
    write_csv(
        DATA_DIR / "vendors.csv",
        ["vendor_code", "name", "risk_tier"],
        vendors,
    )
    write_csv(
        DATA_DIR / "budgets.csv",
        ["cost_centre_code", "period", "amount"],
        budgets,
    )
    write_csv(
        DATA_DIR / "expenses.csv",
        [
            "source_system",
            "source_record_id",
            "cost_centre_code",
            "vendor_code",
            "period",
            "transaction_date",
            "invoice_number",
            "amount",
            "approval_status",
            "description",
        ],
        expenses,
    )
    return {
        "departments": len(departments),
        "cost_centres": len(cost_centres),
        "vendors": len(vendors),
        "budgets": len(budgets),
        "expenses": len(expenses),
    }


if __name__ == "__main__":
    counts = generate()
    print(counts)
