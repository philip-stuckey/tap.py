from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass 
class Record:
    path: list[str]
    pin: bool
    text: str
    todo: Optional[bool] = None
    datetime: datetime = datetime.now()
    
    @property
    def _datetime(self) -> str:
        return self.datetime.isoformat()

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

