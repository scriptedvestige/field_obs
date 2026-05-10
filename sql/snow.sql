CREATE TABLE IF NOT EXISTS manual.snow_events (
    time TIMESTAMPTZ NOT NULL DEFAULT now(),
    event_type TEXT NOT NULL
        CHECK(event_type IN ('fresh_snow', 'melting', 'dusting', 'complete_melt')),
    snow_zone TEXT NOT NULL,
    depth_in REAL NULL,
    snow_character TEXT NULL
        CHECK(snow_character IN ('dry', 'wet', 'mixed')),
    notes TEXT NULL,
    CHECK (
        (event_type = 'dusting' AND depth_in is NULL)
        OR
        (event_type IN ('fresh_snow', 'melting') AND depth_in > 0)
        OR
        (event_type = 'complete_melt' AND depth_in = 0)
    )
);