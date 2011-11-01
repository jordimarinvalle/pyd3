import os
import sys
import mimetypes
import imghdr
import textwrap

from PIL import Image as pil

from unicoder import unicoder
from slugy import slugy
import screaner
import dragger
import id3gateway as id3g
import audiogateway as audiog

class Utils:
    
    def get_file_name(self, file):
        """
        Get filename from a file path.
        
        Arguments:
        :param file: string e.g.: /path/to/file/file.ext
        
        :return: string
        """
        return os.path.basename(file)
        
    
    def get_bytes_converter(self, bytes):
        """
        Get a human readable bits size format from a bunch of bytes
        
        Arguments:
        :param bytes: int
        
        :return: string
        """
        for type in ['bytes','KB','MB','GB','TB']:
            if bytes < 1024.0:
                return "%3.1f %s" % (bytes, type)
            bytes /= 1024.0
            
    
    def get_file_size(self, file):
        """
        Get file size from a filename path into a human readable format.
        
        Arguments:
        :param file: string e.g.: /path/to/file/file.ext
        
        :return: string
        """
        return self.get_bytes_converter(os.path.getsize(file))
    
    
    def get_dir_size(self, the_path, tree=False):
        """
        Get the total size of the directory and its files.

        Also, it can return the total size of the directory --with its directiores 
        and files on a recursive mode--. See optional "tree" param.
        
        Arguments:
        :param the_path: string e.g.: /path/to/get/its/size/
        :param tree: boolean -- True if you want to get size of a directory tree otherwise False
        
        :return: string
        """
        path_size = 0
        for path, dirs, files in os.walk(the_path):
            for file in files:
                path_size += os.path.getsize(os.path.join(path, file))
            if tree is False: return self.get_bytes_converter(path_size)
        return self.get_bytes_converter(path_size)
    
    
    def get_file_mimetype(self, file):
        """
        Get file mimetype from a filename path.
        
        Arguments:
        :param file: string e.g.: /path/to/file/file.ext
        
        :return: string
        """
        return mimetypes.guess_type(file)[0]
        
    

class Audio:
    
    allowed_mimetypes = ('audio/mpeg', 'audio/x-mpg')
    
    def is_a_mp3_file(self, file):
        """
        Check if file is a mp3 file or not.
        
        Arguments:
        :param file: file e.g.: /path/filename.ext
        
        Return: boolean
        """
        file_ext = os.path.splitext(file)[1]
        if self.is_an_audio_file(file) and file_ext == '.mp3':
            return True
        return False
        
    
    def is_an_audio_file(self, file):
        """
        Check if file is an audio file or not.
        
        Arguments:
        :param file: file e.g.: /path/filename.ext
        
        :return: boolean
        """
        file_mimetype = mimetypes.guess_type(file)[0]
        if file_mimetype in self.allowed_mimetypes:
            return True
        return False
        
        
    def get_audio_flattened(self, tunes_data):
        """
        Get a summary of audio tunes data removing duplicated values.
        
        Arguments:
        :param audio_data: dictionary
        
        :return: dictionary -- dictionary with data for each key
        """
        audio_flattened = {}
        for tune in tunes_data:
            empty_tags = []
            for key, value in tune['audio'].iteritems():
                if not str(value):
                    empty_tags.append(key)
                    continue
                if not audio_flattened.has_key(key):
                    audio_flattened[key] = [value]
                elif value not in audio_flattened[key] and value is not None:
                    audio_flattened[key].append(value)
        return audio_flattened


