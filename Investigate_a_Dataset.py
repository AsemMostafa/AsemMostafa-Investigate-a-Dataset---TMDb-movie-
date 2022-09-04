#!/usr/bin/env python
# coding: utf-8

# 
# 
# # Project: Investigate a Dataset - [TMDb movie]
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# 
# This data set contains information
# about 10,000 movies collected from
# The Movie Database (TMDb),
# including user ratings and revenue.
# ● Certain columns, like ‘cast’
# and ‘genres’, contain multiple
# values separated by pipe (|)
# characters.
# ● There are some odd characters
# in the ‘cast’ column.
# ● The final two columns ending
# with “_adj” show the budget and
# revenue of the associated movie
# in terms of 2010 dollars,
# accounting for inflation over
# time. 
# 
# what about using data analysis skills to know some intersting insights about movies, so let's start the analysis.
# 
# 
# ### Question(s) for Analysis
# 1. what is the Average runtime movies from year to year?
# 2. Are there a correlation between popularity and vote_aveage?
# 3. what are the top 10 movies in popularity?
# 4. How did the amount of produced films changed over time? 

# In[2]:


# Use this cell to set up import statements for all of the packages that you plan to use.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')

#changing numbers appearing format
#https://stackoverflow.com/questions/38689125/how-to-get-rid-of-pandas-converting-large-numbers-in-excel-sheet-to-exponential
pd.options.display.float_format = '{:.2f}'.format


# <a id='wrangling'></a>
# ## Data Wrangling
# 
# 
# 
# ### General Properties
# 

# In[3]:


# Load your data and print out a few lines. Perform operations to inspect data
#   types and look for instances of missing or possibly errant data.
df = pd.read_csv('tmdb-movies.csv')
df.head()


# In[4]:


df.shape


# In[5]:


df.describe()


# In[6]:


df.info()


# In[7]:


#calculating null values in each column
df.isna().sum()


# In[8]:


#take a general look at all columns of the data
df.hist(figsize=(16,8));


# 
# 
# 
# 
# ### Frist impression
# there are rows contain several values, which are seperated by an "|",need to be cleaned . 
# From the exploration above i found out that the data has null values in some columns and 0 values in others which kind a weird thing to have 0 values in such a column like how the run time for a movie equal zero or budget...etc,so we need to clean this up and drop unneeded columns.
# 
# 

# 
# ### Data Cleaning
#  

# In[9]:



#replace 0 values with NAN
#sorce:https://stackoverflow.com/questions/49575897/cant-replace-0-to-nan-in-python-using-pandas
df['revenue'].replace(0, np.NAN, inplace=True)
df['revenue_adj'].replace(0, np.NAN, inplace=True)
df['budget'].replace(0, np.NAN, inplace=True)
df['budget_adj'].replace(0, np.NAN, inplace=True)
df['runtime'].replace(0, np.NAN, inplace=True)

df.dropna(axis=0, inplace=True)


# In[10]:


#Seperating columns that have several values
#source: https://apassionatechie.wordpress.com/2018/02/24/how-do-i-split-a-string-into-several-columns-in-a-dataframe-with-pandas-python/

df_cast = (df['cast'].str.split('|', expand=True).rename(columns=lambda x: f"cast_{x+1}"))
df_director = (df['director'].str.split('|', expand=True).rename(columns=lambda x: f"director_{x+1}"))
df_genres = (df['genres'].str.split('|', expand=True).rename(columns=lambda x: f"genres_{x+1}"))
df_keywords = (df['keywords'].str.split('|', expand=True).rename(columns=lambda x: f"keywords_{x+1}"))
df_prod = (df['production_companies'].str.split('|', expand=True).rename(columns=lambda x: f"production_comp_{x+1}"))

df_cast.head()


# In[11]:


#Join the seperated columns and drop unneeded columns 

