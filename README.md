# Occupancy-Level-Prediction-Model-based-on-Historical-Attendance

**Project Overview:**
This project analyzes historical gym attendance data and builds a predictive model to forecast future occupancy levels. It consists of two main parts: data analysis and predictive modeling.

**Files:**
data_analysis.py: Performs exploratory data analysis on the gym dataset
data_predictive_modeling.py: Builds and evaluates a Random Forest model for predicting gym attendance
gym_dataset.csv: Raw dataset containing historical gym attendance data
preprocessed_gym_data.csv: Processed dataset used for predictive modeling

**Data Analysis (data_analysis.py):**
This script performs various analyses on the gym attendance data, including:
Average attendance by weekday and hour
Heatmap of attendance patterns
Identification of peak hours and busiest weekdays
Attendance trends over time
Correlation between hour and attendance

**Generated Images:**
weekday_attendance.png: Bar chart showing average attendance for each day of the week
hourly_attendance.png: Line graph displaying average attendance throughout the day
attendance_heatmap.png: Heatmap visualizing attendance patterns by weekday and hour
weekday_attendance_distribution.png: Box plot showing the distribution of attendance for each weekday
attendance_trend.png: Line graph illustrating the daily attendance trend over time

**Predictive Modeling (data_predictive_modeling.py):**
This script builds a Random Forest model to predict gym attendance. It includes:
Data preprocessing and feature engineering
Model training using RandomizedSearchCV for hyperparameter tuning
Model evaluation using various metrics (MSE, RMSE, R², MAE)
Prediction of attendance for the next 3 days
**Generated Image:**
gym_attendance_prediction.png: Line plot comparing actual attendance with predicted attendance for the next 3 days

**Requirements:**
To run this project, you'll need the following Python libraries:
pandas
numpy
matplotlib
seaborn
scikit-learn

**Usage:**
Ensure you have all required libraries installed.
Run data_analysis.py to perform exploratory data analysis and generate visualizations.
Run data_predictive_modeling.py to train the model and make predictions.

**Results:**
The analysis provides insights into gym attendance patterns, while the predictive model forecasts future attendance levels. Refer to the generated images and console output for detailed results.
