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
