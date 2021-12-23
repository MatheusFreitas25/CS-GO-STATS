import re
from pprint import pprint

log = open(r'matches\5 - 12-21-2021 19-34 - bo3 full_match.log')


class Attack:
    def __init__(self, txt, lnum=None):
        self.line = txt
        self.lineno = lnum
        self.author_id = self.get_author_id()
        self.author_name = self.get_author_name()
        self.victim = self.get_victim_id()
        self.author_name = self.get_victim_name()
        self.weapon = self.get_weapon()
        self.damage = self.get_damage()
        self.damage_armor = self.get_damage_armor()
        self.victim_health = self.get_victim_health()
        self.victim_armor = self.get_victim_armor()
        self.hitgroup = self.get_hitgroup()
        self.author_coord = self.get_author_coord()
        self.victim_coord = self.get_victim_coord()
        self.time = self.get_time()

    def to_dict(self):
        attributes = vars(self)
        del attributes['line']
        return attributes

    def get_time(self):
        m = re.findall('L (.+?): "', self.line)
        if m:
            result = m[0]
            return result

    def get_author_id(self):
        m = re.findall('<(.+?)>', self.line)
        if m:
            result = m[1]
            return result

    def get_author_name(self):
        m = re.findall(' "(.+?)<', self.line)
        if m:
            result = m[0]
            return result

    def get_weapon(self):
        m = re.findall(' with "(.+?)" ', self.line)
        if m:
            result = m[0]
            return result

    def get_victim_id(self):
        m = re.findall('<(.+?)>', self.line)
        if m:
            result = m[1]
            return result

    def get_victim_name(self):
        m = re.findall(' "(.+?)<', self.line)
        if m:
            result = m[1]
            return result

    def get_damage(self):
        m = re.findall('\(damage "(.+?)"\)', self.line)
        if m:
            result = int(m[0])
            return result

    def get_damage_armor(self):
        m = re.findall('\(damage_armor "(.+?)"\)', self.line)
        if m:
            result = int(m[0])
            return result

    def get_victim_health(self):
        m = re.findall('\(health "(.+?)"\)', self.line)
        if m:
            result = int(m[0])
            return result

    def get_victim_armor(self):
        m = re.findall('\(armor "(.+?)"\)', self.line)
        if m:
            result = int(m[0])
            return result

    def get_hitgroup(self):
        m = re.findall('\(hitgroup "(.+?)"\)', self.line)
        if m:
            result = m[0]
            return result

    def get_author_coord(self):
        m = re.findall(' \[(.+?)\] ', self.line)
        if m:
            result = tuple(m[0].split())
            return result

    def get_victim_coord(self):
        m = re.findall(' \[(.+?)\] ', self.line)
        if m:
            result = tuple(m[1].split())
            return result


if __name__ == '__main__':
    attacks = list()

    for lineno, line in enumerate(log):
        if 'attacked' in line:
            attack = Attack(line, lineno)
            attacks.append(attack)

    for i in attacks:
        print(i.to_dict())


