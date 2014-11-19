# Pitch Classes
REST = 0.0
C = 1.0
D = 2.0
E = 3.0
F = 4.5
G = 5.5
A = 6.5
B = 7.5

# Modifiers for equal tempered pitch, modifiy as you wish for alternate tunings
none = 0
sharp = 0.5
flat = -0.5
double_sharp = 1.0
double_flat = -1.0
half_sharp = 0.25
half_flat = -0.25
sharp_half_sharp = 0.75
flat_half_flat = -0.75

# Durations d = dotted, dd = double_dotted
longa = 4.0

breve = 2.0

dd_w = 1.75
d_w = 1.5
#w_q = 1.25
w = 1.0

dd_h = 0.875
d_h = 0.75
#h_e = 0.625
h = 0.5

dd_q = 0.4375
d_q = 0.375
#q_st = 0.3125
q = 0.25

dd_e = 0.21875
d_e = 0.1875
#e_ts = 0.15625
e = 0.125

# currently no dots supported for those small notes ...
st = 0.0625
ts = 0.03125

# needed to calculate odd duration values, like quarter + sixteenth etc ...
modified_duration_values = [dd_w, d_w, dd_h, d_h, dd_q, d_q, dd_e, d_e]
unmodified_duration_values = [longa, breve, w, h, q, e, st, ts]
all_duration_values = [longa, breve, dd_w, d_w, w, dd_h, d_h, h, dd_q, d_q, q, dd_e, d_e, e, st, ts]


# Comparison factor
pitch = "pitch"
dur = "duration"
lyr = "lyrics" #tbd
dyn = "dynamics" #tbd
