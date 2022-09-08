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
        'reload_time': 0.3 # addition to ReLoad time 
        },
    'Dickshot': {
        'fire_rate': -2.2,
        'damage': 8,
        'reload_time': 1.7 # multiplier
        },
    'Elidia': {
        'fire_rate': 1,
        'reload_time': -0.2 # subtraction to Reload time
        },
    'Judicium': {
        'fire_rate': -1.2,
        'damage': 2,
        'Critical_hit': 0.5 # multiplier
        }
    }

barrel_mods = {
    'DaBoom': {
        'accuracy': -2.5, # %
        'damage': 1.1,
        'pellet_speed': -2, # big bullets go slow
        'barrel_count' : 2 
        },
    'Dickshot': {
        'accuracy': -1, # %
        'damage': 1.4,
        'pellet_speed': -4, # big bullets go slow
        'barrel_count' : 1
        },
    'Elidia': {
        'accuracy': +5, # %
        'pellet_speed': +3,
        'barrel_count' : 4 # subtraction from RL time
        },
    'Judicium': {
        'accuracy': +2.5, # %
        'pellet_speed': +5,
        'critical_hit': 0.2, # multiplier
        'barrel_count': 3
        }
    }

sight_mods = {
    'DaBoom': {
        'accuracy': +2.5, # %
        },

    'Dickshot': {
        'accuracy': +1.5, # %
        },

    'Elidia': {
        'accuracy': +10, # %
        },
    'Judicium': {
        'accuracy': +5, # %
        }
    }

grip_mods = {
    'DaBoom' : {
        'fire_rate': +1.1 
        },

    'Dickshot': {
        'fire_rate': +0.8, # %
        },

    'Elidia': {
        'fire_rate': +3, # %
        },
    'Judicium': {
        'fire_rate': +1.5, # %
        'critical_hit': 0.1
        }
    }

clip_mods = {
    'DaBoom' : {
        'reload_time': +0.2,
        'total_ammo' : +10
        },

    'Dickshot': {
        'reload_time': +0.4, # %
        'total_ammo': -5
        },

    'Elidia': {
        'reload_time': -0.3, # %
        'total_ammo': +14
        },

    'Judicium': {
        'reload_time': -0.1, # %
        'total_ammo': +5
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
for x in range(1):
    smg1 = SMG()

print(smg1.weapon_rarity)
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