# Race Strategy Optimization

## Overview
This project aims to optimize race strategies for Formula 1 using a genetic algorithm. The program simulates various tire strategies and pit stop decisions to minimize total race time based on historical lap data.

## Table of Contents
- [Introduction](#introduction)
- [Algorithm Overview](#algorithm-overview)
- [How It Works](#how-it-works)
- [Data Sources](#data-sources)
- [Usage](#usage)
- [Visualizations](#visualizations)
- [Conclusion](#conclusion)
- [Acknowledgments](#acknowledgments)

## Introduction
The program utilizes the FastF1 API to fetch track data, including lap times for different tire compounds. It then applies a genetic algorithm to explore various strategies, optimizing for the fastest race completion time.

## Algorithm Overview
The core of the program is a genetic algorithm that simulates the evolution of race strategies over multiple generations. The algorithm consists of the following steps:

1. **Initialization**: Generate an initial population of potential strategies, each defined by pit stop timings and tire compounds.
2. **Fitness Evaluation**: Calculate the total race time for each strategy, considering lap times, tire degradation, and pit stop durations.
3. **Selection**: Select the best-performing strategies to serve as parents for the next generation.
4. **Crossover**: Combine pairs of parent strategies to create offspring strategies.
5. **Mutation**: Introduce random changes to some offspring to maintain genetic diversity.
6. **Iteration**: Repeat the evaluation, selection, crossover, and mutation steps for a set number of generations.

## How It Works
1. **Data Retrieval**: The program retrieves track data using the `get_track_data` function, which fetches lap times for different tire compounds and calculates Off-Track Sensitivity (OTS) for each circuit.
   
2. **Fitness Function**: The `fitness` function computes the total time taken for a given strategy, factoring in tire degradation and pit stop times.

3. **Population Generation**: The `genetic_algorithm` function initializes a population of strategies, ensuring that each strategy adheres to constraints (e.g., a maximum of two pit stops).

4. **Evolution Process**: The algorithm iteratively refines the population, selecting the best strategies and generating new ones through crossover and mutation.

5. **Output**: After a specified number of generations, the program outputs the optimal race strategy, including the number of stints, pit stop laps, and tire usage.

## Data Sources
The program relies on historical lap data stored in a CSV file (`data_need_filled.csv`) and uses the FastF1 API to fetch real-time data for the current season. The CSV file contains the following columns:
- `Track_name`: Name of the race track
- `LAP_TIME_SOFT`: Average lap time on soft tires
- `LAP_TIME_MEDIUM`: Average lap time on medium tires
- `LAP_TIME_HARD`: Average lap time on hard tires
- `LAPS`: Total number of laps in the race
- `OTS`: Off-Track Sensitivity value

## Usage
To run the program, follow these steps:
1. Ensure you have the required libraries installed:
   ```bash
   pip install -r requirements.txt
   ```
2. Execute the main script:
   ```bash
   python main.py
   ```
3. Follow the prompts to select a track and view the optimized race strategy.

## Visualizations
The program includes visual representations of the race strategy, showing:
- **Lap Timeline**: Displays the distribution of laps across different tire compounds.
- **Pit Stop Markers**: Indicates when pit stops occur during the race.


## Conclusion
This project demonstrates the application of genetic algorithms in optimizing complex decision-making processes, such as race strategies in Formula 1. By leveraging historical data and simulating various strategies, the program provides insights into the most efficient race approaches.

## Acknowledgments
- [FastF1 API](https://github.com/theOehrly/Fast-F1) for providing the data.
- [NumPy](https://numpy.org/) and [Pandas](https://pandas.pydata.org/) for data manipulation and numerical operations.
- [Matplotlib](https://matplotlib.org/) for visualizations.
