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

def add_goal():
    today = pd.to_datetime(datetime.now().date())
    today_data = df[df['Date'] == today]
    if(len(today_data) >= len(DEFAULT_GOALS)):
        print("You have already added all your goals for today.")
        return
    print(f"Logging goals for today {today.date()} : ")
    for goal in DEFAULT_GOALS:
        if not today_data.empty and goal in today_data['Goal'].values:
            continue
        completed = input(f"Did you complete {goal}? (y/n): ")
        if completed.lower() == 'y':
            df.loc[len(df)] = [today, goal, True]
        else:
            df.loc[len(df)] = [today, goal, False]
    df.to_csv(CSV_FILE, index=False)
    print(f"Goals logged for {today.date()}.")
    print(df[df['Date'] == today])

add_goal()