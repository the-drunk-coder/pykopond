# pykopond
#### Orderable music data types for python, designed to work with lilypond.

### What's this ?
This is my attempt at creating a flexible and comparable datatype
to describe and work with music. The main focus is providing a python environment
for algorithmic composition.

Forthermore, this library contains tools to parse this datatype directly to lilypond.

The approach for the datatype is in some parts borrowed from the one you can find in HASKORE.
It has origninally been based on fixed-point decimal arithmethic (using python's "Decimal" type),
but has been switched to simple integer artithmetic in the meantime, to improve performance.

### Usage examples
For examples on how to use this, [take a look at](https://github.com/the-drunk-coder/rangements) the "rangements"-repository. 

### State of the project
So far, i only implemented what i needed for some compositions, so there are still some
things to do to make this a complete environment:
* a lilypond parser to parse existing music
* a shorthand to write the notes more efficiently
* dynamics support
* ~~support for chords~~ (basic data structure implemented)
* comparison methods for chords
* support for tuplets
* support for for key signatures and key changes
* support for clef changes
* support for time signature changes
* documentation, of course ... 

Eventually, a more powerful control over the lilypond output might also be helpful.

--
Released under GPLv3 or later (for full license text see LICENSE.txt)
