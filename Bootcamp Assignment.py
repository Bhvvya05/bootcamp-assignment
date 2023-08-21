#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import re


# In[2]:


get_ipython().system('pip install openai')


# In[3]:


import openai


# In[4]:


csv_files = [
    'US_INDU_INCOME_STATEMENT_KEY.csv',
    'US_INDU_INCOME_STATEMENT.csv',
    'US_INDU_CASH_FLOW_STATEMENT_KEY.csv',
    'US_INDU_CASH_FLOW_STATEMENT.csv',
    'US_INDU_CALCULATIONS_KEY.csv',
    'US_INDU_CALCULATIONS.csv',
    'US_INDU_BALANCE_SHEET_STATEMENT_KEY.csv',
    'US_INDU_BALANCE_SHEET_STATEMENT.csv'
]

data_frames = {}

for csv_file in csv_files:
    df_key = csv_file.replace('.csv', '').replace('US_INDU_', '').replace('_', ' ')
    data_frames[df_key] = pd.read_csv(csv_file)


# In[5]:


openai.api_key = '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'


# In[6]:


def filter_data(data_df, company_name, fiscal_year, quantity_column):
    filtered_data = data_df[
        (data_df['company'] == company_name) &
        (data_df['fiscal_period'] == 'FY') &
        (data_df['fiscal_year'] == fiscal_year)
    ]
    value = filtered_data[quantity_column].iloc[0]
    return value


# In[7]:


def answer_question(user_question: str) -> str:
    response = openai.Completion.create(
        engine="davinci",
        prompt=user_question,
        max_tokens=50,
        temperature=0.6,
    )
    api_response = response.choices[0].text.strip()
    
   
    company_name = "Apple"  
    fiscal_year = "2021"  
    quantity_match = re.search(r'(Total Revenue|Net Income|Price to Earnings|Dividend Yield|Return on Equity)', api_response)
    quantity = quantity_match.group(1) if quantity_match else None
    
    if quantity is None:
        return "I'm sorry, I couldn't understand the question."
    
   
    if quantity in ["Total Revenue", "Net Income"]:
        data_df = data_frames["INCOME STATEMENT"]
        quantity_column = "netincome"
    elif quantity == "Price to Earnings":
        data_df = data_frames["CALCULATIONS"]
        quantity_column = "pricetoearnings"
    elif quantity == "Dividend Yield":
        data_df = data_frames["CALCULATIONS"]
        quantity_column = "dividendyield"
    elif quantity == "Return on Equity":
        data_df = data_frames["CALCULATIONS"]
        quantity_column = "roe"
    else:
        return "I'm sorry, I couldn't understand the question."
    
    
    value = filter_data(data_df, company_name, fiscal_year, quantity_column)
    formatted_value = value  
    
    
    final_response = f"In {fiscal_year}, {company_name} {quantity} was {formatted_value}."
    
    
    response = openai.Completion.create(
        engine="davinci",
        prompt=final_response,
        max_tokens=50,
        temperature=0.6,
    )
    final_response = response.choices[0].text.strip()
    
    return final_response


# In[8]:


user_question = "What was the efficiency of Apple in generating profits from its shareholders' equity in 2021?"
response = answer_question(user_question)
print(response)


# In[ ]:




