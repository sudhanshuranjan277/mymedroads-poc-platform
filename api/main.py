from fastapi import FastAPI

from api.doctors import router as doctor_router
from api.hospitals import router as hospital_router



app = FastAPI(

    title="MyMedRoads API",

    version="1.0"

)



# Routers

app.include_router(
    doctor_router
)


app.include_router(
    hospital_router
)





# =========================
# Root Endpoint
# =========================

@app.get("/")
def home():

    return {

        "message": "MyMedRoads API Running"

    }





# =========================
# Health Check
# =========================

@app.get("/health")
def health():

    return {

        "status": "healthy",

        "service": "MyMedRoads API"

    }