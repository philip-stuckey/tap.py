import grammar
import json
from itertools import islice
from database import TapDatabase
from datetime import datetime
from record import Record
from sys import stdout

class Tap:
    def __init__(self, path: str = 'share/database.tap', pinned=None, show_ids=False, limit=None):
        self.database = TapDatabase(path=path)
        self.pinned = pinned
        self.show_id = show_ids
        self.limit = limit
        self.show_datetime = True


    def add(self, *tokens):
        string = ' '.join(map(str,tokens))
        record = grammar.partial_tap.combine_dict(Record).parse(string)  # command line taps dont need dates
        self.database.add(record)
        self.database.commit()
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
    

    def head(self, limit=10, **args):
        self.limit=limit
        self.list(limit=limit, **args)

    def list(self):
        taps = reversed(sorted(self.database.taps))
        if self.limit is not None:
            taps = islice(taps, self.limit)
        
        if self.pinned is not None:
            taps = filter(lambda t: t.pin and self.pinned, taps)

        for tap in taps:
            if self.show_id:
                print(tap.id[1:5], end=' ')
            if self.show_datetime:
                print(tap._datetime, end=' ')

            print(
                    tap._pin.center(3), 
                    tap._path.ljust(8), 
                    tap._todo.ljust(4), 
                    tap.text
            )


    def pins(self):
        for pin in filter(lambda r: r.pin, self._ordered_taps):
            print(pin)

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


