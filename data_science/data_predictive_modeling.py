import pandas as pd
import numpy as np
from sklearn.model_selection import TimeSeriesSplit, RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.preprocessing import LabelEncoder, StandardScaler
from math import sqrt
import matplotlib.pyplot as plt

# Import the preprocessed data
gym_dataset = pd.read_csv('preprocessed_gym_data.csv')

# Convert 'Date' to datetime and set as index
gym_dataset['Date'] = pd.to_datetime(gym_dataset['Date'])
gym_dataset.set_index('Date', inplace=True)

# Extract additional features
gym_dataset['DayOfWeek'] = gym_dataset.index.dayofweek
gym_dataset['Month'] = gym_dataset.index.month
gym_dataset['IsWeekend'] = (gym_dataset.index.dayofweek >= 5).astype(int)
gym_dataset['DayOfYear'] = gym_dataset.index.dayofyear
gym_dataset['WeekOfYear'] = gym_dataset.index.isocalendar().week

# Create lag features
gym_dataset['PreviousDayAttendance'] = gym_dataset['People Detected'].shift(1)
gym_dataset['Last7DaysAvgAttendance'] = gym_dataset['People Detected'].rolling(window=7).mean()

# Drop rows with NaN values
gym_dataset.dropna(inplace=True)

# Encode the 'Weekday' column
le = LabelEncoder()
gym_dataset['Weekday_Encoded'] = le.fit_transform(gym_dataset['Weekday'])

# Prepare features and target
features = ['DayOfWeek', 'Weekday_Encoded', 'Month', 'IsWeekend', 'DayOfYear', 'WeekOfYear', 'PreviousDayAttendance', 'Last7DaysAvgAttendance']
X = gym_dataset[features]
y = gym_dataset['People Detected']

# Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Time series cross-validation
tscv = TimeSeriesSplit(n_splits=5)

# Random Forest model
rf = RandomForestRegressor(random_state=42)

# Parameter grid for RandomizedSearchCV
param_grid = {
    'n_estimators': [100, 200, 300, 400, 500],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# Perform RandomizedSearchCV
random_search = RandomizedSearchCV(estimator=rf, param_distributions=param_grid, n_iter=100, cv=tscv, verbose=2, random_state=42, n_jobs=-1)
random_search.fit(X_scaled, y)

# Get the best model
best_rf_model = random_search.best_estimator_

# Make predictions
y_pred = best_rf_model.predict(X_scaled)

# Calculate accuracy metrics
rmse = sqrt(mean_squared_error(y, y_pred))
mae = mean_absolute_error(y, y_pred)
r2 = r2_score(y, y_pred)
mape = np.mean(np.abs((y - y_pred) / y)) * 100

print(f'Best Random Forest RMSE: {rmse}')
print(f'Mean Absolute Error: {mae}')
print(f'R-squared Score: {r2}')
print(f'Mean Absolute Percentage Error: {mape}%')

# Create next week's dates
last_date = gym_dataset.index[-1]
next_week_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=7, freq='D')

# Prepare features for next week
next_week_features = pd.DataFrame({
    'DayOfWeek': next_week_dates.dayofweek,
    'Weekday_Encoded': le.transform(next_week_dates.day_name()),
    'Month': next_week_dates.month,
    'IsWeekend': (next_week_dates.dayofweek >= 5).astype(int),
    'DayOfYear': next_week_dates.dayofyear,
    'WeekOfYear': next_week_dates.isocalendar().week,
    'PreviousDayAttendance': [gym_dataset['People Detected'].iloc[-1]] + list(y_pred[-6:]),
    'Last7DaysAvgAttendance': [gym_dataset['People Detected'].iloc[-7:].mean()] * 7
})

# Scale the features
next_week_features_scaled = scaler.transform(next_week_features)

# Make predictions
next_week_predictions = best_rf_model.predict(next_week_features_scaled)

# Create a DataFrame with the results
next_week_attendance = pd.DataFrame({
    'Date': next_week_dates,
    'Predicted Attendance': next_week_predictions.round().astype(int)
})

print("\nNext week's predicted attendance:")
print(next_week_attendance)

# Visualizing Results
plt.figure(figsize=(12, 6))
plt.plot(gym_dataset.index[-30:], gym_dataset['People Detected'][-30:], label='Actual')
plt.plot(next_week_attendance['Date'], next_week_attendance['Predicted Attendance'], label='Predicted')
plt.title('Gym Attendance: Actual vs Predicted')
plt.xlabel('Date')
plt.ylabel('Number of People')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()