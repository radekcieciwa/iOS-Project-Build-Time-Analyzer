import fileinput
from numpy import arange
import json
import os
import operator

# Returns array of lines 
def read_stdin_as_string_array():
	tmp = []
	for line in fileinput.input():
		tmp.append(line)
	return tmp


def convert_string_array_to_string(array):
	tmp = ""
	for line in array:
		tmp += line
	return tmp

# Read array of strings and counts number of spaces in the begging to index of line 
# Index of line is the index in returned array
# Returns array of ints
def count_number_of_spaces_in_file(array):
	number_of_spaces = []
	line_index = 0
	for line in array:
		number_of_spaces.append(count_spaces(line))
	return number_of_spaces

# Count spaces on begging of @line
def count_spaces(line):
	count = 0
	for i in line:
		if i == ' ':
			count += 1
		else:
			return count

# Returns array of indexes that values match @checked_value
# @array_of_values is a array of ints
def set_of_indexes(checked_value, array_of_values):
	indexes = []
	for index, element in enumerate(array_of_values):
		if element == checked_value:
			indexes.append(index)
	return indexes

def decrease_by_one_all_values_greater_than(value, from_array):
	array_copy = []
	for index, x in enumerate(from_array):
		if x > value:
			array_copy.append(x-1)
		else:
			array_copy.append(x)
	return array_copy

# Function normalize the array
# Returns array without missing counts of spaces
def normalize_array(temp_array):
	iterator = 0
	# temp_array = array
	while iterator <= max(temp_array):
		while len(set_of_indexes(iterator, temp_array)) == 0:
			temp_array = decrease_by_one_all_values_greater_than(iterator, temp_array)
		iterator += 1
	return temp_array

# Returns array of sub elements
def convert_tree_to_array_by_depth(depths_array, line_numbers_array, depth_level):
	indexes_on_depth = set_of_indexes(depth_level, depths_array)
	if len(indexes_on_depth) == 0:
		return []
	else:
		elements = []
		for i in range(0, len(indexes_on_depth)):
			dict = {}
			array_index = indexes_on_depth[i]
			dict['line'] = line_numbers_array[array_index]
			start = array_index + 1
			end = len(depths_array) - 1
			if i + 1 < len(indexes_on_depth):
				# take one element before next element on same depth
				end = indexes_on_depth[i+1] - 1
			# if next subelement is to far
			if start > len(depths_array):
				dict['childs'] = []
			else:
				dict['childs'] = convert_tree_to_array_by_depth(depths_array[start:end], line_numbers_array[start:end], depth_level + 1)

			elements.append(dict)

		return elements

def read_names(array):
	names = []
	for line in array:
		name = line.split(":")[0].strip()
		names.append(name)
	return names

def read_times(array):
	times = []
	for line in array:
		time = line.split(":")[1].strip()
		# take the first time, and remove last char from it 'r'
		time = time.split(" ")[0][:-1] 
		times.append(float(time))
	return times

def extract_time(dict):
	return e['time']

def populate_values(elements, names, times):
	if len(elements) == 0:
		return None

	for e in elements:
		line = e['line']
		e['time'] = times[line]
		e['name'] = names[line]
		e['childs'] = populate_values(e['childs'], names, times)
		del e['line']
	elements.sort(key=operator.itemgetter('time'), reverse=True)
	return elements

def get_system_profile():
	profile = os.popen("system_profiler SPHardwareDataType | grep -v 'Hardware' | grep -v '^$' | awk '{$1=$1};1'").read()
	return profile

# Execution
file_as_string_array = read_stdin_as_string_array()
readed_array = count_number_of_spaces_in_file(file_as_string_array)
normalized_array = normalize_array(readed_array)
indexed_array = arange(len(normalized_array))
MAX_DEPTH = max(normalized_array)

# make tree structure
line_depth_result = convert_tree_to_array_by_depth(normalized_array, indexed_array, 0)
# lines_json = json.dumps(result, ensure_ascii=False)

# get values from lines
names = read_names(file_as_string_array)
times = read_times(file_as_string_array)

json_result = json.dumps(populate_values(line_depth_result, names, times), ensure_ascii=False)
print json_result
# print "\n\tRetreive from machine:\n\n" + get_system_profile()
