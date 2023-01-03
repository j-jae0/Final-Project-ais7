import streamlit as st
import pandas as pd
import seaborn as sns

# 폰트 적용 
with open( "style.css" ) as css:
    st.markdown(f'<style>{css.read()}</style>' , unsafe_allow_html= True)
    
"# 작전명: 띵작을 찾아서"

def main() :
    df_link = pd.read_csv("https://raw.githubusercontent.com/j-jae0/Final-Project-ais7/main/data/%E1%84%8B%E1%85%B0%E1%86%B8%E1%84%90%E1%85%AE%E1%86%AB_%E1%84%89%E1%85%A5%E1%86%B7%E1%84%82%E1%85%A6%E1%84%8B%E1%85%B5%E1%86%AF_%E1%84%85%E1%85%B5%E1%86%BC%E1%84%8F%E1%85%B3.csv")

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
