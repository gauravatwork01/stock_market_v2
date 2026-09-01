
import streamlit as st
from contexts.financials import api_controller

st.set_page_config(
    page_title="Financial Explorer",
    layout="wide"
)
print(f"pg config-set ")

st.title("Financial Explorer")
print(f"written title")

company_isin_map = {
    "ITC": "INE154A01025"  ,  
    "COFORGE": "INE591G01025",
    "VOEPL": "INE0I0T01010", 
    # "Infosys": "INE009A01021",
}

company = st.selectbox(
    "Company",
    list(company_isin_map.keys())
)
# st.toast(f"Switched to {company}") 

print(f"Selected company: {company}")
isin = company_isin_map[company]
df = api_controller.get_financials(isin)

st.write(f"Selected company is: {company}")
st.dataframe(df)


