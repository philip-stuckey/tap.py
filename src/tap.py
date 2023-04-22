import grammar
import json
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

    def export(self):
        json.dump(list(map(Record.to_dict,self.database.taps)), stdout)    

    def inport(self, path):
        with open(path, 'r') as file:
            data = json.load(file)

        for entry in data:
            entry['datetime'] = datetime.strptime(entry['datetime'], Record.DATE_FORMAT)  # FIXME this should go somwhere else
            self.database.add(Record(**entry))
        self.database.commit()

    def list(self, id=False):
        for tap in self._ordered_taps:
            print(tap.id[:5] if id else '', tap)
    
    def pins(self):
        for pin in filter(lambda r: r.pin, self._ordered_taps):
            print(pin)



if __name__ == '__main__':
    from fire import Fire
    Fire(Tap)

