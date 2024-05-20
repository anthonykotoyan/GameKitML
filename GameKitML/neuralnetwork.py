import random
import math
import copy


def sign(x):
    if x != 0:
        return abs(x) / x
    else:
        return 0


class NeuralNetwork:
    def __init__(self, layers):
        # Initialize the neural network with given layers
        self.layers = layers
        self.weights = []  # List to store weights for each layer
        self.biases = []  # List to store biases for each layer

    def randomize(self):
        # Randomly initialize weights and biases for the neural network
        weights = []
        biases = []
        for layer in range(len(self.layers) - 1):
            # For each layer pair, create weights matrix
            weightsInLayer = []
            for weight in range(self.layers[layer] * self.layers[layer + 1]):
                # Generate a random weight for each connection
                weightsInLayer.append(random.uniform(-1, 1))
            weights.append(weightsInLayer)

            # Generate biases only for hidden layers (not the output layer)
            biasesInLayer = []
            if layer != len(self.layers) - 1:
                for bias in range(self.layers[layer + 1]):
                    # Randomly assign biases between -1 and 1
                    biasesInLayer.append(random.uniform(-1, 1))
                biases.append(biasesInLayer)
        self.weights = copy.deepcopy(weights)
        self.biases = copy.deepcopy(biases)

    @staticmethod
    def mutate(nn, rate, change):
        # Mutate weights and biases based on a given mutation rate
        we = copy.deepcopy(nn.weights)
        ba = copy.deepcopy(nn.biases)
        parameters = [we, ba]
        for parameter in range(len(parameters)):
            for layer in range(len(parameters[parameter])):
                for value in range(len(parameters[parameter][layer])):
                    percent = random.random()

                    if percent < rate:
                        # Randomly change the value if the mutation rate allows
                        changeValue = random.uniform(-change, change)
                        paramValue = parameters[parameter][layer][value] + changeValue
                        if abs(paramValue) > 1:
                            parameters[parameter][layer][value] = sign(paramValue)

        return NeuralNetwork.copyNN([nn.layers, parameters[0], parameters[1]])

    @staticmethod
    def copyNN(nn):
        copiedNetwork = NeuralNetwork(nn[0])
        copiedNetwork.weights = nn[1]
        copiedNetwork.biases = nn[2]
        return copiedNetwork

    # Activation functions are provided as static methods for simplicity
    @staticmethod
    def Linear(value):
        return value

    @staticmethod
    def ReLU(value):
        return max(0, value)

    @staticmethod
    def LeakyReLU(value):
        return max(value * 0.05, value)

    @staticmethod
    def Sigmoid(value):
        # Sigmoid function to squash values between 0 and 1
        return 1 / (1 + (2.718 ** (-value)))

    @staticmethod
    def Tanh(value):
        # Hyperbolic tangent function to map values between -1 and 1
        return math.tanh(value)

    @staticmethod
    def Step(value):
        # either -1 or 1
        if value > 0:
            return 1
        else:
            return -1

    def run(self, inputs, activation):
        # current input layer being ran
        currentInput = inputs
        # Loops through all layers but output
        for layer in range(len(self.layers) - 1):
            # resetting calculated output list from last run (instantiating new output list if it is the first run)
            currentOutput = []
            # looping through the current output layer
            for output in range(self.layers[layer + 1]):
                # resetting calculated value for the output node (instantiating new output node list if it is the first run)
                nodeValue = 0
                # looping through the current input layer
                for input in range(self.layers[layer]):
                    # adding up all the node values per each input to the current output node
                    nodeValue += currentInput[input] * self.weights[layer][self.layers[layer + 1] * input + output]
                # appending the calculated sum of output node to the output layer to be used as input in the next run
                currentOutput.append(activation(nodeValue + self.biases[layer][output]))
            # setting the currentOutput to the next run's input
            currentInput = currentOutput
        # once all layers have been iterated through
        return currentInput

    @staticmethod
    def convert_to_bool(outputs):
        bool_outputs = []
        for output in outputs:
            if output > 0:
                bool_outputs.append(True)
            else:
                bool_outputs.append(False)
        return bool_outputs
