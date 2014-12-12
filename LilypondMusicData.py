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
# tuplets are currently not (really) possible, as well. This might be a bit more of a
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

# duration default is needed if note is within chord
class Note:
    def __init__(self, pitch_class, pitch_modifier, octave, duration=Decimal("0.25"), syllable="", compare_by = "pitch", **kwargs):
        self.pitch_class = pitch_class
        self.pitch_modifier = pitch_modifier
        self.octave = Decimal(str(octave))
        self.duration = duration
        self.syllable = syllable
        self.compare_by = compare_by
        # if true, the note will be bound to the next note
        self.connect = kwargs.get("connect", False)
        self.in_chord = False
    # calculate actual pitch including all modifiers as a fixed point decimal number
    def actual_pitch(self):
        # multiply octave by 8 to achieve enough distance between octaves for calculation
        overall_pitch = (self.octave * Decimal('8.0'))+ (self.pitch_class + self.pitch_modifier)        
        return overall_pitch
    # note comparison functions
    def __lt__(self, other):
        if(self.compare_by == "pitch"):
            if(other.compare_by == "duration"):
                raise NoteError("Can't compare pitch to length !")
            else:
                return self.actual_pitch() < other.actual_pitch()
        else:
            if(other.compare_by == "pitch"):
                raise NoteError("Can't compare length by pitch !")
            else:
                return self.duration < other.duration
    def __eq__(self, other):
        if(self.compare_by == "pitch"):
            if(other.compare_by == "duration"):
                raise NoteError("Can't compare pitch to length !")
            else:
                return self.actual_pitch() == other.actual_pitch()
        else:
            if(other.compare_by == "pitch"):
                raise NoteError("Can't compare length by pitch !")
            else:
                return self.duration == other.duration
    def __le__(self, other):
        if(self.compare_by == "pitch"):
            if(other.compare_by == "duration"):
                raise NoteError("Can't compare pitch to length !")
            else:
                return self.actual_pitch() <= other.actual_pitch()
        else:
            if(other.compare_by == "pitch"):
                raise NoteError("Can't compare length by pitch !")
            else:
                return self.duration <= other.duration
    # returns the note in its lilypond representation
    def __str__(self):
        # assemble lilypond note string
        note_string = "";
        # map pitch class
        note_string += pitch_class_mapping[self.pitch_class]
        # map pitch modifier        
        note_string += modifier_mapping[self.pitch_modifier]
        # map octave, unless it's a rest
        if self.pitch_class != 0:
            note_string += octave_mapping[self.octave]
        if not self.in_chord:
            # map duration
            note_string += duration_mapping[self.duration]
        if self.connect:
            note_string += " ~ "        
        return note_string

class Rest(Note):
    def __init__(self, duration, compare_by = "pitch"):
        self.pitch_class = REST
        self.pitch_modifier = none
        self.octave = Decimal("0.0")
        self.duration = duration
        self.compare_by = compare_by
        self.syllable = ""
        self.connect = False
        self.in_chord = False
        
# comparing chords ?? consonance ? dissonance ? distance measures ? 
# chord class ... notes only need no duration in that case, as the duration is set for the whole chord
class Chord:
    def __init__(self, notes, duration, **kwargs):
        self.notes = notes
        self.duration = duration
        self.connect = kwargs.get("connect", False)
    def __str__(self):
        chord = "<"
        for note in self.notes:
            note.in_chord = True
            # just to be sure
            note.connect = False
            chord += str(note) + " "
        chord += ">"
        chord += duration_mapping[self.duration]
        if self.connect:
            chord += " ~ "        
        return chord

