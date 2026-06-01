from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from database import get_conn
from datetime import datetime
from zoneinfo import ZoneInfo

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Main Menu
@app.get("/menu", name="menu")
def menu(request: Request):
    return templates.TemplateResponse("index.html", {"request":request})

# Fertilizer Events
@app.get("/fertilizer", name="fertilizer")
def fertilizer_form(request: Request):
    return templates.TemplateResponse("fertilizer.html", {"request":request})

@app.post("/fertilizer")
def log_fertilizer(
    zones: list[str] = Form(...),
    fertilizer_name: str = Form(...),
    amount: float | None = Form(None),
    amount_unit: str | None = Form(None),
    application_method: str | None = Form(None),
    nutrients: str | None = Form(None),
    nitrogen: float | None = Form(None),
    phosphorus: float | None = Form(None),
    potassium: float | None = Form(None),
    notes: str | None = Form(None),
):
    conn = get_conn()
    cur = conn.cursor()
    for zone in zones:
        cur.execute(
            """
            INSERT INTO manual.fertilizer_events 
                (zone, fertilizer_name, amount, amount_unit, application_method, nutrients, nitrogen, phosphorus, potassium, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (zone, fertilizer_name, amount, amount_unit, application_method, nutrients, nitrogen, phosphorus, potassium, notes)
        )
    conn.commit()
    cur.close()
    conn.close()

    return RedirectResponse("/fertilizer", status_code=303)

# Snow Events
@app.get("/snow", name="snow")
def snow_form(request: Request):
    return templates.TemplateResponse("snow.html", {"request":request})

@app.post("/snow")
def log_snow(
    event_type: str = Form(...),
    snow_zone: str = Form(...),
    depth_in: float | None = Form(None),
    snow_character: str | None = Form(None),
    notes: str | None = Form(None),
):
    # Validation: dusting depth must be None
    if event_type == "dusting":
        depth_in = None
    elif event_type == "complete_melt":
        depth_in = 0

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO manual.snow_events (event_type, depth_in, snow_character, notes, snow_zone)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (event_type, depth_in, snow_character, notes, snow_zone)
    )
    conn.commit()
    cur.close()
    conn.close()

    return RedirectResponse("/snow", status_code=303)

# Disease/Pest Treatment Events
@app.get("/treatment", name="treatment")
def treatment_form(request: Request):
    return templates.TemplateResponse("treatment.html", {"request":request})

@app.post("/treatment")
def log_treatment(
    request: Request,
    zones: list[str] = Form(...),
    treatment_type: str = Form(...),
    product_name: str = Form(...),
    target: str | None = Form(None),
    amount: float | None = Form(None),
    amount_unit: str | None = Form(None),
    application_method: str | None = Form(None),
    notes: str | None = Form(None),
):
    conn = get_conn()
    cur = conn.cursor()
    for zone in zones:
        cur.execute(
            """
            INSERT INTO manual.treatment_events (zone, treatment_type, product_name, target, amount, amount_unit, application_method, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (zone, treatment_type, product_name, target, amount, amount_unit, application_method, notes)
        )
    conn.commit()
    cur.close()
    conn.close()

    return RedirectResponse("/treatment", status_code=303)

# Watering Events
@app.get("/watering", name="watering")
def watering_form(request: Request):
    return templates.TemplateResponse("watering.html", {"request":request})

@app.post("/watering")
def log_watering(
    request: Request,
    zones: list[str] = Form(...),
    duration: float | None = Form(None),
    application_method: str | None = Form(None),
    notes: str | None = Form(None),
):
    conn = get_conn()
    cur = conn.cursor()
    for zone in zones:
        cur.execute(
            """
            INSERT INTO manual.watering_events (zone, duration, application_method, notes)
            VALUES (%s, %s, %s, %s)
            """,
            (zone, duration, application_method, notes)
        )
    conn.commit()
    cur.close()
    conn.close()

    return RedirectResponse("/watering", status_code=303)

# Migraine Events, selecting open events with no end date and time
@app.get("/migraine", name="migraine")
def migraine_form(request: Request):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, onset FROM manual.migraine_events WHERE ended IS NULL ORDER BY onset DESC"
    )
    open_migraines = cur.fetchall()
    cur.close()
    conn.close()
    return templates.TemplateResponse("migraine.html", {
        "request": request,
        "open_migraines": open_migraines
    })


@app.post("/migraine")
def log_migraine(
    onset: str | None = Form(None),
    ended: str | None = Form(None),
    severity: int | None = Form(None),
    excedrin_pills: int | None = Form(None),
    workout_yesterday: str | None = Form(None),
    hydration_yesterday: str | None = Form(None),
    notes: str | None = Form(None),
):
    
    # Handling timezone, enter as local time, insert to db in UTC
    pacific = ZoneInfo("America/Los_Angeles")

    onset_dt = datetime.fromisoformat(onset).replace(tzinfo=pacific).astimezone(ZoneInfo("UTC")) if onset else None
    ended_dt = datetime.fromisoformat(ended).replace(tzinfo=pacific).astimezone(ZoneInfo("UTC")) if ended else None

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO manual.migraine_events 
            (onset, ended, severity, excedrin_pills, hydration_yesterday, notes, workout_yesterday)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (onset_dt, ended_dt, severity, excedrin_pills, hydration_yesterday, notes, workout_yesterday)
    )
    conn.commit()
    cur.close()
    conn.close()

    return RedirectResponse("/migraine", status_code=303)

# Close a migraine entry with an end time, updating a row instead of creating a new row.
@app.post("/migraine/close")
def close_migraine(
    migraine_id: int = Form(...),
    ended: str = Form(...),
):
    pacific = ZoneInfo("America/Los_Angeles")
    ended_dt = datetime.fromisoformat(ended).replace(tzinfo=pacific).astimezone(ZoneInfo("UTC"))
    
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "UPDATE manual.migraine_events SET ended = %s WHERE id = %s",
        (ended_dt, migraine_id)
    )
    conn.commit()
    cur.close()
    conn.close()
    return RedirectResponse("/migraine", status_code=303)

# Hydration Events
@app.get("/hydration", name="hydration")
def hydration_form(request: Request):
    return templates.TemplateResponse("hydration.html", {"request": request})

@app.post("/hydration")
def log_hydration(
    consumed_at: str = Form(...),
    beverage_type: str = Form(...),
    volume_oz: float = Form(...),
    notes: str | None = Form(None),
):
    pacific = ZoneInfo("America/Los_Angeles")
    consumed_at_dt = datetime.fromisoformat(consumed_at).replace(tzinfo=pacific).astimezone(ZoneInfo("UTC"))

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO manual.hydration_events
            (consumed_at, beverage_type, volume_oz, notes)
        VALUES (%s, %s, %s, %s)
        """,
        (consumed_at_dt, beverage_type, volume_oz, notes)
    )
    conn.commit()
    cur.close()
    conn.close()

    return RedirectResponse("/hydration", status_code=303)
