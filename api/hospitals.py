from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session


from api.database import get_db


from database.models import (
    Hospital,
    Doctor
)


from api.schemas import (
    HospitalSchema,
    DoctorSchema
)



router = APIRouter(

    prefix="/hospitals",

    tags=["Hospitals"]

)





# =========================
# Get All Hospitals
# =========================

@router.get(
    "/",
    response_model=list[HospitalSchema]
)
def get_hospitals(

    db: Session = Depends(get_db)

):

    hospitals = (

        db.query(Hospital)

        .all()

    )


    return hospitals





# =========================
# Get Hospital By ID
# =========================

@router.get(
    "/{hospital_id}",
    response_model=HospitalSchema
)
def get_hospital(

    hospital_id: int,

    db: Session = Depends(get_db)

):

    hospital = (

        db.query(Hospital)

        .filter(

            Hospital.hospital_id == hospital_id

        )

        .first()

    )


    if not hospital:

        raise HTTPException(

            status_code=404,

            detail="Hospital not found"

        )


    return hospital





# =========================
# Get Doctors Of Hospital
# =========================

@router.get(
    "/{hospital_id}/doctors",
    response_model=list[DoctorSchema]
)
def get_hospital_doctors(

    hospital_id: int,

    db: Session = Depends(get_db)

):

    hospital = (

        db.query(Hospital)

        .filter(

            Hospital.hospital_id == hospital_id

        )

        .first()

    )


    if not hospital:

        raise HTTPException(

            status_code=404,

            detail="Hospital not found"

        )


    doctors = (

        db.query(Doctor)

        .filter(

            Doctor.hospital_id == hospital_id

        )

        .all()

    )


    return doctors