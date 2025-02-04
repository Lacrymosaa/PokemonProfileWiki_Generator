import re

def process_locations(file_path):
    locations = {}

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    pokemon_pattern = r'\| \d+ \|\| \[\[File:[^\|]+\|[^\]]+\]\] ([^|]+) \|\| (.+?)(?=\n|-|$)'

    for line in lines:
        match = re.search(pokemon_pattern, line)
        if match:
            pokemon_name = match.group(1).strip()
            location = match.group(2).strip()

            location_list = [loc.strip() for loc in location.split('\n') if loc.strip()]

            locations[pokemon_name] = location_list

    return locations

def generate_location_output(locations):
    output = []
    for pokemon, locs in locations.items():
        output.append(f"{pokemon},[{', '.join(locs)}]")

    return output

file_path = 'locations.txt'

locations_data = process_locations(file_path)
output_data = generate_location_output(locations_data)

with open('pokemonlocations.txt', 'w', encoding='utf-8') as output_file:
    for entry in output_data:
        output_file.write(entry + '\n')

print("Arquivo pokemonlocations.txt gerado com sucesso!")
