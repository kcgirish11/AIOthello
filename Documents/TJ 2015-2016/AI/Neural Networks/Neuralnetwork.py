import sys,math
import numpy as np

def sigmoid(x): return 1.0/(1.0+ np.exp(-x)  )

def dsigmoid(x): return sigmoid(x)*(1.0 -  sigmoid(x))

def forward(expected,inputs,ihw,how,i):
    hidden = []
    output = 0
    input = inputs[i]
    newputs =[0,0]
    for j in range(2): newputs[j] = sigmoid(input[0]*ihw[0][j] + input[1]*ihw[1][j] + input[2]*ihw[2][j])
    for j in range(len(how[0])):output = sigmoid(newputs[0]*how[0][j] + newputs[1]*how[1][j])
    return (newputs,output)

def backpropogation(expected,how,hidden_outputs,outputs,input):
    hidden_outputs = np.array(hidden_outputs)
    outputs = np.array(outputs)
    deltaj1 = []
    deltaj2 = []
    deltak = (outputs-expected[input])*outputs*(1-outputs)
    deltaj1.append(deltak*hidden_outputs[0]*(1-hidden_outputs[0])*how[0][0])
    deltaj2.append(deltak*hidden_outputs[1]*(1-hidden_outputs[1])*how[1][0])
    return [deltak,deltaj1,deltaj2]

def network():

    learningrate = 10.0
    num_input = 3 #number of input nodes +1
    num_hidden = 2 #number of hidden nodes
    num_output = 1 #number of output nodes
    inputs = np.array([[0,0,1],[1,0,1],[0,1,1],[1,1,1]])
    expected = np.array([0,1,1,0])
    ihw = 10*np.random.randn(num_input, num_hidden)
    how = 10*np.random.randn(num_hidden, num_output)
    error=1
    while error>.005:
        output= []
        for p in range(len(expected)):
            hiddenactive, outputs = forward(expected,inputs,ihw,how,p)
            output.append(outputs)
            deltas = backpropogation(expected,how,hiddenactive,outputs,p)

            for i in range(ihw.shape[0]):
                for j in range(ihw.shape[1]):
                    derivative = -1*learningrate*deltas[j+1][0]*inputs[p,i]
                    ihw[i,j]+=derivative

            for i in range(how.shape[0]):
                for j in range(how.shape[1]):
                    derivative = -1*learningrate*deltas[0]*hiddenactive[i]
                    how[i,j]+=derivative
        output = np.array(output)
        error = np.sum((output-expected)**2)
        print(error)
    print(ihw,how)
    print(output)
    print("End Error: "+str(error))

network()
