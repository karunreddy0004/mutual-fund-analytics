-- 1 Top 5 funds by AUM
SELECT *
FROM aum_by_fund_house
ORDER BY aum_crore DESC
LIMIT 5;

-- 2 Average NAV
SELECT strftime('%Y-%m', date) AS month,
AVG(nav) avg_nav
FROM nav_history
GROUP BY month;

-- 3 Transactions by State
SELECT state,
COUNT(*) transactions
FROM investor_transactions
GROUP BY state
ORDER BY transactions DESC;

-- 4 Expense Ratio < 1%
SELECT scheme_name,
expense_ratio_pct
FROM scheme_performance
WHERE expense_ratio_pct < 1;

-- 5 Top Return Funds
SELECT scheme_name,
return_5yr_pct
FROM scheme_performance
ORDER BY return_5yr_pct DESC
LIMIT 10;

-- 6 Average Transaction Amount
SELECT AVG(amount_inr)
FROM investor_transactions;

-- 7 Transaction Type Distribution
SELECT transaction_type,
COUNT(*)
FROM investor_transactions
GROUP BY transaction_type;

-- 8 Top States by Investment
SELECT state,
SUM(amount_inr)
FROM investor_transactions
GROUP BY state
ORDER BY SUM(amount_inr) DESC;

-- 9 Highest Alpha Funds
SELECT scheme_name,
alpha
FROM scheme_performance
ORDER BY alpha DESC
LIMIT 10;

-- 10 Highest Sharpe Ratio Funds
SELECT scheme_name,
sharpe_ratio
FROM scheme_performance
ORDER BY sharpe_ratio DESC
LIMIT 10;
