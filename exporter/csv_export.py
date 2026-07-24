import csv
import os



def export_doctors_csv(
        doctors,
        output_path="output/doctors.csv"
):


    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )


    if not doctors:

        print(
            "No doctors available for CSV"
        )

        return



    fields = doctors[0].keys()



    with open(
        output_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:


        writer = csv.DictWriter(
            file,
            fieldnames=fields
        )


        writer.writeheader()


        writer.writerows(
            doctors
        )



    print(
        f"✅ CSV Exported: {output_path}"
    )