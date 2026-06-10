import sys
import os
from datetime import datetime

# Add scripts folder to path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from extract import extract
from load_staging import load_staging
from transform import transform
from export import export


def run_pipeline():
    start_time = datetime.now()
    print(f"\n{'='*50}")
    print(f"ETL Pipeline started at {start_time}")
    print(f"{'='*50}\n")

    try:
        # Step 1 — Extract from API
        print("--- STEP 1: EXTRACT ---")
        data = extract()
        if data is None:
            print("Extraction failed. Aborting pipeline.")
            return

        # Step 2 — Load raw data into staging
        print("\n--- STEP 2: LOAD STAGING ---")
        load_staging(data)

        # Step 3 — Transform into warehouse
        print("\n--- STEP 3: TRANSFORM ---")
        transform()

        # Step 4 — Export CSVs for Power BI
        print("\n--- STEP 4: EXPORT ---")
        export()

        end_time = datetime.now()
        duration = (end_time - start_time).seconds

        print(f"\n{'='*50}")
        print(f"Pipeline completed successfully.")
        print(f"Duration: {duration} seconds")
        print(f"{'='*50}\n")

    except Exception as e:
        print(f"\nPipeline failed with error: {e}")
        raise


if __name__ == "__main__":
    run_pipeline()