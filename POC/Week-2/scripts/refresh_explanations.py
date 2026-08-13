import json

import joblib
import numpy as np

from expense_ml.evaluation import calibrated_predict, dump_json
from expense_ml.explain import counterfactual_search, local_contributions
from expense_ml.modeling import chronological_split, xy
from expense_ml.paths import MODEL_PATH, RAW_DATA_PATH, REPORT_DIR
from expense_ml.quality import read_expenses


if __name__ == "__main__":
    bundle = joblib.load(MODEL_PATH)
    test = chronological_split(read_expenses(RAW_DATA_PATH))["test"]
    features, _ = xy(test)
    probabilities = calibrated_predict(bundle, features)
    local_records = []
    counterfactual_records = []
    for index in np.argsort(-probabilities)[:5]:
        row = features.iloc[[index]]
        expense_id = test.iloc[index]["expense_id"]
        local_records.append(
            {
                "expense_id": expense_id,
                "probability": float(probabilities[index]),
                "contributions": local_contributions(bundle, row),
                "caveat": bundle["explanation_caveat"],
            }
        )
        counterfactual_records.append({"expense_id": expense_id, **counterfactual_search(bundle, row)})
    dump_json(REPORT_DIR / "local_explanations.json", local_records)
    dump_json(REPORT_DIR / "counterfactual_explanations.json", counterfactual_records)
    print(json.dumps({"local_explanations": len(local_records), "counterfactuals": len(counterfactual_records)}))
