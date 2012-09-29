"""
Mutagen package extension to make ID3 (http://en.wikipedia.org/wiki/ID3)
life easier and a more readable code.

Abstract Mutagen layer for ID3 data management.
"""
import os
import sys
import mimetypes

from mutagen.id3 import ID3, TRCK, TALB, TPE1, TPE2, TIT2, TCON, TDRC, COMM, TCMP, APIC

stdout_encoding = sys.stdout.encoding

class Id3Gw():

    f = ''
    id3 = None

    def __init__(self, f):
        self.f = f
        self.id3 = self.open(f)


    def open(self, f):
        """
        Open an audio file to get and/or set data into it's ID3.

        Arguments:
        :param f: string e.g.: /path/to/file/file.mp3

        :return: mutagen ID3 object
        """
        try: return ID3(f)
        except: return ID3()


    def delete(self):
        """Delete ID3 data."""
        self.id3.delete()


    def save(self, f=''):
        """Save ID3 data."""
        if not f: f = self.f
        try:
            self.id3.save(filename=f, v1=2)
        except:
            raise Exception ("Except error: ID3 from file %s was NOT saved." %(os.basename(self.f)))


    def get_id3(self):
        """
        Get basic ID3 data.

        :return: dictionary with basic ID3 data such as trackn, album, artist, title, genre, year, comment, band, compilation.
        """
        return {
            'trackn': self.get_trackn(),
            'album': self.get_album(),
            'artist': self.get_artist(),
            'title': self.get_title(),
            'genre': self.get_genre(),
            'year': self.get_year(),
            'comment': self.get_comment(),
            'band': self.get_band(),
            'compilation': self.get_compilation(),
            }

    def set_id3_tag_tune(self, id3_tag, id3_tag_value):
        case = {
            'trackn': self.set_trackn,
            'album' : self.set_album,
            'artist' : self.set_artist,
            'band' : self.set_band,
            'title' : self.set_title,
            'genre' : self.set_genre,
            'year' : self.set_year,
            'comment': self.set_comment,
            'compilation': self.set_compilation,
            }
        case[id3_tag](id3_tag_value)


    def set_trackn(self, value):
        """
        TRCK Track number/Position.

        Arguments:
        :param value: string -- value to set on mutagen object
        """
        self.id3.add(TRCK(encoding=3, text=value.decode(stdout_encoding)))


    def set_album(self, value):
        """
        TALB Album/Movie/Show title.

        Arguments:
        :param value: string -- value to set on mutagen object
        """
        self.id3.add(TALB(encoding=3, text=value.decode(stdout_encoding)))


    def set_artist(self, value):
        """
        TPE1 Lead performer(s)/Soloist(s).

        Arguments:
        :param value: string -- value to set on mutagen object
        """
        self.id3.add(TPE1(encoding=3, text=value.decode(stdout_encoding)))


    def set_band(self, value):
        """
        TPE2 Band/orchestra/accompaniment.

        Arguments:
        :param value: string -- value to set on mutagen object
        """
        if value is "VA":
            self.set_compilation("1")
        self.id3.add(TPE2(encoding=3, text=value.decode(stdout_encoding)))



    def set_compilation(self, value):
        """
        TPE2 Compilation.

        Arguments:
        :param value: string -- value to set on mutagen object
        """
        self.id3.add(TCMP(encoding=3, text=value.decode(stdout_encoding)))


    def set_title(self, value):
        """
        TIT2 Title/songname/content description.

        Arguments:
        :param value: string -- value to set on mutagen object
        """
        self.id3.add(TIT2(encoding=3, text=value.decode(stdout_encoding)))


    def set_genre(self, value):
        """
        TCON Content type.

        Arguments:
        :param value: string -- value to set on mutagen object
        """
        self.id3.add(TCON(encoding=3, text=value.decode(stdout_encoding)))


    def set_year(self, value):
        """
        TDRC Year (replaced for TYER in v2.3).

        Arguments:
        :param value: string -- value to set on mutagen object
        """
        self.id3.add(TDRC(encoding=3, text=value.decode(stdout_encoding)))


    def set_comment(self, text):
        """
        COMM User defined text information frame

        Arguments:
        :param text: string -- text to set on mutagen object

        :return: mutagen COMM object
        """
        text = 'Add PyD3 into your life.'
        desc = 'PyD3'
        self.id3.add(COMM(encoding=3, text=value.decode(stdout_encoding)), desc=desc)


    def set_picture(self, f, type, encoding=3):
        """
        APIC image

        Attributes for mutagen.id3.APIC:
        encoding -- text encoding for the description
        mime -- a MIME type (e.g. image/jpeg) or '-->' if the data is a URI
        type -- the source of the image (3 is the album front cover)
        desc -- a text description of the image
        data -- raw image data, as a byte string

        Arguments:
        :param f        : string  -- image file path to set/add on mutagen object
        :param type     : integer -- value which determine the assignement of the image given to id3 data:
                                    The metadata can also contain images of the following types:
                                    cover (front) = 3, cover (back) = 4, Media (e.g. label side of CD) = 6, ....
        :param encoding : integer -- encoding type

        :return: mutagen APIC object
        """
        return self.id3.add(
            APIC(encoding = encoding,
                mime    = mimetypes.guess_type(f)[0],
                type    = type,
                desc    = str(type),
                data    = open(f).read()
            )
        )


    def get_trackn(self):
        """
        Get TRCK Track number/Position from a ID3.

        :return: unicode track number
        """
        value = str(self.id3.get('TRCK', ''))
        if '/' in value:
            value = value.split('/')[0]

        try:
            value = str(int(value))
        except ValueError:
            pass

        return unicode(value)


    def get_album(self):
        """
        Get TALB Album/Movie/Show title from a ID3.

        :return: unicode album
        """
        return unicode(self.id3.get('TALB', ''))


    def get_artist(self):
        """
        Get TPE1 Lead performer(s)/Soloist(s) from a ID3.

        :return: unicode artist
        """
        return unicode(self.id3.get('TPE1', ''))


    def get_band(self):
        """
        Get TPE2 Band/orchestra/accompaniment from a ID3.

        :return: unicode band
        """
        #if value is "VA":
        #    self.set_compilation("1")
        return unicode(self.id3.get('TPE2', ''))


    def get_compilation(self):
        """
        Get TCMP Compilation from a ID3.

        :return: unicode compilation
        """
        return unicode(self.id3.get('TCMP', ''))


    def get_title(self):
        """
        Get TIT2 Title/songname/content description from a ID3.

        :return: unicode title
        """
        return unicode(self.id3.get('TIT2', ''))


    def get_genre(self):
        """
        Get TCON Content type from a ID3.

        :return: unicode genre
        """
        return unicode(self.id3.get('TCON', ''))


    def get_year(self):
        """
        Get TDRC Year (replaced for TYER in v2.3) from a ID3.

        :return: unicode year
        """
        return unicode(self.id3.get('TDRC', ''))


    def get_comment(self):
        """
        Get COMM User defined text information frame from a ID3.

        :return: unicode comment
        """
        return unicode('Add PyD3 into your life.')

    def get_picture(self):
        """
        Get APIC Attached picture from a ID3.

        :return: binary image
        """
        return self.id3.get('APIC', None)

    #def __unicode__(self):
    #    self.get_id3()

