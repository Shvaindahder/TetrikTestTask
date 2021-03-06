import random
import math


def task_linear(array: str) -> int:
	# O(n) = n
	for i, item in enumerate(array):
		if item == '0':
			return i
	return -1


def task_log(array: str) -> int:
	# O(n) = log(n)
	if len(array) == 1:
		return (0, -1)[array[0] == '1']

	if len(array) == 2:
		if array[1] == '1':
			return -1
		elif array[0] == '1':
			return 1
		else:
			return 0
	center = math.ceil(len(array) / 2) - 1

	if array[center] == '1':
		out = task_log(array[center:])
		if out == -1:
			return -1
		return out + center
	else:
		return task_log(array[:center + 1])


def test_task():
	# Рандомные тесты
	ones, twos = random.randint(0, 1000), random.randint(0, 1000)
	test_string = '1' * ones + '0' * twos
	try:
		assert task_linear(test_string) == ones, f"Linear solver error. Excepted {ones}, actualy {task_linear(test_string)}"
		assert task_log(test_string) == ones,    f"Log solver error. Excepted {ones}, actualy {task_log(test_string)}"
	except AssertionError as err:
		print(err)
	else:
		print("OK")


if __name__ == "__main__":
	test_strings = [
	    ("111111111111111111111111100000000", 25),
		("1111110000", 6),
		("1000", 1),
		("11111111111100", 12),
		("1", -1),
		("0", 0)
	]

	for string in test_strings:
		print(f"String\t: {string[0]}")
		try:
			assert task_linear(string[0]) == string[1], f"Linear solver error. Excepted {string[1]}, actualy {task_linear(string[0])}"
		except AssertionError as err:
			print(err)
		else:
			print("Linear\t: OK")

		try:
			assert task_log(string[0]) == string[1], f"Log solver error. Excepted {string[1]}, actualy {task_log(string[0])}"
		except AssertionError as err:
			print(err)
		else:
			print("Log\t: OK")

		print()

