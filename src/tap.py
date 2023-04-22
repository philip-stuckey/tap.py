import grammar
import json
from datetime import datetime
from record import Record
from sys import stdout
from dataclasses import dataclass, field


record_parser = grammar.tap.combine_dict(Record)

@dataclass
class TapDatabase:
    path: str 
    buffer: list[Record]=field(default_factory=list)
    
    def __del__(self):
        self.commit()

    @property
    def taps(self):
        with open(self.path, 'r') as file:
            for line in file:
                yield record_parser.parse(line.strip())

    def select(self, id: str) -> Record:
        return (tap for tap in self.taps if tap.id.startswith(str(id)))

    def commit(self):
        if len(self.buffer) > 0:
            with open(self.path, 'a') as file:
                print('\n'.join(map(str,self.buffer)), file=file)
            self.buffer=[]

    def add(self, tap):
        self.buffer.append(tap)


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

