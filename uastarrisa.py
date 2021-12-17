#Tarrisa Cindy Fitriani
#12220055
#Kelas-01
#UAS PEMROGRAMAN KOMPUTER SEMESTER 3 TAHUN AJARAN 2021/2022 

import pandas as pd
import streamlit as st
import altair as alt
import json

# Container declarations
titlec = st.container()
container_a = st.container()
container_b = st.container()
container_c = st.container()
informasi_negara = st.container()
container_d = st.container()

st.markdown(
        """
        <style>
        .reportview-container {
            background: url("https://img.freepik.com/free-photo/hand-painted-watercolor-background-with-sky-clouds-shape_24972-1095.jpg?size=626&ext=jpg")
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# load data
df = pd.read_csv('produksi_minyak_mentah.csv', index_col="kode_negara")
negara_dict_al3 = {negara['alpha-3']:negara for negara in json.loads(open("kode_negara_lengkap.json").read())}
negara_dict_name = {negara['name']:negara for negara in json.loads(open("kode_negara_lengkap.json").read())}

# data cleaning
for n in df.index.unique().tolist():
    if n not in negara_dict_al3:
        print("out")
        df.drop([n], inplace=True)

df.reset_index(inplace=True)
list_negara = [negara_dict_al3[kode]['name'] for kode in df['kode_negara'].unique().tolist()]
# membuat altair bar yang di sort
def make_altair_bar(df, x, y):
    st.altair_chart(alt.Chart(df[[x, y]]).mark_bar().encode(
        x=alt.X(x, sort=None),
        y=y
        ), use_container_width=True
    )
# membuat dict dari nama negara
def get_info_negara(nama):
    print(nama)
    negara = negara_dict_name[nama]
    negara_dict = {
        'Nama': negara['name'],
        'Kode': negara['alpha-3'],
        'Region': negara['region'],
        'Subregion': negara['sub-region']
    }
    return negara_dict
# secara iteratif membuat markdown dengan pasangan key dan value dari sebua dict
def create_markdown_from_dict(text_dict:dict):
    for key, val in text_dict.items():
        st.markdown(f"{key}: *{val}*")
# secara iteratif membuat markdown dari elemen list
def create_markdown_from_list(text_list):
    for text in text_list:
        st.markdown(text)
#Container for title
with titlec:
    st.title("Data Produsen Minyak Mentah Dunia")
    st.write('dibuat oleh: Tarrisa Cindy Fitriani (12220055|Teknik Perminyakan ITB)') 

# Container yang berisi fitur soal A
with container_a:
    st.markdown("---")
    st.markdown("## Data produsen")

    select_negara = st.selectbox("", list_negara) # interactive user input
    kodeNegara = negara_dict_name[select_negara]['alpha-3'] # translate to kode negara

    st.markdown(f"Negara yang dipilih: *{select_negara}*")
    st.markdown(f"Kode alpha-3: *{kodeNegara}*")
    display_data = df[df["kode_negara"] == kodeNegara][['tahun', 'produksi']] # create dataframe
    display_data = display_data.set_index('tahun')
    st.bar_chart(display_data)
# Container yang berisi fitur soal B
with container_b:
    st.markdown("---")
    st.markdown('## Ranking produsen tahunan')

    year = df["tahun"] #year list
    # interactive user input
    y = st.slider('Tahun', min(year), max(year))
    n = st.slider('Jumlah peringkat', 1, len(df['kode_negara'].unique()), value=10, key='b')
    # create dataframe
    minyak_year_n = df.loc[df["tahun"] == y].sort_values('produksi', ascending=False)[:n] 
    make_altair_bar(minyak_year_n, 'kode_negara', 'produksi') # bar chart
    st.dataframe(display_data)
# Container yang berisi fitur soal C
with container_c:
    st.markdown('---')
    st.markdown('## Ranking total produksi produsen')
    # User input
    n = st.slider('Jumlah peringkat', 1, len(df['kode_negara'].unique()), value=10, key='c')
    # data frame
    prod_all_time = df[['kode_negara', 'produksi']].groupby('kode_negara', as_index=False).sum().sort_values('produksi', ascending=False)[:n]
    make_altair_bar(prod_all_time, 'kode_negara', 'produksi') # bar chart
# Container extra fitur
with informasi_negara:
    st.markdown('---')
    st.markdown('## Filter produsen')
    # input user
    select_negara = st.selectbox("Pilih negara yang ingin dicek", list_negara)
    #info negara
    negara = negara_dict_name[select_negara]
    kode = negara['alpha-3']

    produksi_negara = df.loc[df['kode_negara'] == kode] 
    index_max = produksi_negara['produksi'].idxmax() 
    max_prod = produksi_negara['produksi'][index_max]
    max_prod_year = produksi_negara['tahun'][index_max]
    prod_total = produksi_negara['produksi'].sum()

    st.markdown(f'#### Data negara {select_negara}')
    create_markdown_from_dict(get_info_negara(select_negara)) # buat markdown dari info negara

    st.markdown(f'#### Data produksi minyak {select_negara}')
    info_prod = [
        f'Produksi Paling tinggi sebanyak *{max_prod}* pada tahun *{max_prod_year}*',
        f'Selama ini telah memproduksi sebanyak *{prod_total}*'
    ]
    create_markdown_from_list(info_prod) # membuat markdown dari info produksi
# Container yang berisi fitur soal D
with container_d:
    st.markdown('---')
    st.markdown('## Produksi minyak berdasarkan kategori')
    #user input
    switch_filter = st.selectbox('Filter', ['Paling tinggi', 'Paling rendah', 'Kosong'])
    switch_freq = st.selectbox('Cakupan', ['Total', 'Masukkan tahun'], key='test1')

    if switch_freq == 'Total':# lakukan grouping dan jumlahkan
        grouped = df.groupby('kode_negara', as_index=False).sum()
    else:# jika tidak buat slider lalu filter dataframe pada tahun tersebut
        y = st.slider(f'Tahun yang akan dicek untuk {switch_filter}', min(year), max(year), key='d')
        grouped = df.loc[df['tahun'] == y]
    grouped.reset_index(inplace=True)
    # disini grouped sudah menjadi total atau tahunan
    # tipe 1
    if switch_filter == 'Paling tinggi':
        print(grouped)
        rowid = grouped['produksi'].idxmax() # dapatkan index nilai max
        print(f"row id ={rowid}") 
        negaradf = grouped[rowid:rowid+1] # dapatkan dataframe row dengan index nilai max
        negara = negara_dict_al3[negaradf['kode_negara'].values[0]] # dapatkan dict dari kode negara
        create_markdown_from_dict(get_info_negara(negara['name'])) # buat markdown dari dict
    elif switch_filter == 'Paling rendah': # tipe 2
        mindf = grouped[grouped['produksi'] > 0] # buat dataframe baru dari hasil filter lebih besar dari 0
        mindf.reset_index(inplace=True)
        rowid = mindf['produksi'].idxmin()
        negaradf = mindf[rowid:rowid+1]
        negara = negara_dict_al3[negaradf['kode_negara'].values[0]]
        create_markdown_from_dict(get_info_negara(negara['name']))
    else:#tipe 3
        noldf = grouped[grouped['produksi'] == 0] # buat dataframe baru yang memiliki nilai produksi 0
        noldf.reset_index(inplace=True)
        #inisialisasi list kosong
        nama = []
        region = []
        subregion = []
        for _, row in noldf.iterrows():# secara iteratif tambahkan data nama, region dan subregion ke list yang bersesuaian
            negara_dict = negara_dict_al3[row['kode_negara']]
            nama.append(negara_dict['name'])
            region.append(negara_dict['region'])
            subregion.append(negara_dict['sub-region'])
        # untuk melengkapi dataframe, tambahkan kolom baru
        noldf['Nama'] = nama
        noldf['Region'] = region
        noldf['Subregion'] = subregion
        # lakukan filter untuk menaruh kolom yang diinginkan
        st.dataframe(noldf.filter(items=['Nama', 'kode_negara', 'Region', 'Subregion']))

    #sebagai info tambahan menunjukan angka produksi
    if switch_filter != 'Kosong':
        if switch_freq == 'Semua waktu':
            st.markdown(f"Produksi kumulatif {negara['name']} adalah {negaradf['produksi'].values[0]}")
        else:
            st.markdown(f"Produksi {negara['name']} pada tahun {negaradf['tahun'].values[0]} adalah {negaradf['produksi'].values[0]}")

