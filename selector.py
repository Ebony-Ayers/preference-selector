#MIT License
#
#Copyright (c) 2021 Ebony Ayers
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

import sys

#arg 0: file name
#arg 1: data file
#arg 2: collum containing identidier for responce (e.g. name)
#arg 3: number of preferences
#arg 4: collum containing preference one
#arg 4: collum containing preference two
...
#arg n: collum containing preference n

if(len(sys.argv) < 4):
	print("Error: not enough arguments")
	quit()

file_name = sys.argv[1]
identifier_collum = int(sys.argv[2])
num_preferences = int(sys.argv[3])

if(len(sys.argv) < 4 + num_preferences):
	print("Error: not enough arguments")
	quit()

#map mapping first preference to its location and so on
preference_locations = [None] * num_preferences

i = 0
while(i < num_preferences):
	preference_locations[i] = int(sys.argv[4 + i])
	i += 1

#everyones preferences
preferences = list()

with open(file_name, 'r') as data_file:
	responce_number = 0
	for line in data_file:
		if responce_number == 0:
			responce_number += 1
			continue
		
		split_line = line.rstrip().replace('"', '').split(',')
		
		person_identifier = split_line[identifier_collum]
		
		person_preferences = [None] * num_preferences
		i = 0
		while(i < num_preferences):
			person_preferences[i] = split_line[preference_locations[i]]
			i += 1
		
		preferences.append((person_identifier, person_preferences, responce_number))
		responce_number += 1

num_people = len(preferences)

#a partial solution is a list of preferences
#it is valid if an only if there are collisions caused by two preferences being for the same thing
def is_partial_solution_valid(sol):
	collisions = dict()
	
	i = 0
	while i < num_people:
		country = preferences[i][1][sol[i]]
		collisions[country] = collisions.get(country, 0) + 1
		i += 1
	
	for country in collisions:
		if collisions[country] >= 2: return False
	return True

#returns increments a partial solution
#running until the function return None garantees that all possible partial solutions will be generators
#returning 0 indicates that the generated solution is garanteed to be rejected
def generate_partial_solution(sol):
	if sol == None: return None

	new_sol = [0] * num_people
	
	new_sol = sol
	new_sol[0] += 1
	
	i = 0
	while i < num_people:
		if new_sol[i] > num_preferences - 1:
			if i + 1 > num_people - 1: return None
			new_sol[i] = 0
			new_sol[i + 1] += 1
		else:
			break
		i += 1
		
	return sol

#the better the solution the lowre the result
#if a < b then a is better than b
def score_partial_solution(sol):
	return sum(sol)

possible_solution = [0] * num_people
best_solution = None

#test every possible sulution
#if it is the first valid solution record it
#if the current sollution is better than the previous record it
while possible_solution != None:
	if possible_solution != 0:
		if is_partial_solution_valid(possible_solution):
			if best_solution == None:
				best_solution = (score_partial_solution(possible_solution), possible_solution.copy())
			elif score_partial_solution(possible_solution) <= best_solution[0]:
				best_solution = (score_partial_solution(possible_solution), possible_solution.copy())
	
	possible_solution = generate_partial_solution(possible_solution)

if best_solution == None:
	print("No valid solution found")
else:
	i = 0
	while i < num_people:
		print(preferences[i][0] + ": " + preferences[i][1][best_solution[1][i]] + "  |  got preference: " + str(best_solution[1][i] + 1))
		i += 1
