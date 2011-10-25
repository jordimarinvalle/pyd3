"""
Mutagen package extension to make ID3 (http://en.wikipedia.org/wiki/ID3) 
life easier and a more readable code.

Abstract Mutagen layer to get tune audio info:
    - Bit Rate
    - Sample Rate
    - Format
    - Channels
    - ...
"""

import os

from mutagen.mp3 import MP3

def open_mp3(mp3_file):
    """
    Open a audio file to get and/or set data into it's ID3.
    
    Arguments:
    :param mp3_file: string e.g.: /path/to/file/file.mp3
    
    :return: mutagen mp3 class object
    """
    mp3 = MP3(mp3_file)
    try: 
        if len(mp3) is 0: mp3.add_tags()
    except: 
        pass
    return mp3

def get_audio_tune(mp3_file):
    """
    Get audio information from a mp3 file.
    
    size    -- file size, in mb
    length  -- audio length, in seconds
    bitrate -- audio bitrate, in bits per second
    version -- MPEG version (1, 2, 2.5)
    layer   -- 1, 2, or 3
    mode    -- One of STEREO, JOINTSTEREO, DUALCHANNEL, or MONO (0-3)
    sample_rate -- audio sample rate, in Hz
    
    Arguments:
    :param mp3_file: string e.g.: /path/to/file/file.mp3
    
    :return: dictionary 
    """
    audio = open_mp3(mp3_file)
    return {'size'   :get_file_size(mp3_file),
        'length' :get_audio_length(audio.info.length),
        'bitrate':get_audio_bitrate(audio.info.bitrate), 
        'format' :get_audio_format(audio.info.version, audio.info.layer),
        'mode'   :get_audio_mode(audio.info.mode),
        'samplerate':get_audio_samplerate(audio.info.sample_rate),
    }

def get_file_size(file):
    """
    Get file size from a filename path to human easy readable format in megabytes.
    
    Arguments:
    :param file: string e.g.: /path/to/file/file.ext
    
    :return: string
    """
    return "%0.1f MB" % (os.path.getsize(file)/(1024*1024.0))

def get_audio_length(length):
    """
    Get audio length from seconds to human easy readable format.
        hh:mm:ss --in case that is longer than a hour, otherwise-- mm:ss
    
    Arguments:
    :param length: integer -- audio length in seconds
    
    :return: string
    """
    minutes, seconds = divmod(length, 60)
    hours, minutes   = divmod(minutes, 60)
    if hours == 0:
        return "%02d:%02d" % (minutes, seconds)
    return "%02d:%02d:%02d" % (hours, minutes, seconds)
    
def get_audio_bitrate(bitrate):
    """
    Get audio bitrate from bits to human easy readable format in kbits.
    
    Arguments:
    :param bitrate: integer -- audio bitrate in bits per seconds
    
    :return: string
    """
    return "%s kbps" %(bitrate/1000)

def get_audio_version(version):
    """
    Get audio version into a human easy readable format.
    
    Arguments:
    :param version: integer
    
    :return: string
    """
    return "MPG-%i" %(version)
    
def get_audio_layer(layer):
    """
    Get audio layer into a human easy readable format.
    
    Arguments:
    :param layer: integer
    
    :return: string
    """
    return "Layer %i" %(layer)

def get_audio_format(version, layer):
    """
    Get audio layer into a human easy readable format.
    
    Arguments:
    :param layer: integer
    
    :return: string
    """
    return "%s, %s" %(get_audio_version(version), get_audio_layer(layer))

def get_audio_mode(mode):
    """
    Get audio mode (channels mode) into a human easy readable format.
    
    Arguments:
    :param mode: integer
    
    :return: string
    """
    options = {0: "Stereo",
        1: "Joint Stereo",
        2: "Dual Channel",
        3: "Mono",
    }
    return options.get(mode, "Unknown Mode")

def get_audio_samplerate(samplerate):
    """
    Get audio sample rate into a human easy readable format.
    
    Arguments:
    :param samplerate: integer
    
    :return: string
    """
    return "%s kHz" %(samplerate)

def get_id3_tune(mp3_file):
    """
    Get a certain ID3 data from a mp3 file.
    
    Arguments:
    :param mp3_file: string e.g.: /path/to/file/file.mp3
    
    :return: dictionary with Mutagen data for each key
    """
    id3 = open_id3(mp3_file)
    return {'trackn': get_track_number(id3),
        'album'  : get_album(id3),
        'artist' : get_artist(id3),
        'band'   : get_band(id3),
        'title'  : get_title(id3),
        'genre'  : get_genre(id3),
        'year'   : get_year(id3),
        'comment': get_comment(id3),
    }
    