class Id3:
    
    def get_tune_data(self, mp3_file):
        """
        Get MP3 data for a file given. 
            - Filename and file path.
            - Audio data
            - ID3 data
            
        Arguments:
        :param mp3_file: string -- mp3 file path: e.g.: /path/filename.mp3
        
        :return: dictionary
        """
        return {
            'filename': {'source': mp3_file},
            'audio': audiog.get_audio_tune(mp3_file),
            'id3': id3g.get_id3_tune(mp3_file)
        }
        
    
    def get_id3_flattened(self, tunes_data):
        """
        Get a summary of id3 tunes data removing duplicated values.
        
        Arguments:
        :param tunes_data: dictionary -- dictionary with Mutagen objects data for each key (id3 tag)
        
        :return: dictionary -- dictionary with data for each key (id3 tag)
        """
        id3_flattened = {'warnings': {}}
        for tune in tunes_data:
            empty_tags = []
            for tag, id3_object in tune['id3'].iteritems():
                if not str(id3_object) and tag is not 'band':
                    empty_tags.append(tag)
                    continue
                if not id3_flattened.has_key(tag):
                    id3_flattened[tag] = [id3_object]
                elif id3_object not in id3_flattened[tag] and id3_object is not None:
                    id3_flattened[tag].append(id3_object)
            if empty_tags: 
                id3_flattened['warnings'][tune['filename']['source']] = empty_tags
        return id3_flattened
        
    
    def is_va_tunes_collection(self, tunes_data):
        """
        Check if tunes have several artists or not.
        @not_in_use.
        
        Arguments:
        :param tunes_data: dictionary
        
        :return: boolean
        """
        artist = []
        for tune in tunes_data:
            if tune['id3']['artist'] not in artist:
                artist.append(tune['id3']['artist'])
        return True if len(artist) > 1 else False
        
    
    def get_band_tag_value_attr(self, is_a_va_album=False):
        """
        Get value attribute band for various artists tunes collection.
        
        Arguments:
        :param is_a_va_album: boolean
        
        :return: string
        """
        return 'VA' if is_a_va_album else ''
        
    
    def set_value_attr_to_band_tag(self, tunes_data, value="VA"):
        """
        Set value to attr band ID3 tag.
        For albums which have several artists (AKA compilations), 
        tunes needs to be grouped by band ID3 tag.
        
        Arguments:
        :param tunes_data: dictionary
        :param value: string
        
        :return tunes_data: dictionary -- dictionary updated
        """
        for i, tune in enumerate(tunes_data):
            tunes_data[i]['id3']['band'] = id3g.set_band(value)
        return tunes_data
        
    
    def save_id3_data(self, tune_file, id3, apic_images):
        """
        Save ID3 data into a tune file -- also attach a image.
        
        Arguments:
        :param tune_file: string -- file path e.g.: /path/to/tune_file.ext
        :param id3: dictionary -- dictionary with id3 data which contains Mutagen objects
        :param apic_images: dictionary -- dictionary with apic image data (image file path is included)
        
        :return: boolean
        """
        try: id3g.save_id3_data(tune_file, id3, apic_images)
        except Exception, e: raise PyD3Error(e)
        
    
    def get_folder_summary(self, tunes):
        """
        Get a "summary" of the data processed.
        - Files (tunes files)
        - Audio data
        - ID3 data
        - Image(s)
        - Paths
        - Non expected files
        
        :return: dictionary
        """
        return {
            'files': {'tune': tunes},
            'audio': self.flattened_data['audio'],
            'id3'  : self.flattened_data['id3'],
            'image': self.apic_images,
            'path' : {'source_dir': self.paths['source_dir'], 'target_dir': self.paths['target_dir']},
            'non_expected_files': self.non_expected_files
        }
        
    
    def list_empty_tags(self):
        if not self.flattened_data['id3']['warnings']: return raw_input("[ii] All ID3 tags has a value. None is empty.")
        for file in self.flattened_data['id3']['warnings']:
            print "ID3 tag(s) %s has not a value on %s file" %(', '.join(self.flattened_data['id3']['warnings'][file]), unicoder(os.path.basename(file)))
        return raw_input("Press a KEY to continue.")


