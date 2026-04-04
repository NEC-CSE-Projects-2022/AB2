
# Team Number – Project Title

## Team Info
- 22471A0509 — CHERUKURI THIRUMALA MALYADRI ( [LinkedIn](https://linkedin.com/in/xxxxxxxxxx) )
_Work Done: xxxxxxxxxx_

- 22471A0507 — CHALLA ROHITH ( [LinkedIn](https://linkedin.com/in/xxxxxxxxxx) )
_Work Done: xxxxxxxxxx_

- 22471A0538 — MITTA VENU ( [LinkedIn](https://linkedin.com/in/xxxxxxxxxx) )
_Work Done: xxxxxxxxxx_

- 22471A0511 — **CHEVURI CHANDU** ( [LinkedIn](https://linkedin.com/in/xxxxxxxxxx) )
_Work Done: xxxxxxxxxx_

---

## Abstract
Stock price prediction remains a challenging prob
lem due to the inherent noise, volatility, and nonlinearity of
f
inancial time series. Traditional statistical approaches often fail
to fully capture these complexities, whereas deep learning models,
despite their predictive power, are computationally expensive,
prone to overfitting, and lack interpretability—limiting their
practical use in financial decision-making. In this paper, we
propose a lightweight yet effective preprocessing framework
that focuses on variance stabilization to enhance stock price
forecasting. The methodology sequentially applies a logarithmic
transformation followed by a Yeo–Johnson power transformation
to reduce skewness and heteroscedasticity, thereby improving
data distribution for linear modeling. After preprocessing, a
Ridge Regression model with mild regularization is employed to
handle multicollinearity among correlated stock features such as
Open, High, and Low prices. The approach was evaluated using
historical Google stock data, achieving an R² score of 0.97–0.98,
with near-zero Mean Squared Error (MSE) and significantly re
duced prediction variance. Experimental results demonstrate that
a carefully designed variance-stabilized preprocessing pipeline
can substantially improve the accuracy and robustness of linear
models, providing an interpretable and computationally efficient
alternative to more complex deep learning architectures for stock
price prediction.Unlike prior work that applies single-stage log
or Box–Cox normalization, this study introduces a sequential
log–power normalization strategy that integrates logarithmic com
pression with Yeo–Johnson variance stabilization. This dual-stage
preprocessing improves linear model conditioning and enhances
interpretability for financial forecasting.

---

## Paper Reference (Inspiration)
👉 **[Paper Title- Stock Market Prediction Using Sequential
Log-Power Normalization and Ridge Regression
  – Author Names K. S. Sekhar, 
  C. T. Malyadri,
  C. Rohith, 
  M. Venu, 
  C. Chandu, 
  D. Siri, and 
  S. Moturi.
 ](Paper URL here)**
Original conference/IEEE paper used as inspiration for the model.

---

## Our Improvement Over Existing Paper
Compared to the referenced paper, our work introduces practical, implementation-level improvements while preserving the original modeling philosophy. We design a fully reproducible end-to-end pipeline that strictly separates training, validation, and inference to prevent data leakage. All preprocessing steps, including logarithmic shifting, Yeo–Johnson transformation, and standard scaling, are saved and reused during prediction, improving deployment reliability. The model supports dynamic column alignment and missing-feature handling, enabling robust use across heterogeneous datasets. Additionally, performance evaluation is standardized with consistent metrics and automated reporting. These enhancements transform the original experimental framework into a deployment-ready, transparent, and reusable stock prediction system for real applications.

---

## About the Project
Give a simple explanation of:
- What your project does
- This project predicts future stock closing prices using historical stock market data. It applies advanced data preprocessing techniques to stabilize price fluctuations and then uses a Ridge Regression model to generate accurate and reliable stock price predictions.
- Why it is useful
- Stock market data is noisy and highly volatile, which often reduces prediction accuracy. By stabilizing variance and reducing skewness before modeling, this project improves prediction accuracy while keeping the model simple, fast, and interpretable. This makes it suitable for academic use as well as real-world financial analysis and decision support.
- General project workflow (input → processing → model → output)
- Stock data (Open, High, Low, Close, Volume) is taken as input → data is preprocessed using logarithmic and Yeo–Johnson transformations with scaling → Ridge Regression model is trained → predicted stock prices are generated and compared with actual values.

---

## Dataset Used
👉 **[Google Stock Price Datase](https://www.kaggle.com/datasets/medharawat/google-stock-price)**

**Dataset Details:**
Dataset Name: Google (Alphabet Inc.) Historical Stock Price Dataset

Company Ticker: GOOGL / GOOG

Data Type: Financial time-series data

Frequency: Daily records

Time Period: Historical data covering multiple years (from initial public listing to recent dates, depending on source)

---

## Dependencies Used
pandas
Used for reading CSV stock datasets, handling tabular data, column selection, and data preprocessing operations.

numpy
Used for numerical computations, logarithmic transformations (log1p), array operations, and mathematical processing of stock values.

scikit-learn (sklearn)

train_test_split – for splitting the dataset into training and testing sets

StandardScaler – for feature standardization (zero mean, unit variance)

PowerTransformer (Yeo–Johnson) – for variance stabilization and distribution normalization

Ridge – for Ridge Regression modeling with L2 regularization

mean_squared_error, mean_absolute_error, r2_score – for model performance evaluation

matplotlib
Used for plotting and visualizing actual vs predicted stock prices and performance graphs.

seaborn
Used for statistical visualization and exploratory data analysis (EDA) support.

joblib
Used to save and load the trained Ridge Regression model and preprocessing transformers for deployment and inference.

google.colab
Used for Google Drive integration, dataset access, and file upload functionality in the Colab execution environment.

---

## EDA & Preprocessing
Checked for missing values and handled them using median imputation
Visualized stock price distributions and trends
Identified skewness and heteroscedasticity in raw data
Preprocessing Steps:
Log Transformation → reduces skewness and compresses large values
Yeo–Johnson Transformation → stabilizes variance
StandardScaler → normalizes features
Data Cleaning → ensures consistent and usable dataset

---

## Model Training Info
Model Used: Ridge Regression
Regularization Parameter (α): 0.1
Train/Test Split: 80% / 20%
Training Process:
Load dataset
Apply preprocessing pipeline
Split dataset into training and testing sets
Train Ridge Regression model
Save trained model using joblib

---

## Model Testing / Evaluation
Evaluation Metrics:
Mean Squared Error (MSE)
Mean Absolute Error (MAE)
R² Score
Performance:
MSE ≈ 0.00003
MAE ≈ 0.003 – 0.005
R² ≈ 0.98

The model shows high accuracy with very low prediction error and stable outputs.

---

## Results
Ridge Regression outperformed:
Linear Regression
Support Vector Regression (SVR)
Neural Networks
Predictions closely match actual stock prices
Significant reduction in variance and noise

---

## Limitations & Future Work
Limitations:
Uses only OHLCV features
Does not consider external factors (news, sentiment, macroeconomics)
Future Work:
Add technical indicators (RSI, Moving Averages)
Integrate sentiment analysis
Develop hybrid models (Ridge + LSTM)
Build real-time prediction system

---

## Deployment Info
The trained model is saved using joblib and can be deployed using:

Flask API
FastAPI
Streamlit Dashboard
Deployment Steps:
Load saved model
Apply same preprocessing pipeline
Predict on new stock data

---
