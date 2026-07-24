class HospitalCleaner:


    # =========================
    # Text Cleaning
    # =========================

    def clean_text(self, text):

        if not text:

            return ""


        text = str(text)


        text = text.replace(
            "\xa0",
            " "
        )


        text = text.replace(
            "\n",
            " "
        )


        text = " ".join(
            text.split()
        )


        return text.strip()



    # =========================
    # Hospital Name Cleaning
    # =========================

    def clean_name(
            self,
            name
    ):


        name = self.clean_text(
            name
        )


        remove_words = [

            "[Hospital]",

            "[Hospitals]"

        ]


        for word in remove_words:

            name = name.replace(
                word,
                ""
            )


        return name.strip()



    # =========================
    # Website Validation
    # =========================

    def clean_website(
            self,
            website
    ):


        if not website:

            return ""


        website = self.clean_text(
            website
        )


        if website.startswith(
            "http"
        ):

            return website


        return (
            "https://"
            +
            website
        )



    # =========================
    # Duplicate Removal
    # =========================

    def remove_duplicates(
            self,
            hospitals
    ):


        seen = set()

        result = []



        for hospital in hospitals:


            key = hospital.get(
                "hospital_name",
                ""
            ).lower()



            if key in seen:

                continue



            seen.add(
                key
            )


            result.append(
                hospital
            )



        return result



    # =========================
    # Empty Field Handling
    # =========================

    def clean_empty_fields(
            self,
            hospital
    ):


        for key,value in hospital.items():


            if value == "":

                hospital[key] = None



        return hospital



    # =========================
    # Main Cleaner
    # =========================

    def clean_hospitals(
            self,
            hospitals
    ):


        hospitals = self.remove_duplicates(
            hospitals
        )


        cleaned = []



        for hospital in hospitals:


            hospital["hospital_name"] = (
                self.clean_name(
                    hospital.get(
                        "hospital_name"
                    )
                )
            )


            hospital["location"] = (
                self.clean_text(
                    hospital.get(
                        "location"
                    )
                )
            )


            hospital["address"] = (
                self.clean_text(
                    hospital.get(
                        "address"
                    )
                )
            )


            hospital["website"] = (
                self.clean_website(
                    hospital.get(
                        "website"
                    )
                )
            )



            hospital = self.clean_empty_fields(
                hospital
            )



            # Skip invalid hospitals

            if not hospital.get(
                "hospital_name"
            ):

                continue



            cleaned.append(
                hospital
            )



        return cleaned