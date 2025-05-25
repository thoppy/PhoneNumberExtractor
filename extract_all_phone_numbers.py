import os
import re
import pandas as pd

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
                for num in found:
                    clean = re.sub(r'[-.\s()]', '', num)
                    if len(clean) >= 7:  # Valid length check
                        all_numbers.add(clean)
        elif ext in ['.xls', '.xlsx']:
            df = pd.read_excel(filepath, engine='openpyxl')
            for col in df.columns:
                content = ' '.join(df[col].astype(str).dropna())
                found = re.findall(phone_pattern, content)
                for num in found:
                    clean = re.sub(r'[-.\s()]', '', num)
                    if len(clean) >= 7:
                        all_numbers.add(clean)
    except Exception as e:
        print(f"❌ Error reading {filepath}: {e}")

def scan_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(('.txt', '.csv', '.sql', '.xls', '.xlsx')):
                extract_all_phones(os.path.join(root, file))

# 🔍 Set your folder path here
folder_to_scan = "D:/Your/Folder/Here"
scan_directory(folder_to_scan)

# 📤 Save to CSV
output_path = os.path.expanduser("~/Desktop/All Phone Numbers Only.csv")
pd.DataFrame(sorted(all_numbers), columns=["Phone Number"]).to_csv(output_path, index=False)

print(f"\n📞 Extracted {len(all_numbers)} unique phone numbers.")
print(f"📄 Saved to: {output_path}")
