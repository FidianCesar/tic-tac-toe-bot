# tic-tac-toe-bot

This bot learns to play Tic Tac Toe using Q-learning. It is able to almost perfectly defeat a random player after enough iterations, draw against a minimax player (playing a best move at random).

The last try is a static opponent whose Q table is updated after every episode, to match that of the dynamically changing one.
I have not been able to achieve desirable results: Even after tweaking the hyperparameters, I have not been able to achieve desirable results: The bot still looses to me after 30000 episodes, each consisting of 100 games played.

If you know how to fix this, feel free to read the code and tell me about anything you think can be improved. I will be very grateful to you!

Also, this is my first github repo, so any advice/criticism you could give me about it is welcome too! Thanks!
