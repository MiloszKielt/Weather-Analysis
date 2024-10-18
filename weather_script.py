import requests
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import argparse
import os
import sys

__API_KEY__ = ""

def parse_arguments():
    """
    Parses command-line arguments to retrieve the name of the city for which 
    weather data is to be fetched.

    Returns:
        argparse.Namespace: Object containing the parsed city name argument.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--city', type=str, required=True)
    return parser.parse_args()

def get_API_data(city: str, f_path: str):
    """
    Fetches weather data from WeatherAPI for the specified city for the past 7 days 
    and saves it as a CSV file.

    Args:
        city (str): The name of the city to get weather data for.
        f_path (str): The file path where the weather data CSV should be saved.

    Raises:
        ConnectionError: If there's an issue with the API connection.
        ValueError: If the data fetched is empty (e.g., due to fetching right after midnight).
    """
    
    # initialization of data structures
    data = {
        'timestamp': [],
        'temp_c': [],
        'wind_kph': [],
        'humidity': []
    }

    date = datetime.datetime.today()

    # Importing data from WeatherAPI day by day for the last 7 days
    for _ in range(0,7):
        try:
            date -= datetime.timedelta(days=1)

            weather_req = f"http://api.weatherapi.com/v1/history.json?key={__API_KEY__}&q={city}&dt={date.strftime('%Y-%m-%d')}"
            weather_json = requests.get(weather_req).json()

            if 'error' in weather_json.keys(): 
                raise ConnectionError
            if weather_json['forecast']['forecastday'] == []: 
                raise ValueError

            # Appending weather data to the data dictionary
            for hour_entry in weather_json['forecast']['forecastday'][0]['hour']:
                data['timestamp'].append(hour_entry['time'])
                data['temp_c'].append(hour_entry['temp_c'])
                data['wind_kph'].append(hour_entry['wind_kph'])
                data['humidity'].append(hour_entry['humidity'])

        except ConnectionError:
            print("Error: ", weather_json['error']['message'])
            sys.exit(0)
        except ValueError:
            print("Error: Error fetching data, please try again")
            sys.exit(0)

    # Convert to dataframe and save to CSV file
    df = pd.DataFrame.from_dict(data)
    df.to_csv(f_path, index=False)

def analyze_weather_data(df: pd.DataFrame):
    """
    Analyzes and prints key weather statistics from the DataFrame.

    Args:
        df (pd.DataFrame): A DataFrame containing the weather data.

    Prints:
        - Average temperature in Celsius.
        - Minimum temperature in Celsius.
        - Maximum temperature in Celsius.
        - Standard deviation of the average temperature.
    """
    print("Average Temperature (in Celsius): {:.3f}".format(df['temp_c'].mean()))
    print("Minimal Temperature (in Celsius): {:.3f}".format(df['temp_c'].min()))
    print("Maximal Temperature (in Celsius): {:.3f}".format(df['temp_c'].max()))
    print("St Dev of Average Temperature: {:.3f}".format(df['temp_c'].std()))

def plot_temperature(df: pd.DataFrame, city:str):
    """
    Plots the average daily temperature from the weather data.

    Args:
        df (pd.DataFrame): A DataFrame containing the weather data.
        city (str): string name of the city relevant to data

    Displays:
        A line plot of the average daily temperatures.
    """
    plt.title(f"Temperature in {city} over last 7 days (in Celsius)")
    plt.xlabel("Date")
    plt.ylabel("Temperature")
    plt.grid()
    plt.plot(df['timestamp'], df['temp_c'])
    plt.show()

if __name__=='__main__':
    """
    Main execution block:
    - Parses arguments to get the city.
    - Fetches and saves weather data for the past 7 days if the file does not exist or is outdated.
    - Loads the weather data, performs analysis, and displays a temperature plot.
    """
    _args = parse_arguments()
    city = _args.city
    f_path = "weather_data/" + city + "_weather_data.csv"

    # Check if file exists and if data is older than 60 minutes
    if(os.path.isfile(f_path)):
        timestamp = datetime.datetime.fromtimestamp(os.path.getmtime(f_path))
        diff_mins = int(round((datetime.datetime.now() - timestamp).total_seconds() / 60))
        if(diff_mins > 60):
            get_API_data(city, f_path)
    else:
        get_API_data(city, f_path)

    # Load, analyze, and plot the weather data
    df = pd.read_csv(f_path, delimiter=',')

    # Sort by timestamp ascending to select dates as one of the axis
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values(by='timestamp', ascending=True)

    analyze_weather_data(df)
    plot_temperature(df, city)