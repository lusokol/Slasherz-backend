import enum

class CardType(str, enum.Enum):
    survivant = "survivant"
    victime = "victime"
    personnage = "personnage"
    objet = "objet"
    evenement = "evenement"
    lieu = "lieu"

class CardDimension(str, enum.Enum):
    desert = "desert"
    espace = "espace"
    enfer = "enfer"
    nature = "nature"
    urbain = "urbain"

class CardRarity(int, enum.Enum):
    commun = 1
    rare = 2
    super_rare = 3
    mythique = 4