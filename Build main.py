import random
import numpy as np
import pandas as pd
from data_entry import get_track_data
data = pd.read_csv('data_need_filled.csv')
print("Columns in the CSV file:", data.columns)  
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
        # Ensure that the number of pit stops does not exceed 2
        pit_stop_count = random.randint(0, 2)
        pit_stops = [0] * laps
        if pit_stop_count > 0:
            # Avoid placing pit stops on the last lap
            pit_stop_indices = random.sample(range(laps-1), pit_stop_count) 
            for index in pit_stop_indices:
                pit_stops[index] = 1

        tire_compounds = [random.choice(['Soft', 'Medium', 'Hard']) for _ in range(laps)]
        
        # Fix: Create a function to get stint compounds safely
        def get_stint_compounds(pit_stops, tire_compounds):
            compounds = [tire_compounds[0]]  # First stint compound
            
            for i, stop in enumerate(pit_stops):
                if stop == 1 and i+1 < len(tire_compounds):
                    compounds.append(tire_compounds[i+1])
            
            return compounds
        
        # Ensure at least one pit stop and at least 2 different compounds
        while sum(pit_stops) == 0 or len(set(get_stint_compounds(pit_stops, tire_compounds))) < 2:
            # Reinitialize to satisfy constraints
            pit_stop_count = random.randint(1, 2)  # At least one pit stop
            pit_stops = [0] * laps
            
            # Avoid placing pit stops on the last lap
            available_indices = list(range(laps-1))
            if available_indices:  # Make sure there are available indices
                pit_stop_indices = random.sample(available_indices, min(pit_stop_count, len(available_indices)))
                for index in pit_stop_indices:
                    pit_stops[index] = 1
            
            # This ensures we use at least 2 different compounds across our stints
            compounds_to_use = random.sample(['Soft', 'Medium', 'Hard'], 2)
            # Start with a compound
            first_compound = compounds_to_use[0]
            tire_compounds = [first_compound] * laps
            
            # For each pit stop, change to a different compound
            current_compound_idx = 0
            for i, stop in enumerate(pit_stops):
                if stop == 1:
                    current_compound_idx = (current_compound_idx + 1) % len(compounds_to_use)
                    for j in range(i+1, laps):
                        if j < laps - 1 and pit_stops[j] == 1:
                            break
                        tire_compounds[j] = compounds_to_use[current_compound_idx]
                        
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

            # Enforce maximum of 2 pit stops
            child1_pit_stops = [int(stop) for stop in child1_pit_stops]
            child2_pit_stops = [int(stop) for stop in child2_pit_stops]

            child1_pit_stops = enforce_pit_stop_limit(child1_pit_stops)
            child2_pit_stops = enforce_pit_stop_limit(child2_pit_stops)

            # Ensure at least one pit stop if required
            for child_pit_stops in [child1_pit_stops, child2_pit_stops]:
                if sum(child_pit_stops) == 0:
                    random_index = random.randint(0, laps - 1)
                    child_pit_stops[random_index] = 1

            offspring.append((child1_pit_stops, child1_tire_compounds))  # Keeping as tuple
            offspring.append((child2_pit_stops, child2_tire_compounds))  # Keeping as tuple

        # Mutation
        new_offspring = []
        for individual in offspring:
            pit_stops, tire_compounds = individual
            if random.random() < mutation_rate:
                mutation_point = random.randint(0, laps - 1)
                # Toggle pit stop
                pit_stops = pit_stops.copy()  # Make a copy to avoid mutating the original
                pit_stops[mutation_point] = 1 - pit_stops[mutation_point]
                # Ensure pit_stops are integers
                pit_stops = [int(stop) for stop in pit_stops]
                # Enforce pit stop limit after mutation
                pit_stops = enforce_pit_stop_limit(pit_stops)

                # Mutate tire compound
                tire_compounds = tire_compounds.copy()
                tire_compounds[mutation_point] = random.choice(['Soft', 'Medium', 'Hard'])

                # Ensure constraints
                if sum(pit_stops) == 0:
                    random_index = random.randint(0, laps - 1)
                    pit_stops[random_index] = 1
                while len(set(tire_compounds)) < 2:
                    tire_compounds[mutation_point] = random.choice(['Soft', 'Medium', 'Hard'])
                
                # Replace with new tuple
                new_offspring.append((pit_stops, tire_compounds))
            else:
                # No mutation; keep the individual as is
                new_offspring.append(individual)

        offspring = new_offspring

        # Select the next generation
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
def enforce_pit_stop_limit(pit_stops):
    pit_stop_count = sum(pit_stops)
    if pit_stop_count > 2:
        excess = pit_stop_count - 2
        indices = [i for i, stop in enumerate(pit_stops) if stop == 1]
        remove_indices = random.sample(indices, excess)
        for index in remove_indices:
            pit_stops[index] = 0
    return pit_stops
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
    
    # Ensure optimal_pit_stops is a list of integers
    optimal_pit_stops = [int(stop) for stop in optimal_pit_stops]  # Convert to integers if necessary
    
    # Fix the stint calculation logic
    strat_list = []
    current_compound = optimal_tire_compounds[0]
    current_stint_length = 0  # Start at 0 to count laps correctly
    
    # Build stints correctly
    for i in range(LAPS):
        current_stint_length += 1  # Count the current lap
        if optimal_pit_stops[i] == 1:  # Check if this is a pit stop
            # End the previous stint
            if current_stint_length > 0:  # Only add if there's a stint to add
                strat_list.append((current_stint_length, current_compound))  # Add the stint before the pit stop
            # Start a new stint
            current_compound = optimal_tire_compounds[i]  # Change compound after pit stop
            current_stint_length = 0  # Reset stint length for the new stint
            
    # Add the final stint if there are laps left
    if current_stint_length > 0:
        strat_list.append((current_stint_length, current_compound))
    
    # Add code to identify the pit stop laps
    pit_stop_laps = [i + 1 for i, stop in enumerate(optimal_pit_stops) if stop == 1]
    
    # Basic strategy information
    print("\n--- RACE STRATEGY SUMMARY ---")
    print("Strategy list (stint length, compound used):")
    for stint_number, (stint_length, compound_used) in enumerate(strat_list):
        print(f"Stint {stint_number + 1}: {stint_length} laps on {compound_used}")

    num_pit_stops = sum(optimal_pit_stops)
    print("Number of stints:", num_pit_stops)
    print("Pit stop laps:", pit_stop_laps)
    
    compound_usage = {compound: 0 for compound in ['Soft', 'Medium', 'Hard']}
    for stint_length, compound in strat_list:
        compound_usage[compound] += stint_length

    print("Compound usage (laps):")
    for compound, laps in compound_usage.items():
        if laps > 0:  # Only show compounds actually used
            print(f"{compound}: {laps} laps")
    
    # Enhanced visual representation
    print("\n--- RACE STRATEGY VISUALIZATION ---")
    
    # Color mapping for tire compounds
    compound_symbols = {'Soft': 'S', 'Medium': 'M', 'Hard': 'H'}
    
    # Print lap numbers timeline
    print("LAP:", end=" ")
    current_lap = 1
    for i, (stint_length, _) in enumerate(strat_list):
        end_lap = current_lap + stint_length - 1
        print(f"{current_lap:2d}-{end_lap:<2d}", end="")
        current_lap = end_lap + 1
        if i < len(strat_list) - 1:
            print(" | ", end="")
    print()
    
    # Print visual tire stint bars
    race_width = 60  # Adjust based on your terminal width
    total_race_laps = sum(stint[0] for stint in strat_list)
    
    print("TIRES:  ", end="")
    for i, (stint_length, compound) in enumerate(strat_list):
        # Calculate how many characters to use for this stint
        stint_width = max(int((stint_length / total_race_laps) * race_width), 1)
        stint_display = compound_symbols[compound] * stint_width
        print(f"{stint_display}", end="")
        if i < len(strat_list) - 1:
            print(" P ", end="")  # P for pit stop
    print("\n")
    
    # Add pit stop markers on a separate line
    print("PITS:   ", end="")
    current_lap = 1
    for i in range(total_race_laps):
        if current_lap in pit_stop_laps:
            print("P", end="")
        else:
            print(" ", end="")
        current_lap += 1
    print()
    
    # Alternative graphical representation
    print("STRATEGY CHART:")
    print("START " + "=" * 40 + " FINISH")
    
    for compound in ['Soft', 'Medium', 'Hard']:
        if compound_usage[compound] > 0:  # Only show compounds actually used
            print(f"{compound:6s} |", end="")
            current_lap = 1
            for stint_length, stint_compound in strat_list:
                # Print tire usage bar
                bar = ""
                if stint_compound == compound:
                    bar = "█" * max(int((stint_length / total_race_laps) * 40), 1)
                else:
                    bar = " " * max(int((stint_length / total_race_laps) * 40), 1)
                print(f"{bar}", end="")
                current_lap += stint_length
            print("|")
    
    print("\nLAP     |", end="")
    markers = []
    current_lap = 0
    for stint_length, _ in strat_list:
        current_lap += stint_length
        position = int((current_lap / total_race_laps) * 40)
        markers.append((position, current_lap))
    
    for i in range(40):
        marked = False
        for pos, lap in markers:
            if i == pos - 1:
                print(f"{lap}", end="")
                marked = True
                break
        if not marked:
            print(" ", end="")
    print("|")

if __name__ == "__main__":
    main()
