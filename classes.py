from dataclasses import dataclass
from skills import FuryPunch, HardShot, Skill


@dataclass
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    attack: float
    stamina: float
    armor: float
    skill: Skill


""" Инициализируем экземпляр класса UnitClass и присваиваем ему необходимые значения аттрибуотов """
WarriorClass = UnitClass(
    name='Войн',
    max_health=60,
    max_stamina=30,
    attack=0.8,
    stamina=0.9,
    armor=1.2,
    skill=FuryPunch(),
)

ThiefClass = UnitClass(
    name='Вор',
    max_health=50,
    max_stamina=25,
    attack=1.5,
    stamina=1.2,
    armor=1,
    skill=HardShot(),
)

HeroClass = UnitClass(
    name='Герой',
    max_health=48,
    max_stamina=30,
    attack=2.0,
    stamina=1.2,
    armor=1.2,
    skill=HardShot(),
)

AstroClass = UnitClass(
    name='Астролог',
    max_health=30,
    max_stamina=20,
    attack=2.5,
    stamina=0.9,
    armor=0.7,
    skill=FuryPunch(),
)

ProphetClass = UnitClass(
    name='Пророк',
    max_health=32,
    max_stamina=18,
    attack=2.0,
    stamina=1.4,
    armor=0.7,
    skill=FuryPunch(),
)

SamuraiClass = UnitClass(
    name='Самурай',
    max_health=34,
    max_stamina=25,
    attack=2.1,
    stamina=1.0,
    armor=1.0,
    skill=HardShot(),
)

WildClass = UnitClass(
    name='Дикарь',
    max_health=60,
    max_stamina=40,
    attack=3.0,
    stamina=1.5,
    armor=0.1,
    skill=FuryPunch(),
)

unit_classes = {
    ThiefClass.name: ThiefClass,
    WarriorClass.name: WarriorClass,
    HeroClass.name: HeroClass,
    AstroClass.name: AstroClass,
    ProphetClass.name: ProphetClass,
    SamuraiClass.name: SamuraiClass,
    WildClass.name: WildClass,
}
