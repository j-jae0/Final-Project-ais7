import streamlit as st
import pandas as pd
import seaborn as sns
import webbrowser
from bokeh.models.widgets import Div

# st.set_page_config(layout="wide")

# 폰트 적용 
with open( "style.css" ) as css:
    st.markdown(f'<style>{css.read()}</style>' , unsafe_allow_html= True)

st.markdown(
    """
    <style>
    input {
        font-size: 0.8rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 데이터 로드
url = "https://raw.githubusercontent.com/j-jae0/Final-Project-ais7/main/data/%E1%84%8B%E1%85%B0%E1%86%B8%E1%84%90%E1%85%AE%E1%86%AB_%E1%84%89%E1%85%A5%E1%86%B7%E1%84%82%E1%85%A6%E1%84%8B%E1%85%B5%E1%86%AF_%E1%84%85%E1%85%B5%E1%86%BC%E1%84%8F%E1%85%B3.csv"

@st.cache
def load_data():
    df = pd.read_csv(url).drop_duplicates()
    df["title_new"] = df["title"].map(lambda x: x.replace(" ", ""))
    return df

df_link = load_data()

"# 작전명: 띵작을 찾아서"

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False
    st.session_state.placeholder = "작품명을 입력해 주세요."

webtoon_list = sorted(df_link["title"].tolist())

title_input = st.text_input(label="작품명을 입력해 주세요.", 
                            key="webtoon_title",
                            label_visibility="collapsed",
                            disabled=st.session_state.disabled,
                            placeholder=st.session_state.placeholder,
                            )

title_img_df = df_link[df_link["title_new"].str.contains(title_input.replace(" ", ""))].copy()


default_checkbox_value = False
checkbox_statusses = []
detail_statusses = []
test_link = 'https://mblogthumb-phinf.pstatic.net/20110213_48/sk5428_1297564312257kHvzA_JPEG/%B9%AB%C7%D1%B5%B5%C0%FC.E236.110212.SDTV.H264.600p-SeSang%A2%E2.avi_003076042.jpg?type=w2'
if title_input:
    with st.form(key='data_approval'):
        st.write(f"'{title_input}' 에 대한 검색 결과입니다.")
        
        for i in range(title_img_df.shape[0]):
            col, col1, col2 = st.columns([0.5, 2, 10])
            with col:
                st.markdown('')
                checkbox_statusses.append(st.checkbox('', key=str(i), value=default_checkbox_value))
                detail_statusses.append(title_img_df.id.iloc[i])
            with col1:
                st.image(title_img_df["thumbnail"].iloc[i], width=80)
            with col2:
                st.markdown('')
                st.markdown(f'##### {title_img_df["title"].iloc[i]}')

        beta1, beta2, beta3 = st.columns([1, 1, 1])
        with beta2:
            approve_button = st.form_submit_button("정식연재 승격 여부 확인하기")
            
        if approve_button:
            if checkbox_statusses.count(True) == 1:
                index_num = detail_statusses[checkbox_statusses.index(True)]
                # st.write(index_num)
                # webbrowser.open_new(test_link)
                js = "window.location.href = 'https://j-jae0-final-project-ais7-webtoon-tvyirp.streamlit.app/result'"  # Current tab
                html = '<img src onerror="{}">'.format(js)
                div = Div(text=html)
                st.bokeh_chart(div)
            elif checkbox_statusses.count(True) == 0:
                st.warning('작품을 선택해 주세요!')
            else:
                st.warning('작품을 하나만 선택해 주세요!')    
