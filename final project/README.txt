PART I:
For the final project I went into the direction of Reinforcement learning.
As an entry point I figured the game 'Snake' to be approachable.
Following various examples on the internet I programmed an agent (largely based on existing code) that learns to play snake independendly.

I changed the agent in a way that the Bellman equation is not applied each time the model is called but rather after each episode, to directly backpropagate the rewards along time with the chosen Gamma.

I also added an increasing Gamma over time (starting at 0) as well as an decreasing reward (starting at 1) for distance to the apple. Both changes seemingly (not measured) sped up learning and lead to a better highscore more quickly.

I then added a bias for the mini-batch training which puts a strong emphasis on states just before game over, so that the importance of those states is represented in the training data (30/70 game over/normal game states).

PART II:
In part 2 I tried to apply Reinforcement Learning onto a renewable energy system. As a first step I set up a simulation of a solar-energy-system with battery-storage and validated it (made sure it works correctly).
In a subsequent step I set up an agent that would learn to optimize the battery-storage usage, depending on the time-variant electricity price.
That part did not work out in this stage. I think this is due to the high complexity of input values and one way of trying another approach would be to bin or binarize the input state (just like in Snake) and simplify the learning task.