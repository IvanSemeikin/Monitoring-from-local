#!/usr/bin/env python
# coding: utf-8

# In[36]:


import pandas as pd
import requests
import datetime
import warnings
from datetime import datetime
import time
import streamlit as st
# import schedule  # Пока что скрыл, потому что streamlit не пропускает schedule


# In[2]:


def take_info_sku(sku_list, clientid, apikey):#выгрузка из sku
    url = "https://api-seller.ozon.ru/v2/product/info"
    headers = {
        "Client-Id": clientid,
        "Api-Key": apikey,
        "Content-Type": "application/json"
    }
    
    final_df = pd.DataFrame()

    for sku in sku_list:
        data = {"sku": sku}
        response = requests.post(url, headers=headers, json=data)
        result_data = response.json()

    #Проверка на ошибку или отсутствие данных
        if isinstance(result_data, str) or 'result' not in result_data:
            print(f"Данных по SKU {sku} нет.")
            continue  # Пропуск текущей итерации

        df = pd.json_normalize(result_data['result'])
        df = df[['id', 'name','marketing_price', 'min_ozon_price','old_price', 'premium_price', 'price', 'recommended_price', 'min_price','price_index','price_indexes.price_index',
                 'price_indexes.external_index_data.minimal_price',
                 'price_indexes.external_index_data.minimal_price_currency',
                 'price_indexes.external_index_data.price_index_value']]

        
        warnings.filterwarnings("ignore")

        df.index = [sku] * len(df)
        final_df = pd.concat([final_df, df])        # было так final_df = final_df.append(df)

    return final_df

#     return final_df.to_excel(r'C:\Users\iv18s\Desktop\Champ Commerce\indexes.xlsx')


# In[14]:


# АННОР ГРУПП ООО
sku_1 = [583849836, 591277100, 591413879, 1032159418, 974739870, 595719315, 974735426, 1123269788, 1140364359, 842403637, 842404691, 1151844229, 857790599, 1151835491, 1151835845, 1151837403, 1151753898, 1151848598, 1151839306, 1151837986, 1151841444] 
client_Id_1 = "356810"
api_Key_1 = "63572e24-e7a4-4a60-9d8b-8a110af5a43a"

# Бакина В.А. (Гуменюк) ИП
# sku_2 = [1184491881, 1184490550, 1184508336, 1184490550, 1184508336, 1184508336, 1184508336, 1223241618]
# client_Id_2 = ""
# api_Key_2 = ""

# ИП Корыткина Г. Э
# sku_3 = [1223695977, 1223688125]
# client_Id_3 = ""
# api_Key_3 = ""

# Казаков А. А. ИП
sku_4 = [1052881196]
client_Id_4 = "206273"
api_Key_4 = "d6d9710d-14f8-48be-83dc-978784ef52d7"


# Мисиоцкая К. К. ИП
sku_5 = [942887676, 1011620714]
client_Id_5 = "743131"
api_Key_5 = "23977008-7525-4d00-afdf-9d9d89d22c88"


# Неклюдова Т. В. ИП
sku_6 = [821015069, 892024999, 893028679, 893031207, 1036222833, 1036231739, 1036246444]
client_Id_6 = "795940"
api_Key_6 = "10831bd1-87ee-4a79-abcf-800c64868210"


# ООО ФЭЛФРИ
sku_7 = [938702199, 882130038]
client_Id_7 = "802356"
api_Key_7 = "4957fe6a-13b1-4887-83ee-5e105721cd68"


# In[53]:


# ФУНКЦИИ

# def download_excel(dataset):
#     dataset.to_excel(r'C:\Users\iv18s\Desktop\Champ Commerce\indexes.xlsx')

def nuzhn_stolb(dataset):
    # Только нужные столбцы
    dataset = dataset.iloc[:, [1,2,10,11]]
    
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    new_name_1 = f'Price {current_datetime}'
    new_name_2 = f'Index {current_datetime}'
    new_name_3 = f'Minimal other price {current_datetime}'
    dataset.rename(columns={'marketing_price': new_name_1}, inplace=True)
    dataset.rename(columns={'price_indexes.price_index': new_name_2}, inplace=True)
    dataset.rename(columns={'price_indexes.external_index_data.minimal_price': new_name_3}, inplace=True)
    
    df = dataset
    return df

