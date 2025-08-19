from dataclasses import dataclass, asdict

@dataclass
class WarpPointItem:
    x:        str	
    y:        str
    WorldIdx: str	
    nation1x: str=None	
    nation1y: str=None	
    nation2x: str=None	
    nation2y: str=None	
    nation3x: str=None	
    nation3y: str=None	
    w_code:   str="0"	
    Fee:      str="0"	
    level:    str="1"

    def __post_init__(self):
        if self.nation1x is None: self.nation1x = self.x
        if self.nation1y is None: self.nation1y = self.y
        if self.nation2x is None: self.nation2x = self.x
        if self.nation2y is None: self.nation2y = self.y
        if self.nation3x is None: self.nation3x = self.x
        if self.nation3y is None: self.nation3y = self.y    