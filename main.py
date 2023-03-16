import csv
import math


def read_csv(filename):
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        all_data = []
        for row in csv_reader:
            row_data = [float(element) for element in row[:-1]]
            row_data += [row[-1]]  # add last element as string
            all_data.append(row_data)  # add row_data to list
    return all_data
def euclydian_distance (coordinates):
    x = coordinates[:-1]
    sum= 0
    for value in x:
        sum += value**2
    return math.sqrt(sum)

#def knn (k, data, test)

data_in = read_csv('data/iris.data')
data_test = read_csv('data/iris.test.data')
for row in data_test:






data = []



