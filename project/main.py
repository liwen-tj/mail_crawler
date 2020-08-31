
def divide(x, y):
    ans = 0
    try:
        ans = x / y
    except ZeroDivisionError:
        pass
    return ans


res = divide(1, 0)
print(res)
