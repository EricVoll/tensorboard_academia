import matplotlib.pyplot as plt
import numpy as np
import os

class Plotter:
    def __init__(self, title):
        plt.figure().clear()
        plt.close()
        plt.cla()
        plt.clf()
        plt.title(title)

    def plot_raw(self, data):
        plt.plot(data, 'lightgray')

    def plot_smooth(self, data):
        plt.plot(data, 'black')

    def plot_region(self, mins, maxs):
        plt.fill_between(np.arange(0, mins.shape[0]), mins, maxs, color='lightgray')

    def save(self, path):
        img_path = os.path.join(os.path.dirname(__file__), 'output', path)
        img_dir = os.path.dirname(img_path)
        if not os.path.isdir(img_dir):
            os.mkdir(os.path.dirname(img_path))
        plt.savefig(img_path, format = 'png', transparent = True)

    def show(self):
        plt.show()