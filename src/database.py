import grammar
from record import Record
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

