
from plotter import Plotter
from tensorboard_reader import TensorboardReader
import yaml
import os

class TensorboardPlotter:
    def __init__(self, name_map_file):
        self.reader = TensorboardReader()
        with open(os.path.dirname(__file__) + "/" + name_map_file, 'r') as stream:
            self.cfg = yaml.safe_load(stream)

        self.name_map = self.cfg['name_map']

    def plot_all(self, file):
        tags = self.reader.get_tag_names(file)

        if 'white_list' in self.cfg:
            tags = [tag for tag in tags if tag in self.cfg['white_list']]
        if 'black_list' in self.cfg:
            tags = [tag for tag in tags if tag not in self.cfg['black_list']]

        for tag in tags:
            
            raw, smoothed = self.reader.extract_from_file(file, tag)

            
            title = tag
            if tag in self.name_map:
                title = self.name_map[tag]
            
            p = Plotter(title)
            p.plot_smooth(smoothed)
            mi,ma = self.reader.calc_region(raw, 30)
            p.plot_region(mi, ma)

            print(f"Saving {tag} into {tag}.png")
            p.save(f"{tag}.png")