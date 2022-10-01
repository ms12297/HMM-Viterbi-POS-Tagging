import sys
import os

def score (keyFileName, responseFileName):
	keyFile = open(keyFileName, 'r')
	key = keyFile.readlines()
	responseFile = open(responseFileName, 'r')
	response = responseFile.readlines()
	if len(key) != len(response):
		print("length mismatch between key and submitted file")
		exit()
	correct = 0
	incorrect = 0
	for i in range(len(key)):
		key[i] = key[i].rstrip(os.linesep)
		response[i] = response[i].rstrip(os.linesep)
		if key[i] == "":
			if response[i] == "":
				continue
			else:
				print ("sentence break expected at line " + str(i))
				exit()
		keyFields = key[i].split('\t')
		if len(keyFields) != 2:
			print ("format error in key at line " + str(i) + ":" + key[i])
			exit()
		keyToken = keyFields[0]
		keyPos = keyFields[1]
		responseFields = response[i].split('\t')
		if len(responseFields) != 2:
			print ("format error at line " + str(i))
			exit()
		responseToken = responseFields[0]
		responsePos = responseFields[1]
		if responseToken != keyToken:
			print ("token mismatch at line " + str(i))
			exit()
		if responsePos == keyPos:
			correct = correct + 1
		else:
			incorrect = incorrect + 1
	print (str(correct) + " out of " + str(correct + incorrect) + " tags correct")
	accuracy = 100.0 * correct / (correct + incorrect)
	print("  accuracy: %f" % accuracy)

def main(args):
	key_file = args[1]
	response_file = args[2]
	score(key_file,response_file)

if __name__ == '__main__': sys.exit(main(sys.argv))
