from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse, RedirectResponse
from uvicorn import run as app_run

from typing import Optional

from us_visa.constants import APP_HOST, APP_PORT
from us_visa.pipline.prediction_pipeline import USvisaData, USvisaClassifier
from us_visa.pipline.training_pipeline import TrainPipeline

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory='templates')

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DataForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.CONTINENT: Optional[str] = None
        self.EDUCATION_OF_EMPLOYEE: Optional[str] = None
        self.HAS_JOB_EXPERIENCE: Optional[str] = None
        self.REQUIRES_JOB_TRAINING: Optional[str] = None
        self.NO_OF_EMPLOYEES: Optional[str] = None
        self.COMPANY_AGE: Optional[str] = None
        self.REGION_OF_EMPLOYMENT: Optional[str] = None
        self.PREVAILING_WAGE: Optional[str] = None
        self.UNIT_OF_WAGE: Optional[str] = None
        self.FULL_TIME_POSITION: Optional[str] = None

    async def get_usvisa_data(self):
        form = await self.request.form()
        self.CONTINENT = form.get("continent")
        self.EDUCATION_OF_EMPLOYEE = form.get("education_of_employee")
        self.HAS_JOB_EXPERIENCE = form.get("has_job_experience")
        self.REQUIRES_JOB_TRAINING = form.get("requires_job_training")
        self.NO_OF_EMPLOYEES = form.get("no_of_employees")
        self.COMPANY_AGE = form.get("company_age")
        self.REGION_OF_EMPLOYMENT = form.get("region_of_employment")
        self.PREVAILING_WAGE = form.get("prevailing_wage")
        self.UNIT_OF_WAGE = form.get("unit_of_wage")
        self.FULL_TIME_POSITION = form.get("full_time_position")

@app.get("/", tags=["authentication"])
async def index(request: Request):
    return templates.TemplateResponse(
            "usvisa.html", {"request": request, "context": "Rendering"})

@app.get("/train")
async def trainRouteClient():
    try:
        train_pipeline = TrainPipeline()
        train_pipeline.run_pipeline()
        return Response("Training successful !!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")

@app.post("/")
async def predictRouteClient(request: Request):
    try:
        form = DataForm(request)
        await form.get_usvisa_data()

        usvisa_data = USvisaData(
            CONTINENT=form.CONTINENT,
            EDUCATION_OF_EMPLOYEE=form.EDUCATION_OF_EMPLOYEE,
            HAS_JOB_EXPERIENCE=form.HAS_JOB_EXPERIENCE,
            REQUIRES_JOB_TRAINING=form.REQUIRES_JOB_TRAINING,
            NO_OF_EMPLOYEES=form.NO_OF_EMPLOYEES,
            COMPANY_AGE=form.COMPANY_AGE,
            REGION_OF_EMPLOYMENT=form.REGION_OF_EMPLOYMENT,
            PREVAILING_WAGE=form.PREVAILING_WAGE,
            UNIT_OF_WAGE=form.UNIT_OF_WAGE,
            FULL_TIME_POSITION=form.FULL_TIME_POSITION,
        )

        usvisa_df = usvisa_data.get_usvisa_input_data_frame()

        model_predictor = USvisaClassifier()

        value = model_predictor.predict(dataframe=usvisa_df)[0]

        status = "Visa-approved" if value == 1 else "Visa Not-Approved"

        return templates.TemplateResponse(
            "usvisa.html",
            {"request": request, "context": status},
        )

    except Exception as e:
        return {"status": False, "error": f"{e}"}

if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)
