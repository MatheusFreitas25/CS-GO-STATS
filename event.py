import re


class Event:
    def __init__(self, txt, lnum, moment, mapnumber, round, map_name, match_id):
        self.line = txt
        self.lineno = lnum
        self.moment = moment
        self.mapnumber = mapnumber
        self.round = round
        self.map_name = map_name
        self.match_id = match_id
        self.type = self.get_type()
        if self.type != 'blinded':
            self.author_name = self.get_author_name()
            self.author_id = self.get_author_id()
            self.author_side = self.get_author_side()
        else:
            self.author_name = self.get_victim_name()
            self.author_id = self.get_victim_id()
            self.author_side = self.get_victim_side()

        if self.type != 'blinded':
            self.victim_id = self.get_victim_id()
            self.victim_name = self.get_victim_name()
            self.victim_side = self.get_victim_side()
        else:
            self.victim_name = self.get_author_name()
            self.victim_id = self.get_author_id()
            self.victim_side = self.get_author_side()

        self.weapon = self.get_weapon()
        self.damage = self.get_damage()
        self.blinded_time = self.get_blinded_time()
        self.flashbang_id = self.get_flashbang_id()
        self.damage_armor = self.get_damage_armor()
        self.victim_health = self.get_victim_health()
        self.victim_armor = self.get_victim_armor()
        self.hitgroup = self.get_hitgroup()
        self.hs = self.get_hs()
        self.penetrated = self.get_penetrated()
        self.throughsmoke = self.get_throughsmoke()
        self.author_coord = self.get_author_coord()
        self.victim_coord = self.get_victim_coord()
        self.time = self.get_time()
        self.equipment = self.get_equipment()
        self.item_bought = self.get_item_bought()
        self.equipment_value = self.get_equipment_value()

    def to_dict(self):
        attributes = vars(self)
        del attributes['line']
        x = list(attributes.keys())
        for key in x:
            if attributes[key] is None:
                del attributes[key]
        return attributes

    def get_type(self):
        player_events = ['attacked', 'threw flashbang', 'blinded', 'killed', 'left buyzone', 'say_team', 'say',
                         'threw molotov', 'committed suicide', 'changed name',
                         'threw hegrenade', 'threw smokegrenade',
                         'purchased',
                         'Dropped_The_Bomb', 'Got_The_Bomb',
                         'switched from team', 'assisted killing', 'Planted_The_Bomb', 'Bomb_Begin_Plant',
                         'flash-assisted killing',
                         'Begin_Bomb_Defuse_With_Kit', 'Defused_The_Bomb', 'entered the game', 'disconnected',
                         'threw decoy', 'Begin_Bomb_Defuse_Without_Kit', 'SFUI_Notice_Terrorists_Win',
                         'SFUI_Notice_CTs_Win', 'SFUI_Notice_Bomb_Defused', 'SFUI_Notice_Target_Bombed',
                         'SFUI_Notice_Target_Saved']

        for event in player_events:
            if event in self.line:
                return event

    def get_penetrated(self):
        return 1 if 'penetrated' in self.line else 0

    def get_hs(self):
        return 1 if 'headshot' in self.line else 0

    def get_throughsmoke(self):
        return 1 if 'throughsmoke' in self.line else 0

    def get_time(self):
        try:
            m = re.findall('L (.+?): ', self.line)
            if m:
                result = m[0]
                return result
        except IndexError:
            return None

    def get_blinded_time(self):
        try:
            m = re.findall('blinded for (.+?) by', self.line)
            if m:
                result = float(m[0])
                return result
        except IndexError:
            return None

    def get_flashbang_id(self):
        try:
            m = re.findall('flashbang entindex (.+?) ', self.line)
            if m:
                result = int(m[0])
                return result
        except IndexError:
            return None

    def get_author_side(self):
        try:
            m = re.findall('<(.+?)>', self.line)
            if m:
                result = m[2]
                return result
        except IndexError:
            return None

    def get_victim_side(self):
        try:
            m = re.findall('<(.+?)>', self.line)
            if m:
                result = m[5]
                return result
        except IndexError:
            return None

    def get_author_id(self):
        try:
            m = re.findall('<(.+?)>', self.line)
            if m:
                result = m[1]
                return result
        except IndexError:
            return None

    def get_author_name(self):
        try:
            m = re.findall(' "(.+?)<', self.line)
            if m:
                result = m[0]
                return result
        except IndexError:
            return None

    def get_weapon(self):
        try:
            m = re.findall(' with "(.+?)"', self.line)
            if m:
                result = m[0]
                return result
        except IndexError:
            return None

    def get_victim_id(self):
        try:
            m = re.findall('<(.+?)>', self.line)
            if m:
                result = m[4]
                return result
        except IndexError:
            return None

    def get_victim_name(self):
        try:
            m = re.findall(' "(.+?)<', self.line)
            if m:
                result = m[1]
                return result
        except IndexError:
            return None

    def get_damage(self):
        try:
            m = re.findall('\(damage "(.+?)"\)', self.line)
            if m:
                result = int(m[0])
                return result
        except IndexError:
            return None

    def get_damage_armor(self):
        try:
            m = re.findall('\(damage_armor "(.+?)"\)', self.line)
            if m:
                result = int(m[0])
                return result
        except IndexError:
            return None

    def get_victim_health(self):
        try:
            m = re.findall('\(health "(.+?)"\)', self.line)
            if m:
                result = int(m[0])
                return result
        except IndexError:
            return None

    def get_victim_armor(self):
        try:
            m = re.findall('\(armor "(.+?)"\)', self.line)
            if m:
                result = int(m[0])
                return result
        except IndexError:
            return None

    def get_hitgroup(self):
        try:
            m = re.findall('\(hitgroup "(.+?)"\)', self.line)
            if m:
                result = m[0]
                return result
        except IndexError:
            return None

    def get_author_coord(self):
        try:
            m = re.findall(' \[(.+?)\] ', self.line)
            if m:
                result = tuple(m[0].split())
                return result
        except IndexError:
            return None

    def get_victim_coord(self):
        try:
            m = re.findall(' \[(.+?)\] ', self.line)
            if m:
                result = tuple(m[1].split())
                return result
        except IndexError:
            return None

    def get_equipment(self):
        try:
            m = re.findall('left buyzone with \[ (.+?) \]', self.line)
            if m:
                result = str(tuple(m[0].split())).replace("'", "")
                return result
        except IndexError:
            return None

    def get_equipment_value(self):
        try:
            value = 0

            armas = {
                'weapon_deagle': 700,
                'weapon_m4a1': 3100,
                'weapon_flashbang': 200,
                'weapon_smokegrenade': 300,
                'weapon_incgrenade': 600,
                'defuser': 400,
                'kevlar(x)': 650,
                'helmet': 350,
                'knife': 0,
                'weapon_glock': 200,
                'weapon_ump45': 1200,
                'weapon_usp_silencer': 200,
                'weapon_mp9': 1250,
                'weapon_hegrenade': 300,
                'weapon_mac10': 1050,
                'weapon_molotov': 400,
                'weapon_awp': 4750,
                'weapon_c4': 0,
                'weapon_ak47': 2700,
                'weapon_p250': 300,
                'weapon_taser': 200,
                'weapon_galilar': 1800,
                'weapon_ssg08': 1750,
                'weapon_tec9': 500,
                'weapon_cz75a': 500,
                'weapon_decoy': 50,
                'weapon_sg556': 3000,
                'weapon_fiveseven': 500,
                'weapon_elite': 400,
                'weapon_famas': 2050,
                'weapon_mag7': 1800,
                'weapon_aug': 3100,
                'weapon_hkp2000': 200,
                'weapon_p90': 2300,
                'weapon_mp7': 1500,
                'weapon_g3sg1': 5000}

            m = re.findall('left buyzone with \[ (.+?) \]', self.line)
            if m:
                result = str(tuple(m[0].split())).replace("'", "")
                for arma in armas.keys():
                    if arma in result:
                        value += armas[arma]
                return value
        except IndexError:
            return None

    def get_item_bought(self):
        try:
            m = re.findall('purchased "(.+?)"', self.line)
            if m:
                result = m[0]
                return result
        except IndexError:
            return None
