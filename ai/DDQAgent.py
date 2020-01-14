import gym
import os, datetime, random
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras import backend as K
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Model, clone_model
from tensorflow.keras.layers import Dense, Input, Layer

class Utilities():
    def __init__(self):
        self.aggregate_episode_rewards = {
            'epoch': [],
            'cumulative': [],
            'average': [],
            'loss': [],
            'accuracy': []
            }

    def collect_data(self, epoch, rewards, loss, accuracy):
        self.aggregate_episode_rewards['epoch'].append(epoch)
        self.aggregate_episode_rewards['cumulative'].append(sum(rewards))
        self.aggregate_episode_rewards['average'].append(sum(rewards)/len(rewards))
        self.aggregate_episode_rewards['loss'].append(loss)
        self.aggregate_episode_rewards['accuracy'].append(accuracy)

    def show_plot(self, version):
        if version == 'cumulative':
          plt.plot(self.aggregate_episode_rewards['epoch'], \
            self.aggregate_episode_rewards['cumulative'], label="cumulative rewards")
        elif version == 'accuracy':
          plt.plot(self.aggregate_episode_rewards['epoch'], \
              self.aggregate_episode_rewards['accuracy'], label="accuracy")
        elif version == 'loss':
          plt.plot(self.aggregate_episode_rewards['epoch'], \
              self.aggregate_episode_rewards['loss'], label="loss")
        else:
            plt.plot(self.aggregate_episode_rewards['epoch'], \
              self.aggregate_episode_rewards['average'], label="average rewards")
        plt.legend(loc=4)
        plt.show()

    def format_time(self, seconds):
        if seconds < 400:
            s = float(seconds)
            return "%.1f seconds" % (s,)
        elif seconds < 4000:
            m = seconds / 60.0
            return "%.2f minutes" % (m,)
        else:
            h = seconds / 3600.0
            return "%.2f hours" % (h,)

class Aggregation(Layer):
    def __init__(self,**kwargs):
        super(Aggregation, self).__init__(**kwargs)

    def build(self, input_shape):
        assert isinstance(input_shape, list)
        super(Aggregation, self).build(input_shape)

    def call(self, x):
        assert isinstance(x, list)
        a, b = x
        return b + a - K.mean(a)

    def compute_output_shape(self, input_shape):
        assert isinstance(input_shape, list)
        shape_a, shape_b = input_shape
        return shape_a


