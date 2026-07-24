import re



class DoctorValidator:


    def clean(self, value):

        if not value:

            return ""

        return str(value).strip()



    def validate_required_fields(
        self,
        doctor
    ):

        required = [

            "doctor_name",

            "profile_url",

            "hospital_id"

        ]


        missing = []


        for field in required:


            if not self.clean(
                doctor.get(field)
            ):

                missing.append(
                    field
                )


        return missing



    def validate_profile_url(
        self,
        url
    ):

        if not url:

            return False


        return (
            "/doctor/profile/"
            in url.lower()
        )



    def validate_doctor_name(
        self,
        name
    ):


        if not name:

            return False



        return bool(

            re.search(

                r"\bdr\.?\b",

                name,

                re.I

            )

        )



    def remove_duplicates(
        self,
        doctors
    ):


        unique = []

        seen = set()



        for doctor in doctors:


            url = doctor.get(
                "profile_url"
            )



            if url in seen:

                continue



            seen.add(
                url
            )


            unique.append(
                doctor
            )



        return unique



    def validate(
        self,
        doctors
    ):


        valid = []

        invalid = []



        doctors = self.remove_duplicates(
            doctors
        )



        for doctor in doctors:


            issues = []



            missing = (

                self.validate_required_fields(
                    doctor
                )

            )


            if missing:

                issues.extend(
                    missing
                )



            if not self.validate_profile_url(
                doctor.get(
                    "profile_url"
                )
            ):

                issues.append(
                    "invalid_profile_url"
                )



            if not self.validate_doctor_name(
                doctor.get(
                    "doctor_name"
                )
            ):

                issues.append(
                    "invalid_doctor_name"
                )



            if issues:


                invalid.append({

                    "doctor":
                        doctor,

                    "issues":
                        issues

                })


            else:

                valid.append(
                    doctor
                )



        return {


            "valid":
                valid,


            "invalid":
                invalid,


            "statistics": {


                "total_received":
                    len(doctors),


                "valid_records":
                    len(valid),


                "invalid_records":
                    len(invalid)

            }

        }