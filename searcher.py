#!/usr/bin/env python3
# Copyright 2024 Dakota Winslow winslowd@bu.edu
# Copyright 2024 Devin Kot-Thompson devinkt@bu.edu
# Copyright 2024 Chih Han "Josh" Yeh jy0825@bu.edu

import sys
import os
import datetime as dt
import fnmatch

import stat
import subprocess


# Start Stuff from Database Searcher
cwd_path = os.getcwd()
dir_tree = os.walk(cwd_path)


def flattened_paths():

    flattened_dir = []

    for dirpath, subdir, files in dir_tree:
        for file in files:
            full_path = os.path.join(dirpath, file)
            flattened_dir.append(full_path)

    return flattened_dir


# flattened_dir = flattened_paths()
# print(flattened_dir)


def filename(flattened_dir):
    filenames = []
    for path in flattened_dir:
        filename = os.path.split(path)[1]
        filenames.append(filename)
    return filenames


# filenames = filename()
# print(filenames)


def dates(flattened_dir):
    dates = []
    for path in flattened_dir:
        time_s = os.stat(path).st_mtime
        # date_obj = datetime.datetime.fromtimestamp(time_s)
        # month = date_obj.month
        # day = date_obj.day
        # year = date_obj.year
        # hour = date_obj.hour
        # minute = date_obj.minute
        # date = f"{month} {day} {year} {hour}:{minute}"
        date = time_s
        dates.append(date)
    return dates


# date = dates()
# print(dates)


def file_size(flattened_dir):
    file_sizes = []
    for path in flattened_dir:
        file_size = os.stat(path).st_size
        file_sizes.append(file_size)
    return file_sizes


# file_sizes = file_size()
# print(file_sizes)


def permissions(flattened_dir):
    access = []
    for path in flattened_dir:
        permissions = os.stat(path).st_mode

        if bool(permissions & stat.S_IRUSR):
            usr_r = "r"
        else:
            usr_r = "-"
        if bool(permissions & stat.S_IWUSR):
            usr_w = "w"
        else:
            usr_w = "-"
        if bool(permissions & stat.S_IXUSR):
            usr_x = "x"
        else:
            usr_x = "-"

        if bool(permissions & stat.S_IRGRP):
            grp_r = "r"
        else:
            grp_r = "-"
        if bool(permissions & stat.S_IWGRP):
            grp_w = "w"
        else:
            grp_w = "-"
        if bool(permissions & stat.S_IXGRP):
            grp_x = "x"
        else:
            grp_x = "-"

        if bool(permissions & stat.S_IROTH):
            oth_r = "r"
        else:
            oth_r = "-"
        if bool(permissions & stat.S_IWOTH):
            oth_w = "w"
        else:
            oth_w = "-"
        if bool(permissions & stat.S_IXOTH):
            oth_x = "x"
        else:
            oth_x = "-"
        permission = f"-{usr_r}{usr_w}{usr_x}{grp_r}{grp_w}{grp_x}{oth_r}{oth_w}{oth_x}"
        access.append(permission)
    return access


def extensions(flattened_dir):
    extensions = []
    for path in flattened_dir:
        # current_dir = os.path.split(path)[0]
        # dtype = os.path.split(path)[1]
        # subprocess.run(['cd ', current_dir])
        # extension = os.path.splitext(path)[1]
        # if(extension == ''): extension = None
        extension = subprocess.run(
            ["file", path], capture_output=True, text=True
        ).stdout
        extension = extension.split(":")[1].strip()
        extensions.append(extension)
    return extensions


def searcher_obj():
    flattened_dir = flattened_paths()
    filenames = filename(flattened_dir)
    date = dates(flattened_dir)
    file_sizes = file_size(flattened_dir)
    permission = permissions(flattened_dir)
    extension = extensions(flattened_dir)
    searcher_obj = {
        "fname": filenames,
        "date": date,
        "dtype": extension,
        "size": file_sizes,
        "perm": permission,
        "path": flattened_dir,
    }
    return searcher_obj


# END stuff from database searcher
# import database_searcher as ds

