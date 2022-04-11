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


df = pd.read_csv(r"C:/Users/John/Desktop/db3/User Availability Summary.csv")

df["userid"] = df["FirstName"] + " " + df["LastName"]

df = df.pivot_table(index=["userid"], columns="StatusKey")

df.columns = df.columns.droplevel()
df["total"] = df.sum(axis=1, numeric_only=True)
df["non_productive"] = df["total"] - (df[["acw", "acdagentnotansweringccss", "available, no acd", "it issues"]].sum(axis=1))
df["adherence"] = df["non_productive"] / df["total"]
df["adherence"] = df["adherence"] * 100
adherence = df[["adherence", "total"]]

adherence = adherence.reset_index(level=0)
adherence = adherence.drop("total", axis=1)
adherence["goal"] = 90
