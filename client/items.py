import random
import math
from data_stores import (items_manufacturers,items_body_mods,
items_barrel_mods,items_sight_mods,items_grip_mods,
items_clip_mods,items_rarity_modifiers,items_rarity_list,
items_base_stats,items_part_lib)

# blank variable initializations:
weapon_lst = []

# region manufacturer descriptions
# Dickshot = Massive weapons that break apart, room clearing type weapons like the BFG, high RISKvsREWARD
# Judicium = Few shots big damage / Jakobs, Judicium parts will have additional Crit bonus
# Elidia = Tech/organic with DoT, probably quicker firing that other manus  
# DaBoom = TORGUE basically, slow fire rate to balance the AoE damage from the weapons
# endregion 


class SMG:
    def __init__(self):
        self.weapon_lvl = random.randint(1,6)
        self.weapon_type = 'SMG'
        self.weapon_rarity = random.choice(items_rarity_list)
        self.weapon_part_lib = items_part_lib

        self.base_stats = items_base_stats['SMG']

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
            'damage': (self.base_stats['damage'] * (self.stat_increase_per_lvl['damage+'] * self.weapon_lvl)) * items_rarity_modifiers[self.weapon_rarity],
            'accuracy': math.floor((self.base_stats['accuracy'] + 
                            (1 + (self.stat_increase_per_lvl['accuracy+'] * self.weapon_lvl))) * items_rarity_modifiers[self.weapon_rarity]),
            'clip_count': math.floor((self.base_stats['clip_count'] + 
                            (1 + (self.stat_increase_per_lvl['clip_count+'] * self.weapon_lvl)))* items_rarity_modifiers[self.weapon_rarity]),
            'reload_time': 0.6, # seconds
            'total_ammo': self.base_stats['total_ammo'] + 
                            (1 + ((self.stat_increase_per_lvl['total_ammo+'] * self.weapon_lvl)* items_rarity_modifiers[self.weapon_rarity]))
            }

        for part in ['barrel','body','clip','grip','stock']:
            self.weapon_part_lib[part] = random.choice(items_manufacturers)
        items_manufacturers.append('No Sight')
        self.weapon_part_lib['sight'] = random.choice(items_manufacturers)
        items_manufacturers.remove('No Sight')
        
        self.information = {
            'Weapon Level' : self.weapon_lvl,
            'Weapon Type' : self.weapon_type,
            'Weapon Rarity' : self.weapon_rarity,
            "Weapon Manufacturer" : self.weapon_part_lib['body'],
            "Damage" : int(self.gun_stats['damage']),
            "Accuracy" : self.gun_stats['accuracy'],
            "Clip Size" : self.gun_stats['clip_count'],
            "Reload" : self.gun_stats['reload_time'],
            "Ammo Capacity" : int(self.gun_stats['total_ammo'])
            }
#generates 10 weapons to check for stat changes on weapons with the same levels but different rarities 
# (no part based stat modifiers yet)
# checking the accessibilty of libraries inside libraries
#print()
#print()
#print('Library inside Library test')
#print('___________________________')
#print('DaBoom manufacturer fire rate modifier =  ', body_mods['DaBoom']['fire_rate'])


"""
critical hit formula = (BaseDamage x 2) x (1 + critcal_bonuses)
weapon level bonuses are calculated as part of the BaseDamage (pre-add)
critical_bonuses calculated from weapon parts and character bonuses (post add)

eg: a lvl 5 Judicium Sniper (base damage of 10) with Judicium Barrel and Grip:
10 x 1.25 per level (compounded)
(1.25 x (1.25 x (1.25 x (1.25 x (1.25 x 10))))) = 30.51 (30 BaseDamage [rounded down using !math.floor])

30 x 2 x (1 + 0.5 + 0.2 + 0.1) = critcal hit of 108 (around 3.5x BaseDamage)

the "1" is always used in the post-add to keep bonuses positive otherwise multiplying by 0.x would decrease damage
and if there are no additional bonuses from parts, the damage is multiplied by 1 (no change)

¿how do we trigger critical hits?
 - purely random chance !random.randint(1,40) % 9 == 0:
 - character stat (certain classes have a inherantly higher chance/percentage)
 - weapon stat (possibly more likely with snipers/pistols. less likely with rockets and quick-fire weapons)
 - based off enemy stat (crit damage chance as a percentage !if random.randint(1,100) in Range(1,20): [20% chance]  )
"""  