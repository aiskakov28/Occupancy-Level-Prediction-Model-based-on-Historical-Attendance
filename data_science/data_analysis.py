import pandas as pd
import matplotlib.pyplot as plt


# Define the file path
fp_1 = '/Users/abylai/PycharmProjects/Occupancy_Prediction/gym_occupancy_dataset/gym_dataset.csv'

# Load the dataset
gym_dataset = pd.read_csv(fp_1)

# Convert the 'Date' column to datetime
gym_dataset['Date'] = pd.to_datetime(gym_dataset['Date'])

#  Add the 'Weekday' column
gym_dataset['Weekday'] = gym_dataset['Date'].dt.day_name()

# 1. Line plot of daily attendance
plt.figure(figsize=(10, 6))
plt.plot(gym_dataset['Date'], gym_dataset['People Detected'])
plt.title('Daily Gym Attendance')
plt.xlabel('Date')
plt.ylabel('Number of People')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
plt.close()

# 2. Bar plot of average attendance by weekday
weekday_avg = gym_dataset.groupby('Weekday')['People Detected'].mean().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
plt.figure(figsize=(12, 6))
colors = {'Monday': 'lightgrey', 'Tuesday': 'darkgrey', 'Wednesday': 'grey', 'Thursday': 'lightblue', 'Friday': 'darkblue', 'Saturday': 'lightgreen', 'Sunday': 'darkgreen'}
weekday_avg.plot(kind='bar', color=[colors[day] for day in weekday_avg.index])
plt.title('Average Gym Attendance by Weekday')
plt.xlabel('Weekday')
plt.ylabel('Average Number of People')
plt.tight_layout()
plt.show()
plt.close()

# 3. Box plot of attendance by weekday
plt.figure(figsize=(12, 6))
gym_dataset.boxplot(column='People Detected', by='Weekday', figsize=(12, 6))
plt.title('Gym Attendance Distribution by Weekday')
plt.suptitle('')
plt.ylabel('Number of People')
plt.tight_layout()
plt.show()
plt.close()

# Display the final dataframe
pd.set_option('display.max_columns', None)
print(gym_dataset.head(30))

# Save the DataFrame to a CSV file
gym_dataset.to_csv('preprocessed_gym_data.csv', index=False)

