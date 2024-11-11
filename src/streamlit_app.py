import streamlit as st

# st.container(height=100, border=20, key="contract_inputs")
#
# st.form("contract_inputs", clear_on_submit=False, enter_to_submit=True, border=True)

pg = st.navigation([st.Page("products/options.py", default=True), st.Page("products/fixed_income.py", default=False),
                    st.Page('products/pnl_Calculation.py', default=False)])
pg.run()