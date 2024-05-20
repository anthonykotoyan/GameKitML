from GameKitML.neuralnetwork import NeuralNetwork as nn


# class to initialize training agents
class Training:
    def __init__(self, Agent, population_size):
        # class of the Agent
        self.nn = None
        self.Agent = Agent

        # number of agents in the training
        self.pop_size = population_size

    def initialize_nn(self, layers, mutation_rate, mutation_change, start_nn=False):
        self.nn = nn(layers)
        if not start_nn:
            self.nn.randomize()
        else:
            self.nn = nn.mutate(start_nn, mutation_rate, mutation_change)

    def run_agent(self, activation, nn_inputs, move):
        movement_inputs = self.nn.run(nn_inputs, activation)
        bool_movement_inputs = nn.convert_to_bool(movement_inputs)
        move(bool_movement_inputs)