def actual_sku(dataset1):
    # Получим все SKU из прошлой таблицы. НО! Мы их изначально будем списком загружать, то есть этот список будет неактуален
    sku_now = dataset1.index.values.tolist()
    return sku_now

def sozdanie_datafreima():
    data = {  # 'sku': [],
            'subject': [], 
            'avg subject price': [], 
            'current sku price': [], 
            'previous sku price': [], 
            'delta price': [], 
            'current price index': [], 
            'previous price index': [],
            'current other price': [],
            'previous other price': []}

    osnova_dt = pd.DataFrame(data)
#     osnova_dt = osnova_dt.set_index('sku')  # Нельзя для пустого датафрейма
#     osnova_dt['delta price'] = osnova_dt['current sku price'] - osnova_dt['previous sku price']  # Нельзя для пустого датафрейма
    return osnova_dt

def spisok_new_sku(dataset1):
    sku_imeuschiesya = dataset1.index.values.tolist()
    new_sku = [x for x in sku_now if x not in sku_imeuschiesya]
    return new_sku

def main_dataset(dataset1, dataset2):
    novyi_pd = pd.concat([dataset1, dataset2], axis=1)
    # Заменяем все NaN на 0
    novyi_pd.fillna(0, inplace=True)
    return novyi_pd

def obrabotka_dataseta(dataset):
    columns_to_swap_1 = [2, 3]
    dataset.iloc[:, columns_to_swap_1] = dataset.iloc[:, columns_to_swap_1[::-1]]  # current price становится previous
    
    columns_to_swap_2 = [2, 10]
    dataset.iloc[:, columns_to_swap_2] = dataset.iloc[:, columns_to_swap_2[::-1]]  # новая цена становится current
    
    columns_to_swap_3 = [5, 6]
    dataset.iloc[:, columns_to_swap_3] = dataset.iloc[:, columns_to_swap_3[::-1]]  # current index становится previous
    
    columns_to_swap_4 = [5, 11]
    dataset.iloc[:, columns_to_swap_4] = dataset.iloc[:, columns_to_swap_4[::-1]]  # новый index становится current    
    
    columns_to_swap_5 = [7, 8]
    dataset.iloc[:, columns_to_swap_5] = dataset.iloc[:, columns_to_swap_5[::-1]]  # current other price становится previous
    
    columns_to_swap_6 = [7, 12]
    dataset.iloc[:, columns_to_swap_6] = dataset.iloc[:, columns_to_swap_6[::-1]]  # новая other price становится current 
    
    
    
#     dataset['current sku price'], dataset['previous sku price'] = dataset['marketing_price'], dataset['current sku price']
#     dataset['current price index'], dataset['previous price index'] = dataset['price_indexes.price_index'], dataset['current price index']
    dataset['subject'] = dataset['name']
    dataset['current sku price'] = pd.to_numeric(dataset['current sku price'])
    dataset['delta price'] = dataset['current sku price'] - dataset['previous sku price']

    dataset['Проверка'] = dataset.apply(lambda row: '0' if row['current price index'] == row['previous price index'] else '1', axis=1)
    changes = (dataset['Проверка'] == '1').sum()
    
    if changes == 0:
        st.write('Изменений нет')
    else:
        st.write(f'Количество изменений: {changes}')
    
    return dataset
# # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# # Инициализация st.session_state, если это необходимо
# if 'result' not in st.session_state:
#     st.session_state.result = None

# def your_function(param):
#     # Ваш код функции
#     result = f"This is the result for parameter {param}."
    
#     # Сохранение результата в st.session_state
#     st.session_state.result = result
    
#     return result
# # ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def obrez(dataset):
    dataset_obr = dataset.copy()
    columns_to_drop = [9, 10, 11, 12, 13]
    dataset_obr.drop(dataset_obr.columns[columns_to_drop], axis=1, inplace=True)
    return dataset_obr
    

def dataset_k_pokazu(dataset):
    proverka = ['1']
    novyi_pd_dlya_pokaza = novyi_pd[novyi_pd['Проверка'].isin(proverka)]
    novyi_pd_dlya_pokaza = novyi_pd_dlya_pokaza.iloc[:, [0, 1,2,3,4,5,6,7,8]]
    
    return novyi_pd_dlya_pokaza

