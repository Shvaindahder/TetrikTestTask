from functools import reduce


class Interval:
	def __init__(self, start, end):
		try:
			assert start < end
		except AssertionError:
			print("Error interval. Start time couldn't be less then end time.")
		else:
			self.start = start
			self.end   = end


class IntervalGenerator:
	def __init__(self, intervals: list):
		try:
			assert len(intervals) % 2 == 0
		except AssertionError:
			pass
		else:
			self.intervals = intervals
			self.current = 0

	def has_next(self):
		if self.current < len(self.intervals):
			return True
		return False

	def next(self):
		if self.has_next():
			new_interval = Interval(self.intervals[self.current], self.intervals[self.current + 1])
			self.current += 2
			return new_interval
		else:
			return None

	def to_list(self):
		out_list = list()
		current_interval = self.next()
		while current_interval is not None:
			out_list.extend([current_interval.start, current_interval.end])
			current_interval = self.next()

		return out_list


def cross_intervals(gen1: IntervalGenerator, gen2: IntervalGenerator):
	crossed_intervals = list()

	interval1 = gen1.next()
	interval2 = gen2.next()

	while interval1 is not None and interval2 is not None:
		start = interval1.start
		end   = interval1.end

		if interval2.start <= start:
			if interval2.end <= start:
				# interval1 не входит в interval2
				interval2 = gen2.next()
			elif interval2.end <= end:
				# interval1 пересекает interval2 слева
				crossed_intervals.extend([start, interval2.end])
				if interval2.end == end:
					interval1 = gen1.next()
				interval2 = gen2.next()
			else:
				# interval1 включает в себя interval2
				crossed_intervals.extend([start, end])
				interval2 = gen2.next()
		elif interval2.start < end:
			if interval2.end <= end:
				# interval1 включен в interval2
				crossed_intervals.extend([interval2.start, interval2.end])
				if interval2.end == end:
					interval1 = gen1.next()
				interval2 = gen2.next()
			else:
				# interval1 пересекает interval2 справа
				crossed_intervals.extend([interval2.start, end])
				interval1 = gen1.next()
		else:
			interval1 = gen1.next()

	return IntervalGenerator(crossed_intervals)




def appearance(intervals):
	lesson_generator = IntervalGenerator(intervals["lesson"])
	tutor_generator  = IntervalGenerator(intervals["tutor"])
	pupil_generator  = IntervalGenerator(intervals["pupil"])

	out_generator = reduce(cross_intervals, [lesson_generator, tutor_generator, pupil_generator])
	out_generator = out_generator.to_list()

	total_seconds = 0

	for i in range(1, len(out_generator), 2):
		total_seconds += out_generator[i] - out_generator[i - 1]

	return total_seconds


if __name__ == "__main__":
	tests = [
	   {'data': {'lesson': [1594663200, 1594666800],
	             'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
	             'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
	    'answer': 3117
	    },
	   # {'data': {'lesson': [1594702800, 1594706400],
	   #           'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
	   #           'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
	   #  'answer': 3577
	   #  }, Некорректные интервалы pupil
	   {'data': {'lesson': [1594692000, 1594695600],
	             'pupil': [1594692033, 1594696347],
	             'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
	    'answer': 3565
	    },
	]
	for i, test in enumerate(tests):
		test_answer = appearance(test["data"])
		assert test_answer == test["answer"], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'

