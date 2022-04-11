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


df = pd.read_csv(r"C:/Users/John/Desktop/db3/User Productivity Summary.csv")

df["userid"] = df["FirstName"] + " " + df["LastName"]

#df = df.pivot_table(index = ["userid"])
df = df.groupby(['userid', 'queue'], as_index=True).sum()

df = df.reset_index(level=0)
df = df.reset_index(level=0)

df = df[df['queue'] == "PH_Kinray_CustomerService_Z1_English"]
df = df[df['totnAnsweredACD'] > 0]

df['acw'] = df["totTACW"] / df["totnAnsweredACD"] 
df['aht'] = (df[["totTACW", "totTTalkACD", "totTHoldACD"]].sum(axis=1)) / df["totnAnsweredACD"] / df["totnAnsweredACD"]

acd = df[["userid", "totnAnsweredACD", "acw", "aht"]]
