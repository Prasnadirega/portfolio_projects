
## Project Overview

This project focuses on cleaning, validating, and merging student course data stored in an SQLite database. It automates the process of identifying new records, running unit tests to ensure data integrity, and maintaining a changelog of updates.

## Project Files

- `cademycode.db`: Original source database.
- `cleansed_cademycode_data.db`: Destination database with cleaned and merged data.
- `cleansed_cademycode_data.csv`: Flat file version of the cleaned data.
- `Unit_test_code.py`: Main cleaning script with logging and unit tests.
- `bash_script.sh`: Bash automation script to trigger Python cleaning and move updated files.
- `changelog.md`: Tracks changes and versions of updates.

## Cleaning Steps

- Parsed and normalized nested JSON data from `contact_info`.
- Split and extracted address components from `mailing_address`.
- Converted data types for numeric consistency.
- Filled and dropped missing data where appropriate.
- Calculated `age` using `dob` and current timestamp.

## Unit Tests

To ensure data integrity, the following tests were performed:
- Schema Matching: Check that column types are consistent between updates.
- Column Count: Ensure column number doesn’t change unexpectedly.
- Missing Values: Validate that there are no nulls in critical fields.
- Foreign Key Matching: Ensure `career_path_id` and `job_id` match valid lookup tables.

Errors are logged in `cleaned_db.log`.

## Automation

The included `bash_script.sh` automates the execution of the Python cleaning script and moves updated databases to the production directory if the changelog indicates a successful update.

## Versioning

Every update is recorded in `changelog.md` with version number and details about new or missing data entries.

## How to Run

1. Make sure your environment has Python and required packages installed (`pandas`, `numpy`, `sqlite3`).
2. Run the script via terminal:

   ```bash
   bash bash_script.sh
   ```

3. Review logs and changelog to verify success.

## Contact

For questions or improvements, feel free to reach out.