class Image:
    
    extensions = ('jpg', 'png', 'jpeg', 'JPG', 'PNG', 'JPEG')
    
    image_types = {
        'apic_9': {'id': 3, 'filename':('cover', 'front',), 'name': "Cover (front)",    'desc':"Cover (front)"},
        'apic_8': {'id': 4, 'filename':('back',),           'name': "Cover (back)",     'desc':"Cover (back)"},
        'apic_7': {'id': 6, 'filename':('media',),          'name': "Media",            'desc':"Media (e.g. label side of CD)"},
    }
    
    def get_candidate_filenames(self, key):
        """
        Get candidate filenames.
        
        Arguments:
        :param key: string
        
        :return: list
        """
        candidate_files = []
        for filename in self.image_types[key]['filename']:
            for extension in self.extensions:
                candidate_files.append("%s.%s" %(filename, extension))
        return candidate_files
        
    
    def is_a_image(self, file):
        """
        Check if file is a image file or not.
        
        Arguments:
        :param file: string e.g.: /path/image_file.ext
        
        :return: boolean
        """
        if os.path.isfile(file) and imghdr.what(file):
            return True
        return False
        
        
    def get_image_dimensions(self, img_file):
        """
        Get image dimensions on pixels (width x height)
        
        Arguments:
        :param img_file: string e.g.: /path/image_file.ext
        
        :return: tuple --  (width, height)
        """
        return pil.open(img_file).size
        
        
    def get_image_text_dimensions(self, img_file):
        """
        Get image text dimensions on pixels: widthpxxheight
        
        Arguments:
        :param img_file: string e.g.: /path/image_file.ext
        
        :return: string
        """
        dimensions = self.get_image_dimensions(img_file)
        return "%sx%spx" %(str(dimensions[0]), str(dimensions[1]))
        
        
    def is_a_square_image(self, img_file):
        """
        @not in use.
        Check if image is square or not.
        
        Arguments:
        :param img_file: string e.g.: /path/image_file.ext
        
        :return: boolean
        """
        (width, height) = self.get_image_dimensions(img_file)
        if (float(width)/float(height) == 1):
            return True
        return False
        
    
    def get_apic_images(self, image_files):
        """
        Get tune image(s). By the way its only cover image required.
        
        Arguments:
        :param image_files: tuple -- each item should be like e.g.: /music/library/path/image_file.ext
        
        :return: dictionary
        """
        return {'apic_9': self.get_tune_cover(image_files)}


    def get_tune_cover(self, image_files):
        """
        A cover image must have a filename & extension, as follows:
            - cover.jpg, cover.png, cover.bmp, cover.jpeg
        A square image fit best as a cover image.
        
        :param image_files: tuple -- each element is like e.g.: /path/image.ext
        
        :return: dictionary / None -- image filename path e.g.: /path/image.ext and id3.apic.type -- otherwise None
        """
        candidate_files = self.get_candidate_filenames('apic_9')
        for image_file in image_files:
            if os.path.basename(image_file) in candidate_files:
                return {'file':image_file, 'apictype':self.image_types['apic_9']['id']}
        return None
    

