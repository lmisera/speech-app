{
"cells":[
0:{
"cell_type":"code"
"execution_count":4
"id":"6971d859-4e52-4313-944c-ded16bf7fd9d"
"metadata":{}
"outputs":[
0:{
"name":"stderr"
"output_type":"stream"
"text":[
0:"2024-05-26 14:18:37.426 
"
1:"  [33m[1mWarning:[0m to view this Streamlit app on a browser, run it with the following
"
2:"  command:
"
3:"
"
4:"    streamlit run c:\users\lucas\onedrive\python\venv\lib\site-packages\ipykernel_launcher.py [ARGUMENTS]
"
5:"2024-05-26 14:18:37.427 Session state does not function when running a script without `streamlit run`
"
]
}
]
"source":[
0:"import streamlit as st
"
1:"
"
2:"#Title of the application
"
3:"st.title('Simple Addition Calculator')
"
4:"
"
5:"# Inputs: Get two numbers from the user
"
6:"number1 = st.number_input('Enter the first number', value=0)
"
7:"number2 = st.number_input('Enter the second number', value=0)
"
8:"
"
9:"# Processing: Add the two numbers
"
10:"result = number1 + number2
"
11:"
"
12:"# Output: Display the result
"
13:"st.write(f'The result of adding {number1} and {number2} is {result}')"
]
}
]
"metadata":{
"kernelspec":{
"display_name":"Python 3 (ipykernel)"
"language":"python"
"name":"python3"
}
"language_info":{
"codemirror_mode":{
"name":"ipython"
"version":3
}
"file_extension":".py"
"mimetype":"text/x-python"
"name":"python"
"nbconvert_exporter":"python"
"pygments_lexer":"ipython3"
"version":"3.10.2"
}
}
"nbformat":4
"nbformat_minor":5
}