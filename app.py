from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from database import get_conn

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/menu", name="menu")
def menu(request: Request):
    return templates.TemplateResponse("index.html", {"request":request})

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
