import numpy as np
import cmath
import math
import matplotlib.pyplot as plt 

def despreader(Tss_, gold, M=1): 
    #Input: Spread spectrum sequence, gold sequence, value of M
    #Output: Despread list of recieved symbols
    
    #Function first multiplies input by the gold sequence to remove it
    #Followed by averaging every M symbols and appending to symbols
    symbols = []
    
    for i in range(len(Tss_)):
        Tss_[i] = Tss_[i] * gold[i%len(gold)]
        
    while len(Tss_) != 0:
        symbol = sum(Tss_[:M])/M
        symbols.append(symbol)
        Tss_ = Tss_[M:]
    return symbols

def channel(T, SNRin = None, jammer = None):
    #Input: list of symbols, noise SNRin, jamming signal
    #Output: list of symbols
    
    #If noise is to be added, linear ratio of noise is calculated then noise added to each sampl
    #If a jammer is present, the jamming message is summed to each of the samples
    if SNRin is not None:
        Ps = signalPower(T)
        SNRlin = 10**(SNRin/10)
        Pn = Ps/SNRlin
        T = [t + complex(np.random.normal(scale = math.sqrt(Pn)), np.random.normal(scale = math.sqrt(Pn))) for t in T]
    
    if jammer is not None:
        T = [t+i for t, i in list(zip(T, jammer))]
    return T

def signalPower(T):
    summation = 0
    for i in T:
        summation += (abs(i))**2
    return summation/len(T)

def errorCount(Rx, Tx, percent = False):
    #Input: Two recieved messages (in text format), value of whether to return as a percent or a proportion
    #Output: either proportion or percentage
    
    #Formats messages into binary and joins them into a single string
    #Then iterates through each value and counts how often 2 messages don't match
    Rx = ''.join(sourceEncoder(Rx))
    Tx = ''.join(sourceEncoder(Tx))
    errorCount = 0
    for r, t in list(zip(Rx, Tx)):
        if r != t:
            errorCount += 1
    if percent:
        return errorCount / len(Rx)
    else:
        return errorCount

def spreader(T, gold, M = 1):
    #Input: Message, gold sequence, value of M
    #Output: Spread message
    
    #Extends signal by factor M (ie, M repititions of each sample)
    #Multiplies by gold sequence
    output = np.repeat(T, M)
    for i in range(len(output)):
        output[i] = output[i] * gold[i%len(gold)]
    
    return output  

def generateGold(polynomials, offset=0):
    #Input: tuple of 2 polynomials, offset to be used
    #Output: gold sequence
    PN1 = PN(polynomials[0])
    PN2 = PN(polynomials[1])
    delayedSequence = PN2[-offset:] + PN2[0:-offset]
    gold = [1-2*((i + j)%2) for i, j in list(zip(PN1, delayedSequence))]    
    return gold

def isbalanced(polynomials, offset):
    gold = generateGold(polynomials, offset)
    track1=0
    trackneg1=0
    for i in gold:
        if i == 1:
            track1+=1
        else:
            trackneg1+=1
    if track1 == trackneg1-1:
        print('Balanced')
    else:
        print('Unbalanced')
        print(track1)
        print(trackneg1)

def PN(polynomial): 
    #Input: single polynomial list
    #Output: PN sequence
    
    #creates up an initial setting of all 1s in LFSR, repeats updates until state is again equal to initial value
    PN = [1]  
    initial = [1] * max(polynomial) 
    state = [1] * max(polynomial) 
    polynomial = polynomial[1:] 
    polynomial = [i + 1 for i in polynomial] 

    while True:
        new = state[-1]
        for i in polynomial:
            new += state[-i]
        new = new % 2
        state.insert(0, new)
        state.pop(-1)
        if state == initial: break
        PN.append(state[-1])
        
    return PN

def sourceDecoder(B_):
    #Input: list of binary symbols
    #Output: message string
    charactersBinary = [''.join([a,b,c,d]) for a, b, c, d in list(zip(B_[0::4], B_[1::4], B_[2::4], B_[3::4], ))]
    characters = [chr(int(character, 2)) for character in charactersBinary]
    
    return ''.join(characters)
    
