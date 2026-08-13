import joblib
import pytest

from expense_ml.paths import MODEL_PATH


@pytest.fixture(scope="session")
def model_bundle():
    assert MODEL_PATH.exists(), "Run scripts/train.py before tests"
    return joblib.load(MODEL_PATH)
