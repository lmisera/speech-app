import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
streamlit_dataframe = pd.read_excel(r'C:\Users\Lucas\OneDrive\python\speech_and_debate\Speech_With_Data.xlsx')
streamlit_dataframe['Rank'] = streamlit_dataframe['Feedback'].str.extract(r'Rank:\s*(\d+)', expand=False).astype(float)
streamlit_dataframe["Avg Rank"] = streamlit_dataframe.groupby('Name')['Rank'].transform('mean')


print(streamlit_dataframe)

st.title('Sum of "1s" in Different Categories by Selected Name')


# Dropdown to select a name
selected_name = st.selectbox('Select a Name:', streamlit_dataframe['Name'].unique())

# Filter data for the selected name
filtered_data = streamlit_dataframe[streamlit_dataframe['Name'] == selected_name]
feedback_data = streamlit_dataframe[streamlit_dataframe['Name'] == selected_name]


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

# Display the plot
st.pyplot(fig)

#feedback_data = feedback_data.sort_values(by=['Event','Round'])

for i in feedback_data['Feedback']:
   st.text(str(i))
