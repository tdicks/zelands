import random
import math
from data_stores import (items_manufacturers,items_body_mods,
items_barrel_mods,items_sight_mods,items_grip_mods,items_stock_mods,
items_clip_mods,items_rarity_modifiers,items_rarity_list,
items_base_stats,items_part_lib,lvl_stat_increase)

# blank variable initializations:
weapon_lst = []

# region manufacturer descriptions
# Dickshot = Massive weapons that break apart, room clearing type weapons like the BFG, high RISKvsREWARD
# Judicium = Few shots big damage / Jakobs, Judicium parts will have additional Crit bonus
# Elidia = Tech/organic with DoT, probably quicker firing that other manus  
# DaBoom = TORGUE basically, slow fire rate to balance the AoE damage from the weapons
# endregion 

def item_information_generator(self, type='basic'):
    if type.lower() == 'full':
        return {
            'Weapon Level' : self.weapon_lvl,
            'Weapon Type' : self.weapon_type,
            'Weapon Rarity' : self.weapon_rarity,
            "Weapon Manufacturer" : self.weapon_part_lib['body'],
            "Damage" : int(self.gun_stats['damage']),
            "Crit": float(self.gun_stats['critical_hit']),
            "Barrel Count": int(self.gun_stats['barrel_count']),
            "Accuracy" : self.gun_stats['accuracy'],
            "Fire Rate": round(self.gun_stats['fire_rate'], 2),
            "Pellet Speed": self.gun_stats['pellet_speed'],
            "Clip Size" : self.gun_stats['clip_count'],
            "Reload" : self.gun_stats['reload_time'],
            "Ammo Capacity" : int(self.gun_stats['total_ammo'])
            }
    else:
        return {
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


def gun_stats_generator(self):
        return {
            'damage': ((self.base_stats['damage'] * (self.stat_increase_per_lvl['damage+'] * self.weapon_lvl)) * items_rarity_modifiers[self.weapon_rarity]) + self.additions[2] ,
            'barrel_count': self.additions[4],
            'accuracy': math.floor(((self.base_stats['accuracy'] + 
                            (1 + (self.stat_increase_per_lvl['accuracy+'] * self.weapon_lvl))) * items_rarity_modifiers[self.weapon_rarity])) + self.additions[0],
            'clip_count': (math.floor((self.base_stats['clip_count'] + 
                            (1 + (self.stat_increase_per_lvl['clip_count+'] * self.weapon_lvl)))* items_rarity_modifiers[self.weapon_rarity])) + self.additions[7],
            'reload_time': round(((self.base_stats['reload_time'] + 
                            (0.5 + (0.1 * self.weapon_lvl))) / items_rarity_modifiers[self.weapon_rarity]) + self.additions[3], 2),
            'total_ammo': math.floor(self.base_stats['total_ammo'] + 
                            (1 + ((self.stat_increase_per_lvl['total_ammo+'] * self.weapon_lvl)* items_rarity_modifiers[self.weapon_rarity]))+ self.additions[7] * 3),
            'critical_hit': round(self.base_stats['crit_damage_modifier'] + self.additions[5],2),
            'pellet_speed': self.base_stats['pellet_speed'] + self.additions[6],
            'fire_rate': round(self.base_stats['fire_rate'] + self.additions[1],1) * 10
            }


def part_selection(self,items_manus):
    for part in ['barrel','body','clip','grip','stock']:
        self.weapon_part_lib[part] = random.choice(items_manus)
    items_manus.append('No Sight')
    self.weapon_part_lib['sight'] = random.choice(items_manus)
    items_manus.remove('No Sight')
    return self.weapon_part_lib


def part_additions(self):
    vals = []
    accuracy = fire_rate = damage = reload_time = 0
    barrel_count = critical_hit = pellet_speed = total_ammo = 0
    for number,part in enumerate(self.weapon_part_lib):
        if number == 0:
            accuracy += items_barrel_mods[self.weapon_part_lib[part]]['accuracy'] 
            damage += items_barrel_mods[self.weapon_part_lib[part]]['damage']
            pellet_speed += items_barrel_mods[self.weapon_part_lib[part]]['pellet_speed']
            if self.weapon_type == 'Shotgun':
                barrel_count += items_barrel_mods[self.weapon_part_lib[part]]['barrel_count']
            else:
                barrel_count = 1

            if self.weapon_part_lib[part] == 'Judicium':
                critical_hit += items_barrel_mods[self.weapon_part_lib[part]]['critical_hit']
            else:
                pass
            
        if number == 1:
            fire_rate += items_body_mods[self.weapon_part_lib[part]]['fire_rate'] 
            damage += items_body_mods[self.weapon_part_lib[part]]['damage']
            reload_time += items_body_mods[self.weapon_part_lib[part]]['reload_time']

            if self.weapon_part_lib[part] == 'Judicium':
                critical_hit += items_body_mods[self.weapon_part_lib[part]]['critical_hit']
            else:
                pass

        if number == 2:
            reload_time += items_clip_mods[self.weapon_part_lib[part]]['reload_time'] 
            total_ammo += items_clip_mods[self.weapon_part_lib[part]]['total_ammo']

        if number == 3:
            fire_rate += items_grip_mods[self.weapon_part_lib[part]]['fire_rate'] 
            
            if self.weapon_part_lib[part] == 'Judicium':
                critical_hit += items_grip_mods[self.weapon_part_lib[part]]['critical_hit']
            else:
                pass

        if number == 4:
            accuracy += items_sight_mods[self.weapon_part_lib[part]]['accuracy']

        if number == 5:
            accuracy += items_stock_mods[self.weapon_part_lib[part]]['accuracy']

    return accuracy,fire_rate,damage,reload_time,barrel_count,critical_hit,pellet_speed,total_ammo


def all_generation(self):
    self.weapon_part_lib = part_selection(self,items_manufacturers)
    self.additions = part_additions(self)
    self.gun_stats = gun_stats_generator(self)
    if self.gun_stats['accuracy'] > 90:
        self.gun_stats['accuracy'] = 100 - random.randint(11,26)
    self.information = item_information_generator(self)
    self.full_info = item_information_generator(self,'full')


class All_Weapons:
    def __init__(self):
        self.weapon_lvl = random.randint(1,6)
        self.weapon_rarity = random.choice(items_rarity_list)
        self.weapon_part_lib = items_part_lib


class AssaultRifle(All_Weapons):
    def __init__(self):
        All_Weapons.__init__(self)
        self.weapon_type = 'ASR'
        self.base_stats = items_base_stats[self.weapon_type]
        self.stat_increase_per_lvl = lvl_stat_increase[self.weapon_type]

        self.weapon_type = 'Assault Rifle'
        all_generation(self)


class SMG(All_Weapons):
    def __init__(self):
        All_Weapons.__init__(self)
        self.weapon_type = 'SMG'
        self.base_stats = items_base_stats[self.weapon_type]
        self.stat_increase_per_lvl = lvl_stat_increase[self.weapon_type]

        all_generation(self)


class Pistol(All_Weapons):
    def __init__(self):
        All_Weapons.__init__(self)
        self.weapon_type = 'PSTL'
        self.base_stats = items_base_stats[self.weapon_type]
        self.stat_increase_per_lvl = lvl_stat_increase[self.weapon_type]

        self.weapon_type = 'Pistol'
        all_generation(self)


class Sniper(All_Weapons):
    def __init__(self):
        All_Weapons.__init__(self)
        self.weapon_type = 'SNPR'
        self.base_stats = items_base_stats[self.weapon_type]
        self.stat_increase_per_lvl = lvl_stat_increase[self.weapon_type]

        self.weapon_type = 'Sniper'
        all_generation(self)


class Shotgun(All_Weapons):
    def __init__(self):
        All_Weapons.__init__(self)
        self.weapon_type = 'SHOT'
        self.base_stats = items_base_stats[self.weapon_type]
        self.stat_increase_per_lvl = lvl_stat_increase[self.weapon_type]
        self.pellet_count = random.randint(7,14)

        self.weapon_type = 'Shotgun'
        all_generation(self)
        self.information['Damage'] = (self.information['Damage'], self.pellet_count)
        self.full_info['Damage'] = self.information['Damage']


class Rocket(All_Weapons):
    def __init__(self):
        All_Weapons.__init__(self)
        self.weapon_type = 'RCKT'
        self.base_stats = items_base_stats[self.weapon_type]
        self.stat_increase_per_lvl = lvl_stat_increase[self.weapon_type]
        self.weapon_type = 'Rocket Launcher'

        all_generation(self)



#generates 10 weapons to check for stat changes on weapons with the same levels but different rarities 
# (no part based stat modifiers yet)

gun = random.choice([Pistol(),SMG(),AssaultRifle(),Shotgun(),Sniper(),Rocket()])

print("Basic Information   :")
for line, val in gun.information.items():
    print(line,val)
print('-' * 50)
print('Full information   :')
for line, val in gun.full_info.items():
    print(line,val)



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