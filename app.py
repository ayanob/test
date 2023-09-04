
#ライブラリの読み込み
import time
import streamlit as st
import pandas as pd
import numpy as np

import seaborn as sns
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder


#タイトル
st.title("機械学習アプリ")
st.write("streamlitで実装")

# 以下をサイドバーに表示
st.sidebar.markdown("### 機械学習に用いるcsvファイルを入力してください")
#ファイルアップロード
uploaded_files = st.sidebar.file_uploader("Choose a CSV file", accept_multiple_files= False)
#ファイルがアップロードされたら以下が実行される
if uploaded_files:
    df = pd.read_csv(uploaded_files, encoding='shift_jis')
    df_columns = df.columns
    #データフレームを表示
    st.markdown("### 入力データ")
    st.dataframe(df.style.highlight_max(axis=0))
    #matplotlibで可視化。X軸,Y軸を選択できる
    st.markdown("### 可視化 単変量")
    #データフレームのカラムを選択オプションに設定する
    x = st.sidebar.selectbox("X軸", df_columns)
    y = st.sidebar.selectbox("Y軸", df_columns)
    z = st.sidebar.selectbox("Z軸", df_columns)
    #選択した変数を用いてmtplotlibで可視化

    
    #---------------------
    '''st.sidebar.title('軸の設定')
    xmin=st.sidebar.number_input('x最小値：')
    xmax=st.sidebar.number_input('x最大値：')
    ymin=st.sidebar.number_input('y最小値：')
    ymax=st.sidebar.number_input('y最大値：')
    zmin=st.sidebar.number_input('z最小値：')
    zmax=st.sidebar.number_input('z最大値：')'''
    #---------------------
    #---------------------
    #動的なグラフ
    st.write(
        px.line(df,x,y)
    )
    #---------------------
    #---------------------
    #3D
    st.write(
        px.scatter_3d(df,x,y,z)
    )
    #---------------------
    

    #seabornのペアプロットで可視化。複数の変数を選択できる。
    st.markdown("### 可視化 ペアプロット")
    #データフレームのカラムを選択肢にする。複数選択
    item = st.multiselect("可視化するカラム", df_columns)
    #散布図の色分け基準を１つ選択する。カテゴリ変数を想定
    hue = st.selectbox("色の基準", df_columns)
    
    #実行ボタン（なくてもよいが、その場合、処理を進めるまでエラー画面が表示されてしまう）
    execute_pairplot = st.button("ペアプロット描画")
    #実行ボタンを押したら下記を表示
    if execute_pairplot:
            df_sns = df[item]
            df_sns["hue"] = df[hue]
            
            #streamlit上でseabornのペアプロットを表示させる
            fig = sns.pairplot(df_sns, hue="hue")
            st.pyplot(fig)


    st.markdown("### モデリング")
    #説明変数は複数選択式
    ex = st.multiselect("説明変数を選択してください（複数選択可）", df_columns)

    #目的変数は一つ
    ob = st.selectbox("目的変数を選択してください", df_columns)

    #機械学習のタイプを選択する。
    ml_menu = st.selectbox("実施する機械学習のタイプを選択してください", ["重回帰分析","ロジスティック回帰分析"])
    
    #機械学習のタイプにより以下の処理が分岐
    if ml_menu == "重回帰分析":
            st.markdown("#### 機械学習を実行します")
            execute = st.button("実行")
            
            lr = linear_model.LinearRegression()
            #実行ボタンを押したら下記が進む
            if execute:
                  df_ex = df[ex]
                  df_ob = df[ob]
                  X_train, X_test, y_train, y_test = train_test_split(df_ex.values, df_ob.values, test_size = 0.3)
                  lr.fit(X_train, y_train)
                  #プログレスバー（ここでは、やってる感だけ）
                  my_bar = st.progress(0)
                  
                  for percent_complete in range(100):
                        time.sleep(0.02)
                        my_bar.progress(percent_complete + 1)
                  
                  #metricsで指標を強調表示させる
                  col1, col2 = st.columns(2)
                  col1.metric(label="トレーニングスコア", value=lr.score(X_train, y_train))
                  col2.metric(label="テストスコア", value=lr.score(X_test, y_test))
                  
    #ロジスティック回帰分析を選択した場合
    elif ml_menu == "ロジスティック回帰分析":
            st.markdown("#### 機械学習を実行します")
            execute = st.button("実行")
            
            lr = LogisticRegression()

            #実行ボタンを押したら下記が進む
            if execute:
                  df_ex = df[ex]
                  df_ob = df[ob]
                  X_train, X_test, y_train, y_test = train_test_split(df_ex.values, df_ob.values, test_size = 0.3)
                  lr.fit(X_train, y_train)
                  #プログレスバー（ここでは、やってる感だけ）
                  my_bar = st.progress(0)
                  for percent_complete in range(100):
                        time.sleep(0.02)
                        my_bar.progress(percent_complete + 1)

                  col1, col2 = st.columns(2)
                  col1.metric(label="トレーニングスコア", value=lr.score(X_train, y_train))
                  col2.metric(label="テストスコア", value=lr.score(X_test, y_test))
                  
