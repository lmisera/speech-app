import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import nltk
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.util import ngrams
nltk.download('punkt')
nltk.download('stopwords')

current_dir = os.path.dirname(__file__)
data_path = os.path.join(current_dir, 'data', 'Speech_With_Data.xlsx')

tab1, tab2 = st.tabs(['Student data','Judge data'])

#Page 1: Speech students
# Load data
with tab1:
   streamlit_dataframe = pd.read_excel(data_path)

   print(streamlit_dataframe)

   st.title(f'Data by student')


   #Add "All events' option
   events = []
   for i in streamlit_dataframe.Event:
      if i not in events:
         events.append(i)
      else:
         pass
   events = ["All events"] + events


   rounds = []
   for i in streamlit_dataframe.Round:
      if i not in rounds:
         rounds.append(i)
      else:
         pass
   rounds = ["All rounds"] + rounds


   # Dropdown to select a name
   selected_name = st.selectbox('Select a student:', streamlit_dataframe['Name'].unique())

   # Filter data for the selected name
   filtered_data = streamlit_dataframe[streamlit_dataframe['Name'] == selected_name]
   feedback_data = streamlit_dataframe[streamlit_dataframe['Name'] == selected_name]



   # Add "All events' option
   selected_round = st.selectbox('Select a round:', rounds)
   selected_event = st.selectbox('Select an event:', events)
   events = []
   for i in filtered_data.Event:
      if i not in events:
         events.append(i)
      else:
         pass
   events = ["All events"] + events


   rounds = []
   for i in filtered_data.Round:
      if i not in rounds:
         rounds.append(i)
      else:
         pass
   rounds = ["All rounds"] + rounds




   if selected_round!="All rounds":
      filtered_data = filtered_data[filtered_data['Round'] == selected_round]
      feedback_data = feedback_data[feedback_data['Round'] == selected_round]
   else:
      filtered_data = filtered_data
      feedback_data = feedback_data

   if selected_event!="All events":
      filtered_data = filtered_data[filtered_data['Event'] == selected_round]
      feedback_data = feedback_data[feedback_data['Event'] == selected_round]
   else:
      filtered_data = filtered_data
      feedback_data = feedback_data


   #Get # of competitions
   number_of_competitions = filtered_data.shape[0]


   filtered_data["Avg Rank"] = filtered_data.groupby('Name')['Rank'].transform('mean')

   st.text(f'Average rank: {filtered_data["Avg Rank"].iloc[0]}')
   st.text(f'Number of pieces of feedback: {number_of_competitions}')

   #Get average round by chart
   grouped_df = feedback_data.groupby(['Name', 'Round']).mean('Rank').reset_index()
   fig, ax = plt.subplots()
   for label, group_df in grouped_df.groupby('Name'):
      group_df.plot(x='Round', y='Rank', ax=ax, label=label, kind='bar', edgecolor='black')

   # Enhancing the plot
   ax.set_xlabel('Round')
   ax.set_ylabel('Rank')
   ax.set_title(f'Average Performance for {selected_name}, by Round')
   ax.get_legend().remove()
   plt.xticks(rotation=90)  # Rotates labels to make them readable
   st.pyplot(plt)


   categories = ['blocking','gesture','character','story','diction','enunciation','eye','professional']

   # Sum the specified categories for the selected name
   sum_by_category = filtered_data[categories].sum()

   # Convert to DataFrame for easier display in Streamlit
   sum_by_category_df = sum_by_category.reset_index()
   sum_by_category_df.columns = ['Category', 'Sum of 1s']

   # Plotting the sums for each category by selected name
   fig, ax = plt.subplots()
   ax.bar(sum_by_category_df['Category'], sum_by_category_df['Sum of 1s'])
   ax.set_title(f'Feedback for {selected_name}')
   ax.set_xticklabels(sum_by_category_df['Category'], rotation=90)

   # Display the plot
   st.pyplot(fig)

   #feedback_data = feedback_data.sort_values(by=['Event','Round'])

   for i,j in zip(feedback_data['Feedback'],feedback_data['Event']):
      st.text(str(j))
      st.text(str(i))
      st.text("*******\n\n")


#Page 2: Judges
# Load data
with tab2:
   streamlit_dataframe = pd.read_excel(data_path)
   streamlit_dataframe['Rank'] = streamlit_dataframe['Feedback'].str.extract(r'Rank:\s*(\d+)', expand=False).astype(float)
   streamlit_dataframe["Avg Rank"] = streamlit_dataframe.groupby('Judge')['Rank'].transform('mean')


   print(streamlit_dataframe)

   st.title('Data by Judge')


   # Dropdown to select a name
   selected_name = st.selectbox('Select a Name:', streamlit_dataframe['Judge'].unique())

   # Filter data for the selected name
   filtered_data = streamlit_dataframe[streamlit_dataframe['Judge'] == selected_name]
   feedback_data = streamlit_dataframe[streamlit_dataframe['Judge'] == selected_name]


   #Get # of competitions
   number_of_competitions = filtered_data.shape[0]


   st.text(f'Average rank: {filtered_data["Avg Rank"].iloc[0]}')
   st.text(f'Number of competitions: {number_of_competitions}')

   categories = ['blocking','gesture','character','story','diction','enunciation','eye','professional']

   # Sum the specified categories for the selected name
   sum_by_category = filtered_data[categories].sum()

   # Convert to DataFrame for easier display in Streamlit
   sum_by_category_df = sum_by_category.reset_index()
   sum_by_category_df.columns = ['Category', 'Sum of 1s']

   # Display the results in a table
   st.dataframe(sum_by_category_df)

   # Plotting the sums for each category by selected name
   fig, ax = plt.subplots()
   ax.bar(sum_by_category_df['Category'], sum_by_category_df['Sum of 1s'])
   ax.set_ylabel('Sum of 1s')
   ax.set_title(f'Sum of "1s" in Categories for {selected_name}')
   ax.set_xticklabels(sum_by_category_df['Category'], rotation=90)
   ax.bar_label(ax.containers[0])

   # Display the plot
   st.pyplot(fig)

   #feedback_data = feedback_data.sort_values(by=['Event','Round'])

   for i,j in zip(feedback_data['Feedback'],feedback_data['Event']):
      st.text(str(j))
      st.text(str(i))
      st.text("*******\n\n")