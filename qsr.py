import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations as c
from plotly.offline import init_notebook_mode, iplot
from plotly.graph_objs import*
import plotly.graph_objects as go
import plotly
import dash
#import chart_studio.tools as tls
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from flask import Flask, render_template


df = pd.read_csv(r"C:/Users/John/Desktop/db3/Queue Summary Report_Table1.csv")

df = df.groupby(by = "DisplaycName", as_index= True).sum()
df["acw"] = df["tAcw"] / df["nAnsweredAcd"]
df["aht"]= df["tHandle"] / df["nAnsweredAcd"]

que_sum = df[['nEnteredAcd','nAnsweredAcd', 'nAbandonedAcd', 'acw', 'aht']]
que_sum = que_sum.reset_index(level=0)

que_sum["acw_goal"] = 60
que_sum["aht_goal"] = 480
que_sum["abn_goal"] = (que_sum["nEnteredAcd"] * .05)

que_sum.head()