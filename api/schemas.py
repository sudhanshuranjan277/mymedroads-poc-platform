from pydantic import BaseModel



# =========================
# Hospital Schema
# =========================

class HospitalSchema(BaseModel):

    hospital_id: int

    hospital_name: str | None = None

    location: str | None = None

    address: str | None = None

    website: str | None = None


    class Config:

        from_attributes = True






# =========================
# Doctor Schema
# =========================

class DoctorSchema(BaseModel):

    doctor_id: int


    hospital_id: int | None = None


    doctor_name: str | None = None


    designation: str | None = None


    department: str | None = None


    speciality: str | None = None


    qualification: str | None = None


    experience: str | None = None


    expertise: str | None = None


    awards: str | None = None


    publications: str | None = None


    languages: str | None = None


    summary: str | None = None


    profile_photo: str | None = None


    profile_url: str | None = None



    class Config:

        from_attributes = True