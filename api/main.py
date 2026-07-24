from fastapi import FastAPI

from api.hospitals import router as hospital_router
from api.doctors import router as doctor_router


app = FastAPI(
    title="MyMedRoads API"
)


app.include_router(
    hospital_router
)

app.include_router(
    doctor_router
)


@app.get("/health")
def health():

    return {
        "status": "healthy",
        "service": "MyMedRoads API"
    }