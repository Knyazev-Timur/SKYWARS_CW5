from __future__ import annotations

from abc import ABC, abstractmethod
from random import randint

from classes import UnitClass
from equipment import Armor, Weapon


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """

    def __init__(self, name: str, unit_class: UnitClass, weapon=None, armor=None):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = weapon
        self.armor = armor
        self._is_skill_used = False

    @property
    def health_points(self) -> float:
        return round(self.hp, 1)

    @property
    def stamina_points(self) -> float:
        return round(self.stamina, 1)

    def equip_weapon(self, weapon: Weapon) -> str:
        """ присваиваем нашему герою новое оружие """
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor) -> str:
        """ одеваем новую броню """
        self.armor = armor
        return f"{self.name} экипирован броней {self.armor.name}"

    def _count_damage(self, target: BaseUnit) -> int:
        """
        Эта функция содержит:
        логику расчета урона игрока
        логику расчета брони цели
        здесь же происходит уменьшение выносливости атакующего при ударе
        и уменьшение выносливости защищающегося при использовании брони
        если у защищающегося нехватает выносливости - его броня игнорируется
        после всех расчетов цель получает урон - target.get_damage(damage)
        и возвращаем предполагаемый урон для последующего вывода пользователю в текстовом виде
        """
        self.stamina -= self.weapon.stamina_per_hit
        damage = self.weapon.damage * self.unit_class.attack

        if target.stamina >= target.armor.stamina_per_turn * target.unit_class.stamina:
            target.stamina -= target.armor.stamina_per_turn * target.unit_class.stamina
            damage -= target.armor.defence * target.unit_class.armor

        damage = round(damage, 1)
        target.get_damage(damage)
        return damage

    def get_damage(self, damage: int) -> float:
        """ получение урона целью присваиваем новое значение для аттрибута self.hp """
        if damage >= 0 and self.hp - damage > 0:
            self.hp -= damage
        elif damage >= 0 >= self.hp - damage:
            self.hp = 0
        return self.hp

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        """
        этот метод будет переопределен ниже
        """
        pass

    def use_skill(self, target) -> str:
        """
        метод использования умения.
        если умение уже использовано возвращаем строку
        Навык использован
        Если же умение не использовано тогда выполняем функцию
        self.unit_class.skill.use(user=self, target=target)
        и уже эта функция вернем нам строку которая характеризует выполнение умения
        """
        if self._is_skill_used is True:
            return "Навык уже был использован"

        skill_use = self.unit_class.skill.use(self, target)
        self._is_skill_used = True
        return skill_use


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        функция удар игрока:
        здесь происходит проверка достаточно ли выносливости для нанесения удара.
        вызывается функция self._count_damage(target)
        а также возвращается результат в виде строки
        """

        if self.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        damage = self._count_damage(target)
        if damage > 0:
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника " \
                   f"и наносит {damage} урона."

        return f"{self.name} используя {self.weapon.name} наносит удар, " \
               f"но {target.armor.name} cоперника его останавливает."


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        функция удар соперника
        должна содержать логику применения соперником умения
        (он должен делать это автоматически и только 1 раз за бой).
        Например, для этих целей можно использовать функцию randint из библиотеки random.
        Если умение не применено, противник наносит простой удар, где также используется
        функция _count_damage(target
        """

        if self._is_skill_used is False and self.stamina >= self.unit_class.skill.stamina and randint(0, 100) < 10:
            return self.use_skill(target)

        if self.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        damage = self._count_damage(target)
        if damage > 0:
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника " \
                   f"и наносит {damage} урона."

        return f"{self.name} используя {self.weapon.name} наносит удар, " \
               f"но {target.armor.name} cоперника его останавливает."
