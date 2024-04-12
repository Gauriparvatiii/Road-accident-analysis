# -- coding: utf-8 --
import time
import itertools
import csv
from prettytable import PrettyTable

def sort_and_limit(dictionary, max_columns=20):
    sorted_dict = dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=True))
    limited_dict = dict(list(sorted_dict.items())[:max_columns])
    return limited_dict

def print_table(dictionary, max_columns=20):
    # Create a PrettyTable instance
    table = PrettyTable()

    # Define columns
    table.field_names = ["Rank", "Itemset", "Count"]

    # Add rows to the table
    for rank, (key, value) in enumerate(dictionary.items(), start=1):
        # Splitting the key into individual items for better formatting
        items = key.split(',')
        table.add_row([rank, ', '.join(items), value])

    # Set the maximum width for each column
    for field in table.field_names:
        table.align[field] = 'l'

    # Print the table
    print(table)

def get_original_order(dataset_file):
    with open(dataset_file, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
    return headers

def apriori(baskets, tHold, start, original_order, max_columns=20):
    C1 = {}
    for transaction in baskets:
        for item in transaction.split(","):
            if item not in C1:
                C1[item] = 1
            else:
                C1[item] += 1

    L1 = {}
    for key in C1:
        if C1[key] > (len(baskets) * tHold):
            L1[key] = C1[key]

    sorted_L1 = sort_and_limit(L1, max_columns)

    # Create PrettyTable for L1
    print("L1")
    print_table(sorted_L1, max_columns)
    print(" ")

    L = [sorted_L1]
    k = 0

    while len(L[k]) > 0:
        Ck = {}
        unique = []
        for key in L[k]:
            for item in key.split(","):
                if item not in unique:
                    unique.append(item)

        for key in itertools.combinations(unique, k+2):
            if key not in Ck:
                Ck[','.join(key)] = 0

        print(" ")
        print(time.time() - start, ': Generated candidates of size', k+2)

        for transactions in baskets:
            for subset in set(itertools.permutations(transactions.split(","), (k+2))):
                candidate = ','.join(subset)
                for keys in Ck:
                    if candidate == keys:
                        Ck[keys] += 1

        print(" ")
        print(time.time() - start, ': Counted candidates of size', k+2)

        Lk = {}
        for key in Ck:
            if Ck[key] > (len(baskets) * tHold):
                Lk[key] = Ck[key]

        sorted_dict = sort_and_limit(Lk, max_columns)

        print(" ")
        print(time.time() - start, f': Frequent itemsets of size {k+2} sorted by values in descending order')
        print_table(sorted_dict, max_columns)
        print(" ")

        L.append(sorted_dict)
        k += 1

def runRetail(tHold):
    dataset_file = 'retail.dat'
    baskets = [[] for _ in range(9)]

    count = 0
    with open(dataset_file) as file:
        for line in file:
            baskets[count // 10000].append(line)
            if count > 88162:
                break
            count += 1

    for i, basket in enumerate(baskets, 1):
        start = time.time()
        original_order = get_original_order(dataset_file)
        apriori(basket, tHold, start, original_order)
        end = time.time()
        print(f'Time taken in seconds for basket {i}:', end - start)

def runMovie(tHold):
    dataset_file = "movies.csv"
    basket = []

    count = 0
    with open(dataset_file) as file:
        for line in file:
            basket.append(line)
            if count > 300:
                break
            count += 1

    start = time.time()
    original_order = get_original_order(dataset_file)
    apriori(basket, tHold, start, original_order)
    end = time.time()
    print('Time taken in seconds for basket:', end - start)

# Uncomment and run either runRetail or runMovie with the desired threshold
#runRetail(0.13)
runMovie(0.05)