class Filename:
    
    def get_trackn_max_digits(self, n_mp3_files):
        """
        Get track number max digits -- i.e.: For a set of 101 files, it will return a 3 digit integer.
        
        Arguments:
        :param n_mp3_files: integer -- the number of a set of files
        
        :return: integer
        """
        return len(str(n_mp3_files))
        
    
    def get_trackn_padded(self, trackn, trackn_max_digits=0):
        """
        Fill with zeros track number as track max digits value has.
        
        Arguments:
        :param trackn: integer
        :param trackn_max_digits: integer
        
        :return: string
        """
        return str(trackn).zfill(trackn_max_digits) if trackn else None
        
    
    def get_tunned_filename(self, filename, id3, trackn_max_digits):
        """
        Get a tunned filename.
        
        Arguments:
        :param filename: string -- e.g.: file.mp3
        :param id3: dictionary -- dictionary which includes mutagen data for each key
        :param trackn_max_digits: integer
        
        :return: string
        """
        return self.get_target_audio_file_filename(filename, id3, trackn_max_digits)
        
    
    def get_target_audio_file_filename(self, filename, id3, trackn_max_digits):
        """
        Get a tunned filename.
        
        Arguments:
        :param filename: string e.g.: file.mp3
        :param id3: dictionary -- dictionary which includes mutagen data for each key
        :paran trackn_max_digits: integer
        
        :return: string
        """
        filename_name, filename_ext = os.path.basename(os.path.splitext(filename)[0]), os.path.splitext(filename)[1]
        (trackn, artist, title) = (id3.get('trackn', []), id3.get('artist', []), id3.get('title', []))
                
        if trackn[0] and artist[0] and title[0]:
            filename_name = "%s %s - %s" %(self.get_trackn_padded(trackn, trackn_max_digits), artist, title)
        elif artist[0] and title[0]:
            filename_name = "%s - %s" %(artist, title)
        return "%s%s" %(slugy(filename_name, "_"), filename_ext)
        
    
    def get_non_expected_files(self, files):
        """
        Get non expected files from a bunch of files.
        Non expected files are:
            - Is not a tune -- mp3 tune.
            - Is not a image attached to a file -- sucha as a cover image.
        
        Arguments:
        :param files: list
        
        :return: list
        """
        tune_files  = [d['filename']['source'] for d in self.tunes]
        image_files = [image['file'] for image in self.apic_images.values() if image is not None]
        image_files = ('',) if image_files is None else image_files
        
        non_expected_files = []
        for f in files:
            filename = os.path.basename(f)
            if f not in tune_files and f not in image_files and filename not in self.dismissing_files:
                d = {'filename': filename, 'data': {'path': f, 'consider': False}}
                non_expected_files.append(d)
        return non_expected_files
        
    
    def copy_file(self, source_file, target_file):
        """
        Copy a file from /path1/file_x.ext to /path2/file_y.ext
        
        Arguments:
        :param source_file: string e.g.: /path1/file_x.ext
        :param target_file: string e.g.: /path2/file_y.ext
        
        :return: None
        """
        import shutil
        try:
            shutil.copyfile(source_file, target_file)
        except (IOError, shutil.Error):
            raise PyD3Error("file %s was not copied." %(os.path.basename(source_file)))
        
        
class Directory:
    
    def get_target_dir(self, directory, id3_flattened, is_a_va_album):
        """
        Get target tune directory.
        
        Arguments:
        :param directory: string -- e.g.: directory
        :param flattened_id3_data: dictionary
        :param is_a_va_album: boolean
        
        :return: string
        """
        return self.get_top_hat_target_dir(directory, id3_flattened, is_a_va_album)
        
    
    def get_top_hat_target_dir(self, directory, id3, is_a_va_album=False):
        """
        Get a "magic" tune directory name from id3 data, determinated as: 
        If there is data on id3_album, id3_artist and id3_genre, creates a string with them, 
        else original path. In any case, it slugs the final string before returning it.
        
        Arguments:
        :param directory: string -- e.g.: directory
        :param id3: dictionary 
        :param is_a_va_album: boolean
        
        :return: string
        """
        (artist, album, genre) = (id3.get('artist', ('',))[0], id3.get('album', ('',))[0], id3.get('genre', ('',))[0])
        
        if album and artist and is_a_va_album is False:
            directory = "%s - %s" %(artist, album)
        elif album and is_a_va_album is True:
            directory = "%s" %(album)
        
        if 'soundtrack' in str(genre).lower():
            directory = "OST - %s" %(directory)
        
        return slugy(directory, ' ', False)
        

    def get_target_tune_path(self, main_target_path, target_dir):
        """
        Get target tune path.
        
        Arguments:
        :param main_target_path: string -- e.g.: /music/target/path/
        :param target_dir: string -- e.g.: directory
        
        :return: string -- e.g.: /music/target/path/directory/
        """
        return os.path.join(main_target_path, target_dir)
        
        
    def get_alternative_custom_target_dir(self, target_dir, main_target_path):
        """
        Get a alternative custom target directory. 
        It will rise when a path already exists and 
        it is mandatory to create a directory.
        
        Arguments:
        :param target_dir: string -- e.g.: directory
        :param main_target_path: string -- e.g.: /music/target/path/
        
        :return:
        """
        custom_target_dir = raw_input(textwrap.dedent("""\
                Directory [%s] already exists on [%s] path. 
                Please, provide a target file container name (AKA folder).
                >>> """) %(target_dir, main_target_path))
        if custom_target_dir == self.skip_key: return False
            
        return custom_target_dir if custom_target_dir is not "" else target_dir
        
    
    def create_dir(self, path, mode=0777):
        """
        Creates a directory for a given path.
        
        Arguments:
        :param path: string e.g.: /path/to/somewhere/
        :param mode: integer (octal) -- system permissions for the path
        
        :return: boolean -- True if success, False if path already exists.
        """
        try:
            os.mkdir(path, mode)
        except OSError:
            return False
        return True
        

