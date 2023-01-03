import streamlit as st
import pandas as pd
import seaborn as sns

# 폰트 적용 
with open( "style.css" ) as css:
    st.markdown(f'<style>{css.read()}</style>' , unsafe_allow_html= True)
    
"# 작전명: 띵작을 찾아서"

df_link = pd.read_csv("data/웹툰_섬네일_링크.csv").drop_duplicates()
df_link["title_new"] = df_link["title"].map(lambda x: x.replace(" ", ""))

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False
    st.session_state.placeholder = "ex) 대학 내일"

webtoon_list = sorted(df_link["title"].tolist())

# option = st.selectbox(
#     "작품명을 선택해 주세요.",
#     (webtoon_list),
#     label_visibility=st.session_state.visibility,
#     disabled=st.session_state.disabled,
# )

title_input = st.text_input(label="작품명을 입력해 주세요.", 
                            key="webtoon_title",
                            label_visibility=st.session_state.visibility,
                            disabled=st.session_state.disabled,
                            placeholder=st.session_state.placeholder,
                            )

title_img_df = df_link[df_link["title_new"].str.contains(title_input.replace(" ", ""))].copy()
# img_link_list["title"].iloc[0], img_link_list["thumbnail"].iloc[0]

if title_input:
    for i in range(title_img_df.shape[0]):
        col1, col2 = st.columns([1, 5])
        with col1:
            st.image(title_img_df["thumbnail"].iloc[i])
        with col2:
            st.markdown(f'{title_img_df["title"].iloc[i]}')
            #st.markdown(title_img_df["summary"].iloc[i])


# img_con = st.container()
# img_con.markdown(f"![Alt Text]({img_link})") 
# img_con.write(f"{option}")