HELPTEXT = """
Welcome to Searcher! 
For easiest use, type 'searcher [query]', where query is any combination of alphanumeric characters
and wildcards. **NOTE** If you do use wildcards, be sure to put the search query in quotes so it parses correctly.

eg: searcher "*.py" 
eg: searcher gitignore -l "/Home/user/Documents/*"

Command Structure:
{searcher} [query] [flag] [query] [flag] [query] ...

Available Flags:

-t | --text: "-t [searchtext]"
    Text to search for. Can be exact string ("cat.jpg") or wildcard ("*.xlsx"; "dog.*"; "*2024*").
    If searcher is called without flags, the input will be interpreted as search text.

-d | --date: "-d [startdate]~[enddate]
    Specify a date range. Dates should be in %Y-%m-%d-%H:%M:%S format, and should always include the '~' 
    character. Leave off the start or end for an open-ended search.

-y | --datatype: "-y [datatype]
    Specify a data type string to search for files containing certain types of data. This uses the linux "file"
    tool, which can be somewhat verbose in its responses, so it's probably a good idea to wrap your query in **.

-s | --size: "-s [minsize]:[maxsize]
    Specify a size range to exclude results based on size. Sizes must be specified in bytes and always include 
    a ":". Leave off the min or max for open-ended searching.

-p | --permissions: "-p [permission#]
    Specify a 3-digit permissions flag to return only files with that exact flag.

-l | --location: "-l [filepath]
    Specify a filepath to only search for files in that directory. Use a wildcard to find files in subdirectories 
    ("/path/to/*" can find a file in "/path/to/my/folder/").

-v | --verbose
    Add this tag for verbose output, including all the information that can be searched on.    

-h | --help:
    Display this message.
"""
VERBOSE = False


# Date to unix function
def string2unix(date_string, format_string):
    try:
        date_time = dt.datetime.strptime(date_string, format_string)
    except ValueError as e:
        print(f"Improperly formatted date. Error: {e}")
        quit()
    return int(date_time.timestamp())


# Convert 3 digit octal numbers into permissions strings
def octal_to_string(octal):
    permission = ["---", "--x", "-w-", "-wx", "r--", "r-x", "rw-", "rwx"]
    result = ""
    # Iterate over each of the digits in octal
    for digit in [int(n) for n in str(octal)]:
        result += permission[digit]
    return result


# Nake dictionary to readable table function
def dict_2_table(dict_lib):
    # Get dictionary keys as headers

    headers = dict_lib.keys()

    # Message to display when the search returns no results
    if len(dict_lib[list(headers)[0]]) == 0:
        print("No Results Found.")
        quit()

    # Find the maximum width for each column (header or content)
    col_widths = {
        header: max(len(str(header)), max(len(str(item)) for item in dict_lib[header]))
        for header in headers
    }

    # Format string for each row adjusting the widths
    row_format = " | ".join(
        ["{{:<{}}}".format(col_widths[header]) for header in headers]
    )

    # print header row
    print(row_format.format(*headers))
    print("-" * (sum(col_widths.values()) + 3 * (len(headers) - 1)))  # Separator line

    # Print the data rows
    for row in zip(*dict_lib.values()):
        print(row_format.format(*row))


def fslookup(
    file_lib,
    fname=None,
    sdate=None,
    edate=None,
    maxSize=None,
    minSize=None,
    dtype=None,
    perm=None,
    path=None,
):

    # Dictionary to be appended, returned and printed out
    search_lib = {"fname": [], "date": [], "size": [], "perm": [], "path": []}
    # moved date functions to parser section -DW

    # fname search
    for i in range(len(file_lib["fname"])):
        # Looks for all matching keywords, case-insensitive
        if fname and not fnmatch.fnmatch(
            file_lib["fname"][i].lower(), fname.lower()
        ):  # using fnmatch for wildcards
            # if fname and file_lib["fname"][i] != fname:
            continue

        # Date Search
        accessed_date = file_lib["date"][i]

        # accessed_date = string2unix(file_lib["date"][i])
        # sdate2unix = string2unix(sdate) if sdate else None
        # edate2unix = string2unix(edate) if edate else None

        # acc_dte2unix = string2unix(accessed_date, dt_format)

        if sdate or edate:
            # if (sdate2unix and accessed_date < sdate2unix) or (
            #     edate2unix and accessed_date > edate2unix
            # ):
            if (sdate and accessed_date < sdate) or (edate and accessed_date > edate):

                continue

        # dtype search
        if dtype and not fnmatch.fnmatch(
            file_lib["dtype"][i], dtype
        ):  # using fnmatch for wildcards
            continue

        # File Size Search
        size = file_lib["size"][i]
        if (minSize and size < minSize) or (maxSize and size > maxSize):
            continue

        # Perm Search
        if perm and file_lib["perm"][i] != perm:
            continue

        # Path search
        # if path and file_lib["path"][i] != path:  # Modified to use fnmatch, which parses wildcards correctly
        #     continue
        if path and not fnmatch.fnmatch(file_lib["path"][i], path):
            continue
        # Collect file info and compile into search-lib dictionary
        search_lib["fname"].append(file_lib["fname"][i])
        search_lib["date"].append(file_lib["date"][i])
        search_lib["size"].append(file_lib["size"][i])
        search_lib["perm"].append(file_lib["perm"][i])
        search_lib["path"].append(file_lib["path"][i])

    return search_lib  # changed back to returning just the list of dicts DW


