from flask import Blueprint, render_template, request, redirect, url_for
from equipment import Equipment
from unit import PlayerUnit, EnemyUnit
from classes import unit_classes
from base import Arena

main_blueprint = Blueprint('main_blueprint', __name__, template_folder='templates', url_prefix='/')

heroes = {
    "player": NotImplemented,
    "enemy": NotImplemented,
}

arena = Arena()
"""инициализируем класс арены"""


@main_blueprint.route("/")
def menu_page():
    """рендерим главное меню (шаблон index.html)"""

    return render_template("index.html")


@main_blueprint.route("/fight/")
def start_fight():
    """выполняем функцию start_game экземпляра класса арена и передаем ему необходимые аргументы
    рендерим экран боя (шаблон fight.html)"""

    arena.start_game(player=heroes['player'], enemy=heroes['enemy'])
    return render_template('fight.html', heroes=heroes)


@main_blueprint.route("/fight/hit")
def hit():
    """кнопка нанесения удара
    обновляем экран боя (нанесение удара) (шаблон fight.html)
    если игра идет - вызываем метод player.hit() экземпляра класса арены
    если игра не идет - пропускаем срабатывание метода (простот рендерим шаблон с текущими данными)"""

    if arena.game_is_running:
        result = arena.player_hit()
    else:
        result = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@main_blueprint.route("/fight/use-skill")
def use_skill():
    """ кнопка использования скилла """

    if arena.game_is_running:
        result = arena.player_use_skill()
    else:
        result = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@main_blueprint.route("/fight/pass-turn")
def pass_turn():
    """ кнопка пропуск хода
    вызываем здесь функцию следующий ход (arena.next_turn())"""

    if arena.game_is_running:
        result = arena.next_turn()
    else:
        result = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@main_blueprint.route("/fight/end-fight")
def end_fight():
    """ кнопка завершить игру - переход в главное меню """
    return render_template("index.html", heroes=heroes)


@main_blueprint.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    """ кнопка выбор героя. 2 метода GET и POST
    на GET отрисовываем форму.
    на POST отправляем форму и делаем редирект на эндпоинт choose enemy """

    if request.method == 'GET':
        header = "Выберите героя"
        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        result = {
            'header': header,
            'weapons': weapons,
            'armors': armors,
            'classes': unit_classes,
        }
        return render_template('hero_choosing.html', result=result)

    if request.method == 'POST':
        name = request.form['name']
        weapon_name = request.form['weapon']
        armor_name = request.form['armor']
        unit_class_name = request.form['unit_class']

        # Проверить что класс с таким именем существует
        unit = unit_classes.get(unit_class_name)
        if unit is None:
            return render_template('index.html')
        player = PlayerUnit(name=name, unit_class=unit_classes.get(unit_class_name))

        # Проверить что класс с таким именем существует
        armor = (Equipment().get_armor(armor_name))
        weapon = (Equipment().get_weapon(weapon_name))
        if armor is None or weapon is None:
            return render_template('index.html')

        player.equip_armor(Equipment().get_armor(armor_name))
        player.equip_weapon(Equipment().get_weapon(weapon_name))
        heroes['player'] = player
        return redirect(url_for('main_blueprint.choose_enemy'))


@main_blueprint.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    """ кнопка выбор соперников. 2 метода GET и POST
     также на GET отрисовываем форму.
     а на POST отправляем форму и делаем редирект на начало битвы """

    if request.method == 'GET':
        header = "Выберите противника"
        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        result = {
            'header': header,
            'weapons': weapons,
            'armors': armors,
            'classes': unit_classes,
        }
        return render_template('hero_choosing.html', result=result)

    if request.method == 'POST':
        name = request.form['name']
        weapon_name = request.form['weapon']
        armor_name = request.form['armor']
        unit_class_name = request.form['unit_class']

        # Проверить что класс с таким именем существует
        unit = unit_classes.get(unit_class_name)
        if unit is None:
            return redirect(url_for('main_blueprint.choose_enemy'))

        enemy = EnemyUnit(name=name, unit_class=unit_classes.get(unit_class_name))

        # Проверить что класс с таким именем существует
        armor = (Equipment().get_armor(armor_name))
        weapon = (Equipment().get_weapon(weapon_name))
        if armor is None or weapon is None:
            return redirect(url_for('main_blueprint.choose_enemy'))

        enemy.equip_armor(Equipment().get_armor(armor_name))
        enemy.equip_weapon(Equipment().get_weapon(weapon_name))
        heroes['enemy'] = enemy
        return redirect(url_for('main_blueprint.start_fight'))
