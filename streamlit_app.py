# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(f":cup_with_straw: Customize your Smoothie! :cup_with_straw:")

order_name = st.text_input("What do you want us to call you?")
if order_name:
    st.write("The name on the cup will be: ", order_name)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop

#Convert the snowpark dataframe to pandas
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop

st.write(
  """Choose the fruits you want in your custom Smoothie!"""
)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe,max_selections=5
)
if ingredients_list:
    #st.write (ingredients_list)
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,order_name) values ('""" + ingredients_string + """' , '""" + order_name + """' )"""
    #st.write(my_insert_stmt)
time_to_insert = st.button('Submit Order!')

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered, ' + order_name + '!', icon="✅")

