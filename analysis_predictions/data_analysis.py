import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
gym_dataset = pd.read_csv('../gym_occupancy_dataset/gym_dataset.csv')

# Convert 'Date' and 'Time' columns to datetime
gym_dataset['DateTime'] = pd.to_datetime(gym_dataset['Date'] + ' ' + gym_dataset['Time'])
gym_dataset['Date'] = pd.to_datetime(gym_dataset['Date'])
gym_dataset['Time'] = pd.to_datetime(gym_dataset['Time'], format='%H:%M').dt.time

# Add 'Weekday' and 'Hour' columns
gym_dataset['Weekday'] = gym_dataset['DateTime'].dt.day_name()
gym_dataset['Hour'] = gym_dataset['DateTime'].dt.hour

# 1. Average attendance by weekday
weekday_avg = gym_dataset.groupby('Weekday')['People Detected'].mean().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

plt.figure(figsize=(12, 6))
weekday_avg.plot(kind='bar')
plt.title('Average Gym Attendance by Weekday')
plt.xlabel('Weekday')
plt.ylabel('Average Number of People')
plt.tight_layout()
plt.savefig('weekday_attendance.png')
plt.close()

# 2. Average attendance by hour
hourly_avg = gym_dataset.groupby('Hour')['People Detected'].mean()

plt.figure(figsize=(12, 6))
hourly_avg.plot(kind='line', marker='o')
plt.title('Average Gym Attendance by Hour')
plt.xlabel('Hour of the Day')
plt.ylabel('Average Number of People')
plt.xticks(range(24))
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('hourly_attendance.png')
plt.close()

# 3. Heatmap of attendance by weekday and hour
pivot_data = gym_dataset.pivot_table(values='People Detected', index='Weekday', columns='Hour', aggfunc='mean')
pivot_data = pivot_data.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

plt.figure(figsize=(15, 8))
sns.heatmap(pivot_data, cmap='YlOrRd', annot=True, fmt='.0f', cbar_kws={'label': 'Average Number of People'})
plt.title('Gym Attendance Heatmap: Weekday vs. Hour')
plt.xlabel('Hour of the Day')
plt.ylabel('Weekday')
plt.tight_layout()
plt.savefig('attendance_heatmap.png')
plt.close()

# 4. Find peak hours and busiest weekdays
peak_hour = hourly_avg.idxmax()
busiest_weekday = weekday_avg.idxmax()

print(f"Peak hour: {peak_hour}:00")
print(f"Busiest weekday: {busiest_weekday}")

# 5. Top 5 busiest hours
top_5_hours = hourly_avg.nlargest(5)
print("\nTop 5 busiest hours:")
for hour, attendance in top_5_hours.items():
    print(f"{hour}:00 - Average attendance: {attendance:.2f}")

# 6. Weekday ranking
weekday_ranking = weekday_avg.sort_values(ascending=False)
print("\nWeekday ranking by average attendance:")
for weekday, attendance in weekday_ranking.items():
    print(f"{weekday}: {attendance:.2f}")

# 7. Box plot of attendance by weekday
plt.figure(figsize=(12, 6))
sns.boxplot(x='Weekday', y='People Detected', data=gym_dataset, order=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
plt.title('Distribution of Gym Attendance by Weekday')
plt.xlabel('Weekday')
plt.ylabel('Number of People')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('weekday_attendance_distribution.png')
plt.close()

# 8. Attendance trend over time
daily_attendance = gym_dataset.groupby('Date')['People Detected'].sum().reset_index()
plt.figure(figsize=(15, 6))
plt.plot(daily_attendance['Date'], daily_attendance['People Detected'])
plt.title('Daily Gym Attendance Over Time')
plt.xlabel('Date')
plt.ylabel('Total Number of People')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('attendance_trend.png')
plt.close()

# 9. Correlation between hour and attendance
correlation = gym_dataset['Hour'].corr(gym_dataset['People Detected'])
print(f"\nCorrelation between hour and attendance: {correlation:.2f}")

# 10. Busiest and quietest hours for each day
busiest_hours = pivot_data.idxmax(axis=1)
quietest_hours = pivot_data.idxmin(axis=1)

print("\nBusiest hours for each day:")
for day, hour in busiest_hours.items():
    print(f"{day}: {hour}:00")

print("\nQuietest hours for each day:")
for day, hour in quietest_hours.items():
    print(f"{day}: {hour}:00")

# Save the preprocessed dataset
gym_dataset.to_csv('preprocessed_gym_data.csv', index=False)