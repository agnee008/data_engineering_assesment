# Hello Fresh BI Assessment

This Python script fetches recipes from a provided URL, extracts chili recipes from the fetched data, and analyzes them to determine their difficulty level based on preparation and cooking times. It saves the extracted chili recipes to a CSV file and calculates the average total time for each difficulty level.

## Instructions

### Running the Script

1. Navigate to the directory where the script is located.

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the main script:

    ```bash
    python /hf_bi_python_excercise/main.py
    ```

4. After running the script, you will find the output CSV files in the `output_data` directory.

### Running the Test Cases

1. Make sure all the dependent libraries are installed first.

2. Run the unit tests:

    ```bash
    python tests/unit_test.py
    ```

3. The test results will be displayed in the terminal, indicating whether the tests passed or failed.

## Dependencies

- requests
- json
