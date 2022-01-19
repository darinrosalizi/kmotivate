import time
import pandas as pd
import numpy as np
import streamlit as st
import pickle
import base64

# background setting
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    #background-size: contain;
    #background-repeat: no-repeat;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)


# recommendation function
def getkorean_low(low_pick):
    song_id = np.where(low_pivot.index == low_pick)[0][0]
    distances, suggestions = low_model.kneighbors(low_pivot.iloc[song_id, :].values.reshape(1, -1), n_neighbors=15)

    recommended_low = []
    for i in range(len(suggestions)):
        recommended_low.append(low_pivot.index[suggestions[i]])
        recommended_low.append(low_tempo[suggestions[i]])
    return recommended_low


def getkorean_steady(steady_pick):
    song_id = np.where(steady_pivot.index == steady_pick)[0][0]
    distances, suggestions = steady_model.kneighbors(steady_pivot.iloc[song_id, :].values.reshape(1, -1), n_neighbors=15)

    recommended_steady = []
    for i in range(len(suggestions)):
        recommended_steady.append(steady_pivot.index[suggestions[i]])
        recommended_steady.append(steady_tempo[suggestions[i]])
    return recommended_steady


def getkorean_power(power_pick):
    song_id = np.where(power_pivot.index == power_pick)[0][0]
    distances, suggestions = power_model.kneighbors(power_pivot.iloc[song_id, :].values.reshape(1, -1), n_neighbors=15)

    recommended_power = []
    for i in range(len(suggestions)):
        recommended_power.append(power_pivot.index[suggestions[i]])
        recommended_power.append(power_tempo[suggestions[i]])
    return recommended_power


def getkorean_dance(dance_pick):
     song_id = np.where(dance_pivot.index == dance_pick)[0][0]
     distances, suggestions = dance_model.kneighbors(dance_pivot.iloc[song_id, :].values.reshape(1, -1), n_neighbors=15)

     recommended_dance = []
     for i in range(len(suggestions)):
          recommended_dance.append(dance_pivot.index[suggestions[i]])
          recommended_dance.append(dance_tempo[suggestions[i]])
     return recommended_dance


# import model
low_dict = pickle.load(open('klow_dict.pkl', 'rb'))
low_list = pd.DataFrame(low_dict)
low_pivot = pickle.load(open('low_pivot.pkl', 'rb'))
low_model = pickle.load(open('low_model.pkl', 'rb'))

steady_dict = pickle.load(open('ksteady_dict.pkl', 'rb'))
steady_list = pd.DataFrame(steady_dict)
steady_pivot = pickle.load(open('steady_pivot.pkl', 'rb'))
steady_model = pickle.load(open('steady_model.pkl', 'rb'))

power_dict = pickle.load(open('kpower_dict.pkl', 'rb'))
power_list = pd.DataFrame(power_dict)
power_pivot = pickle.load(open('power_pivot.pkl', 'rb'))
power_model = pickle.load(open('power_model.pkl', 'rb'))

dance_dict = pickle.load(open('kdance_dict.pkl', 'rb'))
dance_list = pd.DataFrame(dance_dict)
dance_pivot = pickle.load(open('dance_pivot.pkl', 'rb'))
dance_model = pickle.load(open('dance_model.pkl', 'rb'))

steady_tempo = steady_list['tempo'].values
low_tempo = low_list['tempo'].values
power_tempo = power_list['tempo'].values
dance_tempo = dance_list['tempo'].values


st.title('KMotivate Recommender System')
st.subheader('Korean Music For Motivating Exercise')
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.caption("Low-Intensity Exercise such as Yoga (75BPM-90BPM)")

with col2:
    st.caption("Steady-Type Exercise such as Jogging (91BPM-120BPM)")

with col3:
    st.caption("Power-Type Exercise such as Weightlifting (121BPM-140BPM)")

with col4:
    st.caption("Dance-Type Exercise such as Zumba (141BPM-200BPM)")

exercise_type = st.selectbox(
     'Type or select exercise type from the dropdown',
    ('Steady Exercise', 'Low Intensity Exercise', 'Power Exercise', 'Dance Exercise'))
st.write('You have selected:', exercise_type)


# redirect function
if exercise_type == 'Dance Exercise':
    set_background('banner5.png')
    dance_pick = st.selectbox('Type or select songs from the dropdown',
                              dance_list['song'].values)
    st.write('You have selected:', dance_pick)

    if st.button('Get Recommendations'):
        st.caption("Note: First table is the song title-artist and the second table is the tempo for each song")
        with st.spinner('Getting it ready for you...'):
            time.sleep(1)
            dance_recommendations = getkorean_dance(dance_pick)
            for i in dance_recommendations:
                st.write(i)
        st.success('There you go!')
        st.balloons()

elif exercise_type == 'Low Intensity Exercise':
    set_background('banner1.png')
    low_pick = st.selectbox('Type or select songs from the dropdown',
                            low_list['song'].values)
    st.write('You have selected:', low_pick)

    if st.button('Get Recommendations'):
        st.caption("Note: First table is the song title-artist and the second table is the tempo for each song")
        with st.spinner('Getting it ready for you...'):
            time.sleep(1)
            low_recommendations = getkorean_low(low_pick)
            for i in low_recommendations:
                st.write(i)
        st.success('There you go!')
        st.balloons()

elif exercise_type == 'Power Exercise':
    set_background('banner4.png')
    power_pick = st.selectbox('Type or select songs from the dropdown',
                               power_list['song'].values)
    st.write('You have selected:', power_pick)

    if st.button('Get Recommendations'):
        st.caption("Note: First table is the song title-artist and the second table is the tempo for each song")
        with st.spinner('Getting it ready for you...'):
            time.sleep(1)
            power_recommendations = getkorean_power(power_pick)
            for i in power_recommendations:
                st.write(i)
        st.success('There you go!')
        st.balloons()

elif exercise_type == 'Steady Exercise':
    set_background('banner2.png')
    steady_pick = st.selectbox('Type or select songs from the dropdown',
                               steady_list['song'].values)
    st.write('You have selected:', steady_pick)

    if st.button('Get Recommendations'):
        st.caption("Note: First table is the song title-artist and the second table is the tempo for each song")
        with st.spinner('Getting it ready for you...'):
            time.sleep(1)
            steady_recommendations = getkorean_steady(steady_pick)
            for i in steady_recommendations:
                st.write(i)
        st.success('There you go!')
        st.balloons()

else:
    st.write('You have not selected an exercise type yet')

