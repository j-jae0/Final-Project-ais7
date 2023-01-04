import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="웹툰발굴단, 작전명: 띵작을 찾아서",
    page_icon="🔫",
)

# 폰트 적용 
with open( "style.css" ) as css:
    st.markdown(f'<style>{css.read()}</style>' , unsafe_allow_html= True)
    
# 데이터 로드
thumbnail_url = "https://raw.githubusercontent.com/j-jae0/Final-Project-ais7/main/data/item_thumbnail.csv"
final_turn_5_url = "https://raw.githubusercontent.com/j-jae0/Final-Project-ais7/main/data/final_turn_5_df.csv"
final_turn_10_url = "https://raw.githubusercontent.com/j-jae0/Final-Project-ais7/main/data/final_turn_10_df.csv"
maen_turn_5_url = "https://raw.githubusercontent.com/j-jae0/Final-Project-ais7/main/data/turn_5_means_df.csv"
maen_turn_10_url = "https://raw.githubusercontent.com/j-jae0/Final-Project-ais7/main/data/final_turn_10_means.csv"

@st.cache
def info_data():
    df = pd.read_csv(thumbnail_url).drop_duplicates()
    df["title_new"] = df["title"].map(lambda x: x.replace(" ", ""))
    return df

@st.cache
def load_data():
    df = pd.read_csv(final_turn_5_url)
    df = df.fillna(0) 
    return df 

@st.cache
def turn_10_data():
    df = pd.read_csv(final_turn_10_url) # 나중에 url 형태로 바꿔줘야 함
    df = df.fillna(0) 
    return df 

@st.cache
def mean_5_data():
    df = pd.read_csv(maen_turn_5_url)
    return df 

@st.cache
def mean_10_data():
    df = pd.read_csv(maen_turn_10_url, names=mean_10_cols) # 나중에 url 형태로 바꿔줘야 함
    return df 

df_link = info_data()
df_mean_5 = mean_5_data()
df_mean_10 = mean_10_data()
df = load_data()
df10 = turn_10_data()

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False
    st.session_state.placeholder = "작품명을 입력해 주세요."

if "title_id" not in st.session_state:
    st.session_state.title_id = ""
    st.session_state.title_name = ""
    
if "page1" not in st.session_state:
    st.session_state.page1 = False

if "page2" not in st.session_state:
    st.session_state.page2 = False
    st.session_state.per_5 = "" # 5회차 기준 승격 확률
    st.session_state.per_10 = "" # 10회차 기준 승격 확률
    st.session_state.genre = ""
    st.session_state.max_view = ""
    st.session_state.max_rating = ""
    st.session_state.max_people = ""

webtoon_list = sorted(df_link["title"].tolist())
placeholder = st.empty()
with placeholder.container():
    st.title("작전명: 띵작을 찾아서")
    title_input = st.text_input(label="작품명을 입력해 주세요.", 
                                key=st.session_state.title_id,
                                label_visibility="collapsed",
                                disabled=st.session_state.disabled,
                                placeholder=st.session_state.placeholder,
                                )

    title_img_df = df_link[df_link["title_new"].str.contains(title_input.replace(" ", ""))].copy()
    checkbox_statusses = []
    detail_statusses = []
    default_checkbox_value = False

    if title_input:
        # with st.form(key='data_approval'):
        if title_img_df.shape[0] > 0:
            st.write(f"'{title_input}' 에 대한 검색 결과입니다.")
        else:
            st.write(f"'{title_input}'에 대한 검색 결과가 없습니다. 다시 한번 더 확인해 주세요.🙏")        
        for i in range(title_img_df.shape[0]):
            col, col1, col2= st.columns([0.5, 2, 10])
            with col:
                st.markdown('')
                checkbox_statusses.append(st.checkbox('', key=str(i), value=default_checkbox_value))
                detail_statusses.append([title_img_df.id.iloc[i], title_img_df.title.iloc[i]])
            with col1:
                st.image(title_img_df["thumbnail"].iloc[i], width=80)
            with col2:
                st.markdown('')
                st.markdown(f'##### {title_img_df["title"].iloc[i]}')

        beta1, beta2, beta3 = st.columns([1, 1, 1])
        if title_img_df.shape[0] > 0:
            with beta2:
                st.session_state.page1 = st.button('정식연재 가능성')

            if st.session_state.page1:
                if checkbox_statusses.count(True) == 1:
                    st.session_state["title_id"] = detail_statusses[checkbox_statusses.index(True)][0]
                    st.session_state["title_name"] = detail_statusses[checkbox_statusses.index(True)][-1]
                    st.session_state.page2 = placeholder.empty()
                elif checkbox_statusses.count(True) == 0:
                    st.warning('작품을 선택해 주세요!')
                else:
                    st.warning('작품을 하나만 선택해 주세요!')   

# 입력받은 데이터 정보만 가지는 df 생성
if st.session_state.page2:
    title_id = st.session_state["title_id"]
    df_analy = df[df["id"]==title_id].copy()
    df_analy10 = df10[df10["id"]==title_id].copy()
        
    st.session_state["per_5"] = round(df_analy["5_연재확률"].iloc[0] * 100)
    st.session_state["per_10"] = round(df_analy["10_연재확률"].iloc[0] * 100) 
    st.session_state["genre"] = df_analy["genre"].iloc[0]

    def make_input_df(df_name, col):
        df_name = df_analy[[f"{col}_1", f"{col}_2", f"{col}_3", f"{col}_4", f"{col}_5"]].T.reset_index()
        df_name["index"] = df_name["index"].map(lambda x: int(x.split("_")[-1]))
        df_name["작품"] = f"{st.session_state.title_name}"
        df_name.columns = ["회차", f"{col}", "작품"]
        return df_name

    def total_mean_df(genre, col, case):
        df = df_mean_5.loc[df_mean_5["column"]==genre, [f"{col}_1", f"{col}_2", f"{col}_3", f"{col}_4", f"{col}_5"]].T.reset_index()
        df["index"] = df["index"].map(lambda x: int(x.split("_")[-1]))
        df["작품"] = case
        df.columns = ["회차", f"{col}", "작품"]
        return df

    # 5회차  
    # 정식연재O, 주요지표별 평균값
    total_view_mean_df_5 = total_mean_df("total_mean", "view", "정식연재 성공작")
    total_positive_mean_df_5 = total_mean_df("total_mean", "positive", "정식연재 성공작")
    total_rating_people_mean_df_5 = total_mean_df("total_mean", "rating_people", "정식연재 성공작")

    # 정식연재O, 동일 작품전개 주요지표별 평균값
    genre_view_mean_df_5 = total_mean_df(st.session_state.genre, "view", "동일 전개방식의 정식연재 성공작")
    genre_positive_mean_df_5 = total_mean_df(st.session_state.genre, "positive", "동일 전개방식의 정식연재 성공작")
    genre_rating_people_mean_df_5 = total_mean_df(st.session_state.genre, "rating_people", "동일 전개방식의 정식연재 성공작")

    # 5회차 기준 주요 피처에 대한 라인그래프용 df 생성
    input_view_5 = make_input_df("input_view_5", "view")
    input_positive_5 = make_input_df("input_positive_5", "positive")
    input_rating_people_5 = make_input_df("input_rating_people_5", "rating_people")

    # 전체 케이스 묶은 df 만들기
    df_view_5 = pd.concat([input_view_5, total_view_mean_df_5, genre_view_mean_df_5])
    df_positive_5 = pd.concat([input_positive_5, total_positive_mean_df_5, genre_positive_mean_df_5])
    df_rating_people_5 = pd.concat([input_rating_people_5, total_rating_people_mean_df_5, genre_rating_people_mean_df_5])

    def make_input_df10(col):
        df1 = df_analy10[[f"{col}_1", f"{col}_2", f"{col}_3", f"{col}_4", f"{col}_5"]].T.reset_index()
        df2 = df_analy10[[f"{col}_6", f"{col}_7", f"{col}_8", f"{col}_9", f"{col}_10"]].T.reset_index()
        df = pd.concat([df1, df2])
        df["index"] = df["index"].map(lambda x: int(x.split("_")[-1]))
        df["작품"] = f"{st.session_state.title_name}"
        df.columns = ["회차", col, "작품"]
        return df

    def total_mean_df10(genre, col, case):
        df = df_mean_10.loc[df_mean_10["type"]==col, ["index", genre]]
        df["작품"] = case
        df.columns = ["회차", col, "작품"]
        return df

    # 10회차  
    # 정식연재O, 주요지표별 평균값
    total_positive_mean_df_10 = total_mean_df10("전체", "긍정댓글", "정식연재 성공작")
    total_unreco_sum_mean_df_10 = total_mean_df10("전체", "비공감", "정식연재 성공작")
    total_rating_people_mean_df_10 = total_mean_df10("전체", "총별점수", "정식연재 성공작")

    # 정식연재O, 동일 작품전개 주요지표별 평균값
    genre_positive_mean_df_10 = total_mean_df10(st.session_state.genre, "긍정댓글", "동일 전개방식의 정식연재 성공작")
    genre_unreco_sum_mean_df_10 = total_mean_df10(st.session_state.genre, "비공감", "동일 전개방식의 정식연재 성공작")
    genre_rating_people_mean_df_10 = total_mean_df10(st.session_state.genre, "총별점수", "동일 전개방식의 정식연재 성공작")

    # 10회차 기준 주요 피처에 대한 라인그래프용 df 생성
    input_unreco_sum_10 = make_input_df10("비공감")
    input_positive_10 = make_input_df10("긍정댓글")
    input_rating_people_10 = make_input_df10("총별점수")

    # 전체 케이스 묶은 df 만들기
    df_unreco_sum_10 = pd.concat([input_unreco_sum_10, total_unreco_sum_mean_df_10,  genre_unreco_sum_mean_df_10])
    df_positive_10 = pd.concat([input_positive_10, total_positive_mean_df_10, genre_positive_mean_df_10])
    df_rating_people_10 = pd.concat([input_rating_people_10, total_rating_people_mean_df_10, genre_rating_people_mean_df_10])
    
    # 다음 과정으로 넘어가기
    if st.session_state.page1 and checkbox_statusses.count(True) == 1:
        placeholder2 = st.empty()
        with st.container():
            st.write(f"<h1 style='text-align: center;'>{st.session_state.title_name} 의 정식연재 확률은?</h1>", unsafe_allow_html=True)
            st.write(f"<small style='text-align: center; color:gray'>5회차 기준, </small><h1 style='text-align: center; color:red'>{st.session_state.per_5}%</span>", unsafe_allow_html=True)

            # Tab 을 이용해 주요 피처 3개에 대한 분석결과를 제공한다.
            if st.session_state["per_10"] != 0:
                tab, tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Report", "📈 5회차: Top1", "📈 5회차: Top2", "📈 5회차: Top3",
                                                                        "📈 10회차: Top1", "📈 10회차: Top2", "📈 10회차: Top2"])
                with tab:
                    st.caption("💡 위 탭을 통해 확률예측에 가장 많은 영향을 주었던 지표 Top 3 별 분석결과를 확인할 수 있습니다.")
                        # st.write(f"**조회수**는 ?? 번째 회차에서 가장 높습니다.", unsafe_allow_html=True)
                        # """
                        # - {}에서 ~!의 결과는 n 회차입니다.
                        # - 에서 ~의 결과는 s 입니다.
                        # - 에서의 ~~~ 결과는 bbb 입니다.
                        # """
                with tab1:
                    st.caption("💡 위 탭을 통해 확률예측에 가장 많은 영향을 주었던 지표 Top 3 별 분석결과를 확인할 수 있습니다.")
                    st.subheader("👉 5회차에서의 긍정적인 댓글의 수")
                    #st.write()
                    fig1 = px.bar(
                                    df_positive_5[df_positive_5["회차"]==5],
                                    x="작품",
                                    y="positive",
                                    # title="정식연재 작품과의 5회차에서의 긍정적인 댓글의 수 비교",
                                    color_discrete_sequence=["#00d364", "#F2F3F4", "#F2F3F4"],
                                    color="작품",
                                    labels={"작품": "CASE", "positive": "긍정적인 댓글의 수"}
                                    )
                    fig1.update_layout({"showlegend":False, 
                                            "plot_bgcolor":"rgba(0, 0, 0, 0)", 
                                            "paper_bgcolor":"rgba(0, 0, 0, 0)"})
                    fig1.update_xaxes(linecolor='#515A5A', gridcolor='#F4F6F6')                        
                    fig1.update_yaxes(linecolor='#515A5A', gridcolor='#F4F6F6')
                    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)
                                
                    st.subheader("👉 1~5회차에서의 긍정적인 댓글의 수")
                    fig2 = px.line(
                                        df_positive_5,
                                        x="회차",
                                        y="positive",
                                        color_discrete_sequence=["#00d364", "#D0D3D4", "#D0D3D4"],
                                        color="작품",
                                        labels={"작품": "CASE", "positive": "긍정적인 댓글의 수"},
                                        markers=True)
                    fig2.update_xaxes(title_text="회차")
                    fig2.update_layout({"showlegend":True, 
                                                "plot_bgcolor":"rgba(0, 0, 0, 0)", 
                                                "paper_bgcolor":"rgba(0, 0, 0, 0)"})
                    fig2.update_xaxes(linecolor='#515A5A', gridcolor='#F4F6F6')
                    fig2.update_yaxes(linecolor='#515A5A', gridcolor='#F4F6F6')
                    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

                with tab2:
                    st.caption("💡 위 탭을 통해 확률예측에 가장 많은 영향을 주었던 지표 Top 3 별 분석결과를 확인할 수 있습니다.")
                    st.subheader("👉 1회차에서의 조회 수")
                    fig = px.bar(
                                    df_view_5[df_view_5["회차"]==1],
                                    x="작품",
                                    y="view",
                                    # title="정식연재 작품과의 5회차에서의 긍정적인 댓글의 수 비교",
                                    color_discrete_sequence=["#00d364", "#F2F3F4", "#F2F3F4"],
                                    color="작품",
                                    labels={"작품": "CASE", "view": "조회 수"}
                                    )
                    fig.update_layout({"showlegend":False, 
                                            "plot_bgcolor":"rgba(0, 0, 0, 0)", 
                                            "paper_bgcolor":"rgba(0, 0, 0, 0)"})
                    fig.update_xaxes(linecolor='#515A5A', gridcolor='#F4F6F6')
                    fig.update_yaxes(linecolor='#515A5A', gridcolor='#F4F6F6')
                    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

                    st.subheader("👉 1~5회차에서의 조회 수")
                    fig2 = px.line(
                                    df_view_5,
                                    x="회차",
                                    y="view",
                                    color_discrete_sequence=["#00d364", "#D0D3D4", "#D0D3D4"],
                                    color="작품",
                                    labels={"작품": "CASE", "view": "조회 수"},
                                    markers=True)
                    fig2.update_xaxes(title_text="회차")
                    fig2.update_layout({"showlegend":True, 
                                                "plot_bgcolor":"rgba(0, 0, 0, 0)", 
                                                "paper_bgcolor":"rgba(0, 0, 0, 0)"})
                    fig2.update_xaxes(linecolor='#515A5A', gridcolor='#F4F6F6')
                    fig2.update_yaxes(linecolor='#515A5A', gridcolor='#F4F6F6')
                    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

                with tab3:
                    st.caption("💡 위 탭을 통해 확률예측에 가장 많은 영향을 주었던 지표 Top 3 별 분석결과를 확인할 수 있습니다.")
                    st.subheader("👉 5회차에서의 투표받은 총 별점 수")
                    fig = px.bar(
                                    df_rating_people_5[df_rating_people_5["회차"]==5],
                                    x="작품",
                                    y="rating_people",
                                    # title="정식연재 작품과의 5회차에서의 긍정적인 댓글의 수 비교",
                                    color_discrete_sequence=["#00d364", "#F2F3F4", "#F2F3F4"],
                                    color="작품",
                                    labels={"작품": "CASE", "rating_people": "투표받은 총 별점 수"}
                                    )
                    fig.update_layout({"showlegend":False, 
                                                "plot_bgcolor":"rgba(0, 0, 0, 0)", 
                                                "paper_bgcolor":"rgba(0, 0, 0, 0)"})
                    fig.update_xaxes(linecolor='#515A5A', gridcolor='#F4F6F6')
                    fig.update_yaxes(linecolor='#515A5A', gridcolor='#F4F6F6')
                    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
                                
                    st.subheader("👉 1~5회차에서의 투표받은 총 별점 수")
                    fig2 = px.line(
                                        df_rating_people_5,
                                        x="회차",
                                        y="rating_people",
                                        color_discrete_sequence=["#00d364", "#D0D3D4", "#D0D3D4"],
                                        color="작품",
                                        labels={"작품": "CASE", "rating_people": "투표받은 총 별점 수"},
                                        markers=True)
                    fig2.update_xaxes(title_text="회차")
                    fig2.update_layout({"showlegend":True, 
                                                "plot_bgcolor":"rgba(0, 0, 0, 0)", 
                                                "paper_bgcolor":"rgba(0, 0, 0, 0)"})
                    fig2.update_xaxes(linecolor='#515A5A', gridcolor='#F4F6F6')
                    fig2.update_yaxes(linecolor='#515A5A', gridcolor='#F4F6F6')
                    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)
                
                
                with tab4:
                    st.caption("💡 위 탭을 통해 확률예측에 가장 많은 영향을 주었던 지표 Top 3 별 분석결과를 확인할 수 있습니다.")
                    # 10회차 긍정
                    st.subheader("👉 10회차에서의 긍정적인 댓글의 수")
                    fig = px.bar(
                                    df_positive_10[df_positive_10["회차"]==10],
                                    x="작품",
                                    y="positive",
                                    # title="정식연재 작품과의 5회차에서의 긍정적인 댓글의 수 비교",
                                    color_discrete_sequence=["#00d364", "#F2F3F4", "#F2F3F4"],
                                    color="작품",
                                    labels={"작품": "CASE", "positive": "긍정적인 댓글의 수"}
                                    )
                    fig.update_layout({"showlegend":False, 
                                                "plot_bgcolor":"rgba(0, 0, 0, 0)", 
                                                "paper_bgcolor":"rgba(0, 0, 0, 0)"})
                    fig.update_xaxes(linecolor='#515A5A', gridcolor='#F4F6F6')
                    fig.update_yaxes(linecolor='#515A5A', gridcolor='#F4F6F6')
                    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
                                
                    st.subheader("👉 1~10회차에서의 긍정적인 댓글의 수")
                    fig2 = px.line(
                                        df_positive_10,
                                        x="회차",
                                        y="positive",
                                        color_discrete_sequence=["#00d364", "#D0D3D4", "#D0D3D4"],
                                        color="작품",
                                        labels={"작품": "CASE", "positive": "긍정적인 댓글의 수"},
                                        markers=True)
                    fig2.update_xaxes(title_text="회차")
                    fig2.update_layout({"showlegend":True, 
                                                "plot_bgcolor":"rgba(0, 0, 0, 0)", 
                                                "paper_bgcolor":"rgba(0, 0, 0, 0)"})
                    fig2.update_xaxes(linecolor='#515A5A', gridcolor='#F4F6F6')
                    fig2.update_yaxes(linecolor='#515A5A', gridcolor='#F4F6F6')
                    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)
                    
                with tab5:
                    st.caption("💡 위 탭을 통해 확률예측에 가장 많은 영향을 주었던 지표 Top 3 별 분석결과를 확인할 수 있습니다.")
                    # 10회차 긍정
                    st.subheader("👉 2회차에서의 투표받은 총 별점 수")
                    fig = px.bar(
                                    df_rating_people_10[df_rating_people_10["회차"]==2],
                                    x="작품",
                                    y="rating_people",
                                    # title="정식연재 작품과의 5회차에서의 투표받은 총 별점 수 비교",
                                    color_discrete_sequence=["#00d364", "#F2F3F4", "#F2F3F4"],
                                    color="작품",
                                    labels={"작품": "CASE", "rating_people": "투표받은 총 별점 수"}
                                    )
                    fig.update_layout({"showlegend":False, 
                                                "plot_bgcolor":"rgba(0, 0, 0, 0)", 
                                                "paper_bgcolor":"rgba(0, 0, 0, 0)"})
                    fig.update_xaxes(linecolor='#515A5A', gridcolor='#F4F6F6')
                    fig.update_yaxes(linecolor='#515A5A', gridcolor='#F4F6F6')
                    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
                                
                    st.subheader("👉 1~10회차에서의 투표받은 총 별점 수")
                    fig2 = px.line(
                                        df_rating_people_10,
                                        x="회차",
                                        y="rating_people",
                                        color_discrete_sequence=["#00d364", "#D0D3D4", "#D0D3D4"],
                                        color="작품",
                                        labels={"작품": "CASE", "rating_people": "투표받은 총 별점 수"},
                                        markers=True)
                    fig2.update_xaxes(title_text="회차")
                    fig2.update_layout({"showlegend":True, 
                                                "plot_bgcolor":"rgba(0, 0, 0, 0)", 
                                                "paper_bgcolor":"rgba(0, 0, 0, 0)"})
                    fig2.update_xaxes(linecolor='#515A5A', gridcolor='#F4F6F6')
                    fig2.update_yaxes(linecolor='#515A5A', gridcolor='#F4F6F6')
                    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)    
                    
                with tab6:
                    st.caption("💡 위 탭을 통해 확률예측에 가장 많은 영향을 주었던 지표 Top 3 별 분석결과를 확인할 수 있습니다.")
                    # 10회차 긍정
                    st.subheader("👉 5회차에서의 댓글의 총 비공감 수")
                    fig = px.bar(
                                    df_unreco_sum_10[df_unreco_sum_10["회차"]==5],
                                    x="작품",
                                    y="unreco_sum",
                                    color_discrete_sequence=["#00d364", "#F2F3F4", "#F2F3F4"],
                                    color="작품",
                                    labels={"작품": "CASE", "unreco_sum": "댓글의 총 비공감 수"}
                                    )
                    fig.update_layout({"showlegend":False, 
                                                "plot_bgcolor":"rgba(0, 0, 0, 0)", 
                                                "paper_bgcolor":"rgba(0, 0, 0, 0)"})
                    fig.update_xaxes(linecolor='#515A5A', gridcolor='#F4F6F6')
                    fig.update_yaxes(linecolor='#515A5A', gridcolor='#F4F6F6')
                    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
                                
                    st.subheader("👉 1~10회차에서의 댓글의 총 비공감 수")
                    fig2 = px.line(
                                        df_unreco_sum_10,
                                        x="회차",
                                        y="unreco_sum",
                                        color_discrete_sequence=["#00d364", "#D0D3D4", "#D0D3D4"],
                                        color="작품",
                                        labels={"작품": "CASE", "unreco_sum": "댓글의 총 비공감 수"},
                                        markers=True)
                    fig2.update_xaxes(title_text="회차")
                    fig2.update_layout({"showlegend":True, 
                                                "plot_bgcolor":"rgba(0, 0, 0, 0)", 
                                                "paper_bgcolor":"rgba(0, 0, 0, 0)"})
                    fig2.update_xaxes(linecolor='#515A5A', gridcolor='#F4F6F6')
                    fig2.update_yaxes(linecolor='#515A5A', gridcolor='#F4F6F6')
                    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)    
                    
