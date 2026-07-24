import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from scraper.core.base_scraper import BaseScraper



class DoctorListingScraper(BaseScraper):


    def __init__(self, config):

        super().__init__(config)


        self.base_url = self.config.get(
            "base_url",
            "https://www.artemishospitals.com"
        )


        self.api_url = (
            self.base_url
            +
            "/common.aspx/AllDoctorsAndSpecialityListForIndex"
        )



    def clean_text(self, text):

        if not text:

            return ""


        return " ".join(
            text.replace(
                "\xa0",
                " "
            )
            .replace(
                "\n",
                " "
            )
            .split()
        )



    def get_hospital_details(self):

        hospital = self.config.get(
            "hospital",
            {}
        )


        return (

            hospital.get(
                "id"
            ),

            hospital.get(
                "name"
            )

        )



    def is_valid_doctor(
        self,
        profile_url,
        doctor_name
    ):


        blocked_keywords = [

            "raipur",

            "procedure",

            "department",

            "speciality",

            "specialty",

            "treatment"

        ]


        check_text = (

            profile_url
            +
            " "
            +
            doctor_name

        ).lower()



        for word in blocked_keywords:


            if word in check_text:

                return False



        return True



    def scrape(self):


        print(
            "\n👨‍⚕️ Fetching Doctors From Artemis API"
        )


        headers = {


            "Content-Type":

                "application/json; charset=utf-8",



            "User-Agent":

                self.config
                .get(
                    "request",
                    {}
                )
                .get(
                    "user_agent",
                    "Mozilla/5.0"
                )

        }



        payload = {

            "prefix": ""

        }



        try:


            response = requests.post(

                self.api_url,

                headers=headers,

                json=payload,

                timeout=self.config
                .get(
                    "request",
                    {}
                )
                .get(
                    "timeout",
                    30
                )

            )


            response.raise_for_status()



        except Exception as e:


            print(
                "❌ Doctor API Error:",
                e
            )


            return []



        try:


            data = response.json()



        except Exception as e:


            print(
                "❌ JSON Parsing Error:",
                e
            )


            return []



        doctors_html = data.get(
            "d",
            []
        )



        print(
            "API Records:",
            len(doctors_html)
        )



        doctors = []

        seen_urls = set()



        hospital_id, hospital_name = (
            self.get_hospital_details()
        )



        doctor_id = 1



        for item in doctors_html:



            soup = BeautifulSoup(

                item,

                "html.parser"

            )



            anchor = soup.find(
                "a",
                href=True
            )



            if not anchor:

                continue



            href = anchor.get(
                "href"
            )



            if not href:

                continue



            if "/doctor/profile/" not in href.lower():

                continue



            profile_url = urljoin(

                self.base_url,

                href

            )



            profile_url = profile_url.strip()



            doctor_name = self.clean_text(

                anchor.get_text(
                    " ",
                    strip=True
                )

            )



            doctor_name = (

                doctor_name
                .replace(
                    "[Doctor]",
                    ""
                )
                .strip()

            )



            if not doctor_name:

                continue



            # Must start with Dr

            if not doctor_name.lower().startswith(
                (
                    "dr.",
                    "dr "
                )
            ):

                continue



            # Remove unwanted doctors

            if not self.is_valid_doctor(

                profile_url,

                doctor_name

            ):

                continue



            # Remove duplicates

            if profile_url in seen_urls:

                continue



            seen_urls.add(
                profile_url
            )



            doctors.append({

                "doctor_id":

                    doctor_id,


                "hospital_id":

                    hospital_id,


                "hospital_name":

                    hospital_name,


                "doctor_name":

                    doctor_name,


                "specialty":

                    "",


                "profile_url":

                    profile_url

            })



            doctor_id += 1



        print(
            "Total doctors extracted:",
            len(doctors)
        )


        return doctors