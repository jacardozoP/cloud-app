import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLOUDS_JSON_PATH = os.path.join(BASE_DIR, "clouds.json")


def load_clouds():
    with open(CLOUDS_JSON_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

def load_clouds():
    with open("data/clouds.json", "r", encoding="utf-8") as file:
        return json.load(file)


def get_all_clouds():
    return load_clouds()


def get_clouds_by_category(category):
    clouds = load_clouds()
    return [c for c in clouds if c["category"] == category]


def get_cloud_by_name(name):
    clouds = load_clouds()

    aliases = {
        "Altocumulus": "Ac",
        "Altostratus": "As",
        "Cumulonimbus": "Cb",
        "Cirrocumulus": "Cc",
        "Cirrus": "Ci",
        "Cirrostratus": "Cs",
        "Cumulus": "Cu",
        "Nimbostratus": "Ns",
        "Stratocumulus": "Sc",
        "Stratus": "St",
    }

    search_code = aliases.get(name, "").lower()

    for cloud in clouds:
        # 🔥 IGNORA bloques que no son nubes principales
        if not isinstance(cloud, dict):
            continue

        if "name" not in cloud or "code" not in cloud:
            continue

        if cloud.get("name", "").lower() == name.lower():
            return cloud

        if search_code and cloud.get("code", "").lower() == search_code:
            return cloud

    return None


def get_cloud_by_id(cloud_id):
    clouds = load_clouds()
    for cloud in clouds:
        if cloud["id"] == cloud_id:
            return cloud
    return None