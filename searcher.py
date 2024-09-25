import sys
import os


def fslookup(
    fname=None,
    sdate=None,
    edate=None,
    minSize=None,
    maxSize=None,
    dtype=None,
    perms=None,
    path=None,
):
    print("Performed File Lookup with the followwing params:")
    print(locals())


# commands

cmds = sys.argv
# cmds = ["homework", "-s", ""]
cmds = cmds[1:] + [""]
# quit()
query = {}
flag = ""
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
                # YYYY-MM-DD-HH:MM:SS
                query["sdate"] = None
                query["edate"] = None
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
                        f"Permissions should be a 3-digit integer. See help for more information. ValueError:",
                        e,
                    )
                    quit()
                query["perms"] = word
            case "-d" | "--directorypath":
                query["path"] = word
            case "-h" | "--help":
                print("Help text here.")
                quit()
            case _:
                print(
                    f"Unknown flag encountered: {flag}. See help page (-h or --help) for more information."
                )
        flag = ""
    elif word == "":
        break
    if word[0] == "-":
        flag = word

fslookup(**query)
