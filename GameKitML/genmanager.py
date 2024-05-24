import time

from GameKitML.neuralnetwork import NeuralNetwork as nn


# class to initialize training agents
class Trainer:

    def __init__(self, Agent):

        # class of the Agent
        self.agents = []
        self.Agent = Agent

        # info user gives us (each has an assignation function)
        self.nn_info = None
        self.run_info = None
        self.gen_info = None

        # gen time
        self.start_time = time.time()
        self.gen_time = None



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

    # gen_time is the amount of time in seconds the generation will last
    # agent_death_variable_name is the name of the variable that shows if the Agent is dead or not
    def Set_Gen_Info(self, gen_time, agent_death_variable_name, reset_agent, score_variable_name):
        self.gen_time = gen_time
        self.gen_info = [agent_death_variable_name, reset_agent, score_variable_name]

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
            # self.gen_info[0] is the name of the agent_death variable the user provided
            is_dead = getattr(agent[0], self.gen_info[0], None)

            if is_dead:
                continue
            # this finds the variable name input_variable_name inside the Agent class and uses that as nn input
            nn_inputs = getattr(agent[0], self.run_info[2], None)

            # agent[1] would be the nn of the current looped over agent
            # nn_info[3] is the activation function used to get the outputs
            nn_outputs = agent[1].run(nn_inputs, self.nn_info[3])

            # convert nn outputs to the agent inputs
            agent_input = self.run_info[1](nn_outputs)

            # run the agent using the inputs
            self.run_info[0](agent[0], agent_input)

    # run the generation and restart if the gen time is passed
    def Run_Gen(self):
        if time.time() - self.start_time >= self.gen_time:
            self.start_time = time.time()
            self.Reset_Gen()
        else:

            self.Run_Agents()

    # loop through all the agents and reset them using the reset_agent func the user provided
    def Reset_Gen(self):
        print("hi")
        for agent in self.agents:
            # gen_info[1] is the reset_agent func the user provided
            self.gen_info[1](agent[0])

            # not added yet but here we will figure out the agent with the highest score and mutate his network and shit
            # self.gen_info[2] is the name of the agent_death variable the user provided
            score = getattr(agent[0], self.gen_info[2], None)
            
