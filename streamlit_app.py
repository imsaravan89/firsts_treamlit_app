import streamlit
import pandas
import snowflake.connector
import requests
from urllib.error import URLError

streamlit.title('My Parents New Healty Diner')  
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinace & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast')

fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
fruit_list = fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)


streamlit.header("Fruityvice Fruit Advice!")
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")


# write your own comment -what does the next line do? 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
streamlit.dataframe(fruityvice_normalized)

fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)

fruityvice_normalized_response = pandas.json_normalize(fruityvice_response.json())
streamlit.dataframe(fruityvice_normalized_response)

streamlit.stop()


my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains")
streamlit.dataframe(my_data_rows)
fruit_choice = streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.write('Thanks for adding ', fruit_choice)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")
