import pandas as pd

w = pd.DataFrame(["a", "b", "b", "c"], columns=["tag"])
tag_data = pd.DataFrame(w["tag"].unique(), columns=["tag"])
tag_data["id"] = tag_data.index + 1
merged = pd.merge(w, tag_data, how="outer")
