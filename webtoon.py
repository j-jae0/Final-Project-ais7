import streamlit as st
import pandas as pd
import seaborn as sns

# 폰트 적용 
with open( "style.css" ) as css:
    st.markdown(f'<style>{css.read()}</style>' , unsafe_allow_html= True)
    
"# 작전명: 띵작을 찾아서"

def main() :
    df_link = pd.read_csv("data/웹툰_섬네일_링크.csv")

if __name__ == '__main__' :
    main()
    
# @st.cache
# def webtoon_info(URL):
#     df = pd.read_csv(URL)
#     return df

# URL = "data/웹툰_섬네일_링크.csv"
# df_link = webtoon_info(URL)

# df_link = pd.read_csv("/app/final-project-ais7/data/웹툰_섬네일_링크.csv")
# df_link.loc[df_link["title"]=="뱀파이어의 연금술", ["id", "title", "thumbnail"]]

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False
    st.session_state.placeholder = "ex) 대학 내일"

webtoon_list = sorted(df_link["title"].tolist())
option = st.selectbox(
    "작품명을 선택해 주세요.",
    (webtoon_list),
    label_visibility=st.session_state.visibility,
    disabled=st.session_state.disabled,
)

img_link = df_link.loc[df_link["title"]==option, "thumbnail"].iloc[0]

img_con = st.container()
img_con.markdown(f"![Alt Text]({img_link})") 
img_con.write(f"{option}")
