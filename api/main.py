from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.hospitals import router as hospital_router
from api.doctors import router as doctor_router


app = FastAPI(
    title="MyMedRoads API"
)


# CORS Configuration
app.add_middleware(

    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)



# API Routers

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



@app.get("/")
def root():

    return {
        "message": "Welcome to MyMedRoads API",
        "docs": "/docs",
        "health": "/health"
    }