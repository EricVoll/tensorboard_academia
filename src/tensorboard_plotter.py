
from matplotlib.cbook import index_of
from plotter import Plotter
from tensorboard_reader import TensorboardReader
import yaml
import matplotlib.pyplot as plt
import os

class TensorboardPlotter:
    def __init__(self, config_file):
        plt.rcParams['figure.figsize'] = (10,7)
        plt.rcParams['figure.subplot.hspace'] = 0.35
        plt.rcParams['figure.subplot.wspace'] = 0.22
        self.reader = TensorboardReader()
        with open(os.path.dirname(__file__) + "/" + config_file, 'r') as stream:
            self.cfg = yaml.safe_load(stream)
        with open(os.path.dirname(__file__) + "/cfg/name_map.yaml", 'r') as stream:
            self.name_map = yaml.safe_load(stream)['name_map']


        self.rows = self.cfg['plot']['subplot']['rows'] 
        self.cols = self.cfg['plot']['subplot']['cols'] 
        self.subplot = self.rows > 1 or self.cols > 1

    def plot(self, files):
        tags = []

        # find the set of tags that are included in all files
        for file in files:
            t = self.reader.get_tag_names(file)
            if tags == []:
                tags = t
            else:
                for tag in tags:
                    if tag not in tags:
                        tags.remove(tag)

        if 'white_list' in self.cfg:
            tags = [tag for tag in tags if tag in self.cfg['white_list']]
        if 'black_list' in self.cfg:
            tags = [tag for tag in tags if tag not in self.cfg['black_list']]

        colors = ['blue', 'orange']
        backgrounds = ['lightsteelblue', 'bisque']

        if self.subplot:
            p = Plotter(transparent= False, sub_plot = self.subplot, rows = self.rows, cols = self.cols)

        for tag in tags:
            raw = []
            smoothed = []
            for file in files:
                r, s = self.reader.extract_from_file(file, tag)
                raw.append(r)
                smoothed.append(s)

            
            title = tag
            if tag in self.name_map:
                title = self.name_map[tag]

            
            for i in range(len(raw)):
                p.plot_smooth(smoothed[i], colors[i], title=title)
                mi,ma = self.reader.calc_region(raw[i], 30)
                p.plot_region(mi, ma, backgrounds[i])

            if not self.subplot:
                p.save(f"{tag}_combined.png")
                p.clear()
            else:
                if not tag == tags[-1]:
                    p.advance_subplot()

        if self.subplot:
            p.legend(self.cfg['plot']['legend'])
            p.save(f"{self.cfg['plot']['title']}.png")