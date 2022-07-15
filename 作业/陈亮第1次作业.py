def generateList(start):
    if start > 0 and isinstance(start, int):
        return [x for x in range(start, start + 10000)]
    print("start must be natural number")
    return None


def sum(naturalNumList, type):
    if naturalNumList is None or len(naturalNumList) == 0:
        return None

    sumOddDigit = 0
    sumEvenDigit = 0
    for i in range(0, len(naturalNumList), 2):
        sumEvenDigit += naturalNumList[i]
    for i in range(1, len(naturalNumList), 2):
        sumOddDigit += naturalNumList[i]

    if type == 'odd':
        return sumEvenDigit if naturalNumList[0] % 2 == 1 else sumOddDigit
    elif type == 'even':
        return sumOddDigit if naturalNumList[0] % 2 == 1 else sumEvenDigit
    return None


if __name__ == '__main__':
    naturalNumList = generateList(1)
    sumOdd = sum(naturalNumList, 'odd')
    sumEven = sum(naturalNumList, 'even')
