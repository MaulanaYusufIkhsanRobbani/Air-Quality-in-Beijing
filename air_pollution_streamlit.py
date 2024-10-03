import streamlit as st            #Package untuk membuat dashboar visualisasi data
import pandas as pd               #Package untuk pemrosesan data
import numpy as np                #Package untuk perhitungan
import matplotlib.pyplot as plt   #Package untuk visualisasi data dasar
import matplotlib.dates as mdates #Package untuk menyediakan format visualisasi data deret waktu
from matplotlib import cm         #Package untuk penentuan warna peta
import seaborn as sns             #Package untuk visualisasi data lanjut
import geopandas as gpd           #Package untuk pemrosesan data geografis
import os                         #Package untuk mengatur akses file
# Title of the Streamlit app
st.title("Proyek Analisis Data: Air Quality in Beijing")

st.write("""
- **Nama:** Maulana Yusuf Ikhsan Robbani
- **Email:** xyzikhsanxyz@gmail.com
- **ID Dicoding:** Ikhsan Robbani
         """)
# Displaying the packages used
st.write("""
## Packages Used:
- pandas: Data processing
- numpy: Calculations
- matplotlib: Basic data visualization
- seaborn: Advanced data visualization
""")

st.markdown("""
## Menentukan Pertanyaan Bisnis
- Pertanyaan 1  
Bagaimana kualitas udara di Beijing?
- Pertanyaan 2  
Bagaimana tren perubahan kualitas udara di Beijing tiap bulannya?
""")

# Directory containing the dataset files
directory = 'D:/Local Disk C/Python project/project/data_analytics_dicoding/PRSA_Data_20130301-20170228'

# Getting the list of all files in the directory
all_files = os.listdir(directory)

# Filtering the list to include only CSV files
csv_files = [file for file in all_files if file.endswith('.csv')]

# Creating a list to store dataframes
dataframes_list = []

# Looping through each file and reading & appending it to the list of dataframes
for file_name in csv_files:
    file_path = os.path.join(directory, file_name)
    df = pd.read_csv(file_path)
    dataframes_list.append(df)

# Combining all dataframes into one
combined_df = pd.concat(dataframes_list)

# Resetting the index of the combined dataframe
combined_df.reset_index(drop=True, inplace=True)

# Renaming columns
combined_df.rename(columns={'PM2.5': 'PM25'}, inplace=True)

# Creating a date column
combined_df['date'] = pd.to_datetime(combined_df['year'].astype(str) + '-' + combined_df['month'].astype(str) + '-' + combined_df['day'].astype(str), format='%Y-%m-%d')


