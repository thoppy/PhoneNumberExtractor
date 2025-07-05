import pandas as pd

data = {
    'ColumnA': ['Call me at +1-555-888-9999', 'My number is (555) 234-5678', 'Reach me at 5552345678', 'Invalid: 12345', 'Text without number'],
    'ColumnB': ['UK: +44 20 7946 0777', 'Another UK: 02079460777', 'Also 555-234-5678', 'Not a phone: 9876', 'DE: +4912345678904'],
    'ColumnC': ['Just text here', '+15558889999', 'Text and number 555 234 5678', '1234567 (valid short)', 'No numbers in this cell']
}

df = pd.DataFrame(data)

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('test_data/sample.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='Sheet1', index=False)

# Close the Pandas Excel writer and output the Excel file.
writer.close()

print("Excel file created successfully.")
