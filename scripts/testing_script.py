letters = {'a': 'apple', 'b': 'banana', 'c': 'coconut'}
nums = {'1': 'one', '2': 'two', '3': 'three'}

for v1, v2 in zip(letters.values(), nums.values()):
    print(v1, v2)