# How to Add the Google Stock Dataset

## Quick Steps:

1. **Download the Dataset:**
   - Go to: https://www.kaggle.com/datasets/varpit94/google-stock-data
   - Click "Download" button
   - Extract the ZIP file if needed

2. **Place the CSV File:**
   - Copy the CSV file (usually named something like `Google_Stock_Data.csv` or `GOOG.csv`)
   - Paste it in this project folder: `C:\Users\munic\OneDrive\Documents\Desktop\AB2\`
   - Make sure it's in the same folder as `app.py`

3. **Verify:**
   - The CSV file should have columns: Date, Open, High, Low, Close, Adj Close, Volume
   - Restart the Flask server if it's running
   - Go to the "Dataset" tab and click "Load Data"
   - Go to the "Charts" tab to see the graphs

## Expected CSV Format:

```
Date,Open,High,Low,Close,Adj Close,Volume
2020-01-02,68.00,68.50,67.50,68.00,68.00,12345678
...
```

## Troubleshooting:

- **"Dataset not found" error:** Make sure the CSV file is in the project root directory
- **"Error loading dataset" error:** Check that the CSV has the correct column names
- **Charts not showing:** Make sure the dataset loaded successfully first
- **Server not responding:** Restart with `python app.py`