class Prompter:
    
    def prompt_get_id3_tag(self):
        """
        Promts user to get which id3 tags wants to edit.
        It can be select several id3 tags, splitted by semicolons.
        
        :return: list -- list of id3 tags.
        """
        tag_list = ('trackn', 'album', 'artist', 'title', 'genre', 'year')
        while 1:
            option_tag = raw_input(textwrap.dedent("""\
                %s
                Write the ID3 tags (splitted by semicolons) following listed which you want to update. (%s): 
                Write "__ALL__" to get all ID3 tags listed. -- Without quotes --
                >> """) %("-"*120 , ", ".join(tag_list)))
            
            if option_tag == '__ALL__': return tag_list
            if option_tag == '' or option_tag == self.skip_key: return []
            
            option_tags = [tag.strip() for tag in option_tag.split(',')]
            tags_not_ok = [tag for tag in option_tags if tag not in tag_list]
            
            if len(tags_not_ok) == 0:
                return option_tags
            print "Tags [%s] are not valid, check possible ID3 listed tags and spelling." %(", ".join(tags_not_ok))
        
    
    def prompt_get_id3_tag_value(self, tag):
        """
        Prompt user to get a value for a id3 tag presented.
        
        Arguments:
        :param tag: string -- id3 tag name
        
        :return: raw input waiting for a user option.
        """
        return raw_input(textwrap.dedent("""\
            Write a ID3 (%s) tag value. 
            >>> """) %(tag))
    

