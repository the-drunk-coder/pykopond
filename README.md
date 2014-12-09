pykopond
========

Orderable music data types for python, designed to work with lilypond.

This is my attempt at creating a flexible and comparable datatype
to describe and work with music.

Forthermore, this library contains tools to parse this datatype to lilypond.

The approach for the datatype is in some parts borrowed from the one you can find in HASKORE.
It's based on fixed-point arithmetic, using python's 'Decimal' datatype.

There's currently no support to represent accentuation, dynamics etc., though it should
be fairly simple to add them in the future ...

n-lets are currently not (really) possible, as well. This might be a bit more of a
challenge, not so much the calculation part, but the parsing part ...


--
Released under GPLv3 or later
