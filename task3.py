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

	return out_generator.to_list()


if __name__ == "__main__":
	intervals = { 
		'lesson': [1594663200, 1594666800], 
  		'pupil' : [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472], 
  		'tutor' : [1594663290, 1594663430, 1594663443, 1594666473] 
	}
	out = appearance(intervals)

	total_seconds = 0

	for i in range(1, len(out), 2):
		total_seconds += out[i] - out[i - 1]

	print(total_seconds)

