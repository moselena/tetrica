from collections import Counter


def get_list_ip(data):
    list_of_ip = []

    for el in data:
        a = el.split('\t')
        if a[0] != '':
            list_of_ip.append(a[1])

    return list_of_ip


def get_most_common(data):
    most_common_ip = Counter(data).most_common(5)
    result = []
    for el in most_common_ip:
        ip = el[0]
        result.append(ip)

    return result


with open('hits.txt', 'r', encoding='utf-8') as f:
    list_names = f.read().split('\n')


list_ip = get_list_ip(list_names)
most_common = get_most_common(list_ip)
print(most_common)


