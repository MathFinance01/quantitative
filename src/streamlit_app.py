import streamlit as st
import QuantLib as ql

# st.container(height=100, border=20, key="contract_inputs")
#
# st.form("contract_inputs", clear_on_submit=False, enter_to_submit=True, border=True)

pg = st.navigation([st.Page("products/1_options.py", default=True), st.Page("products/2_fixed_income.py", default=False)])
pg.run()