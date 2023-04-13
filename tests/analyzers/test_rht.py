import os
import pytest
import unittest
import pandas as pd
import pickle as pkl

from pyrca.analyzers.rht import RHT, RHTConfig


class TestRHT(unittest.TestCase):

    @pytest.mark.skip(reason="pickle issue")
    def test(self):
        directory = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(directory, "../data/estimated_dag.pkl"), "rb") as f:
            graph = pkl.load(f)
        path = os.path.join(directory, "../data/synthetic0.pkl")

        # load data and meta configuration
        with open(path, "rb") as input_file:
            data = pkl.load(input_file)

        # get normal and abnormal dataset in pd.DataFrame
        training_samples = data['data']['num_samples']
        tot_data = data['data']['data']

        names = [("X%d" % (i + 1)) for i in range(tot_data.shape[1])]
        normal_data = tot_data[:training_samples]
        normal_data_pd = pd.DataFrame(normal_data, columns=names)

        abnormal_data = tot_data[training_samples:]
        abnormal_data_pd = pd.DataFrame(abnormal_data, columns=names)

        model = RHT(config=RHTConfig(graph=graph))
        model.train(normal_data_pd)
        results = model.find_root_causes(abnormal_data_pd, 'X1', True).to_list()
        print(results)


if __name__ == "__main__":
    unittest.main()