import os
import sys

from textwrap import dedent

from pyd3.pyd3 import PyD3
from pyd3.pyd3 import PyD3Error
from pyd3.unicoder import unicoder


try:
    main_source_path, main_target_path = unicoder(sys.argv[1]), unicoder(sys.argv[2])
    if not os.path.exists(main_source_path) or not os.path.exists(main_target_path): raise OSError()
except (IndexError, OSError):
    sys.exit(dedent("""\
        __ARGUMENTS_REQUIRED__
        1. __MAIN_SOURCE_PATH__ Param. Path where the music is stored. e.g.: /music/library/
        2. __MAIN_TARGET_PATH__ Param. Path where the processed music is going to be stored. e.g.: /music/library/pyd3/
    """))

for (path, dirs, files) in os.walk(main_source_path):
    
    if files is None: continue
    
    pyd3 = PyD3(path)
    
    files = [os.path.join(path, f) for f in files]
    mp3_files = [f for f in files if pyd3.is_a_mp3_file(f)]
    pyd3.tunes = [pyd3.get_tune_data(mp3_file) for mp3_file in mp3_files]
    
    if len(pyd3.tunes) is 0: continue
    
    image_files = [f for f in files if f not in mp3_files and pyd3.is_a_image(f)]
    pyd3.apic_images = pyd3.get_apic_images(image_files)
    
    pyd3.non_expected_files = pyd3.get_non_expected_files(files)
    
    while pyd3.process_folder is False and pyd3.skip_folder is False:
        
        pyd3.flattened_data['audio'] = pyd3.get_audio_flattened(pyd3.tunes)
        pyd3.flattened_data['id3'] = pyd3.get_id3_flattened(pyd3.tunes)
        
        pyd3.is_a_va_album = True if len(pyd3.flattened_data['id3'].get('artist', ()))>1 else False
        
        if pyd3.custom_target_dir is False:
            pyd3.paths['target_dir'] = pyd3.get_target_dir(pyd3.paths['source_dir'], pyd3.flattened_data['id3'], pyd3.is_a_va_album)
        
        folder_summary = pyd3.get_folder_summary(mp3_files)
        
        pyd3.clean_screen()
        pyd3.print_dir_info(folder_summary)
        pyd3.print_skip_text()
        
        option = raw_input(dedent("""\
            [1] Above info is OK. Go ahead and PyD3 it!
            [2] Edit target folder directory name.
            [-] Edit ID3 tune(s) tags data for:
                [3] Select id3 tag(s) and values to update all tunes by one shot.
                [4] Select id3 tag(s), and then tune by tune add value(s) for the selected id3 tag(s).
                [5] List tune filenames, view and edit a specific tune.
            [6] Add apic images (they will be attached to every tune).
            [7] Consider non expected files to be copied on target directory (Exclude/Include).
            [8] List empty id3 tags for each file.
            [9] Skip album folder.
            [0] Exit.
            >> """))
        
        case = {
            '1': pyd3.process_folder_data,
            '2': pyd3.edit_target_dir,
            '3': pyd3.edit_all_tunes,
            '4': pyd3.edit_tune_by_tune,
            '5': pyd3.edit_a_tune_from_a_list_of_tunes,
            '6': pyd3.edit_apic_images,
            '7': pyd3.edit_non_expected_files,
            '8': pyd3.list_empty_tags,
            '9': pyd3.skip_folder_data,
            '0': pyd3.exit
        }
        
        try:
            case[option]()
        except KeyError:
            raw_input("__INVALID_OPTION__ [%s]... Press a KEY to continue. " %(option))
        
        if pyd3.process_folder is True and pyd3.skip_folder is False: break
    if pyd3.process_folder is False and pyd3.skip_folder is True: continue
    
    trackn_max_digits = pyd3.get_trackn_max_digits(len(mp3_files))
    pyd3.tunes = pyd3.set_value_attr_to_band_tag(pyd3.tunes, pyd3.get_band_tag_value_attr(pyd3.is_a_va_album))
    
    while 1:
        pyd3.paths['target_path'] = pyd3.get_target_tune_path(main_target_path, pyd3.paths['target_dir'])
        if pyd3.create_dir(pyd3.paths['target_path']): break
        pyd3.paths['target_dir'] = pyd3.get_alternative_custom_target_dir(pyd3.paths['target_dir'], main_target_path)
    
    pyd3.print_going_to_be_copied_in(pyd3.paths['target_path'])
    try:
        pyd3.process_tunes(pyd3.tunes, trackn_max_digits, pyd3.paths['target_path'], pyd3.apic_images)
        pyd3.process_apic_images(pyd3.apic_images, pyd3.paths['target_path'])
        pyd3.process_non_expected_files(pyd3.non_expected_files, pyd3.paths['target_path'])
    except PyD3Error as e: 
        print "[ee] %s" %(unicoder(e.msg))
    pyd3.print_source_path_was()

print "PyD3 ended to process your music library. %s" %(unicode(main_source_path))
