# --------
# PyKoPond
# --------
# This is my attempt at creating a flexible and comparable datatype
# to describe and work with music.
#
# Forthermore, this library contains tools to parse this datatype to lilypond.
#
# The approach for the datatype is in some part borrowed from the one you can find in HASKORE
# but more focused on fixed-point decimal arithmetic, using python's 'Decimal' datatype.
#
# There's currently no support to represent accentuation, dynamics etc., though it should
# be fairly simple to add them in the future ...
#
# n-lets are currently not (really) possible, as well. This might be a bit more of a
# challenge, not so much the calculation part, but the parsing part ...

import copy, os, subprocess
from LilypondMusicDataConstants import *
from LilypondMusicDataTemplates import *
from LilypondMusicDataMappings import *
from decimal import *

class NoteError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

class Note:
    def __init__(self, pitch_class, pitch_modifier, octave, duration, syllable="", compare_by = "pitch"):
        self.pitch_class = pitch_class
        self.pitch_modifier = pitch_modifier
        self.octave = Decimal(str(octave))
        self.duration = duration
        self.syllable = syllable
        self.compare_by = compare_by
    # calculate actual pitch including all modifiers as a floating point number
    def actual_pitch(self):
        overall_pitch = (self.pitch_class + self.pitch_modifier)        
        if self.octave != 0.0:
            overall_pitch = overall_pitch * self.octave
        return overall_pitch
    # note comparison functions
    def __lt__(self, other):
        if(self.compare_by == "pitch"):
            if(other.compare_by == "duration"):
                raise NoteError("Can't compare pitch to length !")
            else:
                #print("{0} : {1}".format(self, self.actual_pitch()))
                #print("{0} : {1}".format(other, other.actual_pitch()))
                return  self.actual_pitch() < other.actual_pitch()
        else:
            if(other.compare_by == "pitch"):
                raise NoteError("Can't compare length by pitch !")
            else:
                #print("{0} : {1}".format(self, self.actual_duration()))
                #print("{0} : {1}".format(other, other.actual_duration()))
                return self.duration < other.duration
    def __eq__(self, other):
        if(self.compare_by == "pitch"):
            if(other.compare_by == "duration"):
                raise NoteError("Can't compare pitch to length !")
            else:
                #print("{0} : {1}".format(self, self.actual_pitch()))
                #print("{0} : {1}".format(other, other.actual_pitch()))
                return  self.actual_pitch() == other.actual_pitch()
        else:
            if(other.compare_by == "pitch"):
                raise NoteError("Can't compare length by pitch !")
            else:
                #print("{0} : {1}".format(self, self.actual_duration()))
                #print("{0} : {1}".format(other, other.actual_duration()))
                return self.duration == other.duration
    def __le__(self, other):
        if(self.compare_by == "pitch"):
            if(other.compare_by == "duration"):
                raise NoteError("Can't compare pitch to length !")
            else:
                #print("{0} : {1}".format(self, self.actual_pitch()))
                #print("{0} : {1}".format(other, other.actual_pitch()))
                return  self.actual_pitch() <= other.actual_pitch()
        else:
            if(other.compare_by == "pitch"):
                raise NoteError("Can't compare length by pitch !")
            else:
                #print("{0} : {1}".format(self, self.actual_duration()))
                #print("{0} : {1}".format(other, other.actual_duration()))
                return self.duration <= other.duration
    # returns the note in it's lilypond representation
    def __str__(self):
        note_string = "";

        # divide odd note durations (like, quarter + sixteenth) to multiple, bounded notes
        if self.duration not in all_duration_values:

            compound_notes = []
            note_to_split = copy.deepcopy(self)

            while (note_to_split.duration > 0):
                print("NOTE_TO_SPLIT: " + str(note_to_split.duration))
                largest_fitting_duration = 0

                for i in range(0, len(unmodified_duration_values)):
                    margin = unmodified_duration_values[i] - note_to_split.duration
                    if margin <= 0:
                        # now we should have the nearest margin
                        largest_fitting_duration = unmodified_duration_values[i]
                        print("FOUND: " + str(largest_fitting_duration))
                        break

                compound_note = copy.deepcopy(note_to_split)
                compound_note.duration = largest_fitting_duration
                note_to_split.duration -= largest_fitting_duration

                compound_notes.append(compound_note)

            for i in range(0, len(compound_notes)):
                if i == (len(compound_notes) - 1):
                    note_string += str(compound_notes[i])
                else:
                    note_string += str(compound_notes[i]) + " ~ "
            return note_string

        # Map pitch class

        note_string += pitch_class_mapping[self.pitch_class]
        note_string += modifier_mapping[self.pitch_modifier]

        if self.pitch_class != 0:
            note_string += octave_mapping[self.octave]

        note_string += duration_mapping[self.duration]

        return note_string

class Rest(Note):
    def __init__(self, duration, compare_by = "pitch"):
        self.pitch_class = REST
        self.pitch_modifier = none
        self.octave = Decimal("0.0")
        self.duration = duration
        self.compare_by = compare_by
        self.syllable = ""
        
