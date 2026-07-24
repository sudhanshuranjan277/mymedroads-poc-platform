from exporter.csv_export import (
    export_doctors_csv,
    export_hospitals_csv
)

from exporter.sql_export import (
    export_doctors_sql,
    export_hospitals_sql
)



def main():


    print(
        "📦 Starting Export"
    )


    export_doctors_csv()

    export_hospitals_csv()


    export_doctors_sql()

    export_hospitals_sql()



    print(
        "✅ Export Completed"
    )



if __name__ == "__main__":

    main()