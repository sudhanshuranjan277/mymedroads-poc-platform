from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from api.database import get_db

from database.models import Doctor

from api.schemas import DoctorSchema



router = APIRouter(

    prefix="/doctors",

    tags=["Doctors"]

)





# =========================
# Get All Doctors
# Pagination
# =========================


@router.get(
    "/",
    response_model=list[DoctorSchema]
)
def get_doctors(

    page: int = 1,

    limit: int = 20,

    db: Session = Depends(get_db)

):


    offset = (

        page - 1

    ) * limit



    doctors = (

        db.query(Doctor)

        .offset(offset)

        .limit(limit)

        .all()

    )


    return doctors





# =========================
# Advanced Doctor Search
# =========================


@router.get(
    "/search",
    response_model=list[DoctorSchema]
)
def advanced_search(

    name: str | None = None,

    speciality: str | None = None,

    hospital_id: int | None = None,

    experience: str | None = None,

    page: int = 1,

    limit: int = 20,

    db: Session = Depends(get_db)

):


    query = db.query(
        Doctor
    )



    # Name Filter

    if name:


        query = query.filter(

            Doctor.doctor_name.ilike(
                f"%{name}%"
            )

        )



    # Speciality Filter

    if speciality:


        query = query.filter(

            Doctor.speciality.ilike(
                f"%{speciality}%"
            )

        )



    # Hospital Filter

    if hospital_id:


        query = query.filter(

            Doctor.hospital_id == hospital_id

        )



    # Experience Filter

    if experience:


        query = query.filter(

            Doctor.experience.ilike(
                f"%{experience}%"
            )

        )



    doctors = (

        query

        .offset(
            (page - 1) * limit
        )

        .limit(
            limit
        )

        .all()

    )


    return doctors





# =========================
# Filter By Speciality
# =========================


@router.get(
    "/speciality/{speciality}",
    response_model=list[DoctorSchema]
)
def get_by_speciality(

    speciality: str,

    db: Session = Depends(get_db)

):


    doctors = (

        db.query(Doctor)

        .filter(

            Doctor.speciality.ilike(
                f"%{speciality}%"
            )

        )

        .all()

    )


    return doctors





# =========================
# Filter By Hospital
# =========================


@router.get(
    "/hospital/{hospital_id}",
    response_model=list[DoctorSchema]
)
def get_by_hospital(

    hospital_id: int,

    db: Session = Depends(get_db)

):


    doctors = (

        db.query(Doctor)

        .filter(

            Doctor.hospital_id == hospital_id

        )

        .all()

    )


    return doctors





# =========================
# Get Doctor By ID
# =========================


@router.get(
    "/{doctor_id}",
    response_model=DoctorSchema
)
def get_doctor(

    doctor_id: int,

    db: Session = Depends(get_db)

):


    doctor = (

        db.query(Doctor)

        .filter(

            Doctor.doctor_id == doctor_id

        )

        .first()

    )


    if not doctor:


        raise HTTPException(

            status_code=404,

            detail="Doctor not found"

        )


    return doctor