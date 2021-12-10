from tensorflow.python.summary.summary_iterator import summary_iterator
import numpy as np

class TensorboardReader:
    def __init__(self):
        pass

    def get_tag_names(self, file):
        names = []
        for summary in summary_iterator(file):
            for item in summary.summary.value:
                if item.tag not in names:
                    names.append(item.tag)

        return names


    def extract_from_file(self, file, name):
        values = []
        for summary in summary_iterator(file):
            for item in summary.summary.value:
                if item.tag == name:
                    values.append(item.simple_value)

        a = np.array(values)
        return a, self.running_average_smoothing(a, 60)

    def running_average_smoothing(self, data, w):
        window = np.array([1]*w)/w
        d = np.zeros_like(data)
        for i in range(w, data.shape[0]):
            d[i] = (window * data[i-w:i]).sum()

        return d

    def calc_region(self, data, w):
        mins = np.zeros_like(data)
        maxs = np.zeros_like(data)


        for i in range(w, data.shape[0]):
            mins[i] = data[i-w:i].min()
            maxs[i] = data[i-w:i].max()

        return self.running_average_smoothing(mins, 40) , self.running_average_smoothing(maxs, 40)