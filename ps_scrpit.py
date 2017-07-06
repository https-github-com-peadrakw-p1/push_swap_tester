#!/usr/bin/env python
# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ps_scrpit.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: kdavis <marvin@42.fr>                      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2017/06/27 16:11:00 by kdavis            #+#    #+#              #
#    Updated: 2017/06/27 16:11:00 by kdavis           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import os
from subprocess import check_output, PIPE, Popen
import shlex
import numpy
import matplotlib.pyplot as plt
import random

'''
Creates a random list of numbers
'''
def create_arg_list(arg_count):
	arg_list = []
	arg_str = ""
	rand = 0
	for i in range(arg_count):
		while (rand in arg_list):
			rand = random.randint(0, arg_count * 100)
		arg_list.append(rand)
		arg_str = arg_str + str(rand) + " "
	return (arg_str)

'''
Takes a path to the push swap program and a list of numbers
Returns the number of operations required to sort the list
def run_program(program, argstr):
	arguments = shlex.split(program + " " + argstr)
	if (program == "./push_swap"):
		proc = Popen(args=arguments, stdout=PIPE)
		out = proc.communicate()[0]
	elif (program == "./checker"):
		print (PIPE)
		proc = Popen(args=arguments, stdin=PIPE)
		out = proc.stdout.read()
		print (out)
	else:
		return (None)
	print("ran Popen")
	return (out)
'''
import json

def results_to_json(results):
	f = open("results.json", 'w+')
	if results != None:
		avg = int(sum(results) / len(results))
		minimum = min(results)
		maximum = max(results)
		dump = json.dump({"avg":avg, "min":minimum, "max":maximum}, f)
	else:
		dump = json.dump({"avg":-1, "min":-1, "max":-1}, f)
	f.close

def run_ps(args):
#	out = check_output("./push_swap {}".format(args), shell=True)
#	check = check_output("echo '{}' | ./checker {}".format(out, args), shell=True)
	ps_args = shlex.split("./push_swap " + args)
	ch_args = shlex.split("./checker " + args)
	ps_proc = Popen(args=ps_args, stdout=PIPE)
	out = ps_proc.communicate()[0]
	f = open("command_list", mode='w+r')
	f.write(out)
	f.seek(0)
	ch_proc = Popen(args=ch_args, stdin=f, stdout=PIPE)
	f.close
	check = ch_proc.communicate()[0]
	if (check == "OK\n"):
		op_count = len(out.split("\n")) - 1
	else:
		op_count = None
	return (op_count)

#Runs push_swap function with random arguments 'n' times
def loop_ps(path, arg_count, n):
	result = []
	for i in range(0, n):
		args = create_arg_list(arg_count)
		op_count = run_ps(args)
		print (i, op_count)
		if (op_count == None):
			return (None)
		result.append(op_count)
	return (result)

#Prints statistical data of a list
def describe_ps(results):
	print ("Mean:{}".format(numpy.mean(results)))
	print ("Std:{}".format(numpy.std(results)))
	print ("Max:{}".format(numpy.max(results)))
	print ("Min:{}".format(numpy.min(results)))
	plt.hist(results)
	plt.show()

#TODO: create a function to retreive the path of the push_swap executable

result = loop_ps(os.getcwd(), int(sys.argv[1]), int(sys.argv[2]))
if result:
	describe_ps(result)
results_to_json(result)
