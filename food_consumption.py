import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Food Consumption Dashboard", page_icon=":bar_chart:", layout="wide")

# ---- READ FILE ----
@st.cache
def get_data_from_csv():
    df = pd.read_csv("food_consumption.csv",encoding="ISO-8859-1")
    # drop columns that are not needed
    df.drop(columns=['Area Abbreviation', 'Area Code', 'Item Code',
            'Element Code', 'Unit', 'latitude', 'longitude'], inplace=True)
    return df

df = get_data_from_csv()

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")

areas = df["Area"].unique()
area = st.sidebar.selectbox(
    "Select the Area:",
    options=areas,
    index=1
)

items = df["Item"].unique()
item = st.sidebar.selectbox(
    "Select the Food Type:",
    options=items
)

years = list(df.columns)[3:]
year = st.sidebar.multiselect(
    "Select the Year:",
    options=years,
    default=years
)

filt = (df['Area'] == area) & (df['Item'] == item)
df_selection = (df.loc[filt])[['Element'] + year]
df_grp = df_selection.groupby('Element')


# ---- MAINPAGE ----
st.title(":bar_chart: Food Consumption Dashboard")
st.markdown("##")

# TOP summary
try:
    food_consume = int(df_grp.get_group('Food').sum()[year].sum())
except:
    food_consume = 0
try:
    feed_consume = int(df_grp.get_group('Feed').sum()[year].sum())
except:
    feed_consume = 0
total_consume = food_consume + feed_consume

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Consumption (thousand tonnes):")
    st.subheader(f"{total_consume}")
with middle_column:
    st.subheader("Food Consumption (thousand tonnes):")
    st.subheader(f"{food_consume}")
with right_column:
    st.subheader("Feed Consumption (thousand tonnes):")
    st.subheader(f"{feed_consume}")

st.markdown("""---""")

# BAR CHART
with st.container():
    df_sum = df_grp.sum()
    st.bar_chart(df_sum.transpose(), use_container_width=True)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)