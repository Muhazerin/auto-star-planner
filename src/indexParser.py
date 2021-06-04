# Example of what the expected result looks like:
# source.indexes = [
#   {
#       'index': '10345',
#       'info': [
#           {
#               'TYPE': 'LEC/STUDIO',
#               'GROUP': 'CS3',
#               'DAY': 'MON',
#               'TIME': '1330-1420',
#               'VENUE': 'ONLINE',
#               'REMARK': ''
#           },
#           {
#               'TYPE': 'LEC/STUDIO',
#               'GROUP': 'CS3',
#               'DAY': 'FRI',
#               'TIME': '1530-1620',
#               'VENUE': 'ONLINE',
#               'REMARK': ''
#           },
#           {
#               'TYPE': 'TUT'
#               'GROUP': 'SSP1',
#               'DAY': 'WED',
#               'TIME': '1430-1520',
#               'VENUE': 'TR+37',
#               'REMARK': 'Teaching Wk2-13'
#           },
#           {
#               'TYPE': 'LAB'
#               'GROUP': 'SSP1',
#               'DAY': 'TUE',
#               'TIME': '1230-1420',
#               'VENUE': 'HWLAB1',
#               'REMARK': 'Teaching Wk1,3,5,7,9,11,13'
#           }
#       ]
#   }
# ]


def parse_new(tds, index, index_list):
    # Add the index and info into the dict
    index_list[index].update({'index': tds[0].string})
    index_list[index].update({'info': []})
    # Pass to parse function to add the other row info
    parse(tds, index, index_list)


def parse(tds, index, index_list):
    # Initialize the other row into data variable
    data = {
        'TYPE': tds[1].string,
        'GROUP': tds[2].string,
        'DAY': tds[3].string,
        'TIME': tds[4].string,
        'VENUE': tds[5].string,
        'REMARK': tds[6].string
    }
    # Append data to info
    index_list[index]['info'].append(data)
