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


def euclydian_distance(coordinates):
    sum = 0
    for value in coordinates[:-1]:
        sum += value ** 2
    return math.sqrt(sum)


def knn(k, train_data, test_row):
    data_tmp = []
    for row in train_data:
        relative_cords = []
        for column in range(len(row) - 1):
            relative_cords.append(row[column] - test_row[column])
        distance = euclydian_distance(relative_cords)
        data_tmp.append((distance, row[-1]))

    data_tmp.sort(key=lambda x: x[0])

    map = {}
    for element in data_tmp[:k]:
        name = element[1]
        if name in map:
            map[name] += 1
        else:
            map[name] = 1
    for key,value in map.items():
        print(f'{key}: {value}')
    return max(map, key=lambda x: map[x])


data_in = read_csv('data/iris.data')
data_test = read_csv('data/iris.test.data')
k = len(data_in)

total = 0
correct = 0
for row in data_test:
    print (f'\nCorrect is:  {row[-1]}')
    total += 1
    name = knn(k, data_in, row)
    print(f'I guessed: {name}')
    if name == row[-1]:
        print('yas')
        correct += 1
    else:
        print(':(')
        # print(f' guessed {knn(k, data_in, row)} should be {row[-1]};')
print(f'Accuracy is {correct * 100 / total}%')
