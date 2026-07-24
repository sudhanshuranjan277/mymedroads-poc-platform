from scraper.hospitals.artemis import ArtemisHospitalScraper
from scraper.doctor.doctor_engine import DoctorEngine


from database.raw_storage import (
    save_hospitals_raw,
    save_hospitals_processed
)


from quality.hospital_cleaner import HospitalCleaner




class ScraperEngine:


    def __init__(self, config):

        self.config = config



    # =========================
    # Hospital Pipeline
    # =========================

    def run_hospital(self):


        print(
            "\n🏥 Starting Hospital Scraper"
        )



        hospital_scraper = ArtemisHospitalScraper(
            self.config
        )



        hospital_data = hospital_scraper.scrape()



        if not hospital_data:


            print(
                "❌ Hospital data not found"
            )


            return []



        hospitals = [

            hospital_data

        ]



        # Raw Save

        save_hospitals_raw(
            hospitals
        )



        # Cleaning

        cleaner = HospitalCleaner()



        cleaned_hospitals = cleaner.clean_hospitals(
            hospitals
        )



        # Processed Save

        if cleaned_hospitals:


            save_hospitals_processed(
                cleaned_hospitals
            )



        print(

            "🏥 Hospitals Processed:",

            len(cleaned_hospitals)

        )


        return cleaned_hospitals





    # =========================
    # Doctor Pipeline
    # =========================

    def run_doctors(self):


        print(
            "\n👨‍⚕️ Starting Doctor Scraper"
        )



        doctor_engine = DoctorEngine(
            self.config
        )


        doctors = doctor_engine.run()



        return doctors





    # =========================
    # Complete Pipeline
    # =========================

    def run(self):


        print(
            "\n=============================="
        )


        print(
            "🚀 MyMedRoads Scraper Engine"
        )


        print(
            "=============================="
        )



        result = {


            "hospital":

                self.run_hospital(),



            "doctors":

                self.run_doctors()

        }



        print(
            "\n✅ Scraping Completed"
        )



        return result