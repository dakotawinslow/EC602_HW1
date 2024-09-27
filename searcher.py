#!usr/bin/python3
import sys
import os
import datetime as dt

import database_searcher as ds

HELPTEXT = """
Welcome to Searcher! 
For easiest use, type 'searcher [query]', where query is any combination of alphanumeric characters
and wildcards.

Command Structure:
{searcher} [query] [flag] [query] [flag] [query] ...

Available Flags:

-t | --text: "-t [searchtext]"
    Text to search for. Can be exact string ("cat.jpg") or wildcard ("*.xlsx"; "dog.*"; "*2024*").
    If searcher is called without flags, the input will be interpreted as search text.

-d | --date: "-d [startdate]~[enddate]
    Specify a date range. Dates should be in YYYY-MM-DD-HH:MM:SS format, and should always include the '~' 
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
    Specify a filepath to only searcnh for files in that directory. Use a wildcard to find files in subdirectories 
    ("/path/to/*" can find a file in "/path/to/my/folder/").

-h | --help:
    Display this message.



"""


# Date to unix function
def string2unix(date_string, format_string):
    date_time = dt.datetime.strptime(date_string, format_string)
    return int(date_time.timestamp())


# Nake dictionary to readable table function
def dict_2_table(dict_lib):
    # Get dictionary keys as headers
    headers = dict_lib.keys()

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
        if fname and file_lib["fname"][i] != fname:
            continue

        # Date Search
        accessed_date = file_lib["date"][i]
        # acc_dte2unix = string2unix(accessed_date, dt_format)

        if sdate or edate:
            if (sdate and accessed_date < sdate) or (edate and accessed_date > edate):
                continue

        # dtype search
        if dtype and file_lib["dtype"][i] != dtype:
            continue

        # File Size Search
        size = file_lib["size"][i]
        if (minSize and size < minSize) or (maxSize and size > maxSize):
            continue

        # Perm Search
        if perm and file_lib["perm"][i] != perm:
            continue

        # Path search
        if path and file_lib["path"][i] != path:
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
library = ds.searcher_obj()
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
                sdate = word.split()[0]
                edate = word.split()[1]
                dt_format = "%Y-%m-%d-%H:%M:%S"
                sdate2unix = string2unix(sdate, dt_format)
                edate2unix = string2unix(edate, dt_format)
                query["sdate"] = sdate2unix
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
                query["perms"] = word
            case "-l" | "--location":
                query["path"] = word
            case "-h" | "--help":
                print(HELPTEXT)
                quit()
            case _:
                print(
                    f"Unknown flag encountered: {flag}. See help page (-h or --help) for more information."
                )
                quit()
        flag = ""
    elif word == "":
        break
    if word[0] == "-":
        flag = word

results = fslookup(**query)
dict_2_table(results)
# print(results)  # fix this Josh
