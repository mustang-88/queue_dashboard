import pandas as pd
from adherence import adherence
from user_prod import acd


results = pd.concat([acd, adherence]).groupby(by='userid', as_index=False)




results = results.reset_index(level=0)
results = results.reset_index(level=0)