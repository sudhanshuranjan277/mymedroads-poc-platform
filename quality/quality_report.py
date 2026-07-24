import json



def generate_quality_report(
        doctors
):


    total = len(
        doctors
    )


    fields = [

        "doctor_name",
        "specialty",
        "qualification",
        "experience",
        "expertise",
        "profile_photo",
        "summary"

    ]


    report = {

        "total_records":
            total,

        "field_coverage": {}

    }



    for field in fields:


        count = 0


        for doctor in doctors:


            if doctor.get(field):

                count += 1



        report["field_coverage"][field] = {

            "available":
                count,

            "missing":
                total-count

        }


    return report