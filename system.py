
import sys
likelihood = {}
transition = {} 

# OOV handling: test 1/1000th
# OOV handling: OOV[tag] = number of appearances of "tag" in OOV words/number of appearances of "tag" in training corpus
OOV = {}
TOTALS = {}
words = set()

if len(sys.argv) == 2:
    file_name = str(sys.argv[1])
else:
    file_name = "WSJ_23.words"


def train():
    in_file = open("WSJ_02-21.pos", "r")
    prev_line = "\n"

    for curr_line in in_file:
        # if previous line is empty, set prev_tag to "Begin_Sent"
        if prev_line != "\n":
            prev_tag = prev_line.rstrip("\n").split()[1]
        else:
            prev_tag = "Begin_Sent"

        # if current line
        if curr_line != "\n":
            # removing trailing characters
            line_string = curr_line.rstrip("\n").split()
            word, curr_tag = line_string[0], line_string[1]
        else:
            word = "Begin_Sent"
            curr_tag= "Begin_Sent"
            likelihood[curr_tag] = likelihood.get(curr_tag, {})
            likelihood[curr_tag][word] = likelihood[curr_tag].get(word, 0) + 1
            words.add(word)
            word = "End_Sent"
            curr_tag = "End_Sent"

        # likelihood population
        likelihood[curr_tag] = likelihood.get(curr_tag, {})
        likelihood[curr_tag][word] = likelihood[curr_tag].get(word, 0) + 1

        # transition population
        transition[prev_tag] = transition.get(prev_tag, {})
        transition[prev_tag][curr_tag] = transition[prev_tag].get(curr_tag, 0) + 1

        # set this line as prev line for next iteration of loop
        prev_line = curr_line

        # set of words population
        words.add(word)
        
    in_file.close()

    # caculating probabilities

    # likelihood probabilities
    for tag in likelihood:
        TOTALS[tag] = sum(likelihood[tag].values())
        for word in likelihood[tag]:
            # OOV handling
            if likelihood[tag][word] == 1:
                OOV[tag] = OOV.get(tag, 0) + 1
                OOV[tag] = OOV[tag]/TOTALS[tag]
            likelihood[tag][word] = likelihood[tag][word]/TOTALS[tag]

    # transition probabilities
    for tag in transition:
        for next_tag in transition[tag]:
            transition[tag][next_tag] = transition[tag][next_tag]/TOTALS[tag]
    

    # calling viterbi after training
    viterbi()


def viterbi():
    in_file = open(file_name, "r")
    out_file = open("output.pos", "w")

    arr = {}
    back = {}
    index = 0
    tags = []

    for word in in_file:
        word = word.rstrip("\n")

        index += 1

        # record tag with maximum likelihood and previous tag with curr_viterbi
        maxTag=""
        maxLikelihood=0.0
        maxPrevTag=""
        maxPrevLikelihood=0.0
        noPath = True

        if word != "":
            for tag, word_prob in likelihood.items(): # word_prob contains prob dict for each tag 

                # handling OOVs
                if word not in words:
                    if (tag!= "Begin_Sent") & (tag!="End_Sent"):
                        if word in OOV:
                            word_prob[word] = OOV[tag] # handling OOV with custom method
                        else:
                            word_prob[word] = word_prob.get(word, 1/1000) # default 1/1000th probability method from slides   

                if index == 1:    # if word after Begin_Sent, viterbi = 1*tran*likelihood
                    arr[index] = arr.get(index, {})
                    back[index] = back.get(index, {})
                    arr[index][tag] = transition["Begin_Sent"].get(tag, 0) * word_prob.get(word, 0)
                    back[index][tag] = "Begin_Sent"

                else:    # viterbi = prev_viterbi*tran*likelihood
                    arr[index] = arr.get(index, {})
                    back[index] = back.get(index, {})
                    arr[index][tag] = 0    # initialize viterbi
                                
                    curr_viterbi = word_prob.get(word, 0) 
                    if curr_viterbi>maxLikelihood:
                        maxTag=tag
                        maxLikelihood = curr_viterbi

                    for prev_tag, prev_prob in arr[index-1].items():
                        
                        if prev_prob != 0:
                            if prev_prob > maxPrevLikelihood:
                                maxPrevTag = prev_tag
                                maxPrevLikelihood = prev_prob
                            
                            curr_viterbi = word_prob.get(word, 0)
                            curr_viterbi *= transition[prev_tag].get(tag, 0)
                            curr_viterbi *= arr[index-1][prev_tag]
                            
                            if curr_viterbi > arr[index][tag]:    # choose only max viterbi probability
                                arr[index][tag] = curr_viterbi
                                back[index][tag] = prev_tag    # point back in output
                                noPath =False

            if noPath:    # manually set arr and backpointer for noPath word
                arr[index][maxTag]=maxLikelihood
                back[index][maxTag]=maxPrevTag
        else:
            arr[index] = arr.get(index, {})
            arr[index]["End_Sent"] = 0    # Ending of a sentence
            back[index] = back.get(index, {})
            curr_viterbi = 1    # highly likely
            for prev_tag, prev_prob in arr[index-1].items():
                if prev_prob != 0:
                    curr_viterbi *= transition[prev_tag].get("End_Sent", 0)
                    curr_viterbi *= arr[index-1][prev_tag]
                    if curr_viterbi > arr[index]["End_Sent"]:    # update arr[index]["End_Sent"] to get max viterbi
                        arr[index]["End_Sent"] = curr_viterbi
                        back[index]["End_Sent"] = prev_tag    # point back to prev_tag for output

            # POS tagging tokens in sentence
            states = ["End_Sent"]
            state = "End_Sent" #from the ending backwards, reverse list later
            for n in range(index, 0, -1):
                # print(n)
                state = back[n][state]
                states.append(state)
                #index -= 1
            
            # print(states)
            # print(states.reverse())
            states.reverse()

            # final output list
            for tag in states: 
                if tag == "Begin_Sent":
                    continue
                else:
                    if tag == "End_Sent":
                        tag = "\n"
                    tags.append(tag)

            arr = {}
            back = {}
            index = 0
    

    in_file.close()

    in_file = open(file_name, "r")

    file_list = []

    # output to file
    count = 0
    for line in in_file:
        if line != "\n":
            line = "\t".join([line.rstrip("\n"), tags[count]])
            file_list.append(line + "\n")
        else:
            file_list.append("\n")
        count += 1

    out_file.writelines(file_list)
    

    in_file.close()
    out_file.close()

train()