class Edit:
    
    def edit_target_dir(self):
        """
        Prompt user to add a custom target directory.
        -- Edit target folder directory name. --
        """
        target_dir = self.paths['target_dir']
        custom_dir = raw_input(textwrap.dedent("""\
            Add a target directory if you don't agree with the following proposal 
            -- %s --. Otherwise leave it empty. 
            >> """ %(target_dir)))
        
        if custom_dir == self.skip_key or custom_dir == "": return True
        
        self.paths['target_dir'] = custom_dir
        self.custom_target_dir = True
    
    
    def edit_all_tunes(self):
        """
        Prompt user to edit id3 tunes values by one shot.     
        -- Select id3 tag(s) and values to update all tunes by one shot. --
        """
        option_tags = self.prompt_get_id3_tag()
        for tag in option_tags:
            tag_value = self.prompt_get_id3_tag_value(tag)
            if tag_value == self.skip_key: return
            for i, tune in enumerate(self.tunes):
                self.tunes[i]['id3'][tag] = id3g.set_id3_tag_tune(tag, tag_value)
    
    
    def edit_tune_by_tune(self):
        """"
        Prompt user and edit tunes, by a shot -- well, a bunch of them.
        -- Select id3 tag(s), and then tune by tune add value(s) for the selected id3 tag(s). --
        """
        option_tags = self.prompt_get_id3_tag()
        if not option_tags: return
        for i, tune in enumerate(self.tunes):
            self.print_tune_short_summary(tune)
            for tag in option_tags:
                tag_value = self.prompt_get_id3_tag_value(tag)
                if tag_value == self.skip_key: return
                self.tunes[i]['id3'][tag] = id3g.set_id3_tag_tune(tag, tag_value)
    
    
    def edit_a_tune_from_a_list_of_tunes(self):
        """
        Promt user with a list of tunes, with the following format.
        [n] filename.ext -- where n is a number.
        Users can see and edit id3 data.
        -- List tune filenames, view and edit a specific tune. --
        """
        for (i, tune) in enumerate(self.tunes, 1):
            print "[%i] %s" %(i, os.path.basename(tune['filename']['source']))
        
        while 1:
            try:
                op = raw_input(textwrap.dedent("""\
                    Select a tune# number to see & edit ID3 data.
                    >> """))
                if op == self.skip_key: return
                
                i = int(op)-1
                self.print_tune_info(self.tunes[i], self.apic_images)
                break
            except (ValueError, IndexError):
                raw_input("__INVALID_OPTION__ [%s]... Press a KEY to continue. " %(op))
            
        self.edit_a_tune(i)
    
    
    def edit_a_tune(self, i):
        """
        Prompt user to edit a ID3 tune data.
        """
        option_tags = self.prompt_get_id3_tag()
        for tag in option_tags:
            tag_value = self.prompt_get_id3_tag_value(tag)
            self.tunes[i]['id3'][tag] = id3g.set_id3_tag_tune(tag, tag_value)
    
    
    def edit_apic_images(self):
        """
        -- Edit apic images. --
        """
        ops = {}
        options = []
        image_reverse_key_types = sorted(self.image_types.keys(), reverse=True)
        for i, type in enumerate(image_reverse_key_types):
            ops[str(i)] = type
            options.append("[%i] %s" %(i, self.image_types[type]['desc']))
        
        while 1:
            try:
                op = raw_input(textwrap.dedent("""\
                    Select an option. %s
                    >> """ %('. '.join(s for s in options))
                ))
                if op == self.skip_key: return
                tune_image_type = self.image_types[ops[op]]
                
                image = str(raw_input(textwrap.dedent("""\
                    Provide the path of a new image. e.g. /path/to/image.ext
                    Note: You can just drag and drop target file into terminal. :)
                    >> """))).strip()
                image = dragger.terminal(image)
                
                if self.is_a_image(image):
                    self.apic_images[ops[op]] = {'file':image, 'apictype':tune_image_type['id']}
                else:
                    raw_input("[ww] There is no image %s." %image)
                break
            except (ValueError, IndexError):
                raw_input("__INVALID_OPTION__ [%s]... Press a KEY to continue. " %(op))
    
    
    def edit_non_expected_files(self):
        """
        -- Consider to include/exclude non expected files. --   
        """
        if len(self.non_expected_files) == 0: 
            raw_input("There aren't non expected files. Press a key to continue.")
        case = {'y': True, 'n': False}
        for i, non_expected_file in enumerate(self.non_expected_files):
            while 1:
                print "Include %s file?" %(non_expected_file['filename'])
                v = raw_input("[Y]es? or [N]o? >>> ").lower()
                if v == self.skip_key: return 
                try:
                    self.non_expected_files[i]['data']['consider'] = case[v]
                    break
                except KeyError:
                    raw_input("__INVALID_OPTION__ [%s]... Press a KEY to continue. " %(v))
    

class Process:
    
    def process_tunes(self, tunes, trackn_max_digits, target_path, apic_images):
        for tune in tunes:
            target_filename = self.get_tunned_filename(tune['filename']['source'], tune['id3'], trackn_max_digits)
            tune['filename']['target'] = os.path.abspath(os.path.join(target_path, target_filename))
            try:
                self.copy_file(tune['filename']['source'], tune['filename']['target'])
                self.save_id3_data(tune['filename']['target'], tune['id3'], apic_images)
                print "[ii] tune %s was processed correctly." %(unicoder(os.path.basename(tune['filename']['source'])))
            except PyD3Error as e:
                print "[ee] %s" %(unicoder(e.msg))
    
    def process_apic_images(self, apic_images, target_path):
        for key in apic_images.keys():
            if apic_images[key]:
                image_file = apic_images[key]['file']
                try:
                    (filename, extension)  = self.image_types[key]['filename'][0], os.path.splitext(image_file)[1]
                    self.copy_file(image_file, os.path.join(target_path, filename+extension))
                    print "[ii] apic image %s was copied correctly." %(unicoder(os.path.basename(filename+extension)))
                except PyD3Error as e: 
                    print "[ee] %s" %(unicoder(e.msg))
    
    def process_non_expected_files(self, non_expected_files, target_path):
        for non_expected_file in non_expected_files:
            if non_expected_file['data']['consider']:
                try: 
                    self.copy_file(non_expected_file['data']['path'], os.path.join(target_path, non_expected_file['filename']))
                    print "[ii] filename %s was copied correctly." %(unicoder(os.path.basename(non_expected_file['filename'])))
                except PyD3Error as e: 
                    print "[ee] %s" %(unicoder(e.msg))
    

