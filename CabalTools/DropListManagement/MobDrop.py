from dataclasses import dataclass

@dataclass
class MobDrop:
    WorldIdx:    int	
    SpeciesIdx:  int	
    ItemKind:    int	
    ItemOpt:     int	
    DropRate:	 float
    MinLv:       int     = 0	
    MaxLv:       int     = 300	
    Group:       int     = 0	
    MaxDropCnt:  int     = 0
    OptPoolIdx:  int     = 0	
    DurationIdx: int     = 0
    DropSvrCh:   int     = 0