def concat_all_datasets(dataset1, dataset4, dataset5, dataset6, dataset7):  # сейчас пропущены dataset2, dataset3
    df_obschiy = pd.concat([dataset1, dataset4, dataset5, dataset6, dataset7])  # сейчас пропущены dataset2, dataset3

    return df_obschiy

def dlit_vypoln(start, stop):
    time_raboty = round(stop - start, 2)
    st.write(f'Время выполнения: {time_raboty} секунд')
    
def time_vypoln():
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.write(f'Время последнего обновления: {time_now}')
    
def pokaz(dataset):
    st.write(dataset)
    
execution_count = 0
# Инициализация st.session_state, если это необходимо
if 'execution_count' not in st.session_state:
    st.session_state.execution_count = None

def schetchick():
    global execution_count
    execution_count += 1
    # Сохранение результата в st.session_state
    st.session_state.execution_count = execution_count    
    return execution_count


# In[54]:


# Не нужно создавать новый датасет, нужно добавить имеющийся и с ним сравнивать - сделал
# Удалять последние столбцы - сделал
# Добавить строчку в конце -"Столько-то изменений" - сделал
# Если нет изменений, то выводить: "Изменений нет" - сделал
# Может быть добавить Столбец "Новый" для новых товаров
# Можно добавить столбец "Название ИП"
# МОЖНО ДОБАВИТЬ ДОПОЛНИТЕЛЬНЫЙ БЛОК С ФУНКЦИЯМИ И ПОЛУЧИТЬ ДВА БЛОКА: ПЕРВЫЙ ЗАПУСК И ПОСЛЕДКЮЩИЕ ЗАПУСКИ


# In[56]:


start = time.time()
# Вызов функций
df_1 = take_info_sku(sku_1, client_Id_1, api_Key_1)
# df_2 = take_info_sku(sku_2, client_Id_2, api_Key_2)
# df_3 = take_info_sku(sku_3, client_Id_3, api_Key_3)
df_4 = take_info_sku(sku_4, client_Id_4, api_Key_4)
df_5 = take_info_sku(sku_5, client_Id_5, api_Key_5)
df_6 = take_info_sku(sku_6, client_Id_6, api_Key_6)
df_7 = take_info_sku(sku_7, client_Id_7, api_Key_7)

df = concat_all_datasets(df_1, df_4, df_5, df_6, df_7)  # сейчас нет df_2 и df_3

df = nuzhn_stolb(df)
sku_now = actual_sku(df)
osnova_dt = sozdanie_datafreima()
# new_sku = spisok_new_sku(osnova_dt)
execution_count = schetchick()
if execution_count == 1:
    novyi_pd = main_dataset(osnova_dt, df)  # В первый раз нужно вставить osnova_dt, начиная со второго dataset_obrez
else:
    novyi_pd = main_dataset(dataset_obrez, df)  # В первый раз нужно вставить osnova_dt, начиная со второго dataset_obrez
novyi_pd = obrabotka_dataseta(novyi_pd)
dataset_obrez = obrez(novyi_pd)
novyi_pd_dlya_pokaza = dataset_k_pokazu(novyi_pd)

stop = time.time()
dlit_vypoln(start, stop)
time_vypoln()
pokaz(novyi_pd_dlya_pokaza)  # Сперва попробую хотя бы просто вывести итог в streamlit