df = df.join([df_cast, df_director,df_genres,df_keywords, df_prod])
df = df.drop(['cast', 'director', 'keywords', 'production_companies', 'imdb_id', 'homepage', 'release_date', 'overview' , 'tagline'], axis=1)


# In[12]:


#checking for duplicates
df.duplicated().sum()


# In[13]:


#chicking the data type if it appropriate or not
df.dtypes


# In[14]:


df


# the data looks prepared for the analysis, no duplicates have been found, no nanull values, columns containing multiple values have been seperated and data types look ready for analysis.

# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# 
# 
# 
# ### Research Question 1 (Average runtime movies from year to year?)

# In[15]:


#creating a plot of the mean of rlease year vs runtime
df.groupby('release_year').mean()['runtime'].plot(figsize=(10,6),color='y');
plt.xlabel('release_year')
plt.ylabel('runtime');
min_av=df.groupby('release_year').mean()['runtime'].min()
max_av=df.groupby('release_year').mean()['runtime'].max()


# the chart indicate that the average runtime movies is about 130.00 m ,the minimum Average runtime movies is 91.0,but maximum is 175.0.

# In[16]:


#calcuating the min and max run time
min_av=df.groupby('release_year').mean()['runtime'].min()
max_av=df.groupby('release_year').mean()['runtime'].max()
min_av,max_av


# ### Research Question 2 (Are there a correlation between popularity and vote_aveage?)

# In[17]:


pop_vote=df[['popularity','vote_average']]
pop_vote.corr()


# ### Research Question 3 (what are the top 10 movies in popularity?)

# In[24]:


index = pd.Index(range(1, 11, 1))#setting index of movies order in the list
top_df=df[['original_title','popularity','genres','release_year']]
top_ten=top_df.nlargest(n=10,columns=['popularity']).set_index(index)
top_ten


# In[23]:


#creating a bar plot for top movies popularity
top_ten.plot(x='original_title',y='popularity',kind='bar')


# nice! this bar chart indicates the top 10 movies in popularity, Jurassic World in the lead...

# ### Research Question 4 (How did the amount of produced films changed over time?)

# In[25]:


#calculating the number of movies in last 10 years
movie_year=df.groupby('release_year').count()['id']
movie_year.tail(10)


# In[26]:


#creating a line chart shows the amonut of movies per year
movie_year.plot(figsize=(16,8),title='Amount of movies over years')
plt.xlabel('Year')
plt.ylabel('Amount');


# form the plot we can see that the amount of movies has increased significantly from 1998 to 2015 and reached its peak in 2011. 

# <a id='conclusions'></a>
# ## Conclusions
# **Results:**
#  
# The first research question "What is the Average runtime movies from year to year?" indicate that the average runtime movies is about 130.00 m ,the minimum and maximum Average runtime movies are respectively(91.0, 175.0).
# 
# The second research question "Are there a correlation between popularity and vote_aveage?" indicate that there is no strong corralation between them.
# 
# The third research question "What are the top 10 movies in popularity?" indicate that jurassic world is the most popular produced movie followed by Mad Max: Fury Road and Interstellar, movies genres concentarted in Action|Adventure|Science Fiction|Thriller, notcing that most of them produced lately. 
# 
#  The forth research question "How did the amount of produced films changed over time?"  reveals that the amount of produced films significantly increased from 1998 to 2015, and reached its peak in 2011, this can be an idicator for the huge developement in cinema in the last decade and we expect it to increase more and more now respectively with the increase in audience,and movies platforms now adays. </pre>
# 
# **limitations:**
# *  Most of our varialbes are categorical, which does not allow for a high level of statistical method that can be used to provide correlatios etc.
# * data outcomes cann't be generalised because some entries in the dataset have been removed due to missing data ,but can be treated as indicators.
# * considering that many inputs in our data have been removed due to missing data.
# * we can add more recent data to this data to have better insights

# In[142]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Investigate_a_Dataset.ipynb'])

