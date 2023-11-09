import streamlit as st
import plotly.express as px
import matplotlib as plt
import seaborn as sns
import pandas as pd
import numpy as np
import plotly.express as px

plt.rcParams.update({'text.color': "white",
                    'axes.labelcolor': "white",
                    'axes.edgecolor': 'white',
                    'xtick.color': 'white',
                    'ytick.color': 'white',
                    'figure.facecolor': '0F1116',
                    'axes.facecolor': '0F1116'})

st.set_page_config(layout="wide")
st.title("EGLE x MSDS Capstone - Brownfields Reporting")

col1, col2= st.columns([1,4])

col1.subheader("Project Background")
