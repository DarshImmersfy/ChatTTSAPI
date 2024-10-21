import copy, random

from src import schema
from src import preset

def choose_voice(request: schema.AllocationRequest):
    print("Hello")
    male_voice_list = preset.MALE_VOICE_LIST.copy()
    female_voice_list = preset.FEMALE_VOICE_LIST.copy()
    
    character_dict = {}     # {name: voice}
    for character_name, character_pack in request.character_list.items():
        if character_pack.get("gender").lower() == "male":
            character_dict[character_name] = random.choice(male_voice_list).replace(".txt","")
            male_voice_list.remove(character_dict[character_name])
            
        elif character_pack.get("gender").lower() == "female":
            character_dict[character_name] = random.choice(female_voice_list).replace(".txt","")
            female_voice_list.remove(character_dict[character_name])
    
    character_dict["narrator"] = random.choice(preset.NARRATION_VOICE_LIST)
    return character_dict