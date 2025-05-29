# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize your Smoothie! :cup_with_straw:")

order_name = st.text_input("What do you want us to call you?")
if order_name:
    st.write("The name on the cup will be: ", order_name)


session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

st.write(
  """Choose the fruits you want in your custom Smoothie!"""
)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe,max_selections=5
)
if ingredients_list:
    st.write (ingredients_list)
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,order_name) values ('""" + ingredients_string + """' , '""" + order_name + """' )"""
    st.write(my_insert_stmt)
time_to_insert = st.button('Submit Order!')

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered, ' + order_name + '!', icon="✅")
