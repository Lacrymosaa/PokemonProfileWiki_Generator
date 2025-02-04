import os

def parse_pokemon_file(filename="pokemon.txt"):
    pokemon_data = {}
    with open(filename, "r") as file:
        content = file.read().split("#-------------------------------")
        for block in content:
            if block.strip():
                lines = block.strip().splitlines()
                pokemon_info = {}
                for line in lines:
                    if '=' in line:
                        key, value = line.split("=", 1)
                        pokemon_info[key.strip()] = value.strip()
                if pokemon_info:
                    dex_number = lines[0].strip("[]")
                    pokemon_data[dex_number] = pokemon_info
    return pokemon_data

def parse_abilities_file(filename="abilities.txt"):
    abilities = {}
    with open(filename, "r") as file:
        for line in file:
            parts = line.strip().split(",", 3)
            if len(parts) == 4:
                abilities[parts[1].strip()] = parts[2].strip()
    return abilities

def parse_moves_file(filename="moves.txt"):
    moves = {}
    with open(filename, "r") as file:
        for line in file:
            parts = line.strip().split(",", 9)
            if len(parts) > 1:
                moves[parts[1].strip()] = (parts[2].strip(), parts[5].strip())  
    return moves

def parse_locations_file(filename="locations.txt"):
    locations = {}
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                pokemon_name, location_str = line.split(",", 1)
                pokemon_name = pokemon_name.strip()
                locations_list = location_str.strip()[1:-1].split(",")
                locations[pokemon_name] = [location.strip() for location in locations_list]
    return locations

def generate_wiki_page(pokemon_info, abilities, moves, locations, dex_number):
    name = pokemon_info.get("Name", "").capitalize()
    dex_number = dex_number.zfill(4)
    type1 = pokemon_info.get("Type1", "").capitalize()
    type2 = pokemon_info.get("Type2", "").capitalize()
    abilities_list = pokemon_info.get("Abilities", "").split(",")

    abilities_list = [abilities.get(ability.strip(), ability.strip()) for ability in abilities_list]
    hidden_ability = pokemon_info.get("HiddenAbility", "").strip()
    if hidden_ability:
        hidden_ability = abilities.get(hidden_ability, hidden_ability)

    egg_types = pokemon_info.get("Compatibility", "").lower().split(",")
    egg_types = [egg.strip().capitalize() for egg in egg_types]
    egg_types = ", ".join(egg_types)
    
    pokedex_entry = pokemon_info.get("Pokedex", "")
    evolutions = pokemon_info.get("Evolutions", "").split(",")

    wiki_page = f"{{{{Pokedex\n| Name = {name}\n| Dex Number = {dex_number}\n| Type1 = {type1}\n"
    if type2:
        wiki_page += f"| Type2 = {type2}\n"
    wiki_page += f"| Abilities = {', '.join(abilities_list)}\n"
    if hidden_ability:
        wiki_page += f"| Hidden Ability = {hidden_ability}\n" 
    wiki_page += f"| Egg Type = {egg_types}\n}}}}"
    wiki_page += f"{pokedex_entry}\n" 

    if name in locations:
        wiki_page += "=== Locations ===\n"
        for location in locations[name]:
            wiki_page += f"* {location}\n"

    if evolutions and evolutions[0]: 
        wiki_page += "=== Evolution ===\n"
        evo_name, *evo_description = evolutions
        evo_description = " ".join(evo_description).strip()
        wiki_page += f"{{{{Evolve\n| Name={evo_name.capitalize()}\n| Evolution Description = {evo_description}\n}}}}\n"

    level_moves = pokemon_info.get("Moves", "").split(",")
    wiki_page += "=== Level Moves ===\n{| class=\"wikitable\"\n!Level!!Move!!Type\n"
    for i in range(0, len(level_moves), 2):
        level = level_moves[i].strip()
        move = level_moves[i+1].strip()
        move_name, move_type = moves.get(move, (move, "Normal"))
        wiki_page += f"|-\n|{level}||{move_name}||[[File:{move_type.capitalize()}Type.png]]\n"
    wiki_page += "|}\n"

    tutor_moves = pokemon_info.get("TutorMoves", "").split(",")
    if tutor_moves != [""]:
        wiki_page += "=== Tutor Moves ===\n{| class=\"wikitable\"\n!Move!!Type\n"
        for move in tutor_moves:
            move_name, move_type = moves.get(move.strip(), (move.strip(), "Normal"))
            wiki_page += f"|-\n|{move_name}||[[File:{move_type.capitalize()}Type.png]]\n"
        wiki_page += "|}\n"

    egg_moves = pokemon_info.get("EggMoves", "").split(",")
    if egg_moves != [""]:
        wiki_page += "=== Egg Moves ===\n{| class=\"wikitable\"\n!Move!!Type\n"
        for move in egg_moves:
            move_name, move_type = moves.get(move.strip(), (move.strip(), "Normal"))
            wiki_page += f"|-\n|{move_name}||[[File:{move_type.capitalize()}Type.png]]\n"
        wiki_page += "|}\n"
    
    return wiki_page

def save_wiki_page(pokemon_name, wiki_page):
    output_dir = "wiki_pages"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with open(f"{output_dir}/{pokemon_name}.txt", "w") as file:
        file.write(wiki_page)

def main():
    pokemon_data = parse_pokemon_file()
    abilities = parse_abilities_file()
    moves = parse_moves_file()
    locations = parse_locations_file()
    
    for dex_number, pokemon_info in pokemon_data.items():
        wiki_page = generate_wiki_page(pokemon_info, abilities, moves, locations, dex_number)
        save_wiki_page(pokemon_info.get("Name", "").capitalize(), wiki_page)

if __name__ == "__main__":
    main()
