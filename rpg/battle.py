from config import MAP_SIZE


class Unit:
    def __init__(self, name, hp, attack, defense, x, y):
        self.name = name
        self.base_hp = hp
        self.hp = hp + (hp * 0.1 * self.level) if hasattr(self, 'level') else hp
        self.attack = attack + (2 * self.level) if hasattr(self, 'level') else attack
        self.defense = defense + (self.level) if hasattr(self, 'level') else defense
        self.x = x
        self.y = y
        if not hasattr(self, 'level'):
            self.level = 1
            self.experience = 0
            self.exp_to_next_level = 100

    def move(self, new_x, new_y):
        if 0 <= new_x < MAP_SIZE and 0 <= new_y < MAP_SIZE:
            self.x, self.y = new_x, new_y

    def take_damage(self, damage):
        actual_damage = max(0, damage - self.defense)
        self.hp -= actual_damage
        return actual_damage

    def gain_experience(self, exp_amount):
        self.experience += exp_amount
        print(f"{self.name} gained {exp_amount} XP! Total: {self.experience}/{self.exp_to_next_level}")
        while self.experience >= self.exp_to_next_level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.experience -= self.exp_to_next_level
        self.exp_to_next_level = int(self.exp_to_next_level * 1.5)
        # Scale stats with level
        self.hp = self.base_hp + (self.base_hp * 0.1 * self.level)
        self.attack += 2
        self.defense += 1
        print(f"🎉 {self.name} reached level {self.level}!")
        print(f"New stats: HP:{self.hp} ATK:{self.attack} DEF:{self.defense}")