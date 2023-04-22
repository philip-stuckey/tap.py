import grammar
from record import Record
import json
from sys import stdout

class Tap:
    path = 'database.tap'
    record_parser = grammar.tap.combine_dict(Record)

    @property
    def _taps(self):
        with open(self.path, 'r') as file:
            for line in file:
                yield self.record_parser.parse(line)

    def add(self, *tokens):
        string = ' '.join(map(str,tokens))
        record =    self.record_parser.parse(string)
        with open(self.path, 'a') as file:
            print(str(record), file=file)

    def export(self):
        json.dump(self._taps, stdout)


    def list(self):
        for tap in sorted(self._taps):
            print(tap)


if __name__ == '__main__':
    from fire import Fire
    Fire(Tap)

