import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 
import os 
from datetime import datetime, timedelta

CSV_FILE = 'goals.csv'

DEFAULT_GOALS = [
    "Exercise",
    "Read",
    "Meditate",
    "Plan",
    "Work"
]

if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Goal'] = df['Goal'].astype(str)
    df['Completed'] = df['Completed'].astype(bool)
else:
    df = pd.DataFrame(columns=['Date', 'Goal', 'Completed'])
    df['Date'] = pd.to_datetime(df['Date'])
    df['Goal'] = df['Goal'].astype(str)
    df['Completed'] = df['Completed'].astype(bool)
    
print("Current DataFrame:")
print(df)
print("\nDataFrame Info:")
print(df.dtypes)

def add_goal():
    
    today = pd.to_datetime(datetime.now().date())
    today_data = df[df['Date'] == today]
    if len(today_data) >= len(DEFAULT_GOALS):
        print(f"You have already added all your goals for {today.date()}.")
        return
    print(f"Logging goals for {today.date()}:")
    for goal in DEFAULT_GOALS:
        if not today_data.empty and goal in today_data['Goal'].values:
            continue
        completed = input(f"Did you complete '{goal}' today? (y/n): ").lower()
        completed = True if completed.lower() == 'y' else False
        df.loc[len(df)] = [today, goal, completed]
    df.to_csv(CSV_FILE, index=False)
    print(f"Goals logged for {today.date()}.")
    print(df[df['Date'] == today])

def calculate_streaks():
    
    df_sorted = df.sort_values(by='Date')
    

    current_streaks = {goal: 0 for goal in DEFAULT_GOALS}
    longest_streaks = {goal: 0 for goal in DEFAULT_GOALS}
    

    today = pd.to_datetime(datetime.now().date())
    
    for goal in DEFAULT_GOALS:
        
        goal_data = df_sorted[df_sorted['Goal'] == goal][['Date', 'Completed']]
        if goal_data.empty:
            continue
        
        
        current_streak = 0
        current_date = today
        while True:
            date_check = goal_data[goal_data['Date'] == current_date]
            if date_check.empty or not date_check['Completed'].iloc[0]:
                break
            current_streak += 1
            current_date -= timedelta(days=1)
        current_streaks[goal] = current_streak
        
        
        longest_streak = 0
        current = 0
        prev_date = None
        for date, completed in zip(goal_data['Date'].dt.date, goal_data['Completed']):
            if completed:
                if prev_date is None or date == prev_date + timedelta(days=1):
                    current += 1
                else:
                    current = 1
                longest_streak = max(longest_streak, current)
            else:
                current = 0
            prev_date = date
        longest_streaks[goal] = longest_streak
    
    
    print("\nStreak Report:")
    for goal in DEFAULT_GOALS:
        print(f"{goal}: Current Streak = {current_streaks[goal]} days, Longest Streak = {longest_streaks[goal]} days")
    
    return current_streaks, longest_streaks


add_goal()
calculate_streaks()