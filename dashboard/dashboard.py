import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load dataset
df = pd.read_csv("dashboard/all_data_day.csv")
df['date'] = pd.to_datetime(df['date'])

st.set_page_config(page_title="Bike-Sharing Dashboard",
                   layout="wide")

# Define helper functions
def create_monthly_users_df(df):
    monthly_users_df = df.resample(rule='M', on='date').agg({
        "casual": "sum",
        "registered": "sum",
    })
    monthly_users_df.index = monthly_users_df.index.strftime('%b-%y')
    monthly_users_df = monthly_users_df.reset_index()
    monthly_users_df.rename(columns={
        "date": "yearmonth",
    }, inplace=True)
    return monthly_users_df

def create_seasonly_users_df(df):
    seasonly_users_df = df.groupby("season").agg({
        "casual": "sum",
        "registered": "sum",
        "count": "sum"
    })
    seasonly_users_df = seasonly_users_df.reset_index()
    seasonly_users_df.rename(columns={
        "count": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    seasonly_users_df.set_index('season', inplace=True)
    seasonly_users_df = seasonly_users_df.stack().reset_index()
    seasonly_users_df.columns = ['season', 'type_of_rides', 'count_rides']
    return seasonly_users_df


# Make filter components
min_date = df["date"].min()
max_date = df["date"].max()

# Sidebar
with st.sidebar:
    st.image("dashboard/logo.png")
    st.sidebar.header("Filter:")
    start_date, end_date = st.date_input(
        label="Date Filter", min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter main_df
main_df = df[(df["date"] >= str(start_date)) & (df["date"] <= str(end_date))]

# Assign main_df to helper functions
monthly_users_df = create_monthly_users_df(main_df)
seasonly_users_df = create_seasonly_users_df(main_df)

# Main page
st.header('Bike Sharing :sparkles:')
st.markdown("##")

# Metrics
total_all_rides = main_df['count'].sum()
st.metric("Total Rides", value=total_all_rides)

st.markdown("---")

# Plot Monthly Count of Bikeshare Rides
plt.figure(figsize=(10, 6))
plt.bar(monthly_users_df['yearmonth'], monthly_users_df['casual'], color='skyblue', label='Casual')
plt.bar(monthly_users_df['yearmonth'], monthly_users_df['registered'], bottom=monthly_users_df['casual'], color='orange', label='Registered')
plt.xlabel('Year-Month')
plt.ylabel('Total Rides')
plt.title('Monthly Count of Bikeshare Rides')
plt.xticks(rotation=45)
plt.legend()
st.pyplot(plt)

# Plot Season Count of Bikeshare Rides
plt.figure(figsize=(10, 6))
sns.barplot(data=seasonly_users_df, x='season', y='count_rides', hue='type_of_rides',
            palette={"casual_rides": "skyblue", "registered_rides": "orange", "total_rides": "red"})
plt.title('Count of bikeshare rides by season')
plt.xlabel('Season')
plt.ylabel('Total Rides')
plt.legend(title='Type of Rides')
st.pyplot(plt)

st.caption('Copyright (c), created by Sahrul saefuloh')
