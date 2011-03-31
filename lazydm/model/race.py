from sqlalchemy import Column
from sqlalchemy.types import Integer, Unicode
from lazydm.model.meta import Base
from lazydm.model.book import BookData
import json

class Race(Base, BookData):
    __tablename__ = "lazydm_races"
    
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(50),unique=True,nullable=False,index=True)
    _str = Column(Integer, default=0)
    _dex = Column(Integer, default=0)
    _int = Column(Integer, default=0)
    _wis = Column(Integer, default=0)
    _con = Column(Integer, default=0)
    _cha = Column(Integer, default=0)
    
    def stats(self):
        return { 
                    'str' : self._str,
                    'dex' : self._dex,
                    'int' : self._int,
                    'wis' : self._wis,
                    'con' : self._con,
                    'cha' : self._cha
                }
        
    def stat_mods_json(self):
        return json.dumps(self.stats())

    def __str__(self):
        return self.name
