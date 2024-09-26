#!/usr/bin/python3

import os
import datetime
import stat
import subprocess

cwd_path = os.getcwd()
dir_tree = os.walk(cwd_path)

def flattened_paths():

    flattened_dir = []

    for dirpath, subdir, files in dir_tree:
        for file in files:
            full_path = os.path.join(dirpath, file)  
            flattened_dir.append(full_path)

    return flattened_dir

#flattened_dir = flattened_paths()
#print(flattened_dir)

def filename(flattened_dir):
    filenames = []
    for path in flattened_dir:
        filename = os.path.split(path)[1]
        filenames.append(filename)
    return filenames

#filenames = filename()
#print(filenames)

def dates(flattened_dir):
    dates = []
    for path in flattened_dir:
        time_s = os.stat(path).st_mtime
        #date_obj = datetime.datetime.fromtimestamp(time_s)
        #month = date_obj.month
        #day = date_obj.day
        #year = date_obj.year
        #hour = date_obj.hour
        #minute = date_obj.minute
        #date = f"{month} {day} {year} {hour}:{minute}"
        date = time_s
        dates.append(date)
    return dates

#date = dates()
#print(dates)

def file_size(flattened_dir):
    file_sizes = []
    for path in flattened_dir:
        file_size = os.stat(path).st_size
        file_sizes.append(file_size)
    return file_sizes

#file_sizes = file_size()
#print(file_sizes)

def permissions(flattened_dir):
    access = []
    for path in flattened_dir:
        permissions = os.stat(path).st_mode

        if (bool(permissions & stat.S_IRUSR)): 
            usr_r  = 'r'
        else: usr_r = '-'
        if (bool(permissions & stat.S_IWUSR)):
            usr_w = 'w'
        else: usr_w = '-'
        if(bool(permissions & stat.S_IXUSR)):
            usr_x = 'x'
        else: usr_x = '-'

        if(bool(permissions & stat.S_IRGRP)):
            grp_r = 'r'
        else: grp_r = '-'
        if(bool(permissions & stat.S_IWGRP)):
            grp_w = 'w'
        else: grp_w = '-'
        if(bool(permissions & stat.S_IXGRP)):
            grp_x = 'x'
        else: grp_x = '-'

        if(bool(permissions & stat.S_IROTH)):
            oth_r = 'r'
        else: oth_r = '-'
        if(bool(permissions & stat.S_IWOTH)):
            oth_w = 'w'
        else: oth_w = '-'
        if(bool(permissions & stat.S_IXOTH)):
            oth_x = 'x'
        else: oth_x = '-'
        permission = f"-{usr_r}{usr_w}{usr_x}{grp_r}{grp_w}{grp_x}{oth_r}{oth_w}{oth_x}"
        access.append(permission)
    return access

#permission = permissions()
#print(permission)

def extensions(flattened_dir):
    extensions = []
    for path in flattened_dir:
        #current_dir = os.path.split(path)[0]
        #dtype = os.path.split(path)[1]
        #subprocess.run(['cd ', current_dir])
        #extension = os.path.splitext(path)[1]
        #if(extension == ''): extension = None
        extension = subprocess.run(['file', path], capture_output = True, text = True).stdout
        extension = extension.split(':')[1].strip()
        extensions.append(extension)
    return extensions

#extension = extensions()
#print(extension)

#searcher_obj = {"fname":filenames,"date":date,"dtype":extension,"size":file_sizes,"perm":permission,"path":flattened_dir}
#print(searcher_obj)


def searcher_obj():
    flattened_dir = flattened_paths()
    filenames = filename(flattened_dir)
    date = dates(flattened_dir)
    file_sizes = file_size(flattened_dir)
    permission = permissions(flattened_dir)
    extension = extensions(flattened_dir)
    searcher_obj = {"fname":filenames,"date":date,"dtype":extension,"size":file_sizes,"perm":permission,"path":flattened_dir}
    return searcher_obj

searcher_dict = searcher_obj()
print(searcher_dict)