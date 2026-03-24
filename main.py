import types

# 1. Итератор для одного уровня вложенности 
class FlatIterator:
    def __init__(self, list_of_list):
        self.list_of_list = list_of_list
        self.outer_index = 0
        self.inner_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.outer_index >= len(self.list_of_list):
            raise StopIteration
        current_list = self.list_of_list[self.outer_index]
        if self.inner_index >= len(current_list):
            self.outer_index += 1
            self.inner_index = 0
            return next(self)
        item = current_list[self.inner_index]
        self.inner_index += 1
        return item

def test_1():
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]
    expected = ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    for flat_item, check_item in zip(FlatIterator(list_of_lists_1), expected):
        assert flat_item == check_item
    assert list(FlatIterator(list_of_lists_1)) == expected
    print("test_1 passed")

# 2. Генератор для одного уровня вложенности 
def flat_generator(list_of_lists):
    for sublist in list_of_lists:
        for item in sublist:
            yield item

def test_2():
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]
    expected = ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    for flat_item, check_item in zip(flat_generator(list_of_lists_1), expected):
        assert flat_item == check_item
    assert list(flat_generator(list_of_lists_1)) == expected
    assert isinstance(flat_generator(list_of_lists_1), types.GeneratorType)
    print("test_2 passed")

# 3. Итератор для произвольной вложенности 
class FlatIteratorDeep:
    def __init__(self, list_of_list):
        self.stack = [(list_of_list, 0)]

    def __iter__(self):
        return self

    def __next__(self):
        while self.stack:
            current_list, idx = self.stack[-1]
            if idx >= len(current_list):
                self.stack.pop()
                continue
            element = current_list[idx]
            self.stack[-1] = (current_list, idx + 1)
            if isinstance(element, list):
                self.stack.append((element, 0))
                continue
            return element
        raise StopIteration

def test_3():
    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]
    expected = ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    for flat_item, check_item in zip(FlatIteratorDeep(list_of_lists_2), expected):
        assert flat_item == check_item
    assert list(FlatIteratorDeep(list_of_lists_2)) == expected
    print("test_3 passed")

# 4. Генератор для произвольной вложенности 
def flat_generator_deep(list_of_list):
    for item in list_of_list:
        if isinstance(item, list):
            yield from flat_generator_deep(item)
        else:
            yield item

def test_4():
    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]
    expected = ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    for flat_item, check_item in zip(flat_generator_deep(list_of_lists_2), expected):
        assert flat_item == check_item
    assert list(flat_generator_deep(list_of_lists_2)) == expected
    assert isinstance(flat_generator_deep(list_of_lists_2), types.GeneratorType)
    print("test_4 passed")

if __name__ == '__main__':
    test_1()
    test_2()
    test_3()
    test_4()