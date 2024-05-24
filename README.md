# GameKitML
Machine Learning / Artifical Intelegance library for python games.

Description:
- This library will allow users to train an AI agent to play their game
- The library will provide many items such as a Neural Network, Agent/Population Manager, and much more
- The user's program must have the following items in their game/program to garantee the sucsess of the AI's training
  - Controls: There needs to be some way for the AI to control a Agent (ai player) in your game using numerical or digital inputs
    - Ex: Inputs {w, a, s, d} in type boolean. Key Up = False, Key Down = True
  - AI Outputs -> Game Inputs: There needs to be a function that converts outputs produced by AI's Neural Network into inputs to the Agent's input to the controls
    - Ex: Network output = [0.23, -0.9, 0.49. -0.3] -> if output < 0: False // else: True -> Agent input = [True, False, True, False]
  - Goal/Reward: There needs a way for the AI to recive rewards for doing an action that would lead it to its goal, this then will be compared across other Agents to see how well the Ai proformed
    - Ex: checkpoints around a race track leading to the finish line. Each checkpoint gives the agent a reward
  - Inputs/Vision: There needs to some type of information given to the AI about its envoroment that would allow it to reach its goal
    - Ex: The distances of line rays going from the AI Agent to the walls of the eviroment (agent will be able to tell how far/close he is to the walls around him)
  - Agent Reset: When the a traning generation ends, there should be a function to reset the agent so the next generation can start
    - Ex: a function that when called, resets the agent's velocity, position, and direction
  - Agent Death: There needs to be a way for the library to know when an Agent dies, the user needs to decide when the agent dies (like when a car hits a track wall)
    - Ex: a boolean variable called AgentDeath for every agent, It is assigned to True if the agent died and is turned back to False when the Agent is reset
- The code for the Agent should idealy be inside of a class in order for the Library to be more compatatble with your code



Contributor: 
- If you wish to contribute dm me on discord: ( id = neuralnetwork. )
- The naming convention is snake case for vairbles (snake_case) and Upper snake case for functions and classes (Upper_Snake_Case)
- Please try not to deviate from the naming convetion
- BE AS SPECIFIC AS POSSIBLE when naming variables for readablity, dont worry about the names being long (no xx or yy shit connor)
- Even though it is difficult try to comment or add short descriptions of your changes in the actual code file
- Unless the commit is small, please discuss with the rest of the contributers before you commit 
- If you know other peoeple that want to help then let me know becuase we might need it if we want to scale
