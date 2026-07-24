import os



def escape(value):

    if value is None:

        return ""

    return str(value).replace(
        "'",
        "''"
    )





def export_doctors_sql(
        doctors,
        output_path="output/doctors.sql"
):


    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )



    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:


        file.write(
            "CREATE TABLE IF NOT EXISTS doctors (\n"
        )

        file.write(
            "doctor_id INT,\n"
        )

        file.write(
            "hospital_id INT,\n"
        )

        file.write(
            "doctor_name TEXT,\n"
        )

        file.write(
            "specialty TEXT,\n"
        )

        file.write(
            "qualification TEXT,\n"
        )

        file.write(
            "experience TEXT,\n"
        )

        file.write(
            "profile_url TEXT\n"
        )

        file.write(
            ");\n\n"
        )



        for doctor in doctors:


            query = f"""
INSERT INTO doctors VALUES(
{doctor.get('doctor_id')},
{doctor.get('hospital_id')},
'{escape(doctor.get('doctor_name'))}',
'{escape(doctor.get('specialty'))}',
'{escape(doctor.get('qualification'))}',
'{escape(doctor.get('experience'))}',
'{escape(doctor.get('profile_url'))}'
);

"""


            file.write(query)



    print(
        f"✅ SQL Exported: {output_path}"
    )