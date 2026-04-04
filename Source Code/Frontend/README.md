# Stock Price Prediction - Google Ridge Model

A Flask web application for stock price prediction using a Ridge Regression model with dataset visualization and interactive charts.

## Features

- **Prediction Form**: Input stock data and get price predictions
- **Dataset Viewer**: Browse and view the Google stock dataset in a table
- **Interactive Charts**: 
  - Historical stock prices (Open, High, Low, Adj Close)
  - Prediction vs Actual comparison chart
- Clean and modern UI with tabbed interface
- Form validation (client-side and server-side)
- Real-time error messages
- Responsive design

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Download the Google Stock dataset from Kaggle:
   - Visit: https://www.kaggle.com/datasets/varpit94/google-stock-data
   - Download the CSV file
   - Place the CSV file in the project root directory (same folder as `app.py`)

3. Make sure `google_ridge_model.pkl` is in the project root directory.

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

### Prediction Tab
1. Enter the required stock data:
   - Date
   - Open Price
   - High Price
   - Low Price
   - Adj Close Price
   - Volume

2. Click "Predict Price" to get the prediction.

### Dataset Tab
- View the Google stock dataset in a table format
- Adjust the number of records to display (default: 50)
- Click "Load Data" to refresh the dataset

### Charts Tab
- View historical stock prices with interactive charts
- Select different time ranges (50, 100, 200, or 500 days)
- See prediction vs actual comparison after making predictions

## Model Features

The model expects the following features:
- Open
- High
- Low
- Adj Close
- Volume
- Date (converted to ordinal)

## Dataset Format

The CSV file should contain columns:
- Date
- Open
- High
- Low
- Close
- Adj Close
- Volume

## Technologies Used

- Flask (Backend)
- Chart.js (Data Visualization)
- HTML/CSS/JavaScript (Frontend)
- scikit-learn (Machine Learning)
- pandas (Data Processing)
