import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import plotly.figure_factory as ff


data = pd.read_csv("zomato.csv")
data = data.drop(['url','address','phone','menu_item',
       'listed_in(type)', 'listed_in(city)'],axis=1)
feature_na = [i for i in data.columns if data[i].isnull().sum() > 0]
data.dropna(subset=['rate'],axis=0,inplace=True)

def split(x):
    return x.split('/')[0].strip()

data['rate'] = data['rate'].apply(split)
data['rate'].replace(['NEW','-'],0,inplace=True)
data['rate'] = data['rate'].astype(float)

rating = pd.pivot_table(data,index='name',values='rate')
rating=rating.sort_values(['rate'],ascending=False)




st.bar_chart(rating[0:20])

fig = ff.create_distplot([data['rate']],group_labels=["Rate"])
st.plotly_chart(fig)

chains = data['name'].value_counts()[0:15]

st.bar_chart(data=chains)

x = data.online_order.value_counts()
labels = ['accepted','not-accepted']

fig1,ax1 = plt.subplots()
ax1.pie(x,labels=labels,autopct='%1.1f%%')
ax1.axis('equal')
st.write("Restaurants accepting online orders")
st.pyplot(fig1)

x = data.book_table.value_counts()
labels = ['accepted','not-accepted']
fig1,ax1 = plt.subplots()
ax1.pie(x,labels=labels,autopct='%1.1f%%')
ax1.axis('equal')
st.write("Restaurants accepting table booking")

st.pyplot(fig1)

rest_typ = data.rest_type.value_counts()[0:15]
st.bar_chart(rest_typ)

voting = data.groupby('name')[['votes']].mean()
high_vot = voting[voting['votes'] >5000]
#HACK CODE
fig1,ax1 = plt.subplots()
ax1.barh(high_vot.index,high_vot['votes'])
st.pyplot(fig1);

voting_rating = data.groupby('name')[['votes']].mean().sort_values('votes',ascending=False)
voting_rating['name'] = voting_rating.index

voting_rating = voting_rating.reset_index(drop=True)
voting_rating = pd.merge(voting_rating,data[['rate','name']])
vote_top = voting_rating[voting_rating['votes'] > 5000]
vote_top = vote_top.groupby('name')[['rate']].mean().sort_values('rate',ascending=False)

st.bar_chart(vote_top['rate'])

bad_count = voting_rating[(voting_rating['rate'] < 3) & (voting_rating['rate'] > 0)]
bad_resturants = bad_count[bad_count['votes'] > 500].groupby('name')[['rate']].mean()

st.bar_chart(bad_resturants['rate'])


location_restro = data[['location']].value_counts()[0:20]