class LilypondScore():
    def __init__(self, *args, **kwargs):
        self.series_number = kwargs.get('series_number', "")
        self.piece_number = kwargs.get('piece_number', "")
        self.series_title = kwargs.get('series_title', "")
        self.piece_title = kwargs.get('piece_title', "default_title")
        self.dedication = kwargs.get('dedication', "")
        self.subtitle = kwargs.get('subtitle', "")
        self.subsubtitle = kwargs.get('subsubtitle', "")
        self.meter = kwargs.get('meter', "")
        self.composer = kwargs.get('composer', "")
        self.copyright = kwargs.get('copyright', "")
        self.version = kwargs.get('version', "2.18.2")
        self.voices = []
    def __str__(self):
        lilypond_string = ""
        lilypond_string += "\\version \"{0}\"\n".format(self.version)
        for voice in self.voices:
            lilypond_string += str(voice) + "\n\n"
        lilypond_string += lilypond_header_template.format(self.series_title + " " + self.piece_title, self.dedication, self.subtitle, self.subsubtitle, self.meter, self.composer, self.copyright)
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
    # assemble base folder
    def assemble_foldername(self):
        foldername = ""
        if self.series_number != "":
            foldername += self.series_number + "_"
        # if it is a series, generate structure
        if self.series_title != "":
            foldername += self.series_title
            if self.piece_number != "":
                foldername += "/" + self.piece_number
        # otherwise generate simple folder
        else:
            foldername += self.piece_title
        return foldername.replace(" ", "_")
    # assemble filename
    def assemble_filename(self):
        filename = ""
        if self.series_number != "":
            filename += self.series_number + "_"
        if self.piece_number != "":
            filename += self.piece_number + "_"
        if self.series_title != "":
            filename += self.series_title + "_"
        filename += self.piece_title
        if self.subtitle != "":
            filename += "_" + self.subtitle
        return filename.replace(" ", "_")
    # generate the lilypond source file
    def output_ly(self):
        folder = self.assemble_foldername()
        if not os.path.exists(folder):
            os.makedirs(folder)
        if not os.path.exists(folder + "/ly"):
            os.makedirs(folder + "/ly")
        score_file = open(folder + "/ly/" + self.assemble_filename() + ".ly", 'w')
        score_file.write(str(self))
        score_file.close()
    # generate pdf file
    def output_pdf(self):
        self.output_ly()
        # actually output to file
        folder = self.assemble_foldername()
        if not os.path.exists(folder + "/pdf"):
            os.makedirs(folder + "/pdf")
        filename = self.assemble_filename() + ".ly"
        os.system("lilypond -V --output=" + folder + "/pdf " + folder + "/ly/" + filename)

