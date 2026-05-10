CREATE TABLE manual.watering_events (
    id                 SERIAL PRIMARY KEY,
    watered_at         TIMESTAMPTZ DEFAULT NOW(),
    zone               TEXT NOT NULL,
    duration           NUMERIC,
    application_method TEXT,
    notes              TEXT
);
