# Tap.py
based on <https://github.com/tatatap-com>
they have a lot of cool features too
if you need a good/professional/working solution, check them out first

this is just a project I made to formalize the add-hoc note takeing I already do.

## key differences bwetween this and  <https://github.com/tatatap-com>
1. pins use `!` instead of `*`. 
This is because this project ismeant to be used on the command line and `*` is the wildcard.

2. tags use '+' instead of `#`, becuase `#` is a comment in most shells
Also, tags aren't implemented per-se, you can interperate the text however you want
I just use +tags because I don't need to escape + in my shell.

3. Events, formulae, and beans are not implemented. While these are all great
idea, they are a bit complicated, and I'd need to think a bit before implementing them.
Except events, they are just fancy tags.


## Grammar
each entry obeys the following pattern

`tap  ::= <datetime> [pin] [path] [todo] <text>`
`pin  ::= '!'`
`path ::= '/'<word>[path]`
`todo ::= 'TODO' | 'DONE'`
`text ::= <anyting>`

note that `<text>` can span multiple lines
an entry is don when it encounters a new `<datetime>` at the beginning of a line
this constitutes the start of the next entry

most of the details are in `src/grammar.py`

