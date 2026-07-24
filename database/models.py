from sqlalchemy.orm import declarative_base, relationship

from sqlalchemy import (
    Column,
    Integer,
    String,
    Index,
    ForeignKey
)



Base = declarative_base()




# =========================
# Hospital Model
# =========================


class Hospital(Base):

    __tablename__ = "hospitals"


    hospital_id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    hospital_name = Column(
        String,
        index=True
    )


    location = Column(
        String,
        index=True
    )


    address = Column(
        String
    )


    website = Column(
        String
    )



    # Relationship

    doctors = relationship(
        "Doctor",
        back_populates="hospital"
    )






# =========================
# Doctor Model
# =========================


class Doctor(Base):

    __tablename__ = "doctors"



    doctor_id = Column(
        Integer,
        primary_key=True,
        index=True
    )



    hospital_id = Column(
        Integer,
        ForeignKey(
            "hospitals.hospital_id"
        ),
        index=True
    )



    doctor_name = Column(
        String,
        index=True
    )



    designation = Column(
        String
    )



    department = Column(
        String
    )



    speciality = Column(
        String,
        index=True
    )



    qualification = Column(
        String
    )



    experience = Column(
        String
    )



    expertise = Column(
        String
    )



    awards = Column(
        String
    )



    publications = Column(
        String
    )



    languages = Column(
        String
    )



    summary = Column(
        String
    )



    profile_photo = Column(
        String
    )



    profile_url = Column(
        String,
        unique=True
    )



    # Relationship

    hospital = relationship(
        "Hospital",
        back_populates="doctors"
    )





# =========================
# Database Indexes
# =========================


Index(
    "idx_doctor_name",
    Doctor.doctor_name
)


Index(
    "idx_doctor_speciality",
    Doctor.speciality
)


Index(
    "idx_doctor_hospital",
    Doctor.hospital_id
)


Index(
    "idx_hospital_name",
    Hospital.hospital_name
)