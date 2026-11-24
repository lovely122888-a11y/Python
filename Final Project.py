import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

st.set_page_config(page_title="候選房源地址搜尋", page_icon="📍", layout="centered")
st.title("📍 候選房源地址搜尋")

geolocator = Nominatim(user_agent="permanent_address_finder_tw")

with st.form("search_form"):
    address_query = st.text_input(
        "請輸入地址",
        placeholder="例如：台北市大安區羅斯福路四段1號"
    )
    submitted = st.form_submit_button("🔍 搜尋地址", use_container_width=True, type="primary")

if submitted:
    if not address_query.strip():
        st.warning("⚠️ 請先輸入地址再搜尋。")
    else:
        with st.spinner("正在定位地址..."):
            try:
                location = geolocator.geocode(address_query.strip(), country_codes="tw", timeout=10)
                if location:
                    lat, lon = location.latitude, location.longitude
                    st.success(f"**定位成功：** {location.address}")
                    st.markdown(f"👉 [在 Google Maps 中開啟](https://www.google.com/maps/search/?api=1&query={lat},{lon})")
                    
                    map_df = pd.DataFrame([{"lat": lat, "lon": lon}])
                    st.map(map_df, zoom=16)
                else:
                    st.error("❌ 找不到該地址，請加上完整的縣市與行政區（例如：台北市大安區...）後重試。")
            except GeocoderTimedOut:
                st.error("⏳ 連線逾時，請稍後再試。")
            except Exception as e:
                st.error(f"發生錯誤：{e}")
