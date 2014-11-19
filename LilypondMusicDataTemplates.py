lilypond_header_template = """
\\header {{
       title = \"{0}\"
       dedication = \"{1}\"
       subtitle = \"{2}\"
       subsubtitle= \"{3}\"
       meter = \"{4}\"
       composer = \"{5}\"

       copyright= \\markup \\teeny {{{6}}}
      }}
"""

lilpond_score_template = """
\\score {{
      <<
      {0}
      >>
}}
"""

lilypond_voice_template = """

    \\new Voice = "{0}" {{
      \\{1}
    }}
    {2}
 \n\n
"""

lilypond_lyrics_template = """
\\new Lyrics \\lyricsto "{0}" {{
  \\{1}lyr
}}\n
"""

lilypond_inner_voice_template = "{0} = {{ \\clef {1} \\time {2}/{3} \n {4} \n }} "
lilypond_inner_lyrics_template = "{0}lyr =  \lyricmode {{ \\clef {1} \\time {2}/{3} \n {4} \n }} "
