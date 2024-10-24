import random
import numpy as np
import itertools


def constant_with_user_input():
    LAPS = int(input("Enter the number of laps: "))
    TRACK_NAME = input("Enter the track name: ")
    TRACK_ID = int(input("Enter the track ID: "))
    return LAPS, TRACK_NAME, TRACK_ID

def fitness(pit_stops, tire_compounds, laps, track_name, track_id, pit_stop_time=20):
    pit_stop_time_lost = sum(int(stop) for stop in pit_stops) * pit_stop_time
    soft_degradation = 0.08
    medium_degradation = 0.05
    hard_degradation = 0.03
    degradation_time = 0
    for i in range(laps):
        if tire_compounds[i] == 'Soft':
            degradation_time += soft_degradation
        elif tire_compounds[i] == 'Medium':
            degradation_time += medium_degradation
        else:
            degradation_time += hard_degradation
    pit_stop_time_lost = sum(int(stop) for stop in pit_stops) * pit_stop_time
    total_time = 0
    for i in range(laps):
        if tire_compounds[i] == 'Soft':
            total_time += 90
        elif tire_compounds[i] == 'Medium':
            total_time += 92
        else:
            total_time += 95
    total_time += degradation_time + pit_stop_time_lost
    if sum(int(stop) for stop in pit_stops) == 0:
        total_time += 100000
    return -total_time

def genetic_algorithm(laps, track_name, track_id, population_size=100, generations=100, mutation_rate=0.01):
    population = []
    for _ in range(population_size):
        pit_stops = [random.randint(0, 1) for _ in range(laps)]
        tire_compounds = [random.choice(['Soft', 'Medium', 'Hard']) for _ in range(laps)]
        population.append((pit_stops, tire_compounds))

    for _ in range(generations):
        fitnesses = [fitness(pit_stops, tire_compounds, laps, track_name, track_id) for pit_stops, tire_compounds in population]
        parents = np.array(population)[np.argsort(fitnesses)].tolist()[-int(population_size / 2):]

        offspring = []
        while len(offspring) < population_size:
            parent1, parent2 = random.sample(parents, 2)
            crossover_point = random.randint(1, laps
 - 1)
            child1_pit_stops = parent1[0][:crossover_point] + parent2[0][crossover_point:]
            child1_tire_compounds = parent1[1][:crossover_point] + parent2[1][crossover_point:]
            child2_pit_stops = parent2[0][:crossover_point] + parent1[0][crossover_point:]
            child2_tire_compounds = parent2[1][:crossover_point] + parent1[1][crossover_point:]
            offspring.append((child1_pit_stops, child1_tire_compounds))
            offspring.append((child2_pit_stops, child2_tire_compounds))

        for i in range(len(offspring)):
            if random.random() < mutation_rate:
                mutation_point = random.randint(0, laps - 1)
                offspring[i][0][mutation_point] = random.choice([0, 1])
                offspring[i][1][mutation_point] = random.choice(['Soft', 'Medium', 'Hard'])

        population = np.array(offspring)[np.argsort([fitness(pit_stops, tire_compounds, laps, track_name, track_id) for pit_stops, tire_compounds in offspring])].tolist()[:population_size]
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
    LAPS, TRACK_NAME, TRACK_ID = constant_with_user_input()
    optimal_pit_stops, _ = genetic_algorithm(LAPS, TRACK_NAME, TRACK_ID)[0]
    print("The optimal pit stop strategy is:", optimal_pit_stops)
    split_stints = split_list_on_value(optimal_pit_stops, "1")
    strat_list=[]
    for i in range(len(split_stints)):
        if len(split_stints[i])>0 and len(split_stints[i])<15:
            strat_list.append("soft")
        elif len(split_stints[i])>15 and len(split_stints[i])<30:
            strat_list.append("medium")
        else:
            strat_list.append("hard")

    print(strat_list)
if __name__ == "__main__":
    main()
    
global optimal_pit_stops
global strat_list
LAPS, TRACK_NAME, TRACK_ID = constant_with_user_input()
optimal_pit_stops, _ = genetic_algorithm(LAPS, TRACK_NAME, TRACK_ID)[0]
split_stints = split_list_on_value(optimal_pit_stops, "1")
strat_list=[]
for i in range(len(split_stints)):
    if len(split_stints[i])>0 and len(split_stints[i])<15:
            strat_list.append("soft")
    elif len(split_stints[i])>15 and len(split_stints[i])<30:
            strat_list.append("medium")
    else:
            strat_list.append("hard")


