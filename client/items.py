import random
import math
manufacturers = ['Dickshot','Judicium','Elidia','DaBoom']
weapon_lst = []
# region manufacturer descriptions
# Dickshot = Massive weapons that break apart, room clearing type weapons like the BFG
# Judicium = Few shots big damage / Jakobs, Judicium parts will have additional Crit bonus
# Elidia = Tech/organic with DoT, probably quicker firing that other manus  
# DaBoom = TORGUE basically, slow fire rate to balance the AoE damage from the weapons
# endregion 

body_mods = {
    'DaBoom': {
        'fire_rate': -1.2,
        'damage': 4,
        'reload_time': 0.3 # addition from RL time 
        },
    'Dickshot': {
        'fire_rate': -2.2,
        'damage': 8,
        'reload_time': 1.7 # multiplier
        },
    'Elidia': {
        'fire_rate': 1,
        'reload_time': -0.2 # subtraction from RL time
        },
    'Judicium': {
        'fire_rate': -1.2,
        'damage': 2,
        'Critical_hit': 1.5 # multiplier
        }
    }

rarity_modifiers = {
    'white': 1,
    'green': 1.2,
    'blue': 1.4,
    'purple': 1.6,
    'gold': 1.8
}

class SMG:
    def __init__(self):
        self.weapon_lvl = random.randint(1,6)
        self.weapon_type = 'SMG'
        self.weapon_rarity = random.choice(['white','green','blue','purple','gold'])
        self.weapon_part_lib = {
            'barrel': '',
            'body': '',
            'clip': '',
            'grip': '',
            'sight': '',
            'stock': ''
            }

        self.base_stats = {
            'damage': 4,
            'fire_rate': 6, # shots per second#
            'accuracy': 40, #percent
            'clip_count': 32,
            'reload_time': 0.6, # seconds
            'total_ammo': 640,
            'crit_damage_modifier': 0.5
            }

        self.stat_increase_per_lvl = {
            'damage+': 1.25,
            'fire_rate': 1, # does not increase by level only increased by 'body' part modifiers
            'accuracy+': 0.1,  
            'clip_count+': 0.5,
            'reload_time': 1, # does not increase only increased by 'clip' part modifiers
            'total_ammo+': 2,
            'crit_damage_modifier': 1 # only increased by certain weapon parts
            }

        self.gun_stats = {
            'damage': (self.base_stats['damage'] * (self.stat_increase_per_lvl['damage+'] * self.weapon_lvl)) * rarity_modifiers[self.weapon_rarity],
            'accuracy': math.floor((self.base_stats['accuracy'] + 
                            (1 + (self.stat_increase_per_lvl['accuracy+'] * self.weapon_lvl))) * rarity_modifiers[self.weapon_rarity]),
            'clip_count': math.floor((self.base_stats['clip_count'] + 
                            (1 + (self.stat_increase_per_lvl['clip_count+'] * self.weapon_lvl)))* rarity_modifiers[self.weapon_rarity]),
            'reload_time': 0.6, # seconds
            'total_ammo': self.base_stats['total_ammo'] + 
                            (1 + ((self.stat_increase_per_lvl['total_ammo+'] * self.weapon_lvl)* rarity_modifiers[self.weapon_rarity]))
            }
        

        print(f"Weapon Level =  {self.weapon_lvl}")
        print(f"Type =  {self.weapon_type}")
        print(f"Rarity = {self.weapon_rarity}")
        for part in ['barrel','body','clip','grip','stock']:
            self.weapon_part_lib[part] = random.choice(manufacturers)
        manufacturers.append('No Sight')
        self.weapon_part_lib['sight'] = random.choice(manufacturers)
        print(f"manufacturer =  {self.weapon_part_lib['body']}")
        for part in self.weapon_part_lib:
            print(f'weapon {part} =  {self.weapon_part_lib[part]}')
        for stat in ['damage','accuracy','clip_count','reload_time','total_ammo']:
            print(f'{stat}  =  {self.gun_stats[stat]}')
        print()
        print()

#generates 10 weapons to check for stat changes on weapons with the same levels but different rarities 
# (no part based stat modifiers yet)
for x in range(10):
    smg1 = SMG()

# checking the accessibilty of libraries inside libraries
#print()
#print()
#print('Library inside Library test')
#print('___________________________')
#print('DaBoom manufacturer fire rate modifier =  ', body_mods['DaBoom']['fire_rate'])

