import grammar
from record import Record
import json
from sys import stdout
from dataclasses import dataclass, field

def record_to_dict(record: Record):
    var_dict = vars(record)
    var_dict['datetime'] = record._datetime
    var_dict['pin'] = False if record.pin is None else record.pin
    return var_dict

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
    def __init__(self, path: str = 'database.tap'):
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
        json.dump(self._taps, stdout)


    def list(self):
        for tap in sorted(self._taps):
            print(tap)


if __name__ == '__main__':
    from fire import Fire
    Fire(Tap)

