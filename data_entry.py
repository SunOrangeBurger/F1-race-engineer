import pandas as pd

def get_track_data():
    # Read data from the Excel file
    data = pd.read_csv('data_need_filled.csv')
    
    # Use the correct case for the column name
    LAPS = data['LAPS'][0]
    TRACK_NAME = data['Track_name'][0]
    TRACK_ID = data['Sno'][0]  # Assuming 'Sno' is the track ID

    return LAPS, TRACK_NAME, TRACK_ID

def main():
    # Read data from the Excel file
    data = pd.read_csv('data_need_filled.csv')

    # Print column names to verify
    print("Column names:", data.columns)

    # Extract relevant data
    LAPS = data['LAPS'][0]
    TRACK_NAME = data['Track_name'][0]
    TRACK_ID = data['Sno'][0]  # Assuming 'Sno' is the track ID

    # Print the extracted data
    print(f"LAPS: {LAPS}")
    print(f"TRACK_NAME: {TRACK_NAME}")
    print(f"TRACK_ID: {TRACK_ID}")

if __name__ == "__main__":
    main()
