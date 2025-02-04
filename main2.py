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
                    name = pokemon_info.get("Name", "").upper()
                    pokemon_data[name] = pokemon_info
    return pokemon_data
def parse_pokemon2_file(filename="pokemon2.txt"):
    alt_forms_data = {}
    with open(filename, "r") as file:
        content = file.read().split("#-------------------------------")
        for block in content:
            if block.strip():
                lines = block.strip().splitlines()
                alt_form_info = {}
                for line in lines:
                    if '=' in line:
                        key, value = line.split("=", 1)
                        alt_form_info[key.strip()] = value.strip()
                if alt_form_info:
                    name_line = lines[0].strip("[]")
                    base_name = name_line.split(",")[0].strip().upper()
                    alt_form_info["BaseName"] = base_name
                    alt_forms_data[base_name] = alt_form_info
    return alt_forms_data

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

def generate_alt_form_wiki_page(alt_form_info, base_pokemon_info, abilities, moves, locations):
    base_name = alt_form_info.get("BaseName", "").capitalize()
    form_name = alt_form_info.get("FormName", "").split()
    form_name = form_name[0].capitalize() if form_name else ""
    name = f"{form_name} {base_name}"
    dex_number = base_pokemon_info.get("DexNumber", "").zfill(4)
    type1 = alt_form_info.get("Type1", base_pokemon_info.get("Type1", "")).capitalize()
    type2 = alt_form_info.get("Type2", base_pokemon_info.get("Type2", "")).capitalize()

    abilities_list = alt_form_info.get("Abilities", base_pokemon_info.get("Abilities", "")).split(",")
    abilities_list = [abilities.get(ability.strip(), ability.strip()) for ability in abilities_list if ability.strip()]
    
    hidden_ability = alt_form_info.get("HiddenAbility", base_pokemon_info.get("HiddenAbility", "")).strip()
    if hidden_ability and hidden_ability not in abilities_list:  
        hidden_ability = abilities.get(hidden_ability, hidden_ability)

    egg_types = base_pokemon_info.get("Compatibility", "").lower().split(",")
    egg_types = [egg.strip().capitalize() for egg in egg_types]
    egg_types = ", ".join(egg_types)

    pokedex_entry = alt_form_info.get("Pokedex", "")

    wiki_page = f"{{{{Pokedex\n| Name = {name}\n| Dex Number = {dex_number}\n| Type1 = {type1}\n"
    if type2:
        wiki_page += f"| Type2 = {type2}\n"
    wiki_page += f"| Abilities = {', '.join(abilities_list)}\n"
    if hidden_ability:
        wiki_page += f"| Hidden Ability = {hidden_ability}\n"  
    wiki_page += f"| Egg Type = {egg_types}\n}}}}"
    wiki_page += f"{pokedex_entry}\n"  

    if base_name in locations:
        wiki_page += "=== Locations ===\n"
        for location in locations[base_name]:
            wiki_page += f"* {location}\n"

    level_moves = alt_form_info.get("Moves", "").split(",")
    wiki_page += "=== Level Moves ===\n{| class=\"wikitable\"\n!Level!!Move!!Type\n"
    for i in range(0, len(level_moves) - 1, 2):  # Garante que não tente acessar um índice inexistente
        level = level_moves[i].strip()
        move = level_moves[i + 1].strip()
        move_name, move_type = moves.get(move, (move, "Normal"))
        wiki_page += f"|-\n|{level}||{move_name}||[[File:{move_type.capitalize()}Type.png]]\n"
    wiki_page += "|}\n"

    tutor_moves = alt_form_info.get("TutorMoves", "").split(",")
    if tutor_moves != [""]:
        wiki_page += "=== Tutor Moves ===\n{| class=\"wikitable\"\n!Move!!Type\n"
        for move in tutor_moves:
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
    base_pokemon_data = parse_pokemon_file()
    alt_forms_data = parse_pokemon2_file()
    abilities = parse_abilities_file()
    moves = parse_moves_file()
    locations = parse_locations_file()

    for base_name, alt_form_info in alt_forms_data.items():
        base_pokemon_info = base_pokemon_data.get(base_name, {})
        if base_pokemon_info: 
            wiki_page = generate_alt_form_wiki_page(alt_form_info, base_pokemon_info, abilities, moves, locations)
            save_wiki_page(alt_form_info.get("FormName", "Unknown") + " " + base_name.capitalize(), wiki_page)
        else:
            print(f"Aviso: Não encontrado Pokémon base para {base_name}")

if __name__ == "__main__":
    main()