class DDQAgent(Utilities):
    def __init__(self, env, **kwargs):
        self.env = env
        self.weights_file = kwargs.get('WEIGHTS_FILE', "")

        self.replay_batch_size = kwargs.get('REPLAY_BATCH_SIZE', 8)
        self.learning_batch_size = kwargs.get('LEARNING_BATCH_SIZE', 2)
        self.max_steps = kwargs.get('MAX_STEPS', 500)
        self.epsilon = kwargs.get('EPSILON_START', 0.98)
        self.epsilon_decay = kwargs.get('EPSILON_DECAY', 0.98)
        self.discount = kwargs.get('DISCOUNT', 0.99)
        self.replay_size = kwargs.get('REPLAY_MEMORY_SIZE', 1000)
        self.min_epsilon = kwargs.get('MIN_EPSILON', 0.01)
        self.learning_rate = kwargs.get('LEARING_RATE', 0.001)
        self.final_score = kwargs.get('FINAL_SCORE', 100)

        self.save_every_epoch = kwargs.get('SAVE_EVERY_EPOCH', False)
        self.save_every_step = kwargs.get('SAVE_EVERY_STEP', False)
        self.best_model_file = kwargs.get('BEST_MODEL_FILE', 'best_model')


        self.memory = list()

        if self.weights_file:
            self.build_model()
            self.model = self.model.load_weights(self.weights_file)
        
        super().__init__()

    def build_model(self, **kwargs):
        if not hasattr(self, 'model'):
            self.num_outputs = self.env.action_space.n
            self.num_features = self.env.observation_space.shape[0]
            self.num_layers = kwargs.get('num_layers', 3)
            self.default_nodes = kwargs.get('default_nodes', 20)
            self.nodes_per_layer = kwargs.get('nodes_per_layer', [])

            assert self.num_layers >= 1, 'Num of layers should be greater than or equal to one'

            inputs = Input(shape=(self.num_features,))
            
            try:
                nodes = self.nodes_per_layer[0]
            except IndexError:
                nodes = self.default_nodes
            action = Dense(nodes, activation='relu')(inputs)
            value = Dense(nodes, activation='relu')(inputs)
            
            for layer in range(1, self.num_layers):
                try:
                    nodes = self.nodes_per_layer[layer]
                except IndexError:
                    nodes = self.default_nodes
                action = Dense(nodes, activation='relu')(action)
                value = Dense(nodes, activation='relu')(value)
                
            action = Dense(self.num_outputs, activation='linear')(action)
            value = Dense(1, activation='linear')(value)
            outputs = Aggregation()([action, value])
            
            model = Model(inputs=inputs, outputs=outputs)
            
            model.compile(optimizer = Adam(lr=self.learning_rate),
                          loss = 'mse',
                          metrics=['accuracy'])
            model.summary()

            self.model = model
            
    def get_batch(self):
        batch_size = min(len(self.memory), self.replay_batch_size)
        batch = random.sample(self.memory, batch_size)
        inputs = np.zeros((batch_size, self.num_features))
        targets = np.zeros((batch_size, self.num_outputs))

        for i, val in enumerate(batch):
            envstate, action, reward, next_envstate, done = val
            adj_envstate = envstate.reshape(1,-1)
            adj_next_envstate = next_envstate.reshape(1,-1)
            
            inputs[i] = adj_envstate
            targets[i] = self.model.predict(adj_envstate)
            if done:
                targets[i,action] = reward
            else:
                best_action = self.predict(adj_next_envstate)
                Q_sa = self.model_target.predict(adj_next_envstate)[0][best_action]
                targets[i,action] = reward + self.discount * Q_sa

        return inputs, targets

    def predict(self, envstate):
        assert self.model, 'Model must be present to make prediction'
        if np.random.rand() < self.epsilon:
            action = random.choice(range(self.env.action_space.n))
        else:
            qvals = self.model.predict(envstate.reshape(1,-1))[0]
            action = np.argmax(qvals)
        return action

    def learn(self):
        inputs, targets = self.get_batch()

        history = self.model.fit(inputs,
                                 targets,
                                 batch_size = max(self.learning_batch_size, 1),
                                 verbose = 0,
                                 )

        loss,accuracy = self.model.evaluate(inputs, targets, verbose=0)

        return loss, accuracy

    def evaluate(self, n_epochs=1, render=False, verbose=True):
        start_time = datetime.datetime.now()
        print(f'Evaluating... Starting at: {start_time}')

        total_rewards = []

        for epoch in range(n_epochs):
            n_steps = 0
            done = False
            envstate = self.env.reset()
            rewards = []
            while (not done and n_steps < self.max_steps):
                prev_envstate = envstate
                q = self.model.predict(prev_envstate.reshape(1,-1))

                action = np.argmax(q[0])
                envstate, reward, done, info = self.env.step(action)

                n_steps += 1
                rewards.append(reward)
                if render:
                    self.env.render()

            if verbose:
                dt = datetime.datetime.now() - start_time
                t = self.format_time(dt.total_seconds())
                results = f'Epoch: {epoch}/{n_epochs-1} | ' + \
                          f'Steps {n_steps} | ' + \
                          f'Cumulative Reward: {sum(rewards)} | ' + \
                          f'Time: {t}'
                print(results)

            total_rewards.append(rewards)

        self.env.close()
        return total_rewards

    def train(self, n_epochs=15000, max_steps=0, render=False):
        self.start_time = datetime.datetime.now()
        print(f'Starting training at {self.start_time}')

        self.model_target = clone_model(self.model)
        max_steps = max_steps or self.max_steps
        for epoch in range(n_epochs):
            n_steps = 0
            done = False
            envstate = self.env.reset()
            self.model_target.set_weights(self.model.get_weights())
            rewards = []
            while (not done and n_steps < max_steps):
                prev_envstate = envstate
                action = self.predict(prev_envstate)

                envstate, reward, done, info = self.env.step(action)

                episode = [prev_envstate, action, reward, envstate, done]
                self.memory.append(episode)
                if len(self.memory) > self.replay_size:
                    del self.memory[0]

                loss, accuracy = self.learn()
                rewards.append(reward)
                n_steps += 1

                if self.save_every_step:
                    self.is_best(loss, rewards)

                if render:
                    self.env.render()

            dt = datetime.datetime.now() - self.start_time
            t = self.format_time(dt.total_seconds())
            results = f'Epoch: {epoch + 1}/{n_epochs} | ' +\
                f'Loss: %.4f | ' % loss +\
                f'Steps {n_steps} | ' +\
                f'Epsilon: %.3f | ' % self.epsilon +\
                f'Reward: %.3f | ' % sum(rewards) +\
                f'Time: {t}'
            print(results)

            if self.save_every_epoch:
                self.is_best(loss, rewards)

            self.epsilon = max(self.min_epsilon, self.epsilon_decay * self.epsilon)
            self.collect_data(epoch, rewards, loss, accuracy)

    def is_best(self, loss, rewards):
        if not hasattr(self, 'best_model'):
            self.best_model = {
                'weights' : self.model.get_weights(),
                'loss' : loss,
                'reward' : self.final_score
                }

        reward = sum(rewards)
        mod_info = None
        if reward > self.best_model['reward']:
            mod_info = {
                'weights' : self.model.get_weights(),
                'loss' : loss,
                'reward' : reward
                }
        elif reward == self.best_model['reward'] and loss < self.best_model['loss']:
            mod_info = {
                'weights' : self.model.get_weights(),
                'loss' : loss
                }

        if mod_info:
            self.best_model.update(mod_info)
            print('New best model reached: {', self.best_model['loss'], self.best_model['reward'], '}')
            self.model.save_weights(self.best_model_file, overwrite=True)

    def load_weights(self, filename):
        h5file = filename + '.h5'
        self.model.load_weights(h5file)
        print(f'Sucessfully loaded weights from: {h5file}')

    def save_weights(self, filename):
        assert self.model, 'Model must be present to save weights'
        h5file = filename + ".h5"
        self.model.save_weights(h5file, overwrite=True)
        print('Weights saved to:', h5file)
    
