import argparse
import re
"""
//                                  _ (`-.    ('-.     _  .-')    .-')      ('-.  _  .-')   
//                                 ( (OO  )  ( OO ).-.( \( -O )  ( OO ).  _(  OO)( \( -O )  
// ,--.      ,--.     .---.       _.`     \  / . --. / ,------. (_)---\_)(,------.,------.  
// |  |.-')  |  |.-')/_   |      (__...--''  | \-.  \  |   /`. '/    _ |  |  .---'|   /`. ' 
// |  | OO ) |  | OO )|   |       |  /  | |.-'-'  |  | |  /  | |\  :` `.  |  |    |  /  | | 
// |  |`-' | |  |`-' ||   |       |  |_.' | \| |_.'  | |  |_.' | '..`''.)(|  '--. |  |_.' | 
//(|  '---.'(|  '---.'|   |       |  .___.'  |  .-.  | |  .  '.'.-._)   \ |  .--' |  .  '.' 
// |      |  |      | |   |       |  |       |  | |  | |  |\  \ \       / |  `---.|  |\  \  
// `------'  `------' `---'       `--'       `--' `--' `--' '--' `-----'  `------'`--' '--' 
//
//
//  Created by Ian Cleasby on 08/05/2015.
//  Copyright © 2017 Ian Cleasby. All rights reserved.
"""
parser = argparse.ArgumentParser() # Parse through arguments
parser.add_argument('file', type=argparse.FileType('r'))
parser.add_argument('-e', action='store_true', help='Implement error recovery feature') # little help feature added on
args = parser.parse_args()
data=args.file.read().replace('\n', '').replace(' ', '').replace('\r', '').replace('\t', '')

def followcheck (prev, options): # Search for missing entries
	follow = {
	'S': {'}': '}'}, #follows for our rules
	'S1': {'}': '}', '':''},
	'E': {'x': 'x', 'y': 'y'},
	'E1': {'x': 'x', 'y': 'y'},
	'E2': {'x': 'x', 'y': 'y'},
	'E3': {'x': 'x', 'y': 'y'},
	'E4': {'x': 'x', 'y': 'y'},
	'E5': {'x': 'x', 'y': 'y'},
	'E6': {'x': 'x', 'y': 'y'},
	'D':  {'x': 'x', 'y': 'y'},
	'D1': {'x': 'x', 'y': 'y'},
	'D2': {'x': 'x', 'y': 'y'},
	'D3': {'x': 'x', 'y': 'y'},
	'A': {'x': 'x', 'y': 'y'},
	'A1': {'x': 'x', 'y': 'y'},
	'A2': {'x': 'x', 'y': 'y'},
	'A3': {'x': 'x', 'y': 'y'},
	'C': {')':')'},
	'C1': {')':')'},
	'C2': {')':')'},
	'V': {'<':'<', '>':'>',')':')', ':=':':='},
	'O': {'x': 'x', 'y': 'y', 'a': 'a', 'b': 'b'},
	'T': {'<':'<', '>':'>',')':')', ';':';'}
	}
	list = follow[prev].keys() # if searched pattern is found 
	for o in options:
		for l in list:
			if o == l:
				return o
	return 'fail'
	
def parser(data):
	input = [i for i in re.split(r'(if|\(|\)|else|\{|\}|\<\>|x|y|a|b|:=|\;|\"\")', data ) if i] # capture all our input into tokens
	input.append('$')
	stack=['S','$']
	rules = { # Make Rules = {Rule -> FIRST ->NEXT STEP}
	'S': {'if': 'E S1', 'x': 'A S1', 'y':'A S1'},
	'S1': {'x': 'A S1', 'y': 'A S1', '':''},
	'E': {'if': 'if E1'},
	'E1': {'(': '( E2'},
	'E2': {'x': 'C E3', 'y': 'C E3', 'a':'C E3', 'b':'C E3'},
	'E3': {')': ') E4'},
	'E4': {'{': '{ E5'},
	'E5': {'if': 'S E6', 'x': 'S E6', 'y': 'S E6'},
	'E6': {'}': '} D'},
	'D': {'else': 'else D1','':''},
	'D1': {'{': '{ D2'},
	'D2': {'if':'S D3', 'x': 'S D3', 'y': 'S D3'},
	'D3': {'}': '}'},
	'A': {'x':'V A1', 'y':'V A1'},
	'A1': {':=':':= A2'},
	'A2': {'a': 'T A3', 'b': 'T A3'},
	'A3': {';': ';'},
	'C': {'x':'V C1', 'y': 'V C1', 'a':'T C1', 'b':'T C1'},
	'C1': {'<': 'O C2', '>':'O C2'},
	'C2': {'x': 'V', 'y': 'V', 'a':'T', 'b':'T'},
	'V': {'x': 'x', 'y': 'y'},
	'O': {'<': '<', '>': '>'},
	'T': {'a':'a', 'b':'b'}
	}
	prev = ''
	prevtoken = ''
	print ''.join(input) + ' ' + ''.join(stack)
	while len(input)!=1 or len(stack)!=1:
		error =0;
		rule = stack[0]	
		token = input[0]
		if (rule not in rules): # if illegitimate Variable is not in our Rules then the grammar is unaccepted
			print "REJECTED"
			print "expected a " + rule + ' instead of ' + token
			break
		if ('' in rules[rule].keys() and token not in rules[rule].keys()): # Check for Epsilon first before popping anything
			stack.pop(0)
		elif (token in rules[rule].keys()): # Check token path
			next = rules[rule].get(token).split() # Take the path split it into variables to be placed on stack
			next.reverse() # Reverse and Replace Variable on stack
			stack.pop(0)
			for i in next:
				stack.insert(0,i)
		elif (args.e): # error recovery part
			if (token == prevtoken): # duplicate token case
				input.pop(0)
				print "WARNING ERROR STOP WITH THE DUPLICATES "
			else: 
				print "WARNING ERROR FOUND WE EXPECTED " + rule # adds guesses the missing entries, not 100%
				options = rules[rule].keys()
				item = followcheck(prev, options)
				if (item != 'fail'):
					input.insert(0,item)
				else:
					print "WARNING ERROR WE COULD NOT FIX THE ERRORS" # failed to fix the errors
					print "REJECTED"
					break;
					
		else: # FAILING CASE WHEN -e is not active
			print "REJECTED" 
			print "expected a " + token + ' instead of ' + ' '.join(rules[rule].keys())
			break
		print ''.join(input) + ' ' + ''.join(stack)
		
		if (input[0] == stack[0] and input[0] != '$'): # IF terminals = each other pop stack and input
			input.pop(0)
			stack.pop(0)
			print ''.join(input) + ' ' + ''.join(stack)
			prevtoken = token
			prev = rule
	if (stack[0] == '$' and input[0]=='$'): # IF both are dollar sign print accepted
		print "ACCEPTED"
parser(data)
