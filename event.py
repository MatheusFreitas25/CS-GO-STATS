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
        self.author_id = self.get_author_id()
        self.author_name = self.get_author_name()
        self.victim_id = self.get_victim_id()
        self.victim_name = self.get_victim_name()
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
        self.author_side = self.get_author_side()
        self.victim_side = self.get_victim_side()
        self.time = self.get_time()

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
                         'threw hegrenade', 'threw smokegrenade', 'purchased', 'Dropped_The_Bomb', 'Got_The_Bomb',
                         'switched from team', 'assisted killing', 'Planted_The_Bomb', 'Bomb_Begin_Plant',
                         'flash-assisted killing',
                         'Begin_Bomb_Defuse_With_Kit', 'Defused_The_Bomb', 'entered the game', 'disconnected',
                         'threw decoy', 'Begin_Bomb_Defuse_Without_Kit']

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
            m = re.findall('L (.+?): "', self.line)
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
            m = re.findall('<(.?)>', self.line)
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
            m = re.findall(' with "(.+?)" ', self.line)
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