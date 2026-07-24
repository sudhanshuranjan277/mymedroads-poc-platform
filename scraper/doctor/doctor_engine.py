from database.raw_storage import save_doctors_processed, save_doctors_raw
from exporter.csv_export import export_doctors_csv
from exporter.report_exporter import export_quality_report
from exporter.sql_export import export_doctors_sql
from quality.doctor_cleaner import DoctorCleaner
from quality.doctor_validator import DoctorValidator
from quality.quality_report import generate_quality_report
from scraper.doctor.listing import DoctorListingScraper
from scraper.doctor.profile import DoctorProfileScraper


class DoctorEngine:
    def __init__(self, config):
        self.config = config

    def run(self):
        print("\nðŸ‘¨â€âš•ï¸ Starting Doctor Pipeline")

        # =========================
        # Doctor Listing
        # =========================
        listing_scraper = DoctorListingScraper(self.config)
        doctors = listing_scraper.scrape()

        print(f"\nðŸ“‹ Doctors Found: {len(doctors)}")

        if not doctors:
            print("âŒ No doctors found")
            return []

        # Save Raw Listing
        save_doctors_raw(doctors)

        # =========================
        # Profile Extraction
        # =========================
        profile_scraper = DoctorProfileScraper(self.config)
        final_doctors = []
        failed_profiles = []
        total = len(doctors)

        for index, doctor in enumerate(doctors, start=1):
            try:
                print(f"[{index}/{total}] {doctor.get('doctor_name')}")
                data = profile_scraper.scrape(doctor)

                if data:
                    final_doctors.append(data)
                else:
                    failed_profiles.append(doctor.get("doctor_name"))
            except Exception as error:
                print("âŒ Profile Failed:", doctor.get("doctor_name"))
                print(error)
                failed_profiles.append(doctor.get("doctor_name"))

        print("\nProfiles Extracted:", len(final_doctors))
        print("Profiles Failed:", len(failed_profiles))

        # =========================
        # Validation
        # =========================
        validator = DoctorValidator()
        validation_result = validator.validate(final_doctors)
        valid_doctors = validation_result.get("valid", [])

        cleaner = DoctorCleaner()
        valid_doctors = cleaner.clean_doctors(valid_doctors)
        quality_report = generate_quality_report(valid_doctors)

        print("\n========== VALIDATION REPORT ==========")
        print(validation_result.get("statistics"))
        print("========================================")

        # =========================
        # Save Processed Data
        # =========================
        if valid_doctors:
            save_doctors_processed(valid_doctors)

            # =========================
            # Export Layer
            # =========================
            export_doctors_csv(valid_doctors)
            export_doctors_sql(valid_doctors)
            export_quality_report(validation_result)
        else:
            print("âš ï¸ No valid doctors to save")

        return valid_doctors