class Typewriter:
    
    def clean_screen(self):
        """Clean screen terminal --whatever OS is."""
        screaner.screaner()
    
    def get_text_line_block(self, title=""):
        line_char, total_chars = "-", 120
        if title:
            title = "=%s=" %(title)
            return title
        return line_char*total_chars
        
    def get_text_source_path_is(self):
        return "=SOURCE PATH= %s" %(self.paths['source_path'])
    
    def get_text_n_tunes(self, tune_files):
        return "%i tunes" %(len(tune_files))
    
    def get_text_tunes_audio(self, audio):
        t2s = lambda t: ', '.join(v for v in t if v)
        return "Bit Rate: %s -- Sample Rate: %s -- Format: %s -- Channels: %s" %(
            t2s(audio.get('bitrate')), t2s(audio.get('samplerate')), t2s(audio.get('format')), t2s(audio.get('mode'))
        )
    
    def get_text_tunes_id3(self, id3):
        t2s = lambda t: ', '.join(unicode(v) for v in t if v)
        l = []
        l.append("Track#: %s" %(t2s(id3.get('trackn', ('',)))))
        l.append("Album : %s" %(t2s(id3.get('album',  ('',)))))
        l.append("Artist: %s" %(t2s(id3.get('artist', ('',)))))
        l.append("Title : %s" %(t2s(id3.get('title',  ('',)))))
        l.append("Genre : %s" %(t2s(id3.get('genre',  ('',)))))
        l.append("Year  : %s" %(t2s(id3.get('year',   ('',)))))
        return os.linesep.join(l)
    
    def get_text_attached_images(self, images):
        l = []
        for key in images.keys():
            image = self.apic_images.get(key, None)
            if image:
                text = "%s %s (%s) [%s]" %(
                    self.get_file_name(image['file']), 
                    self.get_image_text_dimensions(image['file']), 
                    self.get_file_mimetype(image['file']), 
                    self.get_file_size(image['file'])
                )
            else:
                text = "[There is no image attached!]"
            l.append("%s: %s" %(self.image_types[key]['name'], text))
        return "%s" %(' -- '.join(l))
    
    def get_text_current_dir(self, folder):
        return "Current Dir: ..%s%s%s" %(os.sep, os.path.basename(folder), os.sep)
    
    def get_text_target_dir(self, folder):
        return "Target  Dir: ..%s%s%s" %(os.sep, os.path.basename(folder), os.sep)
    
    def get_text_non_expected_files(self, files):
        if len(files) is 0: return
        tf  = lambda v: 'Included' if v is True else 'Excluded'
        fnc = lambda f: '%s [%s]' %(unicoder(f['filename']), tf(f['data']['consider']))
        return "%s" %(', '.join(fnc(f) for f in files))
    
    def print_dir_info(self, folder_summary):
        print unicoder("%s (%s) [%s]" %(
            unicoder(self.get_text_source_path_is()), 
            self.get_text_n_tunes(folder_summary['files']['tune']),
            self.get_dir_size(self.paths['source_path']))
        )
        print unicoder(self.get_text_line_block())
        print unicoder(self.get_text_line_block("AUDIO DATA"))
        print unicoder(self.get_text_tunes_audio(folder_summary['audio']))
        print unicoder(self.get_text_line_block())
        print unicoder(self.get_text_line_block("ID3 DATA"))
        print unicoder(self.get_text_tunes_id3(folder_summary['id3']))
        print unicoder(self.get_text_line_block())
        if folder_summary['id3']['warnings']:
            print unicoder(self.get_text_line_block("ID3 DATA HAS WARNINGS!!!"))
            print unicoder(self.get_text_line_block())
        print unicoder(self.get_text_line_block("ATTACHED IMAGES (ID3)"))
        print unicoder(self.get_text_attached_images(folder_summary['image']))
        print unicoder(self.get_text_line_block())
        print unicoder(self.get_text_line_block("PATHS"))
        print unicoder(self.get_text_current_dir(folder_summary['path']['source_dir']))
        print unicoder(self.get_text_target_dir(folder_summary['path']['target_dir']))
        print unicoder(self.get_text_line_block())
        if len(folder_summary['non_expected_files'])>0:
            print unicoder(self.get_text_line_block("NON EXPECTED FILES"))
            print unicoder(self.get_text_non_expected_files(folder_summary['non_expected_files']))
        print unicoder(self.get_text_line_block())
    
    def get_text_tune_filename(self, file):
        return "Filename: %s" %(os.path.basename(file))
    
    def get_text_tune_id3(self, id3):
        l = []
        l.append("Track#: %s" %(unicoder(id3.get('trackn', ''))))
        l.append("Album : %s" %(unicoder(id3.get('album',  ''))))
        l.append("Artist: %s" %(unicoder(id3.get('artist', ''))))
        l.append("Title : %s" %(unicoder(id3.get('title',  ''))))
        l.append("Genre : %s" %(unicoder(id3.get('genre',  ''))))
        l.append("Year  : %s" %(unicoder(id3.get('year',   ''))))
        return os.linesep.join(l)
    
    def get_text_short_tune_summary(self, tune):
        return "[FILENAME: %s] | [TRACKN#: %s] | [ARTIST: %s] | [ALBUM: %s] | [TITLE: %s]" %(
            os.path.basename(tune['filename'].get('source', '')), 
            tune['id3'].get('trackn', ''), 
            tune['id3'].get('artist', ''), 
            tune['id3'].get('album', ''), 
            tune['id3'].get('title', ''), 
        )
    
    def print_tune_info(self, tune_data, image=None):
        print unicoder(self.get_text_tune_filename(tune_data['filename']['source']))
        print unicoder(self.get_text_tune_id3(tune_data['id3']))
        print unicoder(self.get_text_attached_images(image))
        
    def print_tune_short_summary(self, tune):
        print self.get_text_short_tune_summary(tune)
    
    def get_text_going_to_copied_in(self, path):
        return "Files are going to be copied in %s path." %(unicoder(path))
    
    def print_going_to_be_copied_in(self, path):
        print self.get_text_going_to_copied_in(path)
    
    def print_source_path_was(self):
        raw_input("%s path was processed. Please, press a key to continue." %(unicoder(self.paths['source_path'])))
    
    def print_skip_text(self):
        print "NOTE: Enter %s anytime to skip from the menu presented." %(self.skip_key)
        print self.get_text_line_block()
    

