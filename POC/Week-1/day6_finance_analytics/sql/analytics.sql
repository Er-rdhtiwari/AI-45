-- 1. Budget-versus-actual by department and period.
WITH budgeted AS (
    SELECT d.code AS department_code,
           b.period,
           SUM(b.amount) AS budget
    FROM budgets b
    JOIN cost_centres cc ON cc.id = b.cost_centre_id
    JOIN departments d ON d.id = cc.department_id
    WHERE b.period BETWEEN DATE '2025-01-01' AND DATE '2025-12-01'
    GROUP BY d.code, b.period
),
actuals AS (
    SELECT d.code AS department_code,
           e.period,
           SUM(e.amount) AS actual
    FROM expenses e
    JOIN cost_centres cc ON cc.id = e.cost_centre_id
    JOIN departments d ON d.id = cc.department_id
    WHERE e.period BETWEEN DATE '2025-01-01' AND DATE '2025-12-01'
    GROUP BY d.code, e.period
)
SELECT b.department_code,
       b.period,
       b.budget,
       COALESCE(a.actual, 0) AS actual,
       COALESCE(a.actual, 0) - b.budget AS variance,
       ROUND((COALESCE(a.actual, 0) - b.budget) * 100.0 / NULLIF(b.budget, 0), 2)
           AS variance_pct
FROM budgeted b
LEFT JOIN actuals a USING (department_code, period)
ORDER BY b.period, b.department_code;

-- 2. Monthly trend with a rolling three-month total.
WITH monthly AS (
    SELECT e.period,
           SUM(e.amount) AS actual
    FROM expenses e
    GROUP BY e.period
)
SELECT period,
       actual,
       SUM(actual) OVER (
           ORDER BY period ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
       ) AS rolling_3m_actual
FROM monthly
ORDER BY period;

-- 3. Ranked exception candidates. The score is triage logic, not a fraud label.
WITH scored AS (
    SELECT e.id,
           e.period,
           d.code AS department_code,
           cc.code AS cost_centre_code,
           v.vendor_code,
           v.risk_tier,
           e.amount,
           e.approval_status,
           b.amount AS monthly_budget,
           ROUND(e.amount * 100.0 / NULLIF(b.amount, 0), 2) AS budget_share_pct,
           ROUND(
               e.amount * 100.0 / NULLIF(b.amount, 0)
               + CASE e.approval_status
                   WHEN 'REJECTED' THEN 50
                   WHEN 'PENDING' THEN 30
                   ELSE 0
                 END
               + CASE v.risk_tier
                   WHEN 'HIGH' THEN 25
                   WHEN 'MEDIUM' THEN 10
                   ELSE 0
                 END,
               2
           ) AS exception_score
    FROM expenses e
    JOIN cost_centres cc ON cc.id = e.cost_centre_id
    JOIN departments d ON d.id = cc.department_id
    JOIN vendors v ON v.id = e.vendor_id
    JOIN budgets b ON b.cost_centre_id = e.cost_centre_id AND b.period = e.period
)
SELECT *,
       ROW_NUMBER() OVER (ORDER BY exception_score DESC, id ASC) AS stable_rank
FROM scored
WHERE exception_score >= 25
ORDER BY exception_score DESC, id ASC
LIMIT 100;

-- 4. Duplicate-invoice review query. Not exposed as an endpoint in the PoC.
SELECT vendor_id,
       invoice_number,
       COUNT(*) AS duplicate_count,
       SUM(amount) AS duplicate_amount
FROM expenses
GROUP BY vendor_id, invoice_number
HAVING COUNT(*) > 1
ORDER BY duplicate_amount DESC;
