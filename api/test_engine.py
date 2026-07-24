import json

from scraper.core.scraper_engine import ScraperEngine


def load_hospitals():

    with open(
        "config/hospitals.json",
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)



def main():

    hospitals = load_hospitals()


    config = {
        "request_timeout": 30,
        "user_agent": "Mozilla/5.0"
    }


    engine = ScraperEngine(
        config
    )


    result = engine.run(
        hospitals
    )


    print("\n========== RESULT ==========")

    for item in result:
        print(item)



if __name__ == "__main__":
    main()