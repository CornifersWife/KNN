import csv
import math


def read_csv(filename):
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        all_data = []
        for row in csv_reader:
            row_data = [float(element) for element in row[:-1]]
            row_data += [row[-1]]
            all_data.append(row_data)
    return all_data


def euclidean_distance(coordinates):
    sum = 0
    for value in coordinates[:-1]:
        sum += value ** 2
    return math.sqrt(sum)


def single_row_knn(train_set, test_row, k):
    data_tmp = []
    for row in train_set:
        relative_cords = []
        for column in range(len(row) - 1):
            relative_cords.append(row[column] - test_row[column])
        distance = euclidean_distance(relative_cords)
        data_tmp.append((distance, row[-1]))
    data_tmp.sort(key=lambda x: x[0])
    map = {}
    for element in data_tmp[:k]:
        name = element[1]
        if name in map:
            map[name] += 1
        else:
            map[name] = 1
    for key, value in map.items():
        print(f'{key}: {value}')
    return max(map, key=lambda x: map[x]) == test_row[-1]
    """
    z racji że max w momencie gdy ma wybrać spośród równych sobie wartości 
    to wybiera najwcześniej dodaną najwcześniej to dokładność 
    jest często większa niż spoedziewana
    """


def knn(train_set, test_set, k):
    total = 0
    correct = 0
    for test_row in test_set:
        total += 1
        if (single_row_knn(train_set, test_row, k)):
            correct += 1
    return correct, total


def Accuracy(correct, total):
    print(f'Accuracy is {correct * 100 / total}%')


train_set = read_csv('data/iris.data')
test_set = read_csv('data/iris.test.data')
k = len(train_set)
correct, total = knn(train_set, test_set, k)
Accuracy(correct, total)
vector = train_set[0]
formatted_vector = ", ".join([f"{elem}" for elem in vector[:-1]]) + f", {vector[-1]}"
print(f"Input singular vector written in the same vector as \n{formatted_vector}")
while True:
    input_vector_str = input(':')
    input_vector_str = input_vector_str.replace(" ", "").replace("\t", "").replace("\n", "")
    input_vector = input_vector_str.split(',')
    input_vector[:-1] = [float(x) for x in input_vector[:-1]]
    output = "correctly" if single_row_knn(train_set,input_vector,k) else "incorrectly"
    print(f'For this vector the program has guessed {output}')