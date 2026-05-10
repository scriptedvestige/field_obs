CREATE TABLE manual.fertilizer_events (
    id                 SERIAL PRIMARY KEY,
    applied_at         TIMESTAMPTZ DEFAULT NOW(),
    zone               TEXT NOT NULL,
    fertilizer_name    TEXT NOT NULL,
    amount             NUMERIC,
    amount_unit        TEXT,
    application_method TEXT,
    nutrients          TEXT,
    nitrogen           NUMERIC,
    phosphorus         NUMERIC,
    potassium          NUMERIC,
    notes              TEXT
);
