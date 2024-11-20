import pandas as pd
import numpy as np
from sklearn.model_selection import TimeSeriesSplit, RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

# Import the preprocessed data
gym_dataset = pd.read_csv('preprocessed_gym_data.csv')

# Convert 'DateTime' to datetime and set as index
gym_dataset['DateTime'] = pd.to_datetime(gym_dataset['DateTime'])
gym_dataset.set_index('DateTime', inplace=True)

# Filter data for hours between 8:00 and 23:00
gym_dataset = gym_dataset.between_time('08:00', '23:00')

# Extract additional features
gym_dataset['DayOfWeek'] = gym_dataset.index.dayofweek
gym_dataset['Month'] = gym_dataset.index.month
gym_dataset['IsWeekend'] = (gym_dataset.index.dayofweek >= 5).astype(int)
gym_dataset['DayOfYear'] = gym_dataset.index.dayofyear
gym_dataset['WeekOfYear'] = gym_dataset.index.isocalendar().week
gym_dataset['Hour'] = gym_dataset.index.hour

# Create lag features
gym_dataset['PreviousHourAttendance'] = gym_dataset['People Detected'].shift(1)
gym_dataset['PreviousDayAttendance'] = gym_dataset['People Detected'].shift(16)
gym_dataset['Last7DaysAvgAttendance'] = gym_dataset['People Detected'].rolling(window=16*7).mean()

# Drop rows with NaN values
gym_dataset.dropna(inplace=True)

# Encode the 'Weekday' column
le = LabelEncoder()
gym_dataset['Weekday_Encoded'] = le.fit_transform(gym_dataset.index.day_name())

# Prepare features and target
features = ['DayOfWeek', 'Weekday_Encoded', 'Month', 'IsWeekend', 'DayOfYear', 'WeekOfYear', 'Hour', 'PreviousHourAttendance', 'PreviousDayAttendance', 'Last7DaysAvgAttendance']
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

# Make predictions on the training set
y_pred = best_rf_model.predict(X_scaled)

# Calculate Mean Squared Error (MSE)
mse = mean_squared_error(y, y_pred)

# Calculate Root Mean Squared Error (RMSE)
rmse = np.sqrt(mse)

# Calculate R-squared (R²) score
r2 = r2_score(y, y_pred)

# Calculate Mean Absolute Error (MAE)
mae = np.mean(np.abs(y - y_pred))

# Print the evaluation metrics
print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
print(f"R-squared (R²) Score: {r2:.4f}")
print(f"Mean Absolute Error (MAE): {mae:.2f}")

# Calculate the 95% confidence interval
confidence_interval = 1.96 * rmse
print(f"95% Confidence Interval: ±{confidence_interval:.2f}")

# Create next 3 days' dates and hours (8:00 to 23:00)
last_date = gym_dataset.index[-1]
next_3_days_dates = pd.date_range(start=last_date.normalize() + pd.Timedelta(days=1, hours=8), periods=16*3, freq='h')
next_3_days_dates = next_3_days_dates[next_3_days_dates.hour.isin(range(8, 24))]

# Create a DataFrame for next 3 days' features
next_3_days_features = pd.DataFrame(index=next_3_days_dates)
next_3_days_features['DayOfWeek'] = next_3_days_features.index.dayofweek
next_3_days_features['Weekday_Encoded'] = le.transform(next_3_days_features.index.day_name())
next_3_days_features['Month'] = next_3_days_features.index.month
next_3_days_features['IsWeekend'] = (next_3_days_features.index.dayofweek >= 5).astype(int)
next_3_days_features['DayOfYear'] = next_3_days_features.index.dayofyear
next_3_days_features['WeekOfYear'] = next_3_days_features.index.isocalendar().week
next_3_days_features['Hour'] = next_3_days_features.index.hour

# Add lag features (fixed)
next_3_days_features['PreviousHourAttendance'] = [gym_dataset['People Detected'].iloc[-1]] + list(y[-31:])
next_3_days_features['PreviousDayAttendance'] = list(gym_dataset['People Detected'].iloc[-16:]) + list(y[-16:])
next_3_days_features['Last7DaysAvgAttendance'] = gym_dataset['People Detected'].iloc[-16*7:].mean()

# Scale the features
next_3_days_features_scaled = scaler.transform(next_3_days_features)

# Make predictions
next_3_days_predictions = best_rf_model.predict(next_3_days_features_scaled)

# Create a DataFrame with the results
next_3_days_attendance = pd.DataFrame({
    'DateTime': next_3_days_dates,
    'Predicted Attendance': next_3_days_predictions.round().astype(int)
})

# Ensure the DateTime column is of datetime type
next_3_days_attendance['DateTime'] = pd.to_datetime(next_3_days_attendance['DateTime'])

# Visualizing Results
plt.figure(figsize=(20, 10))
sns.lineplot(x=gym_dataset.index[-16*3:], y=gym_dataset['People Detected'][-16*3:], label='Actual')
sns.lineplot(x=next_3_days_attendance['DateTime'], y=next_3_days_attendance['Predicted Attendance'], label='Predicted')
plt.title('Gym Attendance: Actual vs Predicted (Hourly, 8:00-23:00)')
plt.xlabel('Date and Time')
plt.ylabel('Number of People')
plt.legend()

# Customize x-axis ticks to show each 3-hour interval between 8:00-23:00
plt.gca().xaxis.set_major_locator(mdates.HourLocator(byhour=range(8, 24, 3)))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Save the line plot as an image
plt.savefig('gym_attendance_prediction.png')

# Show the line plot
plt.show()

plt.close()