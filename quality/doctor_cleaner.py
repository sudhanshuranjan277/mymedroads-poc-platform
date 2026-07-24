import re


class DoctorCleaner:
    # =========================
    # Basic Text Cleaning
    # =========================
    def clean_text(self, text):
        if not text:
            return ""

        text = str(text)
        for item in ("\xa0", "\n", "\t"):
            text = text.replace(item, " ")

        return " ".join(text.split()).strip()

    # =========================
    # Doctor Name Cleaning
    # =========================
    def clean_name(self, name):
        return self.clean_text(name).replace("[Doctor]", "").strip()

    # =========================
    # Experience
    # =========================
    def normalize_experience(self, experience):
        if not experience:
            return ""

        match = re.search(r"(\d+\+?)\s*(years?|yrs?)", experience, re.I)
        if match:
            return f"{match.group(1)} years"

        return self.clean_text(experience)

    # =========================
    # Publication Cleaning
    # =========================
    def clean_publications(self, text):
        if not text:
            return ""

        text = self.clean_text(text)

        # Remove website noise.
        noise = [
            "Quick links",
            "About Us",
            "Privacy Policy",
            "Terms of Use",
            "Book Appointment",
            "Contact Us",
        ]
        for word in noise:
            if word in text:
                text = text.split(word)[0]

        # Remove starting words.
        text = re.sub(r"^(like|such as)\s+", "", text, flags=re.I)

        # Stop after publication ending words.
        if " etc." in text:
            text = text.split(" etc.")[0] + " etc."

        return text.strip()

    # =========================
    # Award Extraction
    # =========================
    def clean_awards(self, text):
        if not text:
            return ""

        text = self.clean_text(text)
        matches = re.findall(r"([^.]*Award[^.]*)", text, re.I)

        if matches:
            return " | ".join(matches).strip()

        return ""

    # =========================
    # Empty Field Normalization
    # =========================
    def clean_empty_fields(self, doctor):
        for key, value in doctor.items():
            if value == "":
                doctor[key] = None

        return doctor

    # =========================
    # URL Validation
    # =========================
    def validate_profile_url(self, url):
        return bool(url and "doctor/profile" in url.lower())

    # =========================
    # Duplicate Removal
    # =========================
    def remove_duplicates(self, doctors):
        seen = set()
        cleaned = []

        for doctor in doctors:
            key = doctor.get("profile_url", "") or doctor.get(
                "doctor_name", ""
            ).lower()
            if key in seen:
                continue

            seen.add(key)
            cleaned.append(doctor)

        return cleaned

    # =========================
    # Main Cleaner
    # =========================
    def clean_doctors(self, doctors):
        doctors = self.remove_duplicates(doctors)
        final = []

        for doctor in doctors:
            if not self.validate_profile_url(doctor.get("profile_url")):
                continue

            for key, value in doctor.items():
                if isinstance(value, str):
                    doctor[key] = self.clean_text(value)

            doctor["doctor_name"] = self.clean_name(doctor.get("doctor_name"))
            doctor["experience"] = self.normalize_experience(doctor.get("experience"))
            doctor["publications"] = self.clean_publications(
                doctor.get("publications")
            )
            doctor["awards"] = self.clean_awards(doctor.get("awards"))
            doctor = self.clean_empty_fields(doctor)
            final.append(doctor)

        return final
