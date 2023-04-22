import grammar
import json
from itertools import islice
from database import TapDatabase
from datetime import datetime
from record import Record
from sys import stdout

class Tap:
    def __init__(self, path: str = 'share/database.tap'):
        self.database = TapDatabase(path=path)

    @property
    def _ordered_taps(self):
        return reversed(sorted(self.database.taps))


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
        self.list(limit=limit, **args)

    def list(self, id=False, limit=100):
        for tap in islice(self._ordered_taps, limit):
            print(tap.id[:5] if id else '', tap)

    def pins(self):
        for pin in filter(lambda r: r.pin, self._ordered_taps):
            print(pin)

    def pin(self, id):
        id = str(id)
        record = self.database.select_one(id)
        record.pin = True
        self.database.overwrite(id,record)

    def unpin(self, id):
        id = str(id)
        record = self.database.select_one(id)
        record.pin = False
        self.database.overwrite(id, record)

if __name__ == '__main__':
    from fire import Fire
    Fire(Tap)


