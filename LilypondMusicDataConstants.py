from decimal import *

# seven digits behind the comma should be sufficient ... 
getcontext().prec = 7

# Pitch Classes
REST = Decimal("0.0")
C = Decimal("1.0")
D = Decimal("2.0")
E = Decimal("3.0")
F = Decimal("4.5")
G = Decimal("5.5")
A = Decimal("6.5")
B = Decimal("7.5")

# Modifiers for equal tempered pitch, modifiy as you wish for alternate tunings
none = Decimal("0")
sharp = Decimal("0.5")
flat = Decimal("-0.5")
double_sharp = Decimal("1.0")
double_flat = Decimal("-1.0")
half_sharp = Decimal("0.25")
half_flat = Decimal("-0.25")
sharp_half_sharp = Decimal("0.75")
flat_half_flat = Decimal("-0.75")

# Durations d = dotted, dd = double_dotted
longa = Decimal("4.0")

breve = Decimal("2.0")

dd_w = Decimal("1.75")
d_w = Decimal("1.5")
w = Decimal("1.0")

dd_h = Decimal("0.875")
d_h = Decimal("0.75")
h = Decimal("0.5")

dd_q = Decimal("0.4375")
d_q = Decimal("0.375")
q = Decimal("0.25")

dd_e = Decimal("0.21875")
d_e = Decimal("0.1875")
e = Decimal("0.125")

# currently no dots supported for those small notes ...
st = Decimal("0.0625")
ts = Decimal("0.03125")

# needed to calculate odd duration values, like quarter + sixteenth etc ...
modified_duration_values = [dd_w, d_w, dd_h, d_h, dd_q, d_q, dd_e, d_e]
unmodified_duration_values = [longa, breve, w, h, q, e, st, ts]
all_duration_values = [longa, breve, dd_w, d_w, w, dd_h, d_h, h, dd_q, d_q, q, dd_e, d_e, e, st, ts]

# Comparison factor
pitch = "pitch"
dur = "duration"
lyr = "lyrics" #tbd
dyn = "dynamics" #tbd
