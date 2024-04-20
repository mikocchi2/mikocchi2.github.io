import json
from setup import *

#json db general
def open_db():
    with open('champs.json', 'r') as file:
        data = json.load(file)
        return data
def save_to_db(data):
    with open('champs.json', 'w') as file:
        json.dump(data, file, indent=4)

def reset():
    data = open_db()
     # Iterate through each champion in the database
    for champ in data['champs']:
        # Resetting stats
        champ['total'] = 0
        champ['won'] = 0
        champ['winrate'] = 0.0
        champ['cspm'] = 0
        champ['gpm'] = 0

    save_to_db(data)

#json db maintenance
def restore():  # puni json iz txt, vrv je nepotrebno ako samo imam kopiju json..
    
    def add_champion_to_database(file_path, champ_name):
        # Load the current data from the file
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {"champs": []}  # Initialize if file doesn't exist
        # Check if the champion already exists
        exists = any(champ for champ in data["champs"] if champ["name"] == champ_name)
        if not exists:
            # Champion structure with initial values
            new_champion = {
                "name": champ_name,
                "role": "unknown",  # Assuming role is unknown/undetermined at this point
                "total": 0,
                "won": 0,
                "winrate": 0.0,
                "cspm": 0.0,
                "gpm": 0
            }
            # Add the new champion to the list
            data["champs"].append(new_champion)
            # Save the updated data back to the file
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
            print(f"{champ_name} was added to the database.")
        else:
            print(f"{champ_name} already exists in the database.")
    def add_all_champions_from_file(text_file_path, json_database_path):
        # Open the text file containing the champion names
        with open(text_file_path, 'r') as file:
            champion_names = file.readlines()
        # Trim any newline characters and whitespace from the champion names
        champion_names = [name.strip() for name in champion_names]
        # Call add_champion_to_database for each champion name
        for name in champion_names:
            add_champion_to_database(json_database_path, name)       
    def fix_names():
        data = open_db()  # Assuming this function returns the data correctly
        if 'champs' in data:
            for champ in data['champs']:
                new_name = []
                i = 0
                while i < len(champ['name']):
                    if champ['name'][i] in ["'", " "]:
                        i += 1  # Skip the character
                        if i < len(champ['name']):
                            # Apply case rules based on the previous character
                            if champ['name'][i-1] == "'" or champ['name'][i] in ["'", " "]:
                                new_name.append(champ['name'][i].lower())
                            else:
                                new_name.append(champ['name'][i])
                    else:
                        new_name.append(champ['name'][i])
                    i += 1
                champ['name'] = ''.join(new_name)  # Update the name in the champ dictionary
                # Handle special case renamings
                if champ['name'].lower().replace(" ", "") == 'wukong':
                    champ['name'] = 'MonkeyKing'
                print(f"Processed to {champ['name']}")  # Optional: for debugging
            # Optionally write the modified list back to the file
            with open('champs.json', 'w') as file:
                json.dump(data, file, indent=4)
            print("Data saved to champs.json")
        else:
            print("No 'champs' key in data")
            
    db = 'champs.json'
    source = 'champions.txt'
    add_all_champions_from_file(source, db)
    fix_names()

def add_key_to_all_champs_in_file(key, value):
    
    data = open_db()

    # Add the new key-value pair to each champ
    for champ in data["champs"]:
        champ[key] = value

    save_to_db(data)      
def delete_key_from_all_champs_in_file(key):
    data = open_db()

    # Delete the key from each champ
    for champ in data["champs"]:
        champ.pop(key, None)

    save_to_db(data)

# db work goes here     (lots unfinished)
def update_db(match_id,puuid):
    
    my,enemy = get_teams(match_id,puuid)
    enemy_champs = [player['championName'] for player in enemy]
    me = get_me(get_participants(match_id), puuid)

    print( enemy_champs )

    champs = open_db()
    
    for champ in champs['champs']:
        if champ['name'] in enemy_champs:
            champ['total'] += 1  # Increment games played
            if me['win']:
                champ['won'] += 1  # Increment games won if the match was a win
            champ['winrate'] = champ['won'] / champ['total']

    save_to_db(champs)

