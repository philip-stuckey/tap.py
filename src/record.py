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
   
    def __lt__(self, other): # self < other
        if other.pin and not self.pin:
            return True
        if self.pin and not other.pin:
            return False
        else:
            return self.datetime < other.datetime

    @property
    def id(self):
        m = sha256()
        m.update(self._datetime.encode())
        m.update(self.text.encode())
        return m.hexdigest()

    @property
    def _datetime(self) -> str:
        dt = self.datetime if self.datetime is not None else datetime.now()
        return dt.strftime('%Y-%m-%dT%H:%M:%S')

    @property
    def _path(self)-> str:
        return '/' + '/'.join(self.path) if len(self.path) > 0 else ''

    @property
    def _pin(self) -> str:
        return '*' if self.pin else ''

    @property
    def _todo(self) -> str:
        match self.todo:
            case True:
                return 'todo'
            case False:
                return 'done'
            case None:
                return ''
    @property
    def _parts(self):
        return (self._datetime, self._path, self._pin, self._todo, self.text)

    def __str__(self):
        return ' '.join(part for part in self._parts if len(part)>0)

