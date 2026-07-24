import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = "db/nifty100.db"


@st.cache_resource
def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def query(sql, params=None):
    conn = get_connection()
    if params:
        return pd.read_sql(sql, conn, params=params)
    return pd.read_sql(sql, conn)


# -------------------------------------------------------
# Companies
# -------------------------------------------------------

@st.cache_data(ttl=600)
def get_companies():
    return query("""
        SELECT *
        FROM companies
        ORDER BY company_name
    """)


@st.cache_data(ttl=600)
def get_company(company_id):
    return query("""
        SELECT *
        FROM companies
        WHERE company_name=?
    """, (company_id,))


# -------------------------------------------------------
# Financial Ratios
# -------------------------------------------------------

@st.cache_data(ttl=600)
def get_ratios(company_id=None):

    if company_id:
        return query("""
            SELECT *
            FROM financial_ratios
            WHERE company_id=?
            ORDER BY year
        """, (company_id,))

    return query("""
        SELECT *
        FROM financial_ratios
    """)


# -------------------------------------------------------
# Profit Loss
# -------------------------------------------------------

@st.cache_data(ttl=600)
def get_pl(company_id=None):

    if company_id:
        return query("""
            SELECT *
            FROM profit_loss
            WHERE company_id=?
            ORDER BY year
        """, (company_id,))

    return query("""
        SELECT *
        FROM profit_loss
    """)


# -------------------------------------------------------
# Balance Sheet
# -------------------------------------------------------

@st.cache_data(ttl=600)
def get_bs(company_id=None):

    if company_id:
        return query("""
            SELECT *
            FROM balance_sheet
            WHERE company_id=?
            ORDER BY year
        """, (company_id,))

    return query("""
        SELECT *
        FROM balance_sheet
    """)


# -------------------------------------------------------
# Cash Flow
# -------------------------------------------------------

@st.cache_data(ttl=600)
def get_cf(company_id=None):

    if company_id:
        return query("""
            SELECT *
            FROM cash_flow
            WHERE company_id=?
            ORDER BY year
        """, (company_id,))

    return query("""
        SELECT *
        FROM cash_flow
    """)


# -------------------------------------------------------
# Sector
# -------------------------------------------------------

@st.cache_data(ttl=600)
def get_sectors():
    return query("""
        SELECT *
        FROM sectors
    """)


# -------------------------------------------------------
# Market Cap
# -------------------------------------------------------

@st.cache_data(ttl=600)
def get_marketcap(company_id=None):

    if company_id:
        return query("""
            SELECT *
            FROM market_cap
            WHERE company_id=?
            ORDER BY year
        """, (company_id,))

    return query("""
        SELECT *
        FROM market_cap
    """)


# -------------------------------------------------------
# Peer Comparison
# -------------------------------------------------------

@st.cache_data(ttl=600)
def get_peer_groups():
    return query("""
        SELECT DISTINCT peer_group_name
        FROM peer_comparison
        ORDER BY peer_group_name
    """)


@st.cache_data(ttl=600)
def get_peers(group):

    return query("""
        SELECT *
        FROM peer_comparison
        WHERE peer_group_name=?
    """, (group,))


# -------------------------------------------------------
# Documents
# -------------------------------------------------------

@st.cache_data(ttl=600)
def get_documents(company_id):

    return query("""
        SELECT *
        FROM documents
        WHERE company_id=?
        ORDER BY Year DESC
    """, (company_id,))


# -------------------------------------------------------
# Pros & Cons
# -------------------------------------------------------

@st.cache_data(ttl=600)
def get_pros_cons(company_id):

    return query("""
        SELECT *
        FROM pros_cons
        WHERE company_id=?
    """, (company_id,))



@st.cache_data(ttl=600)
def get_company(company):
    conn = get_connection()

    query = """
    SELECT *
    FROM companies
    WHERE company_name=?
    """

    return pd.read_sql(query, conn, params=[company])


@st.cache_data(ttl=600)
def get_company_financials(company):

    conn = get_connection()

    query = """
    SELECT *
    FROM financial_ratios
    WHERE company_id=?
    ORDER BY year
    """

    return pd.read_sql(query, conn, params=[company])


@st.cache_data(ttl=600)
def get_company_pros(company):

    conn = get_connection()

    query = """
    SELECT *
    FROM pros_cons
    WHERE company_id=?
    """

    return pd.read_sql(query, conn, params=[company])


@st.cache_data(ttl=600)
def get_company_sector(company):

    conn = get_connection()

    query = """
    SELECT *
    FROM sectors
    WHERE company_id=?
    """

    return pd.read_sql(query, conn, params=[company])

@st.cache_data(ttl=600)
def get_financial_table():

    df = get_ratios().copy()

    df["quality_score"] = calculate_quality_score(df)

    df["recommendation"] = df["quality_score"].apply(recommendation)

    return df

@st.cache_data(ttl=600)
def get_screener_data():

    return query("""
    SELECT
        c.company_name,
        s.broad_sector,
        f.*
    FROM financial_ratios f
    LEFT JOIN companies c
        ON f.company_id = c.company_name
    LEFT JOIN sectors s
        ON f.company_id = s.company_id
    """)

@st.cache_data(ttl=600)
def get_peer_groups():
    conn = get_connection()
    return pd.read_sql(
        "SELECT * FROM peer_comparison",
        conn
    )


@st.cache_data(ttl=600)
def get_profit_loss():
    conn = get_connection()
    return pd.read_sql("SELECT * FROM profit_loss", conn)

from analytics.ai_stock_score import (
    calculate_quality_score,
    recommendation
)



@st.cache_data(ttl=600)
def get_portfolio():
    return query("""
        SELECT *
        FROM portfolio
    """)


def add_portfolio(company, qty, price, date):

    conn = get_connection()

    conn.execute(
        """
        INSERT INTO portfolio
        (company_id, quantity, buy_price, buy_date)
        VALUES (?,?,?,?)
        """,
        (company, qty, price, date)
    )

    conn.commit()