import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib

class Plotter:
    def __init__(self, transparent = True, sub_plot = False, rows = 1, cols = 1):
        self.transparent = transparent

        self.subplot = sub_plot
        if sub_plot:
            self.rows = rows
            self.cols = cols
            self.fig, self.ax = plt.subplots(self.rows, self.cols)
            self.current_subplot_index = 0
        else:
            self.fig, self.ax = plt.subplot(1,1)

    def clear(self):
        plt.figure().clear()
        plt.close()
        plt.cla()
        plt.clf()

    def get_ax(self):
        if self.subplot:
            row, col = int(self.current_subplot_index / self.rows), self.current_subplot_index % self.cols
            return self.ax[row,col]
        else:
            return self.ax

    def plot_raw(self, data, color = 'lightgray', title = ''):
        self.get_ax().plot(data, color)
        self.set_title(title)

    def plot_smooth(self, data, color = 'black', title = ''):
        self.get_ax().plot(data, color)
        self.set_title(title)

    def plot_region(self, mins, maxs, color = 'lightgray', title = ''):
        c = matplotlib.colors.to_rgba(color, alpha = 0.3)
        self.get_ax().fill_between(np.arange(0, mins.shape[0]), mins, maxs, color=c)
        self.set_title(title)

    def set_title(self, title):
        if title != '':
            self.get_ax().title.set_text(title)

    def advance_subplot(self):
        self.current_subplot_index += 1

    def legend(self, items):
        handles = self.get_ax().get_lines()
        plt.gcf().legend(handles, items, loc='upper center')

    def save(self, path):
        img_path = os.path.join(os.path.dirname(__file__), 'output', path)
        img_dir = os.path.dirname(img_path)
        if not os.path.isdir(img_dir):
            os.mkdir(os.path.dirname(img_path))
        plt.savefig(img_path, format = 'png', transparent = self.transparent)

    def show(self):
        plt.show()