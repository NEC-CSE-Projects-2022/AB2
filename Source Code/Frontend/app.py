from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import pandas as pd
from datetime import datetime
import os
import glob

app = Flask(__name__)

MODEL_PATH = 'google_ridge_model.pkl'
model = None
dataset = None

def load_model():
    global model
    if model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
        model = joblib.load(MODEL_PATH)
    return model

def load_dataset():
    global dataset
    if dataset is None:
        csv_files = glob.glob('*.csv')
        if not csv_files:
            print("No CSV files found in the project directory.")
            return None
        try:
            # Try to load the first CSV file found
            csv_file = csv_files[0]
            print(f"Loading dataset from: {csv_file}")
            df = pd.read_csv(csv_file)
            
            # Normalize column names (handle variations)
            df.columns = df.columns.str.strip()
            df.columns = df.columns.str.replace(' ', '_')
            
            # Check for date column (handle variations)
            date_col = None
            for col in df.columns:
                if col.lower() in ['date', 'dates', 'time', 'timestamp']:
                    date_col = col
                    break
            
            if date_col:
                df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
                df = df.sort_values(date_col)
                # Rename to 'Date' for consistency
                if date_col != 'Date':
                    df = df.rename(columns={date_col: 'Date'})
            
            print(f"Dataset loaded successfully. Shape: {df.shape}, Columns: {list(df.columns)}")
            dataset = df
        except Exception as e:
            print(f"Error loading dataset: {e}")
            import traceback
            traceback.print_exc()
            return None
    return dataset

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/dataset', methods=['GET'])
def get_dataset():
    try:
        df = load_dataset()
        if df is None:
            return jsonify({'error': 'Dataset not found. Please add a CSV file to the project directory.'}), 404
        
        limit = request.args.get('limit', type=int, default=100)
        offset = request.args.get('offset', type=int, default=0)
        
        df_subset = df.iloc[offset:offset+limit]
        
        return jsonify({
            'success': True,
            'data': df_subset.to_dict('records'),
            'total': len(df),
            'columns': list(df.columns)
        })
    except Exception as e:
        return jsonify({'error': f'Error loading dataset: {str(e)}'}), 500

@app.route('/api/dataset/chart', methods=['GET'])
def get_dataset_chart():
    try:
        df = load_dataset()
        if df is None:
            return jsonify({'error': 'Dataset not found'}), 404
        
        limit = request.args.get('limit', type=int, default=100)
        df_subset = df.tail(limit)
        
        # Normalize column names for lookup
        col_map = {}
        for col in df_subset.columns:
            col_lower = col.lower().replace('_', '').replace(' ', '')
            col_map[col_lower] = col
        
        # Get dates
        date_col = None
        for key in ['date', 'dates', 'time', 'timestamp']:
            if key in col_map:
                date_col = col_map[key]
                break
        
        dates = []
        if date_col:
            dates = df_subset[date_col].astype(str).tolist()
        else:
            dates = list(range(len(df_subset)))
        
        # Helper function to get column data
        def get_col_data(col_variations):
            for var in col_variations:
                if var in col_map:
                    return df_subset[col_map[var]].tolist()
            return []
        
        chart_data = {
            'dates': dates,
            'open': get_col_data(['open', 'openprice']),
            'high': get_col_data(['high', 'highprice']),
            'low': get_col_data(['low', 'lowprice']),
            'close': get_col_data(['close', 'closeprice']),
            'adj_close': get_col_data(['adjclose', 'adj_close', 'adjustedclose']),
            'volume': get_col_data(['volume', 'vol'])
        }
        
        return jsonify({
            'success': True,
            'data': chart_data
        })
    except Exception as e:
        return jsonify({'error': f'Error loading chart data: {str(e)}'}), 500

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        model = load_model()
        data = request.get_json()
        
        required_fields = ['open', 'high', 'low', 'adj_close', 'volume', 'date']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        try:
            open_price = float(data['open'])
            high = float(data['high'])
            low = float(data['low'])
            adj_close = float(data['adj_close'])
            volume = float(data['volume'])
            date_str = data['date']
        except (ValueError, TypeError) as e:
            return jsonify({'error': f'Invalid numeric values: {str(e)}'}), 400
        
        if low > high:
            return jsonify({'error': 'Low price cannot be greater than High price'}), 400
        if open_price < low or open_price > high:
            return jsonify({'error': 'Open price must be between Low and High prices'}), 400
        if adj_close < low or adj_close > high:
            return jsonify({'error': 'Adj Close price must be between Low and High prices'}), 400
        if volume < 0:
            return jsonify({'error': 'Volume cannot be negative'}), 400
        
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            date_ordinal = date_obj.toordinal()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        features = np.array([[open_price, high, low, adj_close, volume, date_ordinal]])
        prediction = model.predict(features)
        
        return jsonify({
            'success': True,
            'prediction': float(prediction[0]),
            'date': date_str
        })
        
    except Exception as e:
        return jsonify({'error': f'Prediction error: {str(e)}'}), 500


