MyMedRoads POC Platform - Architecture V2
1. High Level Architecture
                         CONFIGURATION LAYER

                         hospitals.json
                         scraper_config.json

                                  |
                                  |
                                  ↓


                         SCRAPING FRAMEWORK

              +--------------------------------+
              |                                |
              |        Scraper Engine          |
              |                                |
              +--------------------------------+

                    |                  |
                    |                  |

                    ↓                  ↓

          Hospital Adapters       Doctor Scrapers

          Artemis Adapter         Doctor Listing
          Apollo Adapter          Doctor Profile
          Fortis Adapter


                    |
                    |
                    ↓


                 DATA PROCESSING LAYER


          +-----------------------------+
          |                             |
          |       Data Cleaner          |
          |       Normalizer            |
          |       Transformer           |
          |                             |
          +-----------------------------+


                    |
                    |
                    ↓


                 DATA QUALITY LAYER


          +-----------------------------+
          |                             |
          | Validation Engine           |
          | Duplicate Detection         |
          | Completeness Checker        |
          |                             |
          +-----------------------------+


                    |
                    |
                    ↓


                    ETL PIPELINE


              Extract → Transform → Load


                    |
                    |
                    ↓


                 STORAGE LAYER


        +-------------+-------------+
        |             |             |
        ↓             ↓             ↓

       CSV          JSON       PostgreSQL


                    |
                    |
                    ↓


                  API LAYER


                 FastAPI Backend


                    |
                    |
                    ↓


              APPLICATION LAYER


              Dashboard / Portal

2. Layer Explanation
1. Configuration Layer

Purpose:

New hospital add karne ke liye code change na karna pade.

Structure:

config/

├── hospitals.json
├── scraper_config.json
└── settings.py


Example:

{
 "hospital_name": "Artemis Hospitals",
 "website": "https://www.artemishospitals.com",
 "adapter": "artemis"
}

Future:

{
 "hospital_name": "Apollo Hospitals",
 "adapter": "apollo"
}
2. Scraping Framework

Current:

hospital_scraper.py
doctor_scraper.py

Upgrade:

scraper/

├── core/
│
│   ├── base_scraper.py
│   └── scraper_engine.py
│
├── hospitals/
│
│   ├── artemis.py
│   ├── apollo.py
│   └── fortis.py
│
└── doctor/

    ├── listing.py
    └── profile.py

Responsibility:
Base Scraper

Common functionality:

Request handling
Headers
Error handling
Logging
Hospital Adapter

Hospital-specific parsing.

Example:

Artemis HTML
      |
      |
Artemis Adapter
      |
      |
Standard Hospital Object

3. Data Processing Layer

Folder:

processing/

├── cleaner.py
├── normalizer.py
└── transformer.py


Responsibilities:

Cleaner
Remove HTML
Remove unwanted spaces
Remove special characters
Normalizer

Convert:

M.B.B.S.,MBBS

↓

MBBS

Transformer

Convert scraped data into database format.

4. Data Quality Layer

Folder:

quality/

├── validator.py
├── duplicate_checker.py
└── completeness.py


Checks:

Validation

Example:

Doctor name exists?
Profile URL exists?
Hospital mapped?

Duplicate Detection

Example:

Dr. Amit Kumar
Dr. Amit Kumar

Duplicate Found

Completeness

Output:

Qualification : 100%

Experience    : 84%

Membership    : 78%

5. ETL Pipeline

Folder:

etl/

├── extract.py
├── transform.py
└── load.py


Flow:

Website

 ↓

Extract

 ↓

Clean

 ↓

Validate

 ↓

Transform

 ↓

Load Database

6. Database Layer

Folder:

database/

├── connection.py
├── models.py
└── schema.sql


Database:

PostgreSQL

Tables:

hospitals
hospital_id
hospital_name
address
website
contact

doctors
doctor_id
hospital_id
doctor_name
specialty
qualification
experience


Relationship:

Hospital

    |

    | 1:N

    |

Doctors

7. API Layer

Folder:

api/

├── main.py

└── routes/

    ├── doctors.py
    └── hospitals.py


Endpoints:

GET /hospitals


GET /doctors


GET /doctors/{id}


GET /hospitals/{id}

8. Dashboard Layer

Folder:

dashboard/

└── app.py


Dashboard Metrics:

Total Hospitals

Total Doctors

Duplicate Records

Missing Fields

Data Completeness %

Validation Status

9. Testing Layer

Folder:

tests/

├── test_scraper.py
├── test_validation.py
└── test_etl.py


Testing:

Scraper output
Validation rules
ETL pipeline
10. Final Production Structure
mymedroads-poc-platform


│
├── config
│
├── scraper
│
├── processing
│
├── quality
│
├── etl
│
├── database
│
├── api
│
├── dashboard
│
├── tests
│
├── exporter
│
├── models
│
├── docs
│
├── main.py
│
├── validation.py
│
├── requirements.txt
│
└── README.md

Development Order

Ab coding isi order me karenge:

Phase 1
Configuration Driven Scraper

Files:

config/hospitals.json

scraper/core/base_scraper.py

scraper/core/scraper_engine.py


Goal:

Add new hospital only by config change
Phase 2
Data Processing
Phase 3
Quality Dashboard
Phase 4
ETL + Database
Phase 5
FastAPI
Phase 6
Testing + Docker