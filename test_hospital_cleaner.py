import json
import os

from quality.hospital_cleaner import HospitalCleaner



FILE = "database/processed/hospitals.json"



if not os.path.exists(FILE):

    print("❌ Hospital file not found")

    exit()



with open(
    FILE,
    encoding="utf-8"
) as f:


    content = f.read().strip()



    if not content:

        print(
            "⚠️ hospitals.json is empty"
        )

        exit()



    data = json.loads(
        content
    )



hospitals = data.get(
    "data",
    []
)



cleaner = HospitalCleaner()



result = cleaner.clean_hospitals(
    hospitals
)



print(
    json.dumps(
        result,
        indent=4,
        ensure_ascii=False
    )
)