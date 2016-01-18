import tensorflow as tf
import numpy as np
import math
import random

vectorSize = 300
hiddenLayers = 3
hiddenDimensions = [10, 5, 2]
outputDimensions = 2

inputDimensions = vectorSize * 3
activationFunction = "tanh"
costFunction = "crossEntropy"   #"RMSE"

#add inputDimensions as hiddenLayer[0]
hiddenDimensions.insert(0, inputDimensions)
#add outputDimensions as hiddenLayer[+1]
hiddenDimensions.append(outputDimensions)

#placeholders
input = tf.placeholder("float", name="Input", shape=[None, inputDimensions])
label = tf.placeholder("float", name="Label", shape=[None, outputDimensions])

#generate variables in loop
weights = {}
biases = {}

#confirmed correct code!
for i in range(len(hiddenDimensions) - 1):    #+1 to treat the output layer as a "hidden layer"
    weights["W{0}".format(i + 1)] = tf.Variable(tf.random_normal(
        [hiddenDimensions[i], hiddenDimensions[i + 1]],     #hidden[i] x hidden[i + 1]
        mean=0,
        stddev=math.sqrt(float(6) / float(hiddenDimensions[i] + hiddenDimensions[-1] + 1))),
        name="W" + str(i + 1)
    )
    biases["b{0}".format(i + 1)] = tf.Variable(tf.random_normal(
        [1, hiddenDimensions[i]],       #1 x hidden[0]
        mean=0,
        stddev=math.sqrt(float(6) / float(inputDimensions + outputDimensions + 1))),
        name="b" + str(i+1)
    )

#code to set up evaluation of variables
init_op = tf.initialize_all_variables()
sess = tf.Session()
sess.run(init_op)

for v in weights.keys():
    print(v + " has a shape of " + str(weights[v].eval(sess).shape))

for b in biases.keys():
    print(b + " has a shape of " + str(biases[b].eval(sess).shape))



    # #if into first hidden layer
    # if i == 0:      #input -> hidden[0]
    #     weights["W{0}".format(i + 1)] = tf.Variable(tf.random_normal(
    #             [inputDimensions, hiddenDimensions[0]],   #input x hidden[0]
    #             mean=0,
    #             stddev=math.sqrt(float(6) / float(inputDimensions + outputDimensions + 1))),
    #             name="W" + str(i+1))
    #
    #     biases["b{0}".format(i + 1)] = tf.Variable(tf.random_normal(
    #             [1, hiddenDimensions[0]],       #1 x hidden[0]
    #             mean=0,
    #             stddev=math.sqrt(float(6) / float(inputDimensions + outputDimensions + 1))),
    #             name="b" + str(i+1))
    # #if into output layer
    # elif i == hiddenLayers + 1:     #hidden[i-1] -> output
    #     weights["W{0}".format(i + 1)] = tf.Variable(tf.random_normal(
    #             [hiddenDimensions[i - 1], outputDimensions],    #hidden[last] x output
    #             mean=0,
    #             stddev=math.sqrt(float(6) / float(inputDimensions + outputDimensions + 1))),
    #             name="W" + str(i+1))
    #
    #     biases["b{0}".format(i + 1)] = tf.Variable(tf.random_normal(
    #             [1, outputDimensions],         #1 x output
    #             mean=0,
    #             stddev=math.sqrt(float(6) / float(inputDimensions + outputDimensions + 1))),
    #             name="b" + str(i+1))
    # #if into inside layer(s)
    # else:
    #     weights["W{0}".format(i + 1)] = tf.Variable(tf.random_normal(
    #             [hiddenDimensions[i - 1], hiddenDimensions[i]],    #hidden[i-1] x hidden[i]
    #             mean=0,
    #             stddev=math.sqrt(float(6) / float(inputDimensions + outputDimensions + 1))),
    #             name="W" + str(i+1))
    #
    #     biases["b{0}".format(i + 1)] = tf.Variable(tf.random_normal(
    #             [1, hiddenDimensions[i]],       #1 x hidden[i]
    #             mean=0,
    #             stddev=math.sqrt(float(6) / float(inputDimensions + outputDimensions + 1))),
    #             name="b" + str(i+1))