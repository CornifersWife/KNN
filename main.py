import csv
import math
from openpyxl import Workbook
from openpyxl.chart import LineChart, Reference


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
    counts = {}
    for element in data_tmp[:k]:
        name = element[1]
        if name in counts:
            counts[name] += 1
        else:
            counts[name] = 1
    return max(counts, key=lambda x: counts[x]) == test_row[-1].strip()


def knn(train_set, test_set, k):
    total = 0
    correct = 0
    for test_row in test_set:
        total += 1
        if single_row_knn(train_set, test_row, k):
            correct += 1
    return correct, total


def accuracy(correct, total):
    print(f'Accuracy is {correct * 100 / total}%')


def excel(train_set, test_set):
    max_k = len(train_set)
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.append(["K Value", "Accuracy"])
    for k in range(1, max_k + 1):
        correct, total = knn(train_set, test_set, k)
        Accuracy = correct / total
        worksheet.append([k, Accuracy])
    chart = LineChart()
    chart.title = "Accuracy vs. K Value"
    chart.y_axis.title = "Accuracy"
    chart.x_axis.title = "K Value"
    chart.y_axis.scaling.max = 1.0
    chart.y_axis.scaling.min = 0.0
    chart.y_axis.number_format = '0%'
    data = Reference(worksheet, min_col=2, min_row=1, max_col=2, max_row=max_k + 1)
    x_values = Reference(worksheet, min_col=1, min_row=2, max_row=max_k + 1)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(x_values)
    worksheet.add_chart(chart, "D2")
    try:
        workbook.save('KNN Results.xlsx')
    except PermissionError:
        print('Remove KNN Results file first in order to update the data in excel')

train_set = read_csv('data/iris.data')
test_set = read_csv('data/iris.test.data')
#train_set = read_csv('data/wdbc.data')
#test_set = read_csv('data/wdbc.test.data')
k = 14

excel(train_set, test_set)

correct, total = knn(train_set, test_set, k)
accuracy(correct, total)

example_vector = train_set[0]
formatted_vector = ", ".join([f"{elem}" for elem in example_vector])
print(f"Input singular vector written in like this:   (write  stop  to terminate this program)\n{formatted_vector}")

while True:
    input_vector = input()
    if input_vector == "stop":
        break
    input_vector = input_vector.split(',')
    try:
        input_vector[:-1] = [float(x.strip()) for x in input_vector[:-1]]
        output = "correctly" if single_row_knn(train_set, input_vector, k) else "incorrectly"
        print(f'For this vector the program has guessed {output}')
    except Exception:
        print('Incorrect data input, try again')
