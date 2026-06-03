-- 1 Top 5 Funds by AUM
SELECT * FROM aum
ORDER BY aum DESC
LIMIT 5;

-- 2 Average NAV
SELECT AVG(nav) FROM nav_history;

-- 3 Monthly Average NAV
SELECT strftime('%Y-%m', date) AS month,
AVG(nav) AS avg_nav
FROM nav_history
GROUP BY month;

-- 4 Expense Ratio < 1%
SELECT *
FROM performance
WHERE expense_ratio_pct < 1;

-- 5 Transactions By State
SELECT state,
COUNT(*) AS transactions
FROM transactions
GROUP BY state;

-- 6 Total SIP Amount
SELECT SUM(amount_inr)
FROM transactions
WHERE transaction_type='SIP';

-- 7 Top States By Investment
SELECT state,
SUM(amount_inr) total_amount
FROM transactions
GROUP BY state
ORDER BY total_amount DESC
LIMIT 5;

-- 8 Top 5 Funds By 5Y Return
SELECT scheme_name,
return_5yr_pct
FROM performance
ORDER BY return_5yr_pct DESC
LIMIT 5;

-- 9 Average Expense Ratio
SELECT AVG(expense_ratio_pct)
FROM performance;

-- 10 Total Transaction Volume
SELECT COUNT(*)
FROM transactions;