@app.route('/api/predict/bulk', methods=['POST'])
def predict_bulk():
    try:
        model = load_model()

        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request. Use form field "file".'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file.'}), 400

        # Try to parse uploaded file as CSV, fallback to table parsing
        try:
            df = pd.read_csv(file)
        except Exception:
            try:
                file.seek(0)
                df = pd.read_table(file)
            except Exception as e:
                return jsonify({'error': f'Could not parse file: {str(e)}'}), 400

        # Normalize column names
        df.columns = df.columns.str.strip()
        df.columns = df.columns.str.replace(' ', '_')

        # Build a lookup map: simplified_lower -> original_column_name
        col_map = {}
        for col in df.columns:
            col_lower = col.lower().replace('_', '').replace(' ', '')
            col_map[col_lower] = col

        def get_col_series(variations):
            for v in variations:
                if v in col_map:
                    return df[col_map[v]]
            return None

        opens = get_col_series(['open', 'openprice', 'open_price'])
        highs = get_col_series(['high', 'highprice'])
        lows = get_col_series(['low', 'lowprice'])
        adjs = get_col_series(['adjclose', 'adj_close', 'adjustedclose'])
        vols = get_col_series(['volume', 'vol'])

        # Find date column if available
        date_col = None
        for k in ['date', 'dates', 'time', 'timestamp']:
            if k in col_map:
                date_col = col_map[k]
                break

        # Find actual/target column if available
        actual_col = None
        for k in ['close', 'closeprice', 'close_price', 'actual', 'target']:
            if k in col_map:
                actual_col = col_map[k]
                break

        if opens is None or highs is None or lows is None or adjs is None or vols is None:
            return jsonify({'error': 'Missing required columns. Required: open, high, low, adj_close, volume.'}), 400

        results = []
        errors = []

        for idx, row in df.iterrows():
            try:
                open_price = float(row[opens.name])
                high = float(row[highs.name])
                low = float(row[lows.name])
                adj_close = float(row[adjs.name])
                volume = float(row[vols.name])

                # Parse date -> ordinal
                if date_col:
                    date_val = row[date_col]
                    date_obj = pd.to_datetime(date_val, errors='coerce')
                    if pd.isna(date_obj):
                        raise ValueError(f'Invalid date value at row {idx}: {date_val}')
                    date_ordinal = date_obj.to_pydatetime().toordinal()
                    date_str = str(date_val)
                else:
                    # If no date column provided, use today's date for ordinal and empty string for display
                    date_ordinal = datetime.now().toordinal()
                    date_str = ''

                features = np.array([[open_price, high, low, adj_close, volume, date_ordinal]])
                pred = model.predict(features)[0]

                actual = None
                if actual_col:
                    try:
                        actual = float(row[actual_col])
                    except Exception:
                        actual = None

                results.append({
                    'row': int(idx),
                    'date': date_str,
                    'actual': actual,
                    'predicted': float(pred)
                })
            except Exception as e:
                errors.append({'row': int(idx), 'error': str(e)})

        return jsonify({'success': True, 'predictions': results, 'errors': errors, 'count': len(results)})

    except Exception as e:
        return jsonify({'error': f'Bulk prediction error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
