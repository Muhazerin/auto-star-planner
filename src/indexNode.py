# Creates a list of index_node_list similar to indexes_list
# Which is basically a list that contains index_node_list
# and index_node_list contains index_node(s)
def create_list_of_index_node_list(indexes_list):
    # Initialize an empty list
    list_of_index_node_list = []

    # Loop through the indexes_list
    for indexes in indexes_list:
        # Append a list ot list_of_index_node_list
        list_of_index_node_list.append([])
        for elem in indexes:
            # Create a temporary node to hold the index_no and index_info
            temp_node = IndexNode(elem['index'], elem['info'])
            # Add that temp node to the list created in the loop above
            list_of_index_node_list[len(list_of_index_node_list) - 1].append(temp_node)

    # Loop through the list_of_index_node in reverse from second last index
    for i in range(len(list_of_index_node_list) - 2, -1, -1):
        # Loop through the index_node in the index_node_list
        for index_node in list_of_index_node_list[i]:
            # Point the index_node_list to the next index_node_list in list_of_index_node_list
            index_node.index_node_list = list_of_index_node_list[i + 1]

    # Return the list of index_node_list
    return list_of_index_node_list


class IndexNode:
    def __init__(self, new_index_no, new_info):
        self.__index_no = new_index_no
        self.__info = new_info
        self.__index_node_list = None

    @property
    def index_no(self):
        return self.__index_no

    @index_no.setter
    def index_no(self, new_index_no):
        self.__index_no = new_index_no

    @property
    def info(self):
        return self.__info

    @info.setter
    def info(self, new_info):
        self.__info = new_info

    @property
    def index_node_list(self):
        return self.__index_node_list

    @info.setter
    def index_node_list(self, new_index_node_list):
        self.__index_node_list = new_index_node_list

    # For testing, to output how the index graph looks like
    def print_something(self):
        print(self.__index_no, self.__info)
        print('Index Node List')
        if self.__index_node_list:
            for node in self.__index_node_list:
                print(node.index_no)
                print()
        else:
            print('None')