def digitalDemodulator(T_):
    #Input: list of symbols
    #Output: list of binary symbols
    
    #maps symbols to binary values by checking the phase and comparing 
    B_ = []
    for t in T_:
        p = cmath.phase(t)
        if p <= math.radians(88) and p > math.radians(-2):
            B_.append('00')
        elif p <= math.radians(-2) and p > math.radians(-92):
            B_.append('10')
        elif p <= math.radians(178) and p > math.radians(88):
            B_.append('01')
        elif (p <= math.radians(180) and p > math.radians(178)) or (p <= math.radians(-92) and p >= math.radians(-180)):
            B_.append('11')
    return B_
    
def digitalModulator(B, phi = cmath.pi/4, relativePower = 1):
    T = []
    symbols = {"00":cmath.rect(math.sqrt(2*relativePower), phi), 
               "01":cmath.rect(math.sqrt(2*relativePower), phi + cmath.pi/2),
               "11":cmath.rect(math.sqrt(2*relativePower), phi + cmath.pi),
               "10":cmath.rect(math.sqrt(2*relativePower), phi + (3*cmath.pi)/2)
               }
    for i in B:
        T.append(symbols[i[0:2]])
        T.append(symbols[i[2:4]])
        T.append(symbols[i[4:6]])
        T.append(symbols[i[6:8]])
    return(T)
        

def sourceEncoder(message):
    #Creates a list of 8 digit binary characters for the message returns as a list of strings
    integers = [ord(character) for character in message]
    return ['{0:08b}'.format(integer) for integer in integers]

def plotConstellation(symbols, save):
    t_real = [i.real for i in symbols]
    t_imag = [i.imag for i in symbols]
    plt.scatter(t_real, t_imag)
    plt.xlabel('Re')
    plt.ylabel('Im')
    plt.show()
    if save is not False:
        plt.savefig(save)

def run(M=None, SNR=None, SNRj=None, plot = False, save=False):
    B = sourceEncoder(A)
    T = digitalModulator(B, phi)
    
    jammer = None
    if SNRj != None:
        SNRjlin = 10**(SNRj/10)
        encodedInterference = sourceEncoder(interference)
        modulatedInterference = digitalModulator(encodedInterference, relativePower = SNRjlin)
        
        if M != None:
            goldJ = generateGold(polynomialsJ, offset)
            jammer = spreader(modulatedInterference, goldJ, M = M)
        else:
            jammer = modulatedInterference
    
    
    if M != None:
        gold = generateGold(polynomials, offset)
        
        Tss = spreader(T, gold, M = M)
        
        Tss_ = channel(Tss, SNRin = SNR, jammer = jammer)
        
        T_ = despreader(Tss_, gold, M = M)
    else:
        T_ = channel(T, SNRin = SNR, jammer = jammer)
        
    
    B_ = digitalDemodulator(T_)
    
    A_ = sourceDecoder(B_)
        
    if plot:
        print(A_ + '\n')
        print(str( errorCount(A_, A, percent=True) * 100) + "%")
        plotConstellation(T_, save)

    bitErrorCount = errorCount(A_, A)
    return bitErrorCount
        


#Setup
A = str(open("../message.txt","r").read())
interference = str(open("../noise.txt", "r").read())
#phi = alphabetical order of 1st letter of surname + 2x alphabetical order of 1st letter of surname
#phi = 5 + 2(19) = 43
phi = math.radians(43) #in radians

PN1 = [5,2]
PN2 = [5,3,2,1]
polynomials = (PN1, PN2)
offset = 24

PN1J = [5,3]
PN2J = [5,4,2,1]
polynomialsJ = (PN1J, PN2J)

print('Press Enter to run each task. Each task will print the recieved signal, the error percentage, and the constellation diagram at point T^.')

# Task 1
input()
print('Task 1')
run(plot = True)


# Task 2
input()
print('Task 2')
run(SNR = 30, plot = True)


# Task 3
input()
print('Task 3')
run(SNR =  20, plot = True)


# Task 4
input()
print('Task 4')
run(SNR = 0, plot = True)


# Task 6
input()
print('Task 6')
run(SNR = 30, SNRj = 10, plot = True)


# Task 7
input()
print('Task 7')
#run(SNR = 30, SNRj = 10, M = 24, plot = True)
run(SNR = 30, SNRj = 10, M = 30, plot = True)
#run(SNR = 30, SNRj = 10, M = 5, plot = True)