# ХОЧУ ДОБАВИТЬ КНОПКУ!*****************************************************************************************************************************************
if st.button("Пожалуйста, работай нормально!"):
    st.write('GO Vegas!***************************************************')
    start = time.time()
    # Вызов функций
    df_1 = take_info_sku(sku_1, client_Id_1, api_Key_1)
    # df_2 = take_info_sku(sku_2, client_Id_2, api_Key_2)
    # df_3 = take_info_sku(sku_3, client_Id_3, api_Key_3)
    df_4 = take_info_sku(sku_4, client_Id_4, api_Key_4)
    df_5 = take_info_sku(sku_5, client_Id_5, api_Key_5)
    df_6 = take_info_sku(sku_6, client_Id_6, api_Key_6)
    df_7 = take_info_sku(sku_7, client_Id_7, api_Key_7)
    
    df = concat_all_datasets(df_1, df_4, df_5, df_6, df_7)  # сейчас нет df_2 и df_3
    
    df = nuzhn_stolb(df)
    sku_now = actual_sku(df)
    osnova_dt = sozdanie_datafreima()
    # new_sku = spisok_new_sku(osnova_dt)
    execution_count = schetchick()
    if execution_count == 1:
        novyi_pd = main_dataset(osnova_dt, df)  # В первый раз нужно вставить osnova_dt, начиная со второго dataset_obrez
    else:
        novyi_pd = main_dataset(dataset_obrez, df)  # В первый раз нужно вставить osnova_dt, начиная со второго dataset_obrez
    novyi_pd = obrabotka_dataseta(novyi_pd)
    dataset_obrez = obrez(novyi_pd)
    novyi_pd_dlya_pokaza = dataset_k_pokazu(novyi_pd)
    
    stop = time.time()
    dlit_vypoln(start, stop)
    time_vypoln()
    pokaz(novyi_pd_dlya_pokaza)  # Сперва попробую хотя бы просто вывести итог в streamlit

# In[ ]:





# In[ ]:


# ConnectionError: HTTPSConnectionPool(host='api-seller.ozon.ru', port=443): Max retries exceeded with url: /v2/product/info (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x00000202785F02B0>: Failed to establish a new connection: [Errno 11001] getaddrinfo failed'))
            


# In[57]:


# start = time.time()
# # Вызов функций
# df_1 = take_info_sku(sku_1, client_Id_1, api_Key_1)
# # df_2 = take_info_sku(sku_2, client_Id_2, api_Key_2)
# # df_3 = take_info_sku(sku_3, client_Id_3, api_Key_3)
# df_4 = take_info_sku(sku_4, client_Id_4, api_Key_4)
# df_5 = take_info_sku(sku_5, client_Id_5, api_Key_5)
# df_6 = take_info_sku(sku_6, client_Id_6, api_Key_6)
# df_7 = take_info_sku(sku_7, client_Id_7, api_Key_7)

# df = concat_all_datasets(df_1, df_4, df_5, df_6, df_7)  # сейчас нет df_2 и df_3

# df = nuzhn_stolb(df)
# sku_now = actual_sku(df)
# osnova_dt = sozdanie_datafreima()
# # new_sku = spisok_new_sku(osnova_dt)
# novyi_pd = main_dataset(dataset_obrez, df)  # В первый раз нужно вставить osnova_dt, начиная со второго dataset_obrez
# novyi_pd = obrabotka_dataseta(novyi_pd)
# dataset_obrez = obrez(novyi_pd)
# novyi_pd_dlya_pokaza = dataset_k_pokazu(novyi_pd)

# stop = time.time()
# dlit_vypoln(start, stop)
# time_vypoln()
# pokaz(novyi_pd_dlya_pokaza)
# # novyi_pd  # - можно увидеть последние загруженные данные
# novyi_pd_dlya_pokaza  # - вывод конечного результата

# # Лямбда-функция для передачи аргументов в функции
# task_1 = lambda: take_info_sku(sku_1, client_Id_1, api_Key_1)
# # task_2 = lambda: take_info_sku(sku_2, client_Id_2, api_Key_2)
# # task_3 = lambda: take_info_sku(sku_3, client_Id_3, api_Key_3)
# task_4 = lambda: take_info_sku(sku_4, client_Id_4, api_Key_4)
# task_5 = lambda: take_info_sku(sku_5, client_Id_5, api_Key_5)
# task_6 = lambda: take_info_sku(sku_6, client_Id_6, api_Key_6)
# task_7 = lambda: take_info_sku(sku_7, client_Id_7, api_Key_7)
# task_8 = lambda: concat_all_datasets(df_1, df_4, df_5, df_6, df_7)  # сейчас нет df_2 и df_3
# task_9 = lambda: nuzhn_stolb(df)
# task_10 = lambda: actual_sku(df)
# task_11 = lambda: sozdanie_datafreima()
# # task_12 = lambda: spisok_new_sku(osnova_dt)
# task_13 = lambda: main_dataset(osnova_dt, df)  # В первый раз нужно вставить osnova_dt, начиная со второго dataset_obrez
# task_14 = lambda: obrabotka_dataseta(novyi_pd)
# task_15 = lambda: obrez(novyi_pd)
# task_16 = lambda: dataset_k_pokazu(novyi_pd)
# task_17 = lambda: dlit_vypoln(start, stop)
# task_18 = lambda: pokaz(novyi_pd_dlya_pokaza)