class LilypondScore():
    def __init__(self, *args, **kwargs):
        self.title = kwargs.get('title', "some title")
        self.dedication = kwargs.get('dedication', "some dedication")
        self.subtitle = kwargs.get('subtitle', "some subtitle")
        self.subsubtitle = kwargs.get('subsubtitle', "some subsubtitle")
        self.meter = kwargs.get('meter', "some meter")
        self.composer = kwargs.get('composer', "some composer")
        self.copyright = kwargs.get('copyright', "some copyright")
        self.version = kwargs.get('version', "2.18.2")
        self.voices = []
    def __str__(self):
        lilypond_string = ""
        lilypond_string += "\\version \"{0}\"\n".format(self.version)
        for voice in self.voices:
            lilypond_string += str(voice) + "\n\n"
        lilypond_string += lilypond_header_template.format(self.title, self.dedication, self.subtitle, self.subsubtitle, self.meter, self.composer, self.copyright)
        voices_string = ""
        for voice in self.voices:
            lyrics = ""
            if voice.contains_lyrics:
                lyrics += lilypond_lyrics_template.format(voice.full_name, voice.short_name)
            voices_string += lilypond_voice_template.format(voice.full_name, voice.short_name, lyrics)
        score_string = lilpond_score_template.format(voices_string)
        lilypond_string += score_string
        return lilypond_string
    def add_voice(self, voice):
        self.voices.append(voice)
    def add_voices(self, voices):
        self.voices.extend(voices)
    def output_ly(self):
        filename = (self.composer + "_-_" + self.title).replace(" ", "_") + ".ly"
        if not os.path.exists("ly"):
            os.makedirs("ly")
        score_file = open("ly/" + filename, 'w')
        score_file.write(str(self))
        score_file.close()
    def output_pdf(self):
        filename = (self.composer + "_-_" + self.title).replace(" ", "_") + ".ly"
        self.output_ly()
        #actually output to file
        if not os.path.exists("pdf"):
            os.makedirs("pdf")
        os.system("lilypond --output=pdf ly/" + filename)

class LilypondVoice():
    def __init__(self, *args, **kwargs):
        self.full_name = kwargs.get('full_name', "some voice name")
        self.short_name = kwargs.get('short_name', "svn")
        self.clef = kwargs.get('clef', "treble")
        self.time_signature = kwargs.get('time_signature', [Decimal('4.0'),q])
        self.notes = []
        self.contains_lyrics = kwargs.get('contains_lyrics', False)
        self.total_duration = 0
        self.bar_size = self.time_signature[0] * self.time_signature[1]
        # this one should it make easier to parse out the lyrics afterwards ...
    def add_note(self, note):
        self.total_duration += note.duration
        self.notes.append(note)
    def add_notes(self, notes):
        # easier to calculate total duration that way
        for note in notes:
            self.add_note(note)
    def __str__(self):
        bar_count = 1
        current_bar_remainder = self.bar_size
        bars = " "
        lyrics_bars = " "
        for note in self.notes:
            # calculate actual note duration
            # print("CURRENT STATE: {0} : {1}".format(current_bar_remainder, note.duration))
            if current_bar_remainder > note.duration:
                bars += str(note) + " "
                lyrics_bars += note.syllable + " "
                current_bar_remainder = current_bar_remainder - note.duration
            elif current_bar_remainder == note.duration:
                bars += str(note) + " | %" + " " + str(bar_count) + "\n"
                lyrics_bars += note.syllable + " | %" + " " + str(bar_count) + "\n"
                current_bar_remainder = self.bar_size
                bar_count += 1
            else:
                # split note to two bars with binding ... we need two copies, as we don't want to alter the orignal data
                split_note = copy.deepcopy(note)
                original_note = copy.deepcopy(note)
                split_note.duration = split_note.duration - current_bar_remainder
                original_note.duration = current_bar_remainder
                print("SPLT NOTE: {0} : {1}".format(note.duration, split_note.duration))
                bars += str(original_note) + " ~ | % " + " " + str(bar_count) + "\n"
                bars += "% SPLIT POINT\n"
                bars += str(split_note) + " "
                lyrics_bars += note.syllable + " | %" + " " + str(bar_count) + "\n"
                lyrics_bars += "% SPLIT POINT\n"
                current_bar_remainder = self.bar_size - split_note.duration
                bar_count += 1
        inner_voice_string = lilypond_inner_voice_template.format(self.short_name, self.clef,int(self.time_signature[0]), int(Decimal("1.0") / self.time_signature[1]), bars)
        inner_lyrics_string = " "
        if self.contains_lyrics:
            inner_lyrics_string = lilypond_inner_lyrics_template.format(self.short_name, self.clef, int(self.time_signature[0]), int(Decimal("1.0") / self.time_signature[1]), lyrics_bars)
            
        return inner_voice_string + "\n\n" + inner_lyrics_string

# some utilities
class LilypondTools():
    # in case the voices are of different length, pad the shorter ones until the match the longer ones.
    def match_end(self, voices):
        # find longest voice
        longest_voice = voices[0]
        for voice_ptr in range(0,len(voices)):
            if (voices[voice_ptr]).total_duration > longest_voice.total_duration:
                longest_voice = voices[voice_ptr]
        # remove longest voice from list (temporariliy)
        voices.remove(longest_voice)
        # match shorter voices to longer voice       
        for voice in voices:
            
            self.flush_end_to_bar(voice)
            
            # calculate empty bars to be filled
            voice_difference = (longest_voice.total_duration - voice.total_duration)
            empty_bars = voice_difference / voice.bar_size

            for i in range(0, int(empty_bars)):
                voice.add_note(Rest(voice.bar_size))

            total_remainder =  voice_difference % voice.bar_size 

            if total_remainder != Decimal('0.0'):
               voice.add_note(Rest(total_remainder))
            
        # finally, add voice to list of voices again
        voices.append(longest_voice)
        
        
    # if the voice end on some crude measure, pad it to the next full bar
    def flush_end_to_bar(self, voice):
        bar_rest = voice.total_duration % voice.bar_size
        print("TOTAL DUR: " + str(voice.total_duration))
        print("BAR SIZE: " + str(voice.bar_size))
        print("BAR REST:" + str(bar_rest))
        print("DIFFERENCE: " + str(voice.bar_size - bar_rest))
        if bar_rest != Decimal("0.0"):
           voice.add_note(Rest(voice.bar_size - bar_rest))
     
