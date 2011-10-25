"""
Mutagen package extension to make ID3 (http://en.wikipedia.org/wiki/ID3) 
life easier and a more readable code.

Abstract Mutagen layer for ID3 data management.
"""

import os
import sys
import mimetypes

from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TRCK, TALB, TPE1, TPE2, TIT2, TCON, TDRC, COMM, APIC

stdout_encoding = sys.stdout.encoding

def open_id3(audio_file):
    """
    Open an audio file to get and/or set data into it's ID3.
    
    Arguments:
    :param mp3_file: string e.g.: /path/to/file/file.mp3
    
    :return: mutagen mp3 class object
    """
    return ID3(audio_file)

def get_track_number(id3):
    """
    Get TRCK Track number/Position from a ID3.
    
    Arguments:
    :param id3: dictionary with mutagen class objects
    
    :return: mutagen TRCK object
    """
    value = str(id3.get('TRCK', ""))
    if '/' in value: value = value.split('/')[0]
    try: value = str(int(value))
    except ValueError: pass
    return TRCK(encoding=3, text=value)

def get_album(id3):
    """
    Get TALB Album/Movie/Show title from a ID3.
    
    Arguments:
    :param id3: dictionary with mutagen class objects
    
    :return: mutagen TALB object
    """
    return id3.get('TALB', TALB(encoding=3, text=""))

def get_artist(id3):
    """
    Get TPE1 Lead performer(s)/Soloist(s) from a ID3.
    
    Arguments:
    :param id3: dictionary with mutagen class objects
    
    :return: mutagen TPE1 object
    """
    return id3.get('TPE1', TPE1(encoding=3, text=""))

def get_band(id3):
    """
    Get TPE2 Band/orchestra/accompaniment from a ID3.
    
    Arguments:
    :param id3: dictionary with mutagen class objects
    
    :return: mutagen TPE2 object
    """
    return id3.get('TPE2', TPE2(encoding=3, text=""))

def get_title(id3):
    """
    Get TIT2 Title/songname/content description from a ID3.
    
    Arguments:
    :param id3: dictionary with mutagen class objects
    
    :return: mutagen TIT2 object
    """
    return id3.get('TIT2', TIT2(encoding=3, text=""))

def get_genre(id3):
    """
    Get TCON Content type from a ID3.
    
    Arguments:
    :param id3: dictionary with mutagen class objects
    
    :return: mutagen TCON object
    """
    return id3.get('TCON', TCON(encoding=3, text=""))

def get_year(id3):
    """ 
    Get TDRC Year (replaced for TYER in v2.3) from a ID3.
    
    Arguments:
    :param id3: dictionary with mutagen class objects
    
    :return: mutagen TDRC object
    """
    return id3.get('TDRC', TDRC(encoding=3, text=""))

def get_comment(id3):
    """ 
    Get COMM User defined text information frame from a ID3.
    
    Arguments:
    :param id3: dictionary with mutagen class objects
    
    :return: mutagen COMM object
    """
    text = 'Add PyD3 into your life.'
    desc = 'PyD3'
    return COMM(encoding=3, text=text, desc=desc)

def get_picture(id3):
    """
    Get APIC Attached picture from a ID3.
    
    Arguments:
    :param id3: dictionary with mutagen class objects
    
    :return: mutagen APIC object
    """
    return id3.get('APIC', APIC(encoding=3, text=""))

def set_track_number(value):
    """
    TRCK Track number/Position.
    
    Arguments:
    :param value: string -- value to set on mutagen object
    
    :return: mutagen TRCK object
    """
    return TRCK(encoding=3, text=value.decode(stdout_encoding))

def set_album(value):
    """
    TALB Album/Movie/Show title.
    
    Arguments:
    :param value: string -- value to set on mutagen object
    
    :return: mutagen TALB object
    """
    return TALB(encoding=3, text=value.decode(stdout_encoding))

def set_artist(value):
    """
    TPE1 Lead performer(s)/Soloist(s).
    
    Arguments:
    :param value: string -- value to set on mutagen object
    
    :return: mutagen TPE1 object
    """
    return TPE1(encoding=3, text=value.decode(stdout_encoding))

