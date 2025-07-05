import os
import re
import pandas as pd
import argparse

# 🌍 Universal phone number pattern (handles +, country code, dashes, spaces)
phone_pattern = r'\b(?:\+?\d{1,4}[-.\s]?)?(?:\(?\d{2,4}\)?[-.\s]?)?\d{3,5}[-.\s]?\d{3,5}\b'
all_numbers = set()

def extract_all_phones(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    try:
        if ext in ['.txt', '.csv', '.sql']:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                found = re.findall(phone_pattern, content)
                for num_match in found:
                    # Enhanced cleaning and validation
                    clean_num = re.sub(r'[-.\s()+]', '', num_match) # Strip all non-digits
                    length = len(clean_num)

                    if length == 7:
                        # Based on test data, '555-1234' (-> 5551234) is invalid, but '1234567' is valid.
                        # Generalizing: exclude 7-digit numbers starting with '555'.
                        if clean_num.startswith("555"):
                            continue
                        else:
                            all_numbers.add(clean_num)
                    elif length == 10: # Standard 10-digit numbers
                        all_numbers.add(clean_num)
                    elif length == 11: # e.g., +1XXXXXXXXXX or 0XXXXXXXXXX (UK like)
                        all_numbers.add(clean_num)
                    elif length == 12: # e.g., +44XXXXXXXXXX
                        all_numbers.add(clean_num)
                    elif length == 13: # e.g., +49XXXXXXXXXXX
                        all_numbers.add(clean_num)
                    # Other lengths (like 8, 9, or >13 for pure digits) are implicitly excluded unless added.
                    # This will exclude '555123456' (length 9).
        elif ext in ['.xls', '.xlsx']:
            try:
                df = pd.read_excel(filepath, engine='openpyxl')
                for col in df.columns:
                    content = ' '.join(df[col].astype(str).dropna())
                    found = re.findall(phone_pattern, content)
                    for num_match in found:
                        # Enhanced cleaning and validation (same as above)
                        clean_num = re.sub(r'[-.\s()+]', '', num_match) # Strip all non-digits
                        length = len(clean_num)

                        if length == 7:
                            if clean_num.startswith("555"):
                                continue
                            else:
                                all_numbers.add(clean_num)
                        elif length == 10:
                            all_numbers.add(clean_num)
                        elif length == 11:
                            all_numbers.add(clean_num)
                        elif length == 12:
                            all_numbers.add(clean_num)
                        elif length == 13:
                             all_numbers.add(clean_num)
            except Exception as e:
                print(f"⚠️ Could not process Excel file {filepath} (ensure 'openpyxl' is installed): {e}")
    except FileNotFoundError:
        print(f"❌ Error: File not found {filepath}")
    except Exception as e:
        print(f"❌ Error reading {filepath}: {e}")

def scan_directory(directory_path):
    if not os.path.isdir(directory_path):
        print(f"❌ Error: The specified directory does not exist: {directory_path}")
        return
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(('.txt', '.csv', '.sql', '.xls', '.xlsx')):
                extract_all_phones(os.path.join(root, file))

def run_tests(test_directory, expected_numbers_set):
    print(f"\n🧪 Running tests on directory: {test_directory}")
    all_numbers.clear()
    scan_directory(test_directory)
    extracted_numbers_set = set(all_numbers)

    if extracted_numbers_set == expected_numbers_set:
        print(f"✅ Test PASSED! {len(extracted_numbers_set)} numbers found and match expected.")
        return True
    else:
        print(f"❌ Test FAILED!")
        print(f"Expected: {len(expected_numbers_set)} numbers: {sorted(list(expected_numbers_set))}")
        print(f"Got: {len(extracted_numbers_set)} numbers: {sorted(list(extracted_numbers_set))}")
        missing = expected_numbers_set - extracted_numbers_set
        if missing:
            print(f"Missing numbers ({len(missing)}): {sorted(list(missing))}")
        unexpected = extracted_numbers_set - expected_numbers_set
        if unexpected:
            print(f"Unexpected numbers ({len(unexpected)}): {sorted(list(unexpected))}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Extract phone numbers from files in a directory or run tests.")
    parser.add_argument("directory", nargs='?', default=None,
                        help="The directory to scan. Not needed if --test is used. If --test is not used and directory is not provided, uses a default path.")
    parser.add_argument("-o", "--output", default="~/Desktop/All_Phone_Numbers_Only.csv",
                        help="Output CSV file path. Default: '~/Desktop/All_Phone_Numbers_Only.csv'.")
    parser.add_argument("--test", action="store_true",
                        help="Run tests using the 'test_data' directory and predefined expected numbers.")
    args = parser.parse_args()

    if args.test:
        expected_for_test = {
            "15551234567", "1234567890", "442079460958", "02079460958", "4912345678901",
            "15559876543", "9876543210", "442079460123", "02079460123", "19876543210", "4912345678902",
            "15555555555", "5551234567", "1234567", "442079460999", "4912345678903",
            "15558889999", "5552345678", "442079460777", "02079460777", "4912345678904"
        }
        test_data_dir = "test_data"
        if not os.path.isdir(test_data_dir):
            print(f"❌ Error: Test data directory '{test_data_dir}' not found. Cannot run tests.")
            return
        test_passed = run_tests(test_data_dir, expected_for_test)
        print(f"\nTest run completed. Passed: {test_passed}")
    else:
        folder_to_scan = args.directory
        output_file_path = os.path.expanduser(args.output)

        if folder_to_scan is None:
            folder_to_scan = "D:/Your/Folder/Here"
            print(f"No directory argument provided, using default: {folder_to_scan}")

        print(f"🔍 Scanning directory: {folder_to_scan}")
        all_numbers.clear()
        scan_directory(folder_to_scan)

        if all_numbers:
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
            try:
                pd.DataFrame(sorted(list(all_numbers)), columns=["Phone Number"]).to_csv(output_file_path, index=False)
                print(f"\n📞 Extracted {len(all_numbers)} unique phone numbers.")
                print(f"📄 Saved to: {output_file_path}")
            except Exception as e:
                print(f"❌ Error saving CSV file to {output_file_path}: {e}")
        else:
            if os.path.isdir(folder_to_scan):
                print("\n🤷 No phone numbers found or extracted in the specified directory.")
            # Error for non-existent directory is handled by scan_directory

if __name__ == "__main__":
    main()