class Error(Exception):
    """Base class for exceptions in this module."""
    pass
    

class PyD3Error(Error):
    """
    Exception raised for errors.
    
    Arguments:
    :param msg: string -- explanation of the error
    """
    
    def __init__(self, msg):
        self.msg  = msg
    

class PyD3(Id3, Audio, Image, Filename, Directory, Prompter, Edit, Process, Typewriter, Utils):
    
    paths       = []
    tunes       = []
    apic_images = []
    
    custom_target_dir   = False
    
    non_expected_files  = []
    dismissing_files    = ['.DS_Store', 'thumbs.db']
    
    flattened_data  = {'audio': {}, 'id3': {}}
    
    is_a_va_album   = False
    
    process_folder  = False
    skip_folder     = False
    
    skip_key        = '__skip__'
    
    def __init__(self, source_path):
        self.paths = {
            'source_path': source_path,
            'source_dir' : os.path.basename(source_path), 
            'target_path': None,
            'target_dir' : None
        }
    
    def process_folder_data(self):
        """Data is ready to be processed. Set variables for going ahead."""
        self.process_folder = True
        self.skip_folder    = False
    
    def skip_folder_data(self):
        """Data is NOT ready to be processed. Set variables for NOT going ahead."""
        self.process_folder = False
        self.skip_folder    = True
    
    def exit(self):
        """Ends PyD3 program."""
        sys.exit("sys.exit('PyD3 exit -- it was your choice.')")
    
