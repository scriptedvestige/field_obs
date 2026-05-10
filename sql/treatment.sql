CREATE TABLE manual.treatment_events (
    id                 SERIAL PRIMARY KEY,
    treated_at         TIMESTAMPTZ DEFAULT NOW(),
    zone               TEXT NOT NULL,
    treatment_type     TEXT NOT NULL,
    product_name       TEXT NOT NULL,
    target             TEXT,
    amount             NUMERIC,
    amount_unit        TEXT,
    application_method TEXT,
    notes              TEXT
);
