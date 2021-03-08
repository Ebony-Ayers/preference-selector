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
	responce_number = 1
	for line in data_file:
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

print("Finding best preferences selection for", num_people, "people each with", num_preferences, "preferences")

#the better the solution the lower the result
#if a < b then a is better than b
def score_solution(sol):
	return sum(sol)

#get the name of the preference
def get_country_from_preference(person, preference):
	return preferences[person][1][preference]

partial_solution = [0] * num_people
collisions = dict()
index = 0
score = score_solution(partial_solution)

best_solution = None
best_score = None
first_solution = None

country = None
first = True
while True:
	if partial_solution[index] >= num_preferences:
		score -= partial_solution[index]
		partial_solution[index] = 0
		index -= 1
		#print(partial_solution)
		if index < 0: break
		partial_solution[index] += 1
		score += 1
		continue
	
	#get the new preference and add it to the collisions to check in constant time if the preference collides with another
	country = get_country_from_preference(index, partial_solution[index])
	num = collisions.get(country, 0)
	collisions[country] = num + 1
	#if the partial solution is not valid
	if num == 1:		
		collisions[country] -= 1
		partial_solution[index] += 1
		score += 1
	#if the partial solution is valid
	else:
		#if the partial position is a posible solution
		if index >= num_people - 1:
			if first:
				best_solution = partial_solution.copy()
				best_score = score
				first_solution = partial_solution.copy()
				#print("First come first serve solution:", best_solution)
				first = False
			else:
				if score < best_score:
					best_solution = partial_solution.copy()
					best_score = score
			
			collisions[country] -= 1
			partial_solution[index] += 1
			score += 1
			if partial_solution[index] >= num_preferences:
				score -= partial_solution[index]
				partial_solution[index] = 0
				index -= 1
				partial_solution[index] += 1
				score += 1
		#continue to next node in three
		else:
			index += 1

#display the answer
#print("best solution:", best_solution)
if first_solution == best_solution:
	print()	
	print("same solution found as first come first serve")
print()
print("selections:")
i = 0
while i < len(best_solution):
	print("\t" + str(preferences[i][0]) + ": " + str(preferences[i][1][best_solution[i]]) + " preference:" + str(best_solution[i] + 1))
	
	i += 1