class LilypondVoice():
    def __init__(self, *args, **kwargs):
        self.full_name = kwargs.get('full_name', "some voice name")
        self.short_name = kwargs.get('short_name', "svn")
        self.clef = kwargs.get('clef', "treble")
        self.time_signature = kwargs.get('time_signature', [Decimal('4.0'),q])
        self.notes = []
        # flagging a voice whether it contains lyrics or not ... should help the parsing lateron
        self.contains_lyrics = kwargs.get('contains_lyrics', False)
        self.total_duration = 0
        self.bar_size = self.time_signature[0] * self.time_signature[1]
    def add_note(self, note):
        # actualize total duration of the voice
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
        note_pointer = 0
        while note_pointer < len(self.notes):
            note = self.notes[note_pointer]
            # split notes with odd durations and replace the original note
            if note.duration not in all_duration_values:
                print("Found note with odd value")
                original_note_pointer = note_pointer
                compound_notes = []
                note_to_split = copy.deepcopy(note)            
                while (note_to_split.duration > 0):
                    largest_fitting_duration = 0
                    # find nearest fitting note
                    for i in range(0, len(unmodified_duration_values)):
                        margin = unmodified_duration_values[i] - note_to_split.duration
                        if margin <= 0:
                            # now we should have the nearest margin
                            largest_fitting_duration = unmodified_duration_values[i]
                            #print("FOUND: " + str(largest_fitting_duration))
                            break
                    compound_note = copy.deepcopy(note_to_split)
                    compound_note.duration = largest_fitting_duration
                    note_to_split.duration -= largest_fitting_duration
                    compound_notes.append(compound_note)
                # post-process compound notes (notes that have been splitted, that is)
                for j in range(0, len(compound_notes)):
                    if j != 0:
                        # remove syllable from compound notes
                        compound_notes[j].syllable = ""
                    if j < len(compound_notes) - 1:
                        # bind notes unless it's a rest or a chord
                        if not hasattr(compound_notes[j], 'pitch_class') or compound_notes[j].pitch_class != REST:
                            compound_notes[j].connect = True
                # insert splitted notes into note list
                for c_note in compound_notes:
                    self.notes.insert(note_pointer, c_note)
                    note_pointer += 1
                # remove original note, as it has been replaced
                self.notes.pop(note_pointer)
                note_pointer = original_note_pointer
                continue
            # check if note fits bar, act accordingly (if it fits perfectly, start new bar, otherwise split note)
            if current_bar_remainder > note.duration:                
                bars += str(note) + " "
                # chords have no syllable
                if hasattr(note, 'syllable'):
                    lyrics_bars += note.syllable + " "
                current_bar_remainder = current_bar_remainder - note.duration
            elif current_bar_remainder == note.duration:
                bars += str(note) + " | % " + str(bar_count) + "\n"
                # chords have no syllable
                if hasattr(note, 'syllable'):
                    lyrics_bars += note.syllable + " | % " + str(bar_count) + "\n"
                current_bar_remainder = self.bar_size
                bar_count += 1
            else:
                # split note to two bars with binding, remove orignial note 
                split_note = copy.deepcopy(note)
                original_note = copy.deepcopy(note)
                split_note.duration = split_note.duration - current_bar_remainder
                original_note.duration = current_bar_remainder
                # chords have no pitch class or syllables
                if not hasattr(original_note, 'pitch_class') or original_note.pitch_class != REST:
                    original_note.connect = True
                if hasattr(original_note, 'syllable'):    
                    split_note.syllable=""
                self.notes.insert(note_pointer + 1, split_note)
                self.notes.insert(note_pointer + 1, original_note)
                # remove original note, as it has been replaced
                self.notes.pop(note_pointer)
                continue
            # increment note pointer
            note_pointer += 1
        #assemble voice template
        inner_voice_string = lilypond_inner_voice_template.format(self.short_name, self.clef, int(self.time_signature[0]), int(Decimal("1.0") / self.time_signature[1]), bars)
        # assemble lyrics templates
        inner_lyrics_string = " "
        if self.contains_lyrics:
            inner_lyrics_string = lilypond_inner_lyrics_template.format(self.short_name, self.clef, int(self.time_signature[0]), int(Decimal("1.0") / self.time_signature[1]), lyrics_bars)
        return inner_voice_string + "\n\n" + inner_lyrics_string

# some utilities
class LilypondTools():
    # transform the comparison mode
    def set_comparison_type(self, compare_by, notes):
         return list(map(lambda x : Note(x.pitch_class, x.pitch_modifier, x.octave, x.duration, x.syllable, compare_by = compare_by), notes))
    # in case the voices are of different length, pad the shorter ones until they match the longer ones.
    def match_end(self, voices):
        # find longest voice
        longest_voice = voices[0]
        longest_voice_index = 0
        for voice_ptr in range(0,len(voices)):
            if (voices[voice_ptr]).total_duration > longest_voice.total_duration:
                longest_voice = voices[voice_ptr]
        # match shorter voices to longer voice       
        for voice in voices:  
            if voice != longest_voice:
                voice_difference = (longest_voice.total_duration - voice.total_duration)
                voice.add_note(Rest(voice_difference))
    # if the voice ends on some crude measure, pad it to the next full bar
    def flush_end_to_bar(self, voice):
        bar_rest = voice.total_duration % voice.bar_size
        if bar_rest > Decimal("0.0"):
           voice.add_note(Rest(voice.bar_size - bar_rest))
    # calculate the duration of a sequence of notes
    def calculate_duration(self, notes):
        total_duration = Decimal('0.0')
        if len(notes) == 0:
            return total_duration
        for note in notes:
            total_duration += note.duration
        return total_duration
    # transpose one octave down
    def octave_down(self, notes):
        return list(map(lambda x : Note(x.pitch_class, x.pitch_modifier, x.octave - Decimal('1.0'), x.duration, x.syllable, compare_by = x.compare_by), notes))
