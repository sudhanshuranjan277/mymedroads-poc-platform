import json
import re

from bs4 import BeautifulSoup

from scraper.core.base_scraper import BaseScraper



class ArtemisHospitalScraper(BaseScraper):


    def __init__(self, config):

        super().__init__(config)

        self.base_url = config.get(
            "base_url"
        )



    def clean(self, text):

        if not text:

            return ""


        return " ".join(
            str(text)
            .replace(
                "\xa0",
                " "
            )
            .split()
        )



    def extract_jsonld(self, soup):

        data = {}


        for script in soup.find_all(
            "script",
            type="application/ld+json"
        ):


            try:

                obj = json.loads(
                    script.get_text(
                        strip=True
                    )
                )


            except Exception:

                continue



            items = (

                obj
                if isinstance(
                    obj,
                    list
                )
                else
                [obj]

            )



            for item in items:


                if not isinstance(
                    item,
                    dict
                ):

                    continue



                obj_type = item.get(
                    "@type",
                    ""
                )



                if isinstance(
                    obj_type,
                    list
                ):

                    obj_type = ",".join(
                        obj_type
                    )



                if not any(

                    x in obj_type

                    for x in [

                        "Hospital",
                        "MedicalOrganization",
                        "Organization"

                    ]

                ):

                    continue



                name = self.clean(
                    item.get(
                        "name",
                        ""
                    )
                )


                if not name:

                    continue



                # remove Raipur

                if "raipur" in name.lower():

                    continue



                if "artemis" not in name.lower():

                    continue



                data["hospital_name"] = "Artemis Hospitals"


                data["website"] = self.clean(
                    item.get(
                        "url",
                        self.base_url
                    )
                )


                data["overview"] = self.clean(
                    item.get(
                        "description",
                        ""
                    )
                )


                data["contact_details"] = self.clean(
                    item.get(
                        "telephone",
                        ""
                    )
                )


                address = item.get(
                    "address",
                    {}
                )


                if isinstance(
                    address,
                    dict
                ):


                    data["address"] = self.clean(

                        f"""

                        {address.get('streetAddress','')}

                        {address.get('addressLocality','')}

                        {address.get('addressRegion','')}

                        {address.get('postalCode','')}

                        """

                    )



        return data



    def extract_contact_details(self, soup):

        text = soup.get_text(
            " ",
            strip=True
        )


        contacts = []


        phones = re.findall(
            r"(?:\+91[-\s]?)?\d{10}",
            text
        )


        contacts.extend(
            phones
        )


        emails = re.findall(

            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",

            text

        )


        contacts.extend(
            emails
        )


        return ", ".join(
            list(
                set(
                    contacts
                )
            )
        )



    def extract_accreditations(self, soup):

        text = soup.get_text(
            " ",
            strip=True
        ).lower()


        result = []


        mapping = {

            "nabh":
                "NABH Accreditation",

            "jci":
                "JCI Accreditation",

            "nabl":
                "NABL Certification",

            "iso":
                "ISO Certification"

        }


        for key,value in mapping.items():

            if key in text:

                result.append(
                    value
                )



        return ", ".join(
            result
        )



    def extract_number_of_beds(self, text):

        patterns = [

            r"\d+\+?\s*beds",

            r"\d+\+?\s*bedded",

            r"capacity\s+of\s+\d+"

        ]


        for pattern in patterns:


            match = re.search(
                pattern,
                text,
                re.I
            )


            if match:

                return self.clean(
                    match.group()
                )


        return ""



    def extract_awards(self, soup):

        text = soup.get_text(
            "\n",
            strip=True
        )


        awards = []


        keywords = [

            "award",

            "awarded",

            "achievement",

            "recognition",

            "ranked"

        ]


        for line in text.split("\n"):


            line = self.clean(
                line
            )


            if not line:

                continue



            if "raipur" in line.lower():

                continue



            if "shanti" in line.lower():

                continue



            if any(

                word in line.lower()

                for word in keywords

            ):


                if len(line) > 25:

                    awards.append(
                        line
                    )



        return ", ".join(
            list(
                set(
                    awards[:10]
                )
            )
        )



    def scrape(self):


        print(
            "🏥 Running Artemis Hospital Scraper"
        )


        html = self.fetch(
            self.base_url
        )


        if not html:

            return None



        soup = BeautifulSoup(

            html,

            "html.parser"

        )


        text = self.clean(
            soup.get_text(
                " "
            )
        )



        hospital = {


            "hospital_id":

                self.config["hospital"]["id"],


            "hospital_name": "Artemis Hospitals",



            "location":

                "Gurgaon, Haryana",


            "address":

                "",


            "contact_details":

                "",


            "website":

                self.base_url,


            "overview":

                "",


            "accreditations":

                "",


            "number_of_beds":

                "",


            "awards":

                "",


            "images":

                "",

        }



        json_data = self.extract_jsonld(
            soup
        )


        hospital.update(
            json_data
        )



        if not hospital["address"]:

            hospital["address"] = (

                "Artemis Hospitals, "
                "Sector 51, "
                "Gurugram, Haryana, India"

            )



        if not hospital["contact_details"]:

            hospital["contact_details"] = (
                self.extract_contact_details(
                    soup
                )
            )



        hospital["accreditations"] = (
            self.extract_accreditations(
                soup
            )
        )


        hospital["number_of_beds"] = (
            self.extract_number_of_beds(
                text
            )
        )


        hospital["awards"] = (
            self.extract_awards(
                soup
            )
        )



        return hospital