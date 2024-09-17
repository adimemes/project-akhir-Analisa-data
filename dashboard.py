import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import time
from babel.numbers import format_currency
sns.set(style='dark')

def create_daily_orders_df(df):
    df['dteday'] = pd.to_datetime(df['dteday'])
    daily_orders_df = df.resample(rule='D', on='dteday').agg({
        "instant": "nunique",  # assuming instant can represent orders
        "cnt": "sum"  # using cnt for total users as a proxy for total_price
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "instant": "order_count",
        "cnt": "revenue"  # total users as a proxy for revenue
    }, inplace=True)
    
    return daily_orders_df

# Sum Order Items DataFrame (adapted for bike data)
def create_sum_order_items_df(df):
    # Assuming 'cnt' is the closest equivalent for quantity in this dataset
    sum_order_items_df = df.groupby("day_type").cnt.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def create_rfm_df(df):
    df['dteday'] = pd.to_datetime(df['dteday'])
    rfm_df = df.groupby(by="dteday", as_index=False).agg({
        "instant": "nunique",  # frequency as number of unique instances
        "cnt": "sum"  # using total users (cnt) as monetary
    })
    rfm_df.columns = ["order_date", "frequency", "monetary"]
    
    rfm_df["order_date"] = rfm_df["order_date"].dt.date
    recent_date = df["dteday"].dt.date.max()
    rfm_df["recency"] = rfm_df["order_date"].apply(lambda x: (recent_date - x).days)
    
    return rfm_df

all_df = pd.read_csv("data_sepeda.csv")
datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()
 
with st.sidebar:
    st.header("Toko Sepeda Adi.MS")
    # Menambahkan logo perusahaan
    st.image("logo.jpg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

# Applying the adjusted functions to the dataset
daily_orders_df = create_daily_orders_df(main_df)
sum_order_items_df = create_sum_order_items_df(main_df)
rfm_df = create_rfm_df(main_df)

st.header('Tugas Akhir Dicoding DataSet Toko Sepeda')

st.subheader('Daily Orders')
 
col1, col2 = st.columns(2)
 
with col1:
    total_orders = daily_orders_df.order_count.sum()
    st.metric("Total Registrasi", value=total_orders)
 
with col2:
    total_revenue = format_currency(daily_orders_df.revenue.sum(), "AUD", locale='es_CO') 
    st.metric("Total Pendapatan", value=total_revenue)

monthly_orders_df = all_df.resample(rule='M', on='dteday').agg({
    "registered": "sum", 
    "cnt": "sum"
})

# Grafik Pertama
st.subheader('Grafik Jumlah pendaftar sepeda perbulannya')
monthly_orders_df.index = monthly_orders_df.index.strftime('%Y-%m')
monthly_orders_df = monthly_orders_df.reset_index()
monthly_orders_df.rename(columns={
    "registered": "total_registered", 
    "cnt": "total_cnt"                 
}, inplace=True)

monthly_orders_df.head()

plt.figure(figsize=(20, 10)) 
plt.plot(monthly_orders_df["dteday"], monthly_orders_df["total_registered"], marker='o', linewidth=2, color="#72BCD4") 
plt.title("Number of Register per Month", loc="center", fontsize=20) 
plt.xticks(fontsize=10) 
plt.grid(True)
plt.xticks(rotation = 45)
plt.yticks(fontsize=10) 
plt.show()

st.pyplot(plt)

_Penjelasan_grafik = """
Grafik di atas menjelaskan tren dari pendaftara sepeda maupun itu pendaftar pada holiday, workday, weekend dan weathersit
karena semua data dimasukan dan di masukan ke dalam grafik, dan grafik menunjukan tren naik sampai bulan september 2021 
sebagai puncak tertinggi pendaftaran
"""

def stream_data_line():
    for word in _Penjelasan_grafik.split(" "):
        yield word + " "
        time.sleep(0.02)

    for word in _Penjelasan_grafik.split(" "):
        time.sleep(0.02)


if st.button("Stream data line"):
    st.write_stream(stream_data_line)

# Grafik Kedua
st.subheader("data besaran jumlah pendaftar pada holiday, workday dan weekend")
all_df['day_type'] = all_df.apply(lambda row: 'Holiday' if row['holiday'] == 1 
                              else ('Workday' if row['workingday'] == 1 
                              else 'Weekend'), axis=1)

day_type_counts = all_df['day_type'].value_counts()

plt.figure(figsize=(8, 6))
day_type_counts.plot(kind='bar', color=['skyblue', 'lightgreen', 'salmon'])
plt.title('Perbandingan Jumlah Hari: Holiday, Workday, dan Weekend', fontsize=14)
plt.xlabel('Tipe Hari', fontsize=12)
plt.ylabel('Jumlah Hari', fontsize=12)
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

st.pyplot(plt)

_Penjelasan_chart = """
dilihat dari bar chart yang ada bahwa user lebih banyak menyewa sepeda pada hari kerja daripada di hari weekend dan holiday, 
sehingga bisa disimpulkan penjualan paling keras pada workday dimana user mungkin saja menyewa sepeda untuk ke tempat bekerja
"""

def stream_data_chart():
    for word in _Penjelasan_chart.split(" "):
        yield word + " "
        time.sleep(0.02)

    for word in _Penjelasan_chart.split(" "):
        time.sleep(0.02)


if st.button("Stream data chart"):
    st.write_stream(stream_data_chart)

st.caption('I Kadek Adi Memes Subagia')

