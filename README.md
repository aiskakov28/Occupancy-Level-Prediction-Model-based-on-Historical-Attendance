# Occupancy-Level-Prediction-Model-based-on-Historical-Attendance
## 🏃 Project Overview

An advanced machine learning system that analyzes historical gym attendance data to forecast future occupancy levels. The project combines comprehensive data analysis with predictive modeling to provide accurate attendance predictions.

## 📊 Key Components

### 1. Data Analysis Module

Comprehensive analysis of gym attendance patterns including:

- Temporal attendance patterns analysis
- Peak hour identification
- Weekly trend analysis
- Time-based correlation studies

### 2. Predictive Modeling System

Random Forest-based prediction system featuring:

- Advanced feature engineering
- Hyperparameter optimization via RandomizedSearchCV
- Multi-metric model evaluation
- 3-day attendance forecasting

## 📁 Project Structure

```
project/
├── data_analysis.py              # EDA and visualization
├── data_predictive_modeling.py   # ML model implementation
├── gym_dataset.csv              # Raw attendance data
└── preprocessed_gym_data.csv    # Processed dataset
```

## 📈 Generated Visualizations

Data Analysis Outputs:

- weekday_attendance.png - Weekly attendance patterns
- hourly_attendance.png - Daily attendance flow
- attendance_heatmap.png - Time-based pattern visualization
- weekday_attendance_distribution.png - Statistical distribution analysis
- attendance_trend.png - Long-term trend analysis

Predictive Model Output:

- gym_attendance_prediction.png - Forecast validation visualization

## ⚙️ Dependencies

```
pandas
numpy
matplotlib
seaborn
scikit-learn
```

## 🚀 Getting Started

1. Set up your environment:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn
```

1. Run the analysis:

```bash
python data_analysis.py
python data_predictive_modeling.py
```

## 📊 Model Evaluation Metrics

- Mean Squared Error (MSE)
- Root Mean Squared Error (RMSE)
- R-squared (R²)
- Mean Absolute Error (MAE)

## 🎯 Results

The system provides:

- Detailed attendance pattern insights
- Accurate 3-day occupancy forecasts
- Comprehensive performance metrics
- Visual validation of predictions
