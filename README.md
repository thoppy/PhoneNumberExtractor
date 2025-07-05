# PhoneNumberExtractor 📞

A Python script that scans `.txt`, `.csv`, `.sql`, and `.xlsx` files in a folder to extract all valid phone numbers and saves them to a CSV.

## ✅ Features

- Detects local and international phone numbers from various formats.
- Supports scanning `.txt`, `.csv`, `.sql`, `.xls`, and `.xlsx` files.
- Removes duplicate entries to provide a unique list of numbers.
- Outputs cleaned phone numbers (digits only) to a CSV file.
- Includes a test suite to verify extraction logic.

## 🔧 Requirements

- Python 3.8+
- pandas
- openpyxl

(These will be installed by `pip install -r requirements.txt`)

## ▶️ How to Use

1.  **Installation**

    Clone the repository or download the files, then navigate to the script's directory in your terminal. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Running the Script for Phone Number Extraction**

    To extract phone numbers from a specific directory, run the script with the directory path as a command-line argument:
    ```bash
    python extract_all_phone_numbers.py /path/to/your/data_directory
    ```
    *   Replace `/path/to/your/data_directory` with the actual path to the folder you want to scan.
    *   If you do not provide a directory path, the script will attempt to use a hardcoded default path (`D:/Your/Folder/Here`), which you would likely need to modify directly in the script if you intend to use it this way.

    **Output:**
    *   By default, the extracted phone numbers will be saved in a CSV file named `All_Phone_Numbers_Only.csv` on your Desktop (`~/Desktop/All_Phone_Numbers_Only.csv`).
    *   You can specify a custom output file path using the `-o` or `--output` argument:
        ```bash
        python extract_all_phone_numbers.py /path/to/your/data_directory -o /custom/path/output_numbers.csv
        ```

3.  **Running Tests**

    The script includes a set of tests to verify its functionality. These tests use sample files located in the `test_data` directory. To run the tests:
    ```bash
    python extract_all_phone_numbers.py --test
    ```
    The script will print the test results to the console, indicating whether they passed or failed and showing any discrepancies if they occur.

## ⚙️ How it Works

The script traverses the specified directory (and its subdirectories) looking for files with `.txt`, `.csv`, `.sql`, `.xls`, or `.xlsx` extensions. It reads the content of these files and uses regular expressions to find potential phone number patterns.

Found numbers are then cleaned (all non-digit characters like `+`, `-`, `(`, `)`, ` ` are removed) and validated based on their length and specific patterns (e.g., 7-digit numbers starting with '555' are excluded based on common test data conventions).

Unique, valid phone numbers are collected and then saved to the specified CSV output file.
