from LilypondMusicDataConstants import *

pitch_class_mapping = {
    C : "c",
    D : "d",
    E : "e",
    F : "f",
    G : "g",
    A : "a",
    B : "b",
    REST: "r"
}

modifier_mapping = {
    sharp : "is",
    flat : "es",
    double_sharp : "isis",
    double_flat : "eses",
    half_sharp : "ih",
    half_flat : "eh",
    flat_half_flat : "eseh",
    sharp_half_sharp : "isih",
    none : ""
}

octave_mapping = {
    0 : ",,,",
    8 : ",,",
    16 : ",",
    24 : "",
    32 : "\'",
    40 : "\'\'",
    48 : "\'\'\'",
    56 : "\'\'\'\'",
    64 : "\'\'\'\'\'",
    72 : "\'\'\'\'\'\'"
}

duration_mapping = {
    longa : "\\longa",
    breve : "\\breve",
    dd_w : "1..",
    d_w : "1.",
    w : "1",
    dd_h : "2..",
    d_h : "2.",
    h : "2",
    dd_q : "4..",
    d_q : "4.",
    q : "4",
    dd_e : "8..",
    d_e : "8.",
    e : "8",
    st : "16",
    ts : "32"
}
