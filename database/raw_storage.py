import json
import os
from datetime import datetime



DATABASE_PATH = "database"


RAW_PATH = os.path.join(
    DATABASE_PATH,
    "raw"
)


PROCESSED_PATH = os.path.join(
    DATABASE_PATH,
    "processed"
)



def ensure_directories():

    os.makedirs(
        RAW_PATH,
        exist_ok=True
    )


    os.makedirs(
        PROCESSED_PATH,
        exist_ok=True
    )



def save_json(
    folder,
    filename,
    data
):

    ensure_directories()


    file_path = os.path.join(
        folder,
        filename
    )


    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:


        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


    print(
        f"✅ Saved: {file_path}"
    )



def prepare_data(data):

    return {

        "scraped_at":
            datetime.now()
            .isoformat(),


        "total_records":
            len(data),


        "data":
            data
    }



# -------------------------
# RAW DATA
# -------------------------


def save_doctors_raw(doctors):

    save_json(

        RAW_PATH,

        "doctors_raw.json",

        prepare_data(
            doctors
        )

    )



def save_hospitals_raw(hospitals):

    save_json(

        RAW_PATH,

        "hospitals_raw.json",

        prepare_data(
            hospitals
        )

    )



# -------------------------
# PROCESSED DATA
# -------------------------


def save_doctors_processed(doctors):

    save_json(

        PROCESSED_PATH,

        "doctors.json",

        prepare_data(
            doctors
        )

    )



def save_hospitals_processed(hospitals):

    save_json(

        PROCESSED_PATH,

        "hospitals.json",

        prepare_data(
            hospitals
        )

    )