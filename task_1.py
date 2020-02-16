def sorting(data):
    data = [i.replace('"', '') for i in data]
    data.sort()
    return data


def count_alphabet_sum(data):
    list_of_sums = []

    for i in data:
        name = i.lower()
        to_list = [ord(char) - 96 for char in name]
        list_of_sums.append(sum(to_list))

    return list_of_sums


def multiply(data):
    lst = []
    for index, value in enumerate(data):
        ind = index + 1
        lst.append(ind * value)

    return lst


with open('names.txt', 'r', encoding='utf-8') as f:
    list_names = f.read().split(',')

list_sorting_names = sorting(list_names)
list_alphabet_sum = count_alphabet_sum(list_sorting_names)
list_of_multiple = multiply(list_alphabet_sum)
result = sum(list_of_multiple)
print(result)
