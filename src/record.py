from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from hashlib import sha256

@dataclass 
class Record:
    path: list[str]
    pin: bool
    text: str
    todo: Optional[bool] = None
    datetime: datetime = datetime.now()
    
    DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'

    @classmethod
    def from_dict(Self, entry: dict):
        entry['datetime'] = datetime.strptime(entry['datetime'], Self.DATE_FORMAT)
        return Self(**entry)

    def to_dict(self):
        var_dict = vars(self)
        var_dict['datetime'] = self._datetime
        var_dict['pin'] = False if self.pin is None else self.pin
        return var_dict

    def __lt__(self, other): # self < other
       return (self.pin < other.pin) or\
               (self._todo_int < other._todo_int) or\
               (self.datetime < other.datetime)

    @property
    def _todo_int(self):
        match self.todo:
            case True: 
                return 3
            case None:
                return 2
            case False:
                return 1

    @property
    def id(self):
        m = sha256()
        m.update(self._datetime.encode())
        m.update(self.text.encode())
        return m.hexdigest()

    @property
    def _datetime(self) -> str:
        dt = self.datetime if self.datetime is not None else datetime.now()
        return dt.strftime(self.DATE_FORMAT)

    @property
    def _path(self)-> str:
        return '/' + '/'.join(self.path) if len(self.path) > 0 else ''

    @property
    def _pin(self) -> str:
        return '!' if self.pin else ''

    @property
    def _todo(self) -> str:
        match self.todo:
            case True:
                return 'TODO'
            case False:
                return 'DONE'
            case None:
                return ''
    @property
    def _parts(self):
        return (self._datetime, self._pin, self._path,  self._todo, self.text)

    def __str__(self):
        return ' '.join(part for part in self._parts if len(part)>0)

