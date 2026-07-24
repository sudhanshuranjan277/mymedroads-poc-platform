import json
import os
from datetime import datetime



def export_quality_report(
        report,
        output_path="output/quality_report.json"
):


    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )


    data = {

        "generated_at":
            datetime.now().isoformat(),

        "report":
            report

    }



    with open(
        output_path,
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
        f"✅ Report Exported: {output_path}"
    )