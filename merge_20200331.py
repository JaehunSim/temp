import pandas as pd

ncc1 = pd.DataFrame([[0.5, 0.4, 0.3, 0.2], [0.5, 0.3, 0.4, 0.5], [0.6, 0.7, 0.6, 0.8]],
                    index=["A", "B", "E"],
                    columns=[1, 2, 3, 4])

ncc2 = pd.DataFrame([[0.2, 0.5, 0.4, 0.6], [0.8, 0.9, 0.2, 0.1], [0.5, 0.7, 0.9, 0.4], [0.2, 0.1, 0.6, 0.9]],
                    index=["A", "B", "C", "D"],
                    columns=[5, 6, 7, 8])

data = pd.merge(ncc2, ncc1, how="outer", left_index=True, right_index=True)
