from parsy import string, regex, seq, any_char, whitespace
from enum import Enum
from typing import Optional

import datetime

def todo(string: str) -> Optional[bool]:
    match string.lower():
        case 'todo':
            return True
        case 'done':
            return False
        case _ : 
            raise ValueError(f"invalid todo value {string}")


pin = string('!').optional().map(bool)
path = (string('/') >> regex('[\w_-]+')).at_least(1)
todo = (string("todo") | string("done")).map(todo)
text = any_char.many().concat()

dash = string('-')
date = seq(
        year = regex('\d{4}').map(int) << dash,
        month = regex('\d\d').map(int) << dash,
        day =  regex('\d\d').map(int)  
).combine_dict(datetime.date)

colon = string(':')
time = seq(
        hour = regex('\d\d').map(int),
        minute = colon >> regex('\d\d').map(int),
        second = colon >> regex('\d\d').map(int)
).combine_dict(datetime.time)

timezone = regex('[+-]\d\d:\d\d')
datetime = seq(
        date=date,
        time = string('T') >> time << (timezone.optional())
).combine_dict(datetime.datetime.combine)

partial_tap = seq(
    path=(path << whitespace).optional([]), 
    pin=(pin << whitespace).optional(False), 
    todo=(todo << whitespace).optional(), 
    text=text
)

tap = seq(
        datetime = (datetime << whitespace),
        pin=(pin << whitespace).optional(False), 
        path=(path << whitespace).optional([]), 
        todo=(todo << whitespace).optional(), 
        text=text
)

