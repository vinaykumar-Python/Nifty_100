import streamlit as st
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from dashboard.utils.db import (
    get_companies,
    get_documents
)

st.title("📄 Annual Reports")

companies = get_companies()

company = st.selectbox(
    "Select Company",
    companies["company_name"]
)

company_id = companies.loc[
    companies["company_name"] == company,
    "id"
].iloc[0]

docs = get_documents(company_id)

st.dataframe(docs, width="stretch")