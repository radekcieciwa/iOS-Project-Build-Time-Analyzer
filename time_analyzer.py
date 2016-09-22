import fileinput
import json

# Reading data
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

def read_json(text):
	readed_json = json.loads(text)
	return readed_json

# Debug print 
def print_time_recurently(json, depth, spacing):
	if depth == 0:
		print spacing + json['name'] + ": " + str(json['time']) + "s"
		return

	print spacing + json['name'] + ": " + str(json['time']) + "s"
	childs = json['childs']
	if childs != None:
		for child in childs:
			print_time_recurently(child, depth - 1, spacing + " ")

	return 

# Analysis data
# Returns Int with number of nodes
def count_nodes(json):
	childs = json['childs']
	if childs == None:
		return 1
	else:
		sum = 0
		for child in childs:
			sum += count_nodes(child)
		# sum = reduce(lambda a,b: a + count_nodes(b), childs)
		return sum

# Returns array of times on current level of depth
def count_time_distribution_on_depth(json, depth):
	if depth == 0:
		return [json['time']]
	else:
		distribution = []
		childs = json['childs']
		if childs != None:
			for child in childs:
				distribution += count_time_distribution_on_depth(child, depth - 1)

		return distribution

# Main
text = convert_string_array_to_string(read_stdin_as_string_array())
readed_json = read_json(text)[0]
# print_time_recurently(readed_json, 3, "")
number_of_nodes = count_nodes(readed_json)
print number_of_nodes

time_distribution = count_time_distribution_on_depth(readed_json, 2)
print time_distribution
