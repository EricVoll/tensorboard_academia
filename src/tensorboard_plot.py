
import argparse
from tensorboard_plotter import TensorboardPlotter

        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("--file", type=str, help="Path to the tensorboard logfile")
    parser.add_argument("--cfg", type=str, help="Path to the config file")
    args = parser.parse_args()
    p = TensorboardPlotter(args.cfg)
    p.plot_all(args.file)