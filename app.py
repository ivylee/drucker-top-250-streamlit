import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(page_title="Drucker Top 250")

st.title("Drucker Institute Company Ranking Top 250 (2017-2024)")


@st.cache_data
def load_data():
    data = pd.read_csv("./drucker_top_250_2017-2024.csv", dtype={"Year": np.int32})
    return data


data = load_data()

if st.checkbox("Show raw data"):
    st.subheader("Raw data")
    st.dataframe(data)


st.subheader("Top 100 company by average ranking")
top_df = (
    data.groupby("Company")
    .agg(
        appearances=pd.NamedAgg(column="Year", aggfunc="count"),
        avg_ranking=pd.NamedAgg(column="Ranking", aggfunc="mean"),
    )
    .sort_values(by=["appearances", "avg_ranking"], ascending=[False, True])
    .head(100)
)
st.dataframe(top_df)

st.subheader("Explore by company")

company = st.selectbox("Search by company name", sorted(data.Company.unique()))

company_df = data.loc[data["Company"] == company].sort_values(by=["Year"])
st.dataframe(company_df)

ranking_df = company_df[["Year", "Ranking"]]
ranking_fig = px.line(ranking_df, x="Year", y="Ranking")
st.plotly_chart(ranking_fig, theme="streamlit")

metrics_df = company_df[
    [
        "Year",
        "Customer Satisfaction",
        "Employee Engagement and Development",
        "Innovation",
        "Social Responsibility",
        "Financial Strength",
        "Effectiveness",
    ]
]
metrics_fig = px.line(metrics_df, x="Year", y=metrics_df.columns[1:])
st.plotly_chart(metrics_fig, theme="streamlit")
