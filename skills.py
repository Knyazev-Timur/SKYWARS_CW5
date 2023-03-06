from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional, Callable, Any


if TYPE_CHECKING:
    from unit import BaseUnit

class Skill(ABC):
    """
    Базовый класс умения
    """
    def __init__(self):
        self.user = None
        self.target = None

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def stamina(self) -> float:
        pass

    @property
    @abstractmethod
    def damage(self) -> float:
        pass

    @abstractmethod
    def skill_effect(self) -> str:
        pass

    def is_stamina_enough(self) -> bool:
        return self.user.stamina >= self.stamina

    def use(self, user: BaseUnit, target: BaseUnit) -> str:
        """
        Проверка, достаточно ли выносливости у игрока для применения умения.
        Для вызова скилла везде используем просто use
        """
        self.user = user
        self.target = target
        if self.is_stamina_enough():
            return self.skill_effect()
        return f"{self.user.name} попытался использовать {self.name} но у него не хватило выносливости."


class FuryPunch(Skill):
    name = "Свирепый пинок"
    stamina = 6
    damage = 12

    def skill_effect(self) -> str:
        """
        логика использования скилла -> return str
        в классе нам доступны экземпляры user и target - можно использовать любые их методы
        именно здесь происходит уменшение стамины у игрока применяющего умение и
        уменьшение здоровья цели.
        результат применения возвращаем строкой
        """
        self.user.stamina -= self.stamina

        if self.target.hp-self.damage > 0:
            self.target.hp -= self.damage
        else:
            self.target.hp = 0
        return f'{self.user.name} использует {self.name} и наносит {self.damage} урона сопернику {self.target.name}'

class HardShot(Skill):
    name = "Мощный укол"
    stamina = 5
    damage = 15

    def skill_effect(self) -> str:
        self.user.stamina -= self.stamina
        if self.target.hp - self.damage > 0:
            self.target.hp -= self.damage
        else:
            self.target.hp = 0
        return f'{self.user.name} использует {self.name} и наносит {self.damage} урона сопернику {self.target.name} '
