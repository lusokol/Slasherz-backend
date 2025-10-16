import enum

class CardType(str, enum.Enum):
    survivant = "survivant"
    victime = "victime"
    lvl1 = "lvl1"
    lvl2 = "lvl2"
    lvl3 = "lvl3"
    objet = "objet"
    evenement = "evenement"
    lieu = "lieu"
    jeton = "jeton"

class CardDimension(str, enum.Enum):
    desert = "desert"
    nature = "nature"
    urbain = "urbain"
    enfer = "enfer"
    espace = "espace"

class CardRarity(str, enum.Enum):
    commune = "commune"
    rare = "rare"
    super_rare = "super_rare"
    mythique = "mythique"
