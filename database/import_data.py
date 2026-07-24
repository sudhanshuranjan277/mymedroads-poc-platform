import json
import os

from sqlalchemy.orm import sessionmaker

from database.database import engine
from database.models import Doctor, Hospital



SessionLocal = sessionmaker(
    bind=engine
)



DOCTOR_FILE = (
    "database/processed/doctors.json"
)


HOSPITAL_FILE = (
    "database/processed/hospitals.json"
)




# ==========================
# JSON Loader
# ==========================

def load_json(path):

    try:

        if not os.path.exists(path):

            print(
                f"⚠️ File not found: {path}"
            )

            return {}


        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:


            content = file.read().strip()



            if not content:

                print(
                    f"⚠️ Empty file: {path}"
                )

                return {}



            return json.loads(
                content
            )



    except json.JSONDecodeError:


        print(
            f"⚠️ Invalid JSON file: {path}"
        )

        return {}





# ==========================
# Hospital Import
# ==========================

def import_hospitals(session):


    data = load_json(
        HOSPITAL_FILE
    )


    if not data:

        print(
            "⚠️ No hospital data available"
        )

        return 0



    if isinstance(
        data,
        dict
    ):

        hospitals = data.get(
            "data",
            []
        )

    else:

        hospitals = data



    count = 0



    for item in hospitals:


        hospital = Hospital(


            hospital_id=item.get(
                "hospital_id",
                item.get(
                    "id"
                )
            ),


            hospital_name=item.get(
                "hospital_name",
                item.get(
                    "name",
                    ""
                )
            ),


            location=item.get(
                "location",
                ""
            ),


            address=item.get(
                "address",
                ""
            ),


            website=item.get(
                "website",
                ""
            )

        )


        session.merge(
            hospital
        )


        count += 1



    session.commit()



    print(
        f"✅ Hospitals Imported: {count}"
    )


    return count





# ==========================
# Doctor Import
# ==========================

def import_doctors(session):


    data = load_json(
        DOCTOR_FILE
    )



    if not data:

        print(
            "⚠️ No doctor data available"
        )

        return 0



    doctors = data.get(
        "data",
        []
    )



    count = 0



    for item in doctors:



        doctor = Doctor(


            doctor_id=item.get(
                "doctor_id"
            ),


            hospital_id=item.get(
                "hospital_id"
            ),


            doctor_name=item.get(
                "doctor_name"
            ),


            speciality=item.get(
                "specialty"
            ),


            qualification=item.get(
                "qualification"
            ),


            experience=item.get(
                "experience"
            ),


            profile_url=item.get(
                "profile_url"
            )

        )


        session.merge(
            doctor
        )


        count += 1



    session.commit()



    print(
        f"✅ Doctors Imported: {count}"
    )


    return count





# ==========================
# Main
# ==========================

def main():


    print(
        "\n🚀 Starting Database Import"
    )



    session = SessionLocal()



    try:


        import_hospitals(
            session
        )


        import_doctors(
            session
        )



        print(
            "\n✅ Database Import Completed"
        )



    except Exception as e:


        session.rollback()


        print(
            "❌ Import Failed:",
            e
        )


    finally:


        session.close()





if __name__ == "__main__":

    main()