from fuzzywuzzy import process, fuzz
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


   # Dropdown to select a name
   selected_name = st.selectbox('Select a student:', streamlit_dataframe['Name'].unique())


   #Search terms

   def fuzzy_search(query, choices, threshold):
      """Return a list of matches for a given query within a list of choices, including exact matches."""
      # Exact matches
      query = str(query)
      exact_matches = [choice for choice in choices if query.lower() in str(choice).lower()]

      # Fuzzy matches
      fuzzy_matches = process.extractBests(query, choices, score_cutoff=threshold)
      fuzzy_matches = [match[0] for match in fuzzy_matches]

      # Combine and deduplicate
      return list(set(exact_matches + fuzzy_matches))


   # Input for search terms
   search_terms = st.text_input('Enter search terms (comma separated). Leave blank if no specific terms are desired. To get most accurate search use root of word (i.e., "charact" instead of "characters"):')

   # Convert search terms to a list
   if search_terms:
      search_terms_list = [term.strip() for term in search_terms.split(',')]
   else:
      search_terms_list = []

   # Threshold slider
   threshold = st.slider('Fuzzy matching threshold', 0, 100, 80)

   if search_terms_list:
      matches = []
      for term in search_terms_list:
         matches.extend(fuzzy_search(term, streamlit_dataframe['Feedback'], threshold))
      matches = list(set(matches))  # Remove duplicates

      # Filter DataFrame based on matches
      streamlit_dataframe2 = streamlit_dataframe[streamlit_dataframe['Feedback'].isin(matches)]
   else:
      streamlit_dataframe2 = streamlit_dataframe



   # Filter data for the selected name
   filtered_data = streamlit_dataframe2[streamlit_dataframe2['Name'] == selected_name]
   feedback_data = streamlit_dataframe2[streamlit_dataframe2['Name'] == selected_name]



   # Add "All events' option
   events = []
   for i in filtered_data.Event:
      if i not in events:
         events.append(i)
      else:
         pass
   events = ["All events"] + events

   selected_event = st.selectbox('Select an event:', events)


   if selected_event!="All events":
      filtered_data = filtered_data[filtered_data['Event'] == selected_event]
      feedback_data = feedback_data[feedback_data['Event'] == selected_event]
   else:
      filtered_data = filtered_data
      feedback_data = feedback_data


   rounds = []
   for i in filtered_data.Round:
      if i not in rounds:
         rounds.append(i)
      else:
         pass
   rounds = ["All rounds"] + rounds

   selected_round = st.selectbox('Select a round:', rounds)

   if selected_round!="All rounds":
      filtered_data = filtered_data[filtered_data['Round'] == selected_round]
      feedback_data = feedback_data[feedback_data['Round'] == selected_round]
   else:
      filtered_data = filtered_data
      feedback_data = feedback_data


   judges = []
   for i in filtered_data.Judge:
      if i not in rounds:
         judges.append(i)
      else:
         pass
   judges = ["All rounds"] + judges

   selected_judge = st.selectbox('Select a judge:', judges)

   if selected_judge!="All rounds":
      filtered_data = filtered_data[filtered_data['Judge'] == selected_judge]
      feedback_data = feedback_data[feedback_data['Judge'] == selected_judge]
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

   for feedback,event in zip(feedback_data['Feedback'],feedback_data['Event']):
      highlighted_feedback = feedback
      for term in search_terms_list:
         if term.lower() in highlighted_feedback.lower():
            highlighted_feedback = highlighted_feedback.replace(term, f'<mark>{term}</mark>')
            highlighted_feedback = highlighted_feedback.replace(term, f'<mark>{term}</mark>')
      st.markdown(f'**Event:** {event}')
      st.markdown(highlighted_feedback, unsafe_allow_html=True)
      st.markdown("*******\n\n")


#Page 2: Judges
# Load data
with tab2:
   streamlit_dataframe = pd.read_excel(data_path)

   print(streamlit_dataframe)

   st.title(f'Data by Judge')


   # Dropdown to select a name
   selected_judge = st.selectbox('Select a judge:', streamlit_dataframe['Judge'].unique())

   # Filter data for the selected name
   filtered_data = streamlit_dataframe[streamlit_dataframe['Judge'] == selected_judge]
   feedback_data = streamlit_dataframe[streamlit_dataframe['Judge'] == selected_judge]



   # Add "All events' option
   events2 = []
   for i in filtered_data.Event:
      if i not in events2:
         events2.append(i)
      else:
         pass
   events = ["All events"] + events2

   selected_event2 = st.selectbox('Select an event:', events2)


   if selected_event!="All events":
      filtered_data = filtered_data[filtered_data['Event'] == selected_event2]
      feedback_data = feedback_data[feedback_data['Event'] == selected_event2]
   else:
      filtered_data = filtered_data
      feedback_data = feedback_data


   rounds2 = []
   for i in filtered_data.Round:
      if i not in rounds2:
         rounds2.append(i)
      else:
         pass
   rounds = ["All rounds"] + rounds2

   selected_round2 = st.selectbox('Select a round:', rounds2)

   if selected_round!="All rounds":
      filtered_data = filtered_data[filtered_data['Round'] == selected_round2]
      feedback_data = feedback_data[feedback_data['Round'] == selected_round2]
   else:
      filtered_data = filtered_data
      feedback_data = feedback_data


   #Get # of competitions
   number_of_competitions = filtered_data.shape[0]


   filtered_data["Avg Rank"] = filtered_data.groupby('Judge')['Rank'].transform('mean')

   st.text(f'Average rank: {filtered_data["Avg Rank"].iloc[0]}')
   st.text(f'Number of pieces of feedback: {number_of_competitions}')

   #Get average round by chart
   grouped_df = feedback_data.groupby(['Judge', 'Round']).mean('Rank').reset_index()
   fig, ax = plt.subplots()
   for label, group_df in grouped_df.groupby('Judge'):
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
   ax.set_title(f'Feedback for {selected_judge}')
   ax.set_xticklabels(sum_by_category_df['Category'], rotation=90)

   # Display the plot
   st.pyplot(fig)

   #feedback_data = feedback_data.sort_values(by=['Event','Round'])

   for i,j in zip(feedback_data['Feedback'],feedback_data['Event']):
      st.text(str(j))
      st.text(str(i))
      st.text("*******\n\n")