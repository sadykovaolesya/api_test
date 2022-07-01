from random import choice, random


def fraud_detector(service):
    """Детектор мошенничества """
    return random()


def service_classification(service):
    """ Классификатор услуг """
    SERVICES = {
        1: "консультация",
        2: "лечение",
        3: "стационар",
        4: "диагностика",
        5: "лаборатория",
    }

    return SERVICES[choice(list(SERVICES.keys()))]


def get_objects(objects, item):
    """ Поиск и получения из Quryset нужного объекта"""
    for object in objects:
        if object.name == item:
            return object