with st.sidebar:
# Explain the dataset
    st.markdown("""
    Penjelasan kolom pada dataset [1]
    1. No  
    -   Penanda setiap record dalam dataset  
    2. year   
    -   Tahun saat data dikumpulkan.  
    3. month   
    -	Bulan saat data dikumpulkan.  
    4. day   
    -	tanggal saat data dikumpulkan.   
    5. hour  
    -	Jam saat data dikumpulkan  
    6. PM2.5  
    -	Konsentrasi materi partikulat dengan diameter 2,5 mikrometer atau kurang (dalam mikrogram per meter kubik, µg/m³). PM2.5 adalah polutan kritis karena kemampuannya menembus jauh ke dalam paru-paru dan memasuki aliran darah, sehingga menimbulkan risiko kesehatan yang serius.  
    7. PM10  
    -	Konsentrasi materi partikulat dengan diameter 10 mikrometer atau kurang (dalam µg/m³). PM10 termasuk partikel yang lebih besar dari PM2.5 dan juga dapat memengaruhi kesehatan dan jarak pandang.  
    8. SO2  
    -	Konsentrasi sulfur dioksida (dalam µg/m³), gas yang dihasilkan oleh letusan gunung berapi dan proses industri, terutama pembakaran bahan bakar fosil. Kadar yang tinggi dapat menyebabkan masalah pernapasan dan kerusakan lingkungan.  
    9. NO2  
    -	Konsentrasi nitrogen dioksida (dalam µg/m³), yang terutama dihasilkan dari emisi kendaraan dan proses industri. Hal ini dapat mengiritasi saluran udara dalam sistem pernapasan manusia dan berkontribusi pada pembentukan kabut asap dan hujan asam.  
    10. CO  
    -	Konsentrasi karbon monoksida (dalam µg/m³), gas yang tidak berwarna dan tidak berbau yang dihasilkan dari pembakaran bahan bakar fosil. Kadar yang tinggi dapat menyebabkan efek kesehatan yang berbahaya, terutama di ruang tertutup.   
    11. O3  
    -	Konsentrasi ozon di permukaan tanah (dalam µg/m³). Meskipun ozon di atmosfer bagian atas melindungi kita dari radiasi sinar UV, ozon di permukaan tanah merupakan polutan berbahaya yang dapat menyebabkan gangguan pernapasan dan gangguan kesehatan lainnya.   
    12. TEMP  
    -	Suhu (dalam derajat Celcius) pada saat pengukuran, yang dapat memengaruhi konsentrasi polutan dan pola penyebaran.  
    13. PRES  
    -	Tekanan atmosfer (dalam hPa), yang memengaruhi pola cuaca dan dapat memengaruhi kualitas udara dengan memengaruhi cara polutan menyebar di atmosfer.  
    14. DEWP  
    -	Suhu titik embun (dalam derajat Celcius), yang menunjukkan kadar kelembapan di udara, yang dapat memengaruhi tingkat polutan dan kenyamanan manusia.  
    15. RAIN  
    -	Jumlah curah hujan (dalam mm) yang tercatat selama periode pengukuran, yang dapat membantu memahami bagaimana curah hujan memengaruhi kualitas udara dengan membersihkan polutan.  
    16. wd  
    -	Arah angin (dalam derajat), yang penting untuk memahami bagaimana polutan diangkut melalui atmosfer.   
    17. WSPM  
    -	Kecepatan angin (dalam meter per detik), yang memengaruhi penyebaran polutan; kecepatan angin yang lebih tinggi dapat mengencerkan konsentrasi, sedangkan kecepatan yang lebih rendah dapat menyebabkan akumulasi polutan.  
    18. station  
    -	Pengenal untuk stasiun pemantauan tempat data dikumpulkan, memberikan konteks tentang variasi geografis dalam kualitas udara di berbagai lokasi.  
            """)

# Creating a new dataframe with station coordinates
data = {
    'station': ['Gucheng', 'Wanshouxigong', 'Tiantan', 'Guanyuan',
                'Dongsi', 'Nongzhanguan', 'Wanliu', 'Aotizhongxin',
                'Shunyi', 'Changping', 'Dingling', 'Huairou'],
    'Latitude': [39.9116, 39.8802, 39.8824, 39.9327, 39.9304, 39.9415,
                 39.9598, 39.9837, 40.1503, 40.2229, 40.2960, 40.3193],
    'Longitude': [116.1933, 116.3677, 116.4647, 116.3623, 116.4246,
                  116.4647, 116.2982, 116.3995, 116.6411, 116.2202,
                  116.2234, 116.6338]
}
station_coords = pd.DataFrame(data)
# Display a dataset
col5, col6 = st.columns(2)
with col5:
    st.write("""
    # Dataset kualitas udara stasiun-stasiun kota Beijing
            """)
    st.write(combined_df.head(10))
with col6:
    # Display Coordinates Data
    st.write("""
    # Pembuatan kolom Koordinat sebagai tempat pengambilan data [1]
            """)
    st.write(station_coords.head())

# Merging station coordinates with the combined dataframe
combined_df = combined_df.merge(station_coords, how='left', left_on='station', right_on='station')

