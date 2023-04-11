import TGame_new as TGame
import torch
import random
import pygame
import Color
from collections import deque
from model import Linear_QNet, QTrainer
from helper import plot

MAX_MEMORY = 100000000
BATCH_SIZE = 100000
LR = 0.002

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(200, 512, 4)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0,0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move

def train():
    n_games = 0
    record = 0
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0

    gamehigh = 500
    gamewidth = 300
    rcount = 20
    ccount = 10
    frame = 0
    zoom = 25

    rcount = 20
    ccount = 10

    agent = Agent()
    game = TGame.Tetris(rcount,ccount)


    pygame.init()
    screen = pygame.display.set_mode((gamewidth, gamehigh))
    pygame.display.set_caption("Tetris?")

    game = TGame.Tetris(rcount,ccount)
    game.create_block()
    while True:
        done = False
        ##Human Inputs------------------------------------------------
        #for event in pygame.event.get():
        #    if event.type == pygame.QUIT:
        #        done = True

        #    if event.type == pygame.KEYDOWN:
        #        if event.key == pygame.K_UP:
        #            game.turn_block()
        #        if event.key == pygame.K_DOWN:
        #            game.shift_down()
        #        if event.key == pygame.K_LEFT:
        #            game.shift_left()
        #        if event.key == pygame.K_RIGHT:
        #            game.shift_right()
        #    game.game_step();

        #AI Inputs
        state_old = []
        for row in game.get_view():
            for value in row:
                state_old.append(value)
        #state_old = game.get_view()

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        pygame.time.delay(50)
        reward, done, score = game.AI_step(final_move)
        state_new = []
        for row in game.get_view():
            for value in row:
                state_new.append(value)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            game.wipe()
            n_games += 1
            #agent.train_long_memory()

            if score > record:
                record = score

            print('Game', n_games, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

        #plot----------------------------------------------------
        screen.fill(color=Color.WHITE)
        for i in range(game.height):
            for j in range(game.width):
                pygame.draw.rect(screen, Color.clist[game.get_view()[i][j]], [j*zoom,i*zoom,zoom,zoom])
                pygame.draw.rect(screen, Color.DARKGRAY, [j*zoom,i*zoom,zoom,zoom],1)
        pygame.display.flip()
        frame += 1

if __name__ == '__main__':
    train()