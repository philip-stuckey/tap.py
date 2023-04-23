import grammar
from record import Record
from dataclasses import dataclass, field
from tempfile import NamedTemporaryFile
from shutil import copy

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
            previous_record = record_parser.parse(next(file))
            for line in file:
                match (record_parser | grammar.text).parse(line):
                    case Record() as new_record: 
                        yield previous_record
                        previous_record=new_record
                    case str(text):
                        previous_record.text += text
                        continue
                    case _:
                        raise RimtimeError("database corrupt")

    def select(self, id: str):
        return (tap for tap in self.taps if tap.id.startswith(str(id)))

    def select_one(self, id):
        pool = self.select(id)
        try:
            result = next(pool)
        except StopIteration:
            return None
        try:
            next(pool)
        except StopIteration:
            return result
        else:
            return ValueError(f"multiple results for querty {id}")
            
    def commit(self):
        if len(self.buffer) > 0:
            with open(self.path, 'a') as file:
                print('\n'.join(map(str,self.buffer)), file=file)
            self.buffer=[]


    def add(self, tap):
        self.buffer.append(tap)

    def remove(self, id):
        flag=False
        with NamedTemporaryFile(mode='w') as file:
            for item in self.taps:
                if item.id.startswith(str(id)):
                    if not flag:
                        flag = True
                        continue
                    else:
                        raise ValueError(f"multiple ids for query {id}")
                else:
                    print(item, file=file)
            file.flush()
            copy(file.name, self.path)

    def overwrite(self, id, record):
        with NamedTemporaryFile(mode='w') as file:
            for item in self.taps:
                if item.id.startswith(str(id)):
                    print(record, file=file)
                else:
                    print(item, file=file)
            file.flush()
            copy(file.name, self.path)

