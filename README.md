# Tap.py
based on <https://github.com/tatatap-com>
they have a lot of cool features too
if you need a good/professional/working solution, check them out first

this is just a project I made to formalize the add-hoc note takeing I already do.

## Grammar
each entry obeys the following pattern

`<datetime> [pin] [path] [todo] <text>`

note that `<text>` can span multiple lines
an entry is don when it encounters a new `<datetime>` at the beginning of a line
this constitutes the start of the next entry

most of the details are in `src/grammar.py`


