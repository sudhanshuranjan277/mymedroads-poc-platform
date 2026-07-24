from config.config_loader import load_config

from scraper.core.scraper_engine import ScraperEngine



def main():


    print(
        "\n================================"
    )

    print(
        "🚀 MyMedRoads POC Test Runner"
    )

    print(
        "================================"
    )



    # Load Config

    config = load_config()



    print(
        "\nHospital:"
    )

    print(
        config["hospital"]["name"]
    )



    # Start Engine

    engine = ScraperEngine(
        config
    )



    result = engine.run()



    # ==========================
    # OUTPUT SUMMARY
    # ==========================


    print(
        "\n================================"
    )

    print(
        "FINAL RESULT SUMMARY"
    )

    print(
        "================================"
    )



    # ==========================
    # Hospital Output
    # ==========================


    hospitals = result.get(
        "hospital",
        []
    )


    if hospitals:


        print(
            "\n🏥 Hospital:"
        )


        # First hospital display

        print(
            hospitals[0].get(
                "hospital_name",
                "Unknown"
            )
        )


    else:


        print(
            "\n❌ Hospital Data Missing"
        )



    # ==========================
    # Doctor Output
    # ==========================


    print(
        "\n👨‍⚕️ Doctors:"
    )


    print(
        len(
            result.get(
                "doctors",
                []
            )
        )
    )



    print(
        "\n================================"
    )

    print(
        "✅ Pipeline Finished"
    )

    print(
        "================================"
    )





if __name__ == "__main__":

    main()