# data stores for various .py files

#used within level.py

level_tile_lib = {
    'layout1': ['X2XX1',
                'X0X67',
                'X345X',
                'XXX8X'],

    'layout2': ['XX456',
                'X23X7',
                '01XX8',
                'XXXXX'],
                        
    'layout3': ['XXXXX',
                '3102X',
                '6XX4X',
                'XX857'],

    'layout4': ['XXXXX',
                'XX3X8',
                'XX6X5',
                '12074'],

    'layout5': ['045XX',
                'XX2XX',
                'X67XX',
                'XX183'],

    'layout6': ['XX613',
                'XXX8X',
                'XX27X',
                '045XX'],

    'layout7': ['XXXXX',
                '847X3',
                '1X650',
                'XXXX2'],

    'layout8': ['XXXXX',
                '047X3',
                '1X658',
                'XXXX2'],

    'layout9': ['XX603',
                'XXX1X',
                'XX27X',
                '845XX'],
    
    'layout10': ['64103',
                 '5XXXX',
                 '72XXX',
                 '8XXXX'],

    'layout11': ['XXX1X',
                 'X234X',
                 'X5X0X',
                 '87X6X'],
    
    'layout12': ['XX63X',
                 'XX1XX',
                 'X2075',
                 'XX4X8'],

    'layout13': ['XX6XX',
                 'X01XX',
                 'XX375',
                 'X24X8']
                        }

# used within items.py

items_manufacturers = ['Dickshot','Judicium','Elidia','DaBoom']

items_rarity_list = ['white','green','blue','purple','gold']

items_body_mods = {
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

items_barrel_mods = {
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

items_sight_mods = {
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

items_grip_mods = {
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

items_clip_mods = {
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

items_rarity_modifiers = {
    'white': 1,
    'green': 1.2,
    'blue': 1.4,
    'purple': 1.6,
    'gold': 1.8
}

items_base_stats = {
    'SMG': {
        'damage': 4,
        'fire_rate': 6, # shots per second#
        'accuracy': 40, #percent
        'clip_count': 32,
        'reload_time': 0.6, # seconds
        'total_ammo': 640,
        'crit_damage_modifier': 0.5
        } 
    }

items_part_lib = {
            'barrel': '',
            'body': '',
            'clip': '',
            'grip': '',
            'sight': '',
            'stock': ''
            }