from dataclasses import dataclass, asdict

@dataclass
class ShopItem:
    ItemKind: int
    AlzPrice: int
    ItemOpt: int = 0
    DurationIdx: int = 0
    MinLevel: int = 0
    MaxLevel: int = 0
    GuildMinLevel: int = 0
    Reputation: int = -19
    MaxReputation: int = 20
    OnlyPremium: int = 0
    OnlyWin: int = 0
    WExpPrice: int = 0
    APPrice: int = 0
    DPPrice: int = 0
    ItemPrice: int = 0
    ForcegemPrice: int = 0
    D_Limit: int = 0
    W_Limit: int = 0
