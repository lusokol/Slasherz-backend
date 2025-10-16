import json
from datetime import datetime

VJSON = "/home/slasherz/Slasherz-backend/app/data/version.json"

def update_version(update_type):
    with open(VJSON, 'r') as file:
        data = json.load(file)
        version_majeur, version_mineur, patch = map(int, data["version"].split('.'))
        match update_type:
            case "majeur":
                version_majeur += 1
                version_mineur = 0
                patch = 0
            case "mineur":
                version_mineur += 1
                patch = 0
            case "patch":
                patch += 1
            case _:
                raise ValueError("Type de mise à jour invalide : utiliser 'majeur', 'mineur' ou 'patch'.")
        data["version"] = "{}.{}.{}".format(version_majeur, version_mineur, patch)
        data["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(VJSON, "w") as f:
        json.dump(data, f, indent=4)
