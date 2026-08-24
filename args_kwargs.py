
def sm(a, b):
    return a + b

sm(1, 2)
sm(a=1, b=2)
numbers = (1, 2)
sm(numbers[0], numbers[1])
sm(*numbers)
kwargs = {'sep': '   '}
print(*numbers, **kwargs)