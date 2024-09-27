import datetime as dt

#Dummy Library
data_lib = {}

data_lib['fname'] = ["Assignment1", "Assignment1" "ENGR_Thesis", "Lab1"]
data_lib ['date'] = ["2023-02-21 19:00:12", "2024-08-31 00:10:03", "2022-04-29 00:15:21", "2021-09-10 18:12:14"]
data_lib ['dtype'] = ["ipynb", "csv", "txt", "pdf"]
data_lib ['size'] = [778123, 1203459, 9992812, 83847192]
data_lib ['perm'] = [745, 777, 717, 744]
data_lib ['path'] = ["/home/user/Documents/Assignment1.ipynb", "/home/user/Desktop/Assignment1.csv", "/home/user/Desktop/Essays/ENGR_Thesis.txt", "home/user2/Programs/Lab1.pdf"]

print(data_lib)

#fslookup main function
def fslookup(file_lib, fname=None, sdate=None, edate=None, maxSize=None, minSize=None, dtype=None, perm=None, path=None):

    #Dictionary to be appended, returned and printed out
    search_lib = {
        'fname': [],
        'date': [],
        'size': [],
        'perm': [],
        'path': []
        }

    # Date functions
    def string2unix(date_string, format_string):

        date_time = dt.datetime.strptime(date_string, format_string)

        return int(date_time.timestamp())

    dt_format = "%Y-%m-%d %H:%M:%S"
    sdate2unix = string2unix(sdate, dt_format) if sdate else None
    edate2unix = string2unix(edate, dt_format) if edate else None

    # fname search
    for i in range(len(file_lib['fname'])):
        if fname and fname.lower() not in file_lib['fname'][i].lower():
        #if fname and file_lib['fname'][i] != fname:
            continue

    # Date Search
        accessed_date = file_lib['date'][i]
        acc_dte2unix = string2unix(accessed_date, dt_format)

        if sdate2unix or edate2unix:
            if (sdate2unix and acc_dte2unix < sdate2unix) or (edate2unix and acc_dte2unix > edate2unix):
                continue

    # dtype search
        if dtype and file_lib['dtype'][i]!= dtype:
            continue

    # File Size Search
        size = file_lib['size'][i]
        if (minSize and size < minSize) or (maxSize and size > maxSize):
            continue

    # Perm Search
        if perm and file_lib['perm'][i] != perm:
            continue

    # Path search
        if path and file_lib['path'][i] != path:
            continue

    # Collect file info and compile into search-lib dictionary
        search_lib['fname'].append(file_lib['fname'][i])
        search_lib['date'].append(file_lib['date'][i])
        search_lib['size'].append(file_lib['size'][i])
        search_lib['perm'].append(file_lib['perm'][i])
        search_lib['path'].append(file_lib['path'][i])

    return print(search_lib)

#Test case
result = fslookup(data_lib, "Assignment1", "2023-02-21 00:00:00", "2023-02-22 00:00:00", 778300, 778100, "ipynb", 745, "/home/user/Documents/Assignment1.ipynb")
