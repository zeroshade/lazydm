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
    male_ft = Column(Integer, nullable=False)
    female_ft = Column(Integer, nullable=False)
    male_in = Column(Integer, nullable=False)
    female_in = Column(Integer, nullable=False)
    male_lb = Column(Integer, nullable=False)
    female_lb = Column(Integer, nullable=False)
    height_mod = Column(Unicode(5), nullable=False)
    weight_mod = Column(Unicode(5), nullable=False)
    
    def stats(self):
        return { 
                    'str' : self._str,
                    'dex' : self._dex,
                    'int' : self._int,
                    'wis' : self._wis,
                    'con' : self._con,
                    'cha' : self._cha
                }
    
    def personal(self):
        return {
                    'height' : { 'ft' : { 'male' : self.male_ft, 'female' : self.female_ft },
                                 'in' : { 'male' : self.male_in, 'female' : self.female_in }
                               },
                    'weight' : { 'male' : self.male_lb, 'female' : self.female_lb },
                    'height_mod' : self.height_mod,
                    'weight_mod' : self.weight_mod
                }
    
    def stat_mods_json(self):
        return json.dumps(self.stats())

    def __str__(self):
        return self.name
