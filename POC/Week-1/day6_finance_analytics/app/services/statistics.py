from __future__ import annotations

import math

from scipy import stats
from sqlalchemy.orm import Session

from app.exceptions import DomainError
from app.repositories.analytics import amounts_by_approval
from app.schemas import StatisticalTestResult


def approval_amount_welch_test(session: Session) -> StatisticalTestResult:
    approved, non_approved = amounts_by_approval(session)
    if len(approved) < 2 or len(non_approved) < 2:
        raise DomainError("at least two observations are required in each group")

    approved_mean = stats.tmean(approved)
    non_approved_mean = stats.tmean(non_approved)
    approved_var = stats.tvar(approved)
    non_approved_var = stats.tvar(non_approved)
    n1, n2 = len(approved), len(non_approved)
    se = math.sqrt(approved_var / n1 + non_approved_var / n2)
    numerator = (approved_var / n1 + non_approved_var / n2) ** 2
    denominator = ((approved_var / n1) ** 2 / (n1 - 1)) + (
        (non_approved_var / n2) ** 2 / (n2 - 1)
    )
    degrees_of_freedom = numerator / denominator
    mean_difference = non_approved_mean - approved_mean
    critical = stats.t.ppf(0.975, degrees_of_freedom)
    ci_low = mean_difference - critical * se
    ci_high = mean_difference + critical * se
    test = stats.ttest_ind(non_approved, approved, equal_var=False)

    pooled_sd = math.sqrt(
        ((n1 - 1) * approved_var + (n2 - 1) * non_approved_var) / (n1 + n2 - 2)
    )
    cohen_d = mean_difference / pooled_sd if pooled_sd else 0.0
    interpretation = (
        "The synthetic data shows a statistically detectable difference in mean expense "
        "amounts between non-approved and approved transactions. This is association, not causation."
        if test.pvalue < 0.05
        else "The synthetic data does not provide strong evidence of a difference in group means."
    )
    return StatisticalTestResult(
        approved_n=n1,
        non_approved_n=n2,
        approved_mean=round(float(approved_mean), 2),
        non_approved_mean=round(float(non_approved_mean), 2),
        mean_difference=round(float(mean_difference), 2),
        ci_95_low=round(float(ci_low), 2),
        ci_95_high=round(float(ci_high), 2),
        t_statistic=round(float(test.statistic), 4),
        p_value=round(float(test.pvalue), 8),
        cohen_d=round(float(cohen_d), 4),
        interpretation=interpretation,
        limitations=[
            "The dataset is synthetic and intentionally contains approval-related patterns.",
            "Expenses are clustered by department, cost centre, period, and vendor, so observations are not fully independent.",
            "A t-test compares means and does not prove that approval status causes amount differences.",
            "Heavy tails and outliers can affect both the mean difference and confidence interval.",
            "Repeated slicing or multiple tests would require multiplicity control.",
        ],
    )
