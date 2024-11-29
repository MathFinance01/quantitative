import streamlit as st
import pandas as pd

st.title('Decomposition of Yield Curve using PCA')

st.subheader('What is an yield curve?')
st.write('Generally speaking, yield curve is yields of bonds(of the same issuer) plotted against their maturities. '
         'I have plotted the yield curve of US treasuries with maturities varying from 1 month to 30 years as of ${22^{nd}}$ Nov 2024')

st.image('src/products/data/yield_curve_22nd_Nov.png')

st.subheader('How to use PCA to explain PnL?')

st.subheader('Level, Slope and Curvature')

