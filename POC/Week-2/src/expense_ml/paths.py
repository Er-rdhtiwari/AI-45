from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = ROOT / "configs"
DATA_DIR = ROOT / "data"
RAW_DATA_PATH = DATA_DIR / "raw" / "expenses_v1.csv"
MANIFEST_PATH = DATA_DIR / "manifests" / "expenses_v1.manifest.json"
ARTIFACT_DIR = ROOT / "artifacts" / "model"
MODEL_PATH = ARTIFACT_DIR / "expense_risk_v1.joblib"
REPORT_DIR = ROOT / "reports"
EXPERIMENT_PATH = ROOT / "experiments" / "experiments.jsonl"
