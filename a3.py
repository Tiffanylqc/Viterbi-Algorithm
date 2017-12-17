import random
import math

#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
num_hours_i_spent_on_this_assignment = 5
#####################################################
#####################################################

#####################################################
#####################################################
# Give one short piece of feedback about the course so far. What
# have you found most interesting? Is there a topic that you had trouble
# understanding? Are there any changes that could improve the value of the
# course to you? (We will anonymize these before reading them.)
# I want more proctice about what we will be tested in the exams
#####################################################
#####################################################



# Outputs a random integer, according to a multinomial
# distribution specified by probs.
def rand_multinomial(probs):
    # Make sure probs sum to 1
    assert(abs(sum(probs) - 1.0) < 1e-5)
    rand = random.random()
    for index, prob in enumerate(probs):
        if rand < prob:
            return index
        else:
            rand -= prob
    return 0

# Outputs a random key, according to a (key,prob)
# iterator. For a probability dictionary
# d = {"A": 0.9, "C": 0.1}
# call using rand_multinomial_iter(d.items())
def rand_multinomial_iter(iterator):
    rand = random.random()
    for key, prob in iterator:
        if rand < prob:
            return key
        else:
            rand -= prob
    return 0

class HMM():

    def __init__(self):
        self.num_states = 2
        self.prior = [0.5, 0.5]
        self.transition = [[0.999, 0.001], [0.01, 0.99]]
        self.emission = [{"A": 0.291, "T": 0.291, "C": 0.209, "G": 0.209},
                         {"A": 0.169, "T": 0.169, "C": 0.331, "G": 0.331}]

    # Generates a sequence of states and characters from
    # the HMM model.
    # - length: Length of output sequence
    def sample(self, length):
        sequence = []
        states = []
        rand = random.random()
        cur_state = rand_multinomial(self.prior)
        for i in range(length):
            states.append(cur_state)
            char = rand_multinomial_iter(self.emission[cur_state].items())
            sequence.append(char)
            cur_state = rand_multinomial(self.transition[cur_state])
        return sequence, states

    # Generates a emission sequence given a sequence of states
    def generate_sequence(self, states):
        sequence = []
        for state in states:
            char = rand_multinomial_iter(self.emission[state].items())
            sequence.append(char)
        return sequence

    # Outputs the most likely sequence of states given an emission sequence
    # - sequence: String with characters [A,C,T,G]
    # return: list of state indices, e.g. [0,0,0,1,1,0,0,...]
    def viterbi(self, sequence):
        ###########################################
        # Start your code
        length=len(sequence)

        # define probs and prev 2D array for dynamic programming
        # probs[s][i] means the probability to transfrom from prev state to state s at position i
        probs=[[0 for i in range(length)] for j in range(2)]
        prev=[[0 for i in range(length)] for j in range(2)]
        prev[0][0]=-1
        prev[1][0]=-1

        # precalculate the first column in probs using prior
        if(sequence[0]=='A'or sequence[0]=='T'):
            probs[0][0]=math.log(self.prior[0])+math.log(self.emission[0]["A"])
            probs[1][0] = math.log(self.prior[1]) + math.log(self.emission[1]["A"])
        else:
            probs[0][0] = math.log(self.prior[0]) + math.log(self.emission[0]["C"])
            probs[1][0] = math.log(self.prior[1]) + math.log(self.emission[1]["C"])

        # calculate probs and prev position by posistion
        for pos in range(1,length):
            for state in range(2):
                if sequence[pos] == 'A' or sequence[pos] == 'T':
                    prevstate0prob=math.log(self.emission[state]["A"])+math.log(self.transition[0][state])+probs[0][pos-1]
                    prevstate1prob=math.log(self.emission[state]["A"])+math.log(self.transition[1][state])+probs[1][pos-1]

                    if(prevstate0prob>prevstate1prob):
                        probs[state][pos]=prevstate0prob
                        prev[state][pos]=0
                    else:
                        probs[state][pos]=prevstate1prob
                        prev[state][pos]=1

                else:
                    prevstate0prob = math.log(self.emission[state]["C"]) + math.log(self.transition[0][state]) + probs[0][pos - 1]
                    prevstate1prob = math.log(self.emission[state]["C"]) + math.log(self.transition[1][state]) + probs[1][pos - 1]

                    if (prevstate0prob > prevstate1prob):
                        probs[state][pos] = prevstate0prob
                        prev[state][pos] = 0
                    else:
                        probs[state][pos] = prevstate1prob
                        prev[state][pos] = 1

        # go through probs and prev from back to front to store states
        states=[]
        logprob=0
        if probs[0][length-1]>probs[1][length-1]:
            states.append(0)
            logprob=probs[0][length-1]
        else:
            states.append(1)
            logprob = probs[1][length - 1]

        for i in range(length-1,0,-1):
            prestate=states[-1]
            states.append(prev[prestate][i])

        states=states[::-1]

        return [logprob,states]

        # End your code
        ###########################################

def read_sequence(filename):
    with open(filename, "r") as f:
        return f.read().strip()

def write_sequence(filename, sequence):
    with open(filename, "w") as f:
        f.write("".join(sequence))

def write_output(filename, logprob, states):
    with open(filename, "w") as f:
        f.write(str(logprob))
        f.write("\n")
        for state in range(2):
            f.write(str(states.count(state)))
            f.write("\n")
        f.write("".join(map(str, states)))
        f.write("\n")

hmm = HMM()

# sequence = read_sequence("small.txt")
#
# [logprob,viterbi ]= hmm.viterbi(sequence)
# write_output("my_small_output.txt", logprob, viterbi)


sequence = read_sequence("ecoli.txt")
[logprob,viterbi ]= hmm.viterbi(sequence)
write_output("ecoli_output.txt", logprob, viterbi)


