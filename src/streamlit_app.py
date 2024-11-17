import streamlit as st

# st.container(height=100, border=20, key="contract_inputs")
#
# st.form("contract_inputs", clear_on_submit=False, enter_to_submit=True, border=True)

pg = st.navigation([st.Page("products/QuantFinance/Options.py", default=True),
                    st.Page('products/Trading/PnL_Calculation.py', default=False),
                    st.Page('products/Trading/Signals.py', default=False),
                    st.Page('products/QuantFinance/Curve_Bootstrapping.py', default=False),
                    st.Page('products/Mathematics/ARMA.py', default=False),
                    st.Page('products/Mathematics/Correlation-Covariance.py', default=False),
                    st.Page('products/Mathematics/Principal_Components_Analysis.py', default=False)
                    ])
pg.run()