############################ 5회차까지만 있는 경우 ############################

            
            else:
                tab, tab1, tab2, tab3 = st.tabs(["Report", "📈 5회차: Top1", "📈 5회차: Top2", "📈 5회차: Top3"])
                with tab:
                    st.caption("💡 위 탭을 통해 확률예측에 가장 많은 영향을 주었던 지표 Top 3 별 분석결과를 확인할 수 있습니다.")
                        # st.write(f"**조회수**는 ?? 번째 회차에서 가장 높습니다.", unsafe_allow_html=True)
                        # """
                        # - {}에서 ~!의 결과는 n 회차입니다.
                        # - 에서 ~의 결과는 s 입니다.
                        # - 에서의 ~~~ 결과는 bbb 입니다.
                        # """
                with tab1:
                    st.caption("💡 위 탭을 통해 확률예측에 가장 많은 영향을 주었던 지표 Top 3 별 분석결과를 확인할 수 있습니다.")
                    st.subheader("👉 5회차에서의 긍정적인 댓글의 수")
                    #st.write()
                    fig1 = px.bar(
                                    df_positive_5[df_positive_5["회차"]==5],
                                    x="작품",
                                    y="positive",
                                    # title="정식연재 작품과의 5회차에서의 긍정적인 댓글의 수 비교",
                                    color_discrete_sequence=["#00d364", "#F2F3F4", "#F2F3F4"],
                                    color="작품",
                                    labels={"작품": "CASE", "positive": "긍정적인 댓글의 수"}
                                    )
                    fig1.update_layout({"showlegend":False, 
                                            "plot_bgcolor":"rgba(0, 0, 0, 0)", 
                                            "paper_bgcolor":"rgba(0, 0, 0, 0)"})
                    fig1.update_xaxes(linecolor='#515A5A', gridcolor='#F4F6F6')                        
                    fig1.update_yaxes(linecolor='#515A5A', gridcolor='#F4F6F6')
                    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)
                                
                    st.subheader("👉 1~5회차에서의 긍정적인 댓글의 수")
                    fig2 = px.line(
                                        df_positive_5,
                                        x="회차",
                                        y="positive",
                                        color_discrete_sequence=["#00d364", "#D0D3D4", "#D0D3D4"],
                                        color="작품",
                                        labels={"작품": "CASE", "positive": "긍정적인 댓글의 수"},
                                        markers=True)
                    fig2.update_xaxes(title_text="회차")
                    fig2.update_layout({"showlegend":True, 
                                                "plot_bgcolor":"rgba(0, 0, 0, 0)", 
                                                "paper_bgcolor":"rgba(0, 0, 0, 0)"})
                    fig2.update_xaxes(linecolor='#515A5A', gridcolor='#F4F6F6')
                    fig2.update_yaxes(linecolor='#515A5A', gridcolor='#F4F6F6')
                    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

                with tab2:
                    st.caption("💡 위 탭을 통해 확률예측에 가장 많은 영향을 주었던 지표 Top 3 별 분석결과를 확인할 수 있습니다.")
                    st.subheader("👉 1회차에서의 조회 수")
                    fig = px.bar(
                                    df_view_5[df_view_5["회차"]==1],
                                    x="작품",
                                    y="view",
                                    # title="정식연재 작품과의 5회차에서의 긍정적인 댓글의 수 비교",
                                    color_discrete_sequence=["#00d364", "#F2F3F4", "#F2F3F4"],
                                    color="작품",
                                    labels={"작품": "CASE", "view": "조회 수"}
                                    )
                    fig.update_layout({"showlegend":False, 
                                            "plot_bgcolor":"rgba(0, 0, 0, 0)", 
                                            "paper_bgcolor":"rgba(0, 0, 0, 0)"})
                    fig.update_xaxes(linecolor='#515A5A', gridcolor='#F4F6F6')
                    fig.update_yaxes(linecolor='#515A5A', gridcolor='#F4F6F6')
                    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

                    st.subheader("👉 1~5회차에서의 조회 수")
                    fig2 = px.line(
                                    df_view_5,
                                    x="회차",
                                    y="view",
                                    color_discrete_sequence=["#00d364", "#D0D3D4", "#D0D3D4"],
                                    color="작품",
                                    labels={"작품": "CASE", "view": "조회 수"},
                                    markers=True)
                    fig2.update_xaxes(title_text="회차")
                    fig2.update_layout({"showlegend":True, 
                                                "plot_bgcolor":"rgba(0, 0, 0, 0)", 
                                                "paper_bgcolor":"rgba(0, 0, 0, 0)"})
                    fig2.update_xaxes(linecolor='#515A5A', gridcolor='#F4F6F6')
                    fig2.update_yaxes(linecolor='#515A5A', gridcolor='#F4F6F6')
                    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

    
