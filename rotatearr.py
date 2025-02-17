def rotate_array(arr: list, positions: int, direction: str) -> list:

    positions = positions % len(arr) 

    if direction == "right":
        return arr[-positions:] + arr[:-positions]
    elif direction == "left":
        return arr[positions:] + arr[:positions]



print(rotate_array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10],4,"right"))