# # Запускать каждые 15 минут
# t = 1
# # schedule.every(t).minutes.do(start)
# schedule.every(t).minutes.do(task_1)
# # schedule.every(t).minutes.do(task_2)
# # schedule.every(t).minutes.do(task_3)
# schedule.every(t).minutes.do(task_4)
# schedule.every(t).minutes.do(task_5)
# schedule.every(t).minutes.do(task_6)
# schedule.every(t).minutes.do(task_7)
# schedule.every(t).minutes.do(task_8)
# schedule.every(t).minutes.do(task_9)
# schedule.every(t).minutes.do(task_10)
# schedule.every(t).minutes.do(task_11)
# # schedule.every(t).minutes.do(task_12)
# schedule.every(t).minutes.do(task_13)
# schedule.every(t).minutes.do(task_14)
# schedule.every(t).minutes.do(task_15)
# schedule.every(t).minutes.do(task_16)

# # schedule.every(t).minutes.do(stop)
# # schedule.every(t).minutes.do(task_17)
# schedule.every(t).minutes.do(time_vypoln)
# schedule.every(t).minutes.do(task_18)

# while True:
#     schedule.run_pending()
#     time.sleep(1)


# In[ ]:


# # Лямбда-функция для передачи аргументов в функции
# task_1 = lambda: take_info_sku(sku_1, client_Id_1, api_Key_1)
# # task_2 = lambda: take_info_sku(sku_2, client_Id_2, api_Key_2)
# # task_3 = lambda: take_info_sku(sku_3, client_Id_3, api_Key_3)
# task_4 = lambda: take_info_sku(sku_4, client_Id_4, api_Key_4)
# task_5 = lambda: take_info_sku(sku_5, client_Id_5, api_Key_5)
# task_6 = lambda: take_info_sku(sku_6, client_Id_6, api_Key_6)
# task_7 = lambda: take_info_sku(sku_7, client_Id_7, api_Key_7)
# task_8 = lambda: concat_all_datasets(df_1, df_4, df_5, df_6, df_7)  # сейчас нет df_2 и df_3
# task_9 = lambda: nuzhn_stolb(df)
# task_10 = lambda: actual_sku(df)
# task_11 = lambda: sozdanie_datafreima()
# # task_12 = lambda: spisok_new_sku(osnova_dt)
# task_13 = lambda: main_dataset(dataset_obrez, df)  # В первый раз нужно вставить osnova_dt, начиная со второго dataset_obrez
# task_14 = lambda: obrabotka_dataseta(novyi_pd)
# task_15 = lambda: obrez(novyi_pd)
# task_16 = lambda: dataset_k_pokazu(novyi_pd)
# task_17 = lambda: dlit_vypoln(start, stop)
# task_18 = lambda: pokaz(novyi_pd_dlya_pokaza)

# # Запускать каждые 15 минут
# t = 5
# # schedule.every(t).minutes.do(start)
# schedule.every(t).minutes.do(task_1)
# # schedule.every(t).minutes.do(task_2)
# # schedule.every(t).minutes.do(task_3)
# schedule.every(t).minutes.do(task_4)
# schedule.every(t).minutes.do(task_5)
# schedule.every(t).minutes.do(task_6)
# schedule.every(t).minutes.do(task_7)
# schedule.every(t).minutes.do(task_8)
# schedule.every(t).minutes.do(task_9)
# schedule.every(t).minutes.do(task_10)
# schedule.every(t).minutes.do(task_11)
# # schedule.every(t).minutes.do(task_12)
# schedule.every(t).minutes.do(task_13)
# schedule.every(t).minutes.do(task_14)
# schedule.every(t).minutes.do(task_15)
# schedule.every(t).minutes.do(task_16)

# # schedule.every(t).minutes.do(stop)
# # schedule.every(t).minutes.do(task_17)
# schedule.every(t).minutes.do(time_vypoln)
# schedule.every(t).minutes.do(task_18)

# # while True:
# #     schedule.run_pending()
# #     time.sleep(5)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




