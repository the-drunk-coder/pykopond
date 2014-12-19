# Pitch Classes
REST = 0
C = 100
D = 200
E = 300
F = 450
G = 550
A = 650
B = 750

# Modifiers for equal tempered pitch, modifiy as you wish for alternate tunings
none = 0
sharp = 50
flat = -50
double_sharp = 100
double_flat = -100
half_sharp = 25
half_flat = -25
sharp_half_sharp = 75
flat_half_flat = -75

# Durations d = dotted, dd = double_dotted
longa = 40000000

breve = 20000000

dd_w  = 17500000
d_w   = 15000000  
w     = 10000000

dd_h  = 8750000
d_h   = 7500000
h     = 5000000

dd_q  = 4375000
d_q   = 3750000
q     = 2500000

dd_e  = 2187500
d_e   = 1875000
e     = 1250000

# currently no dots supported for those small notes ...
st    = 625000
ts    = 312500

# needed to calculate odd duration values, like quarter + sixteenth etc ...
modified_duration_values = [dd_w, d_w, dd_h, d_h, dd_q, d_q, dd_e, d_e]
unmodified_duration_values = [longa, breve, w, h, q, e, st, ts]
all_duration_values = [longa, breve, dd_w, d_w, w, dd_h, d_h, h, dd_q, d_q, q, dd_e, d_e, e, st, ts]

# Comparison factor
pitch = "pitch"
dur = "duration"
lyr = "lyrics" #tbd
dyn = "dynamics" #tbd
