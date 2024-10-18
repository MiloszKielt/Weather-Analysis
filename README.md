# Weather Data Analysis Script

## Introduction

This Python script fetches, analyzes, and visualizes historical weather data for a given city using the WeatherAPI. It retrieves weather data for the past 7 days and provides statistics, including average, minimum, and maximum temperatures. Additionally, the script generates a temperature trend plot.

## Features

- Fetches historical weather data for the past 7 days from WeatherAPI.
- Saves the weather data as a CSV file.
- Caches the recently downloaded data to prevent unnecessary API usage
- Analyzes key weather metrics (average, minimum, maximum temperatures, and temperature standard deviation).
- Plots the temperature change over the last 7 days.

## Requirements

To run this script, you need the following Python packages:

- `requests`
- `matplotlib`
- `pandas`
- `argparse`

As well as create your own account at [WeatherAPI](www.weatherapi.com) and initialize your API key

You can install the required dependencies by running:

```bash
pip install requests matplotlib pandas argparse
```


## Design Choices

- Usage of libraries:
    - pandas: ease and simplicity of analysing numerical data, and saving/reading csv files built into the package
    - argparse: very nice library for creating named cmd arguments for python scripts
    - requests: basic library for HTTP communication, used to connect with WeatherAPI
    - matplotlib: well-known library used for plotting data, here it fulfills the same role, helping to visualize the temperature trend.


## How to Use

- Ensure that you have an active Internet connection
- Clone the repository or download the script to your local machine.
- Ensure you have installed the necessary Python packages (see Requirements).
- Provide the ```__API_KEY__``` variable with string value of your own API Key
- Run the script from the command line with the city name as an argument.

## Example Usage

```bash
python weather_script.py --city "Warsaw"
```

## Argumemnts

- ```--city``` / ```-c``` : Name of the city you want to fetch the data for **(required)**

## Output

- CSV file saved in the folder ```weather_data```, under the name ```<CITY_NAME>_weather_data.csv```
- Analysis: the script will print-out relevant analysis of the data in the console
- Temperature Plot: A line plot of average daily temperature for the last 7 days of given location

## Example output

```bash
Average Temperature (in Celsius): 12.563
Minimal Temperature (in Celsius): 9.200
Maximal Temperature (in Celsius): 16.400
St Dev of Average Temperature: 2.512
```

## Error Handling

- In case of error on the API side, the script will print out the releevant error message informing user aqbout the problem
