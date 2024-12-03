import streamlit as st
import pandas as pd
from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='競合会社ニュース一覧',)

@st.cache_data
def get_data():
    """Grab data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    DATA_FILENAME = Path(__file__).parent/'data/news.csv'
    raw_df = pd.read_csv(DATA_FILENAME)

# 会社の選択
company_names = data['会社'].unique()
selected_company = st.sidebar.selectbox("会社を選択してください", company_names)

# キーワード検索
keyword = st.sidebar.text_input("キーワードを入力してください")

# 日付フィルタリングのための開始日と終了日を追加
start_date = st.sidebar.date_input("開始日を選択してください", pd.to_datetime(data['日時'].min()))
end_date = st.sidebar.date_input("終了日を選択してください", pd.to_datetime(data['日時'].max()))

# 会社でデータをフィルタリング
filtered_data = data[data['会社'] == selected_company]

# 日付フィルタリング
filtered_data['日時'] = pd.to_datetime(filtered_data['日時'])
filtered_data = filtered_data[(filtered_data['日時'] >= pd.Timestamp(start_date)) &
                              (filtered_data['日時'] <= pd.Timestamp(end_date))]

# キーワードによるフィルタリング
if keyword:
    filtered_data = filtered_data[filtered_data.apply(lambda row: row.astype(str).str.contains(keyword).any(), axis=1)]

# フィルタリングされたデータの表示
if not filtered_data.empty:
    for index, row in filtered_data.iterrows():
        st.markdown(f"### {row['タイトル']}")
        st.write(f"日時: {row['日時']}")
        st.write(f"和訳: {row['和訳']}")
        st.write(f"まとめ: {row['まとめ']}")
        st.write(f"まとめ（和訳）: {row['まとめ（和訳）']}")
        st.markdown(f"[続きを読む]({row['URL']})", unsafe_allow_html=True)
else:
    st.write("該当するニュースが見つかりませんでした。")
