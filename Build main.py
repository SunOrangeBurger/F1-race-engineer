import random
import numpy as np
import pandas as pd
from data_entry import get_track_data
data = pd.read_excel('data_need.xlsx')
print("Columns in the Excel file:", data.columns)  
tracks = data[['Track_name', 'LAP_TIME_SOFT', 'LAP_TIME_MEDIUM', 'LAP_TIME_HARD', 'LAPS']].dropna()

def fitness(pit_stops, tire_compounds, laps, lap_times, pit_stop_time=60):
    pit_stop_time_lost = sum(int(stop) for stop in pit_stops) * pit_stop_time
    soft_degradation = 0.4
    medium_degradation = 0.08
    hard_degradation = 0.05
    degradation_time = 0
    total_time = 0
    for i in range(laps):
        if tire_compounds[i] == 'Soft':
            degradation_time += soft_degradation
        elif tire_compounds[i] == 'Medium':
            degradation_time += medium_degradation
        else:
            degradation_time += hard_degradation
        total_time += lap_times[tire_compounds[i]] + degradation_time
    total_time += pit_stop_time_lost
    if sum(int(stop) for stop in pit_stops) == 0:
        total_time += 100000
    return -total_time

def genetic_algorithm(laps, lap_times, population_size=100, generations=100, mutation_rate=0.01):
    population = []
    for _ in range(population_size):
        pit_stops = [random.randint(0, 1) for _ in range(laps)]
        tire_compounds = [random.choice(['Soft', 'Medium', 'Hard']) for _ in range(laps)]
        while len(set(tire_compounds)) < 2 or sum(pit_stops) == 0:
            pit_stops = [random.randint(0, 1) for _ in range(laps)]
            tire_compounds = [random.choice(['Soft', 'Medium', 'Hard']) for _ in range(laps)]
        population.append((pit_stops, tire_compounds))

    for _ in range(generations):
        fitnesses = [fitness(pit_stops, tire_compounds, laps, lap_times) for pit_stops, tire_compounds in population]
        parents = np.array(population)[np.argsort(fitnesses)].tolist()[-int(population_size / 2):]

        offspring = []
        while len(offspring) < population_size:
            parent1, parent2 = random.sample(parents, 2)
            crossover_point = random.randint(1, laps - 1)
            child1_pit_stops = parent1[0][:crossover_point] + parent2[0][crossover_point:]
            child1_tire_compounds = parent1[1][:crossover_point] + parent2[1][crossover_point:]
            child2_pit_stops = parent2[0][:crossover_point] + parent1[0][crossover_point:]
            child2_tire_compounds = parent2[1][:crossover_point] + parent1[1][crossover_point:]
            while len(set(child1_tire_compounds)) < 2 or sum(map(int, child1_pit_stops)) == 0:
                child1_pit_stops = parent1[0][:crossover_point] + parent2[0][crossover_point:]
                child1_tire_compounds = parent1[1][:crossover_point] + parent2[1][crossover_point:]
            while len(set(child2_tire_compounds)) < 2 or sum(map(int, child2_pit_stops)) == 0:
                child2_pit_stops = parent2[0][:crossover_point] + parent1[0][crossover_point:]
                child2_tire_compounds = parent2[1][:crossover_point] + parent1[1][crossover_point:]
            offspring.append((child1_pit_stops, child1_tire_compounds))
            offspring.append((child2_pit_stops, child2_tire_compounds))

        for i in range(len(offspring)):
            if random.random() < mutation_rate:
                mutation_point = random.randint(0, laps - 1)
                offspring[i][0][mutation_point] = random.choice([0, 1])
                offspring[i][1][mutation_point] = random.choice(['Soft', 'Medium', 'Hard'])
                while len(set(offspring[i][1])) < 2 or sum(map(int, offspring[i][0])) == 0:
                    offspring[i][1][mutation_point] = random.choice(['Soft', 'Medium', 'Hard'])

        population = np.array(offspring)[np.argsort([fitness(pit_stops, tire_compounds, laps, lap_times) for pit_stops, tire_compounds in offspring])].tolist()[:population_size]
    return population

def split_list_on_value(original_list, value):
    sublists = []
    current_sublist = []
    for item in original_list:
        if item == value:
            if current_sublist:
                sublists.append(current_sublist)
            current_sublist = []
        else:
            current_sublist.append(item)
    if current_sublist:
        sublists.append(current_sublist)
    return sublists

def main():
    print("Available tracks:")
    for index, row in tracks.iterrows():
        print(f"{index + 1}: {row['Track_name']}")

    track_choice = int(input("Select a track by number: ")) - 1
    selected_track = tracks.iloc[track_choice]

    LAPS = int(selected_track['LAPS'])
    LAP_TIMES = {
        'Soft': selected_track['LAP_TIME_SOFT'],
        'Medium': selected_track['LAP_TIME_MEDIUM'],
        'Hard': selected_track['LAP_TIME_HARD']
    }

    print(f"Selected Track: {selected_track['Track_name']}")
    print(f"LAPS: {LAPS}")

    global strat_list  
    population = genetic_algorithm(LAPS, LAP_TIMES)
    optimal_pit_stops, optimal_tire_compounds = population[0]  
    split_stints = split_list_on_value(optimal_pit_stops, 1)
    strat_list = []  
    stint_index = 0
    for i in range(len(split_stints)):
        stint_length = len(split_stints[i])
        compound_used = optimal_tire_compounds[stint_index]
        strat_list.append((stint_length, compound_used))
        stint_index += stint_length + 1

    print("Strategy list (stint length, compound used):")
    for stint_length, compound_used in strat_list:
        print(f"Stint Length: {stint_length}, Compound Used: {compound_used}")

    num_pit_stops = sum(map(int, optimal_pit_stops))
    print("Number of pit stops:", num_pit_stops)
    compound_usage = {compound: 0 for compound in ['Soft', 'Medium', 'Hard']}
    for compound in optimal_tire_compounds:
        compound_usage[compound] += 1

    print("Compound usage (laps):")
    for compound, laps in compound_usage.items():
        print(f"{compound}: {laps} laps")

if __name__ == "__main__":
    main()
