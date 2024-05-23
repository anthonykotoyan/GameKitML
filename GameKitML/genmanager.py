from GameKitML.neuralnetwork import NeuralNetwork as nn


# class to initialize training agents
class Trainer:

    def __init__(self, Agent):
        # class of the Agent
        self.Agent = Agent
        self.agents = []
        self.nn_info = None
        self.run_info = None

    # nn_Info creates the params/info for the nn class
    # layer is a list describing the size of the nn
    # mutation_rate, mutation_change are params that describe how the nn will mutate
    # activation_name is the name of the activation function the user wants to use
    # start_nn param is the nn the Agent starts training with, it is set to None as default
    def Set_NN_Info(self, layers, mutation_rate, mutation_change, activation_name, start_nn=None):
        activation = getattr(nn(layers), activation_name)
        self.nn_info = [layers, mutation_rate, mutation_change, activation, start_nn]

    # output_input_converter is a function that the user makes that converts nn output to player input
    # run_func is the code that moves the agent in the game
    # input_variable_name is the name of the variable that contains what the nn would see
    def Set_Run_Info(self, run_func, output_input_converter, input_variable_name):
        self.run_info = [run_func, output_input_converter, input_variable_name]

    # There is a class called NeuralNetwork which we imported as "nn"
    # The nn class contains the code to run and store the neural network for an individual Agent
    # Initialize_nn creates a new nn object using nn_info
    # the new initialized nn is returned to be assigned to the Agents
    def Initialize_NN(self):
        # self.nn_info[0] is the layer list
        NN = nn(self.nn_info[0])

        # self.nn_info[4] is the starting nn, if None that means start from random
        if self.nn_info[4] is None:
            NN.randomize()
        else:

            NN = NN.mutate(self.nn_info[4], self.nn_info[1],
                           self.nn_info[2])  # nn_info 1, 2 are mutation_rate, mutation_change
        return NN

    # loops through pop_size which is the number of Agents in the training
    # per loop, it creates a new agent using self.Agent and creates a new nn for the agent
    # each agent is stored then as a list like this (agent_object, agent_nn) in self.agents
    # *args and **kwargs allows passing a variable parameter into Agent
    def Initialize_Agents(self, pop_size, *args, **kwargs):
        for i in range(pop_size):
            agent_object = self.Agent(*args, **kwargs)
            agent_nn = self.Initialize_NN()
            self.agents.append([agent_object, agent_nn])

   # runs all the agents using the nn_info and the run_info
    def Run_Agents(self):
        for agent in self.agents:
            # this finds the variable name input_variable_name inside the Agent class and uses that as nn input
            nn_inputs = getattr(agent[0], self.run_info[2], None)

            # agent[1] would be the nn of the current looped over agent
            # nn_info[3] is the activation function used to get the outputs

            nn_outputs = agent[1].run(nn_inputs, self.nn_info[3])

            # convert nn outputs to the agent inputs
            agent_input = self.run_info[1](nn_outputs)

            # run the agent using the inputs
            self.run_info[0](agent[0], agent_input)