# parser

cmds = sys.argv
cmds = cmds[1:] + [""]
# calling directory object from flattened directory
library = searcher_obj()
query = {"file_lib": library}
# query = {}
flag = ""
if cmds[0] == "":
    print("Please specify a search term, or use --help for more information.")
    quit()
if cmds[0][0] != "-":
    query["fname"] = cmds[0]
    cmds = cmds[1:]
for word in cmds:
    # print(f"Flag: {flag}, word{word}")
    if flag != "":
        match flag:
            case "-t" | "--text":
                query["fname"] = word
            case "-d" | "--date":
                # For now, users must enter date/time requests in perfect
                # YYYY-MM-DD-HH:MM:SS~YYYY-MM-DD-HH:MM:SS
                if word.count("~") != 1:
                    print(
                        "Date ranges must be entered as YYYY-MM-DD-HH:MM:SS~YYYY-MM-DD-HH:MM:SS. First or second date may be omitted for open ended search."
                    )
                    quit()
                sdate = word.split("~")[0]
                edate = word.split("~")[1]
                dt_format = "%Y-%m-%d-%H:%M:%S"
                if sdate:
                    sdate2unix = string2unix(sdate, dt_format)
                    query["sdate"] = sdate2unix
                if edate:
                    edate2unix = string2unix(edate, dt_format)
                    query["edate"] = edate2unix
            case "-s" | "--size":
                # size should be in slice notation
                # use bytes, maybe add kb, mb, gb in future
                if word.count(":") != 1:
                    print("Size values must be in slice noation using exactly one ':'")
                    quit()
                else:
                    splits = word.split(":")
                    try:
                        minSize = int(splits[0])
                        maxSize = int(splits[1])
                    except ValueError as e:
                        print(
                            "Error: File sizes must be an interger number of bytes. ValueError:",
                            e,
                        )
                        quit()
                    query["minSize"] = minSize
                    query["maxSize"] = maxSize
            case "-y" | "--datatype":
                # should be a string
                query["dtype"] = word
            case "-p" | "--permissions":
                try:
                    if len(word) != 3:
                        raise ValueError
                    perms = int(word)
                except ValueError as e:
                    print(
                        f"Permissions should be a 3-digit integer. See --help for more information. ValueError:",
                        e,
                    )
                    quit()

                permstr = octal_to_string(word)
                query["perm"] = "-" + permstr
            case "-l" | "--location":
                query["path"] = word
            case "-h" | "--help":
                print(HELPTEXT)
                quit()
            case "-v" | "--verbose":
                VERBOSE = True
            case _:
                print(
                    f"Unknown flag encountered: {flag}. See help page (-h or --help) for more information."
                )
                quit()
        flag = ""
    elif word == "":
        break
    if word and word[0] == "-":
        flag = word

results = fslookup(**query)
query.pop("file_lib")
dates = []
for stamp in results["date"]:
    dates.append(dt.datetime.fromtimestamp(stamp).strftime("%Y-%m-%d"))
results["date"] = dates
paths = []
for path in results["path"]:
    paths.append(os.path.split(path)[0])
results["path"] = paths
if VERBOSE:
    dict_2_table(results)
else:
    for item in results["fname"]:
        print(item)