def set_band(value):
    """
    TPE2 Band/orchestra/accompaniment.
    
    Arguments:
    :param value: string -- value to set on mutagen object
    
    :return: mutagen TPE2 object
    """
    return TPE2(encoding=3, text=value.decode(stdout_encoding))

def set_title(value):
    """
    TIT2 Title/songname/content description.
    
    Arguments:
    :param value: string -- value to set on mutagen object
    
    :return: mutagen TIT2 object
    """
    return TIT2(encoding=3, text=value.decode(stdout_encoding))

def set_genre(value):
    """
    TCON Content type.
    
    Arguments:
    :param value: string -- value to set on mutagen object
    
    :return: mutagen TCON object
    """
    return TCON(encoding=3, text=value.decode(stdout_encoding))

def set_year(value):
    """
    TDRC Year (replaced for TYER in v2.3).
    
    Arguments:
    :param value: string -- value to set on mutagen object
    
    :return: mutagen TDRC object
    """
    return TDRC(encoding=3, text=value.decode(stdout_encoding))

def set_comment(text):
    """
    COMM User defined text information frame
    
    Arguments:
    :param text: string -- text to set on mutagen object
    
    :return: mutagen COMM object
    """
    text = 'Add PyD3 into your life.'
    desc = 'PyD3'
    return COMM(encoding=3, text=text.decode(stdout_encoding), desc=desc)

def set_picture(audio, image, type, encoding=3, desc=''):
    """
    APIC image
    
    Attributes for mutagen.id3.APIC:
    encoding -- text encoding for the description
    mime -- a MIME type (e.g. image/jpeg) or '-->' if the data is a URI
    type -- the source of the image (3 is the album front cover)
    desc -- a text description of the image
    data -- raw image data, as a byte string
    
    Arguments:
    :param image    : string  -- image to set/add on mutagen object
    :param type     : integer -- value which determine the assignement of the image given to id3 data:
                                The metadata can also contain images of the following types:
                                cover (front) = 3, cover (back) = 4, Media (e.g. label side of CD) = 6, ....
    :param encoding : integer -- encoding type
    :param desc     : string  -- description text
    
    :return: mutagen APIC object
    """
    return APIC(encoding = 3,
            mime    = mimetypes.guess_type(image)[0],
            type    = type,
            desc    = str(type),
            data    = open(image).read()
    )

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

def set_id3_tag_tune(id3_tag, id3_tag_value):
    """
    Set a Mutagen object for a id3 tag.
    
    Arguments:
    :param id3_tag: string -- id3 tag such as artist, title, album ...
    :param id3_tag_value: string -- id3 tag value 
    
    :return: Mutagen object
    """
    case = {
        'trackn': set_track_number,
        'album'  : set_album,
        'artist' : set_artist,
        'band'   : set_band,
        'title'  : set_title,
        'genre'  : set_genre,
        'year'   : set_year,
        'comment': set_comment,
    }
    return case[id3_tag](id3_tag_value)
    
def save_id3_data(mp3_file, id3, images=None):
    """
    Add & Save ID3 data into a file. Also adds a image on it if exists.
    
    Arguments:
    :param mp3_file: string -- e.g.: /path/to/file/file.mp3
    :param id3: dictionary -- dictionary with Mutagen ID3 Objects
    
    :return: None
    """
    try:
        file_id3_backup = open_id3(mp3_file)
        
        file_id3 = open_id3(mp3_file)
        file_id3.delete()
        file_id3.save(v1=2)
        
        for tag in id3:
            if id3.get(tag) is '': continue
            if id3: file_id3.add(id3[tag])
        if file_id3: file_id3.save(v1=2)
        for key in images.keys():
            if images[key] is None: continue
            file_id3 = open_id3(mp3_file)
            file_id3.add(set_picture(file_id3, images[key]['file'], images[key]['apictype']))
            if file_id3: file_id3.save(v1=2)
        if file_id3: file_id3.save(v1=2)
    except:
        file_id3_backup.save(v1=2)
        raise Exception ("Except error: ID3 from file %s was NOT saved." %(mp3_file))
    
def delete_id3(self, mp3_file):
    """
    @not in use.
    Delete ID3 data from a file.
    """
    try:
        audio_id3 = ID3(mp3_file)
        audio_id3.delete()
        audio_id3.save(v1=2)
        return True
    except:
        return False
    