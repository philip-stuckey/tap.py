import grammar
import json
from itertools import islice
from database import TapDatabase
from datetime import datetime
from record import Record
from sys import stdout

class Tap:
    def __init__(self, path: str = '.local/share/tap', pinned=None, show_ids=False, limit=None, show_datetime=True):
        self.database = TapDatabase(path=path)
        self._pinned = pinned
        self._show_id = show_ids
        self._limit = limit
        self._show_datetime = show_datetime 

    def add(self, token, *tokens):
        string = token + ' ' + (' '.join(map(str,tokens)))
        record = grammar.partial_tap.combine_dict(Record).parse(string)  # command line taps dont need dates
        self.database.add(record)
        self.database.commit()
        return record
    
    def todo(self, token, *tokens):
        record = self.add(token, tokens)
        record.todo = True
#        self.database.overwrite(record.id, record)  # stupidly expensive, optimize here first
        return record

    def remove(self, id):
        victim = self.database.select_one(id)
        self.database.remove(id)
        print("removed", victim)

    def export(self):
        json.dump(list(map(Record.to_dict,self.database.taps)), stdout)    

    def inport(self, path):
        with open(path, 'r') as file:
            data = json.load(file)
        for entry in data:
            self.database.add(Record.from_dict(entry))
        self.database.commit()
    

    def head(self, *args, limit=10, **kwargs):
        self.limit=limit
        self.list(*args, **kwargs)

    def list(self, path=''):
        taps = reversed(sorted(self.database.taps))
        if self._limit is not None:
            taps = islice(taps, self.limit)
        
        if self._pinned is not None:
            taps = filter(lambda t: t.pin and self._pinned, taps)

        taps = filter(lambda t: t._path.startswith(path), taps)
        for tap in taps:
            if tap.long_form:
                continue 

            if self._show_id:
                print(tap.id[0:5], end=' ')
            if self._show_datetime:
                print(tap._datetime, end=' ')

            print(
                    tap._pin if tap.pin else ' ', 
                    tap._path.ljust(8), 
                    tap._todo.ljust(5), 
                    tap.text.strip(),
                    sep=''
            )


    def pins(self, *args, **kwargs):
        self._pinned = True
        self.list(*args, **kwargs)

    def pin(self, id):
        id = str(id)
        record = self.database.select_one(id)
        record.pin = True
        self.database.overwrite(id,record)
        print(record)

    def unpin(self, id):
        id = str(id)
        record = self.database.select_one(id)
        record.pin = False
        self.database.overwrite(id, record)

if __name__ == '__main__':
    from fire import Fire
    Fire(Tap)


