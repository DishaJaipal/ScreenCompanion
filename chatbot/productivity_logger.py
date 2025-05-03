import datetime
import csv

def log_productivity(user_input, focus_area):
    """Logs user activity to a CSV file"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open('productivity_log.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, focus_area, user_input])