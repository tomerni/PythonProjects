########################
# FILE : ex11.py
# WRITER: Tomer Nissim, tomerni, 313232845
# EXERCISE: intro2cs1 Ex11 2019-2020
# DESCRIPTION: Creating and diagnosing illnesses and symptoms
########################
import itertools


class Node:
    def __init__(self, data, positive_child=None, negative_child=None):
        self.data = data
        self.positive_child = positive_child
        self.negative_child = negative_child


class Record:
    def __init__(self, illness, symptoms):
        self.illness = illness
        self.symptoms = symptoms


def parse_data(filepath):
    with open(filepath) as data_file:
        records = []
        for line in data_file:
            words = line.strip().split()
            records.append(Record(words[0], words[1:]))
        return records


class Diagnoser:
    def __init__(self, root):
        self.root = root
        self.__cur_root = root

    def diagnose(self, symptoms):
        return self._diagnose_helper(self.root, symptoms)

    def _diagnose_helper(self, node, symptoms):
        """
        Finds the leaf that matched the symptoms
        :param node: The current Node object that is being checked
        :param symptoms: List of strings with the symptoms
        :return: The name of the illness that matched the symptoms
        """
        if node.positive_child is None and node.negative_child is None:
            data = node.data
            return data
        if node.data in symptoms:
            return self._diagnose_helper(node.positive_child, symptoms)
        else:
            return self._diagnose_helper(node.negative_child, symptoms)

    def calculate_success_rate(self, records):
        counter = 0
        for record in records:
            illness = self.diagnose(record.symptoms)
            if illness == record.illness:
                counter += 1
        return counter / len(records)

    def all_illnesses(self):
        dict = {}
        self._all_illnesses_helper(self.root, dict)
        lst = sorted([[dict[key], key] for key in dict.keys()])
        final_lst = [lst[i][1] for i in range(len(lst) - 1, -1, -1)]
        return final_lst

    def _all_illnesses_helper(self, node, dict):
        """
        Updates the given dictionary according to the appearances of the
        illnesses in the tree
        :param node: The current Node object that is being checked
        :param dict: Dictionary with the illnesses
        """
        if node.data is not None:
            if node.positive_child is None and \
                    node.negative_child is None:
                dict[node.data] = dict.get(node.data, 0) + 1
            else:
                for n in [node.positive_child, node.negative_child]:
                    self._all_illnesses_helper(n, dict)

    def paths_to_illness(self, illness):
        lst = []
        self._paths_to_illness_helper(illness, lst, [], self.root)
        return lst

    def _paths_to_illness_helper(self, illness, lst, cur_lst, node):
        """
        Finds all of the paths to the illness using recursion
        :param illness: String with the checked illness
        :param lst: list of lists
        :param cur_lst: list with True and False according to the path
        :param node: The current Node object that is being checked
        :return: list of lists with all of the paths to the given illness
        """
        if node.positive_child is None and node.negative_child is \
                None and node.data == illness:
            lst.append(cur_lst)
        if node.positive_child is not None:
            temp_lst = cur_lst[:]
            temp_lst.append(True)
            self._paths_to_illness_helper(illness, lst, temp_lst,
                                          node.positive_child)
        if node.negative_child is not None:
            temp_lst = cur_lst[:]
            temp_lst.append(False)
            self._paths_to_illness_helper(illness, lst, temp_lst,
                                          node.negative_child)


def build_tree(records, symptoms):
    if not records and not symptoms:
        return Node(None)
    if not symptoms:  # Empty symptoms but not empty records
        illness_dict = {}
        for val in records:  # Finding the most common illness
            illness_dict[val.illness] = illness_dict.get(val.illness, 0) + 1
        return Node(max(illness_dict, key=illness_dict.get))
    return _build_tree_helper(records, symptoms)


def _build_tree_helper(records, symptoms):
    """
    :param records: list of Record objects
    :param symptoms: list of strings with the symptoms
    :return: Node object which is the root of the tree and connected to his
    children
    """
    if not symptoms:
        return _check_records(records)
    else:
        true_list = [record for record in records if symptoms[0] in
                     record.symptoms]
        false_list = [record for record in records if symptoms[0] not in
                      record.symptoms]
        return Node(symptoms[0], _build_tree_helper(true_list, symptoms[1:]),
                    _build_tree_helper(false_list, symptoms[1:]))


def _check_records(records):
    """
    :param records: list of Record objects
    :return: Node with the record that should be put in the leaf
    """
    if not records:
        return Node(None)
    elif len(records) == 1:
        return Node(records[0].illness)
    else:
        illness_dict = {}
        for val in records:
            illness_dict[val.illness] = illness_dict.get(val.illness, 0) + 1
        return Node(max(illness_dict, key=illness_dict.get))


def optimal_tree(records, symptoms, depth):
    combinations = list(itertools.combinations(symptoms, depth))
    max_success_rate = 0
    max_tree = None
    for combination in combinations:
        tree = build_tree(records, combination)
        temp_diagnoser = Diagnoser(tree)
        temp_success = temp_diagnoser.calculate_success_rate(records)
        if temp_success > max_success_rate:
            max_success_rate = temp_success
            max_tree = tree
    return max_tree


if __name__ == "__main__":

    # Manually build a simple tree.
    #                cough
    #          Yes /       \ No
    #        fever           healthy
    #   Yes /     \ No
    # influenza   cold

    flu_leaf = Node("influenza", None, None)
    cold_leaf = Node("cold", None, None)
    inner_vertex = Node("fever", flu_leaf, cold_leaf)
    healthy_leaf = Node("healthy", None, None)
    root = Node("cough", inner_vertex, healthy_leaf)

    diagnoser = Diagnoser(root)

    # Simple test
    diagnosis = diagnoser.diagnose(["cough"])
    if diagnosis == "cold":
        print("Test passed")
    else:
        print("Test failed. Should have printed cold, printed: ", diagnosis)