# Defining numerical and categorical columns in the dataframe
numerical_columns = ['No', 'year', 'month', 'day', 'hour', 'PM25', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
categorical_columns = ['wd', 'station']

# Defining quartiles and interquartile range (IQR)
q25, q75 = np.percentile(combined_df[numerical_columns], 25), np.percentile(combined_df[numerical_columns], 75)
iqr = q75 - q25
cut_off = iqr * 1.5

# Defining minimum and maximum limits without outliers
minimum, maximum = q25 - cut_off, q75 + cut_off

# # Identifying outliers in the numerical columns
# outliers = [x for x in combined_df[numerical_columns] if x < minimum or x > maximum]
# st.write("## Outliers in Numerical Columns")
# st.write(outliers)

# Interpolating missing values in the dataframe
combined_df.interpolate(inplace=True)

# # Checking for null values again after interpolation
# st.write("## Null Values After Interpolation")
# st.write(combined_df.isnull().sum())
stat_summary = combined_df[numerical_columns].describe(include="all")
# Displaying statistical summary of the numerical columns
# Defining IQR and bounds for outliers in the statistical summary table
stat_summary.loc['IQR'] = stat_summary.loc['75%'] - stat_summary.loc['25%']
stat_summary.loc['Lower Bound'] = stat_summary.loc['25%'] - (1.5 * stat_summary.loc['IQR'])
stat_summary.loc['Upper Bound'] = stat_summary.loc['75%'] + (1.5 * stat_summary.loc['IQR'])
# Setting outlier values to NaN based on bounds defined in statistical summary table
for col in numerical_columns:
    combined_df[col] = np.where((combined_df[col] < stat_summary[col].loc['Lower Bound']) | (combined_df[col] > stat_summary[col].loc['Upper Bound']), np.nan, combined_df[col])

# Interpolating missing values again after setting outliers to NaN
combined_df.interpolate(inplace=True)

col3, col4 = st.columns([2,1])
with col3:
    # Displaying updated statistical summary with IQR and bounds for outliers
    st.write("## Statistical Summary of Numerical Columns")
    st.write(stat_summary)
with col4:
    # Displaying statistical summary of categorical columns
    st.write("## Statistical Summary of Categorical Columns")
    st.write(combined_df[categorical_columns].describe())

st.write("""
**Insight:**
- Berdasarkan tabel statistika, nilai pada data tersebut memiliki rentang yang normal, sesuai dengan logika sehari-hari. Contoh temperature (TEMP) tidak ditemukan suhu dibawah -20, rentang hari dari 1 sampai 31, rentang bulan dari 1-12 dst
- Nilai curah hujan (RAIN) sangatlah ekstrim. Bahkan setelah dihapus outliernya tetap rentangnya 0 - 72.5. Padahal 75% data berada pada 0. Artinya kota Beijing jarang terjadi hujan
         """)
indikator = st.selectbox(
   "Pilih metrik yang ingin digunakan",
   ('PM25',	'PM10',	'SO2',	'NO2',	'CO', 'O3' 'TEMP',	'PRES',	'DEWP',	'RAIN',	'WSPM')
)
# Function to create boxplots for numerical columns to identify outliers visually
def create_boxplots(data, indikator):
    plt.figure(figsize=(18,10))
    sns.boxplot(y=data[indikator], color='green')
    plt.tight_layout()
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    st.pyplot(plt)
    plt.clf()
def create_histogram(data, indikator):
    plt.figure(figsize=(18, 10))
    sns.distplot(data[indikator], color='green', label=indikator)
    plt.tight_layout()
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    st.pyplot(plt)
    plt.clf()

col1, col2 = st.columns(2)
with col1:
    # Creating boxplots for numerical columns to identify outliers visually
    st.write("""
Keberadaan Outlier pada data
             """)
    create_boxplots(combined_df,indikator)

with col2:
    # Creating histogram + kde plot to identify thie distributions
    st.write("""
    Distribusi tiap indikator
                """)
    create_histogram(combined_df, indikator)

# Membuat method pembuatan tabel agregasi berdasarkan kebutuhan
def group_by_method(stat_metric,keycol):
 return combined_df.groupby(keycol).agg(
    PM25 = ('PM25', stat_metric),
    PM10 = ('PM10', stat_metric),
    SO2 = ('SO2', stat_metric),
    NO2 = ('NO2',stat_metric),
    CO = ('CO',stat_metric),
    O3 = ('O3',stat_metric),
    TEMP = ('TEMP',stat_metric),
    PRES = ('PRES',stat_metric),
    DEWP = ('DEWP',stat_metric),
    RAIN = ('RAIN',stat_metric),
    WSPM = ('WSPM',stat_metric)
)

# Pembuatan tabel agregasi berdasarkan tanggal per hari
city_gr_mean_day = group_by_method('mean',['date','station','Longitude','Latitude'])
# Pembuatan tabel agregasi berdasarkan bulan
city_gr_mean_month = group_by_method('mean',['month','year','station','Longitude','Latitude'])
# Pembuatan tabel agregasi berdasarkan stasiun
city_gr_mean_tot = group_by_method('mean',['station','Longitude','Latitude'])

# Mengeluarkan kolom yang menjadi index menjadi kolom biasa
city_gr_mean_day.reset_index(inplace=True)
city_gr_mean_day.set_index('date', inplace=True)
city_gr_mean_month.reset_index(inplace=True)
city_gr_mean_month['year'] = city_gr_mean_month['year'].astype(int)
city_gr_mean_month['month'] = city_gr_mean_month['month'].astype(int)
city_gr_mean_month['date'] = pd.to_datetime(city_gr_mean_month['year'].astype(str) + '-' + city_gr_mean_month['month'].astype(str)+'-01', format='%Y-%m-%d')
# city_gr_mean_month['date'] = pd.to_datetime(city_gr_mean_month['year'].astype(str) + '-' + city_gr_mean_month['month'].astype(str) +'-01', format='%b-%Y')
city_gr_mean_tot.reset_index(inplace=True)

# Pendefinisian data beijing sebagai data geopandas dari city_gr_mean_tot
beijing = gpd.GeoDataFrame(city_gr_mean_tot)

# Memunculkan Beijing GeoJSON
# Sumber file GeoJSON: https://github.com/echarts-maps/echarts-china-cities-js/blob/master/geojson/shape-only/beijing.geojson
beijing_boundary = gpd.read_file('D:/Local Disk C/Python project/project/data_analytics_dicoding/beijing.geojson')
st.write("""
    ### Pertanyaan 1:
    Bagaimana kualitas udara di distrik Beijing, RRC?
"""
)
st.write("""
Peta kota Beijing beserta kadar polutan
         """)
def plot_air_quality_map(data, indicator, color_map='plasma', x_limits=(116.10, 116.70), y_limits=(39.80, 40.40), title="Air Quality Levels in Beijing"):
    """
    Plot peta kota Beijing beserta dengan kualitas udara berdasarkan indikator tertentu.
    Parameters:
    - data: DataFrame yang mengandung data stasiun.
    - indicator: Indikator kualitas udara (contoh, 'CO', 'PM25', 'PM10', dll.).
    - color_map: Warna peta.
    - x_limits: Skala peta (longitude).
    - y_limits: Skala peta (latitude).
    """

    # Membuat plot
    fig, ax = plt.subplots(figsize=(10, 10))
    beijing_boundary.plot(ax=ax, color='lightblue', edgecolor='black')

    # Membuat warna peta
    cmap = cm.get_cmap(color_map)

    # Plot tiap stasiun berdasarkan indikator dan tingkat polusi
    scatter = ax.scatter(
        data['Longitude'], data['Latitude'],
        c=data[indicator],  # Indikator
        cmap=cmap,  # Penerapan Warna Peta
        s=100,  # Ukuran poin data
        edgecolor='black',
        alpha=0.8
    )

    # Pengaturan teks demi keterbacaan
    for x, y, label in zip(data['Longitude'], data['Latitude'], data['station']):
        plt.text(x + 0.002, y + 0.002, label, fontsize=9, ha='left')

    # Menambahkan colorbar sebagai metrik
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label(indicator + ' Levels')

    # Penyesuaian ukuran peta
    ax.set_xlim(x_limits)
    ax.set_ylim(y_limits)

    # Penambahan judul dan label tiap sumbu
    plt.title(title)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    # Menunjukan plot
    st.pyplot(plt)
    plt.clf()

plot_air_quality_map(beijing, indicator=indikator, color_map='plasma')

# Method untuk mencetak tren polusi
# def plot_time_series(data, indicator , daftar_stasiun):
# def plot_time_series(data, indicator ):


    # Plot tren kota Beijing beserta dengan kualitas udara berdasarkan indikator tertentu.
    # Parameters:
    # - data: DataFrame yang mengandung data stasiun.
    # - indicator: Indikator kualitas udara (contoh, 'CO', 'PM25', 'PM10', dll.).
    # - daftar_stasiun: daftar stasiun yang ingin dilihat.
    # - x_limits: Skala peta (longitude).
    # - y_limits: Skala peta (latitude).

st.write("""
    ### Pertanyaan 2:
Bagaimana tren perubahan kualitas udara di distrik Beijing, RRC tiap bulannya?
"""
)
station2 = st.multiselect(
   "Pilih staisun yang ingin dibandingkan",
   ('Wanshouxigong', 'Gucheng', 'Dongsi', 'Wanliu', 'Nongzhanguan',
       'Tiantan', 'Aotizhongxin', 'Guanyuan', 'Shunyi', 'Changping',
       'Huairou', 'Dingling'), default=('Wanshouxigong', 'Gucheng')
)
st.write("""
Tren kadar polutan tiap stasiun di Beijing
         """)
timeseries = city_gr_mean_month[city_gr_mean_month['station'].isin(station2)]
plt.figure(figsize=(18, 6))
sns.lineplot(x='date', y=indikator, data=timeseries, hue='station')
plt.xlabel('Tanggal')
plt.ylabel('Jumlah')
plt.xticks(rotation=25, ha='right', fontsize=10)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
plt.title(f'Tren kadar {indikator} ditiap stasiun')
st.pyplot(plt)
st.write("""
**Insight:**
- Daerah utara yang jauh dari pusat kota cenderung memiliki kadar polutan yang rendah dibanding daerah selatan
- Jika berpacu pada metrik PM 2.5 maka seluruh stasiun itu berada pada level 4 yang artinya udara disana berbahaya
- Jika berpacu pada metrik PM 10 maka seluruh stasiun itu berada pada level 2 yang artinya udara disana cukup berbahaya
- Tren kenaikan dan penurunan kadar polutan di seluruh stasiun cenderung sama dan memiliki pola musiman berdasarkan bulannya
- Ketika mendekati akhir tahun, kadar polutan semakin meningkat drastis
         """)
# plot_time_series(data=city_gr_mean_month,indicator=indikator1)  
multi_indikator3 = st.multiselect(
    "Pilih kolom yang ingin dilihat korelasinya",
    ('PM25',	'PM10',	'SO2',	'NO2',	'CO', 'O3' 'TEMP',	'PRES',	'DEWP',	'RAIN',	'WSPM'), default=('PM25', 'PM10')
)
# Peta korelasi antar kolom/variabel
plt.figure(figsize=(12,12))
correlation = combined_df[multi_indikator3].corr()
sns.heatmap(correlation, annot=True, fmt=".2f")
st.pyplot(plt)
plt.clf()

st.write("""
- Berdasarkan data keseluruhan, sebagian besar stasiun di Beijing memiliki kualitas udara yang tidak sehat
- Kadar polutan di tiap stasiun mengikuti tren berdasarkan bulan    
         """)

st.write("""
Sumber:  
[1] Air Quality Levels and Health Risk Assessment of Particulate Matters in Abuja Municipal Area, Nigeria  
Nathaniel Wambebe, Xiaoli Duan  
Agustus 2020  
  
[2] A hybrid prediction model of air quality for sparse station based on spatio-temporal feature extraction  
Yue Hu, Xiaoxia Chen, Hanzhong Xia  
Juni 2023           

         """)