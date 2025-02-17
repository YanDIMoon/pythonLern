def sortstob(arr: list) -> list:
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def sortbtos(arr: list) -> list:
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] < arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

print(sortstob([5,7,8,9,10,65,48,32,47,15]))
print(sortbtos([5,7,8,9,10,65,48,32,47,15]))