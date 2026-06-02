CREATE TABLE fund_master (
    scheme_code INTEGER PRIMARY KEY,
    scheme_name TEXT,
    fund_house TEXT,
    category TEXT,
    sub_category TEXT,
    risk_grade TEXT
);

CREATE TABLE nav_history (
    scheme_code INTEGER,
    nav_date DATE,
    nav REAL
);