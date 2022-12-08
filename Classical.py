# ELEN4022 - Project - Group 01
# 09/05/2022
# Jesse Van Der Merwe (1829172)
# Keri-Lee Carstens (1384538)
# Tshegofatso Kale (1600916)

# - - - - - - - - - - IMPORTS - - - - - - - - - - #
from matplotlib import pyplot as plt
import random
import numpy as np
import pandas as pd

# - - - - - - - - - - CLASSICAL CLASS - - - - - - - - - - #
class Classical:
    def __init__(self, dp_1, dp_2, ns):
        self.num_simulations = ns
        self.data = pd.DataFrame({'k_value':[1,2], 'default_probability':[dp_1, dp_2]})
        self.losses = self.loss_computation()
        self.values, self.probs = self.get_probabilities()

    def set_data(self, dp_1, dp_2):
        self.data = pd.DataFrame({'k_value':[1,2], 'default_probability':[dp_1, dp_2]})

    def loss_computation(self):
        losses = []
        for n in range(0, self.num_simulations):
            loss = 0
            for i in range(0, self.data.shape[0]): # data.shape[0] returns the number of rows for column 0 (excluding header row)
                if self.data['default_probability'][i] > random.random():
                    loss = loss + self.data['k_value'][i]
            losses.append(loss)
        return losses

    def get_probabilities(self):
        values = []
        probs = []
        values.append(self.losses[0])
        for l in self.losses:
            if l not in values:
                values.append(l)

        values.sort()
        for k in values:
            probs.append(0)

        for i in self.losses:
            for k in values:
                if i == k:
                    probs[k] = probs[k] + 1
        
        for p in range(0, len(probs)):
            probs[p] = probs[p]/self.num_simulations

        return values, probs    

    def plot_expected_loss(self):
        self.losses = self.loss_computation()
        self.values, self.probs = self.probabilities()
        plt.figure()
        plt.bar(self.values, self.probs)
        plt.xlabel("Loss", size=15)
        plt.ylabel("Probability (%)", size=15)
        plt.title("Loss Distribution", size=20)
        plt.xticks(size=15)
        plt.yticks(size=15)
        return plt

    # Expected Loss (EL) = Probability of Default (PD) x Loss Given Default (LGD) x Exposure at Default (EAD) 
    def get_total_expected_loss(self):
        self.losses = self.loss_computation()
        self.values, self.probs = self.get_probabilities()
        return np.dot(self.values, self.probs)