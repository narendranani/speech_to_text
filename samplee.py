def bin_search(arr, start, end, item):
    if end >= start:
        mid = start + (end - start) // 2
        print(mid)
        if arr[mid] == item:
            return mid
        elif arr[mid] > item:
            return bin_search(arr, start, mid - 1, item)
        else:
            return bin_search(arr, mid + 1, end, item)
    else:
        return -1


arr = [4, 12, 365, 456, 3243, 3456, 34554]
start = 0
end = len(arr) - 1
a = bin_search(arr, start, end, 456)
print(a)
