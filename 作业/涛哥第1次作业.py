num1 = int(input("输入数字"))
num2 = int(input("输入数字"))


def appendlist(_num1: int, _num2: int):
    _list = []
    for i in range(_num1, _num2 + 1):
        _list.append(i)
    return _list


def even_list(_list):
    list1 = []
    for i in _list:
        if i % 2 == 0:
            list1.append(i)
    return list1


def odd_list(_list):
    list2 = []
    for i in _list:
        if i % 2 == 1:
            list2.append(i)
    return list2


def my_sum(_sum_list):
    n = 0
    for p in _sum_list:
        n = n + p
    return n


my_list = appendlist(num1, num2)

sum_list = even_list(my_list)
sum1 = my_sum(sum_list)

sum_list = odd_list(my_list)
sum2 = my_sum(sum_list)
print("奇数和=" + str(sum1), "偶数和=" + str(sum2))
input("按任意键结束")
