import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 한글 폰트 설정
import matplotlib
matplotlib.rc('font', family='Malgun Gothic')   # Windows
matplotlib.rcParams['axes.unicode_minus'] = False

# 페이지 설정
st.set_page_config(
    page_title="제주도 버스 데이터 대시보드",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS 스타일
st.markdown(
    """
    <style>
    /* 전체 페이지 스타일 */
    .main {
        background-color: #f8f9fa;
    }
    
    /* 헤더 스타일 */
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem 0;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        color: #e3f2fd;
        font-size: 1.1rem;
        margin: 0;
    }
    
    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff;
        border-radius: 8px 8px 0 0;
        border: 1px solid #e0e0e0;
        padding: 10px 20px;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #1e3c72;
        color: white;
    }
    
    /* 카드 스타일 */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #1e3c72;
        margin-bottom: 1rem;
    }
    
    .metric-card h3 {
        color: #1e3c72;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }
    
    .metric-card .value {
        font-size: 2rem;
        font-weight: bold;
        color: #2a5298;
    }
    
    /* 차트 컨테이너 */
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
    
    /* 데이터프레임 스타일 */
    .dataframe-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    /* 사이드바 스타일 */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* 반응형 그리드 */
    .responsive-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    /* 푸터 스타일 */
    .footer {
        background: #1e3c72;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

@st.cache_data
def load_clean_data():
    df1_clean = pd.read_csv('cleaned_data/df1_clean.csv')
    df2_clean = pd.read_csv('cleaned_data/df2_clean.csv')
    df5_clean = pd.read_csv('cleaned_data/df5_clean.csv')
    return df1_clean, df2_clean, df5_clean

# 데이터 로드
df1_clean, df2_clean, df5_clean = load_clean_data()

# 메인 헤더
st.markdown(
    """
    <div class="main-header">
        <h1>🚌 제주도 버스 데이터 대시보드</h1>
        <p>제주도 버스 이용 현황을 한눈에 파악할 수 있는 종합 분석 대시보드</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 사이드바 - 주요 지표
with st.sidebar:
    st.markdown("### 📊 주요 지표")
    
    # 전체 이용객수
    total_users = df1_clean['user_count'].sum() if 'user_count' in df1_clean.columns else 0
    st.metric("총 이용객수", f"{total_users:,}명")
    
    # 정류장 수
    total_stations = df5_clean['station_id'].nunique() if 'station_id' in df5_clean.columns else 0
    st.metric("총 정류장 수", f"{total_stations:,}개")
    
    # 노선 수
    total_routes = df2_clean['bus_number'].nunique() if 'bus_number' in df2_clean.columns else 0
    st.metric("총 노선 수", f"{total_routes:,}개")
    
    st.markdown("---")
    
    # 필터 옵션
    st.markdown("### 🔍 필터 옵션")
    if 'user_type' in df1_clean.columns:
        user_types = ['전체'] + list(df1_clean['user_type'].unique())
        selected_user_type = st.selectbox("이용자 유형", user_types)
    
    if 'time_category' in df1_clean.columns:
        time_categories = ['전체'] + list(df1_clean['time_category'].unique())
        selected_time = st.selectbox("시간대", time_categories)

# 탭 구성
tab1, tab2, tab3, tab4 = st.tabs([
    "🗺️ 혼잡도 지도", 
    "📈 정류장/노선 통계", 
    "⏰ 시간대/사용자 패턴", 
    "📅 주말/평일/월별 패턴"
])

# =====================
# Tab1: 혼잡도 지도
# =====================
with tab1:
    st.markdown(
        """
        <div class="chart-container">
            <h3>🗺️ 제주도 버스 정류장 혼잡도 히트맵</h3>
            <p>정류장별 이용객수를 기반으로 한 혼잡도 시각화</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    station_total = df5_clean.groupby(
        ['station_id', 'station_name', 'longitude', 'latitude']
    )['total_user_count'].sum().reset_index()

    jeju_center = [33.361666, 126.551944]
    m = folium.Map(location=jeju_center, zoom_start=10, tiles='cartodbpositron')

    heat_data_total = [
        [row['latitude'], row['longitude'], row['total_user_count']]
        for _, row in station_total.iterrows()
    ]
    HeatMap(
        heat_data_total,
        radius=15,
        name='전체 혼잡도',
        gradient={0.2: 'blue', 0.4: 'cyan', 0.6: 'lime', 0.8: 'yellow', 1: 'red'}
    ).add_to(m)

    # 상위 10개 정류장 마커
    top_stations = station_total.sort_values('total_user_count', ascending=False).head(10)
    for _, row in top_stations.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=folium.Popup(
                f"""
                <div style="width: 200px;">
                    <h4>{row['station_name']}</h4>
                    <p><strong>정류장 ID:</strong> {row['station_id']}</p>
                    <p><strong>총 이용객수:</strong> {row['total_user_count']:,}명</p>
                </div>
                """,
                max_width=250
            ),
            icon=folium.Icon(color='red', icon='info-sign', prefix='fa')
        ).add_to(m)

    folium.LayerControl().add_to(m)
    
    # 지도 표시
    col1, col2 = st.columns([2, 1])
    with col1:
        st_folium(m, width=800, height=500)
    
    with col2:
        st.markdown("### 🏆 상위 10개 정류장")
        top_stations_display = top_stations[['station_name', 'total_user_count']].copy()
        top_stations_display['순위'] = range(1, 11)
        top_stations_display = top_stations_display[['순위', 'station_name', 'total_user_count']]
        top_stations_display.columns = ['순위', '정류장명', '총 이용객수']
        
        for _, row in top_stations_display.iterrows():
            st.markdown(
                f"""
                <div class="metric-card">
                    <h3>#{row['순위']} {row['정류장명']}</h3>
                    <div class="value">{row['총 이용객수']:,}명</div>
                </div>
                """,
                unsafe_allow_html=True
            )

# =====================
# Tab2: 정류장/노선 통계
# =====================
with tab2:
    st.markdown(
        """
        <div class="chart-container">
            <h3>📈 정류장별/노선별 이용 통계</h3>
            <p>버스 노선과 정류장의 이용 현황 분석</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    
    with col1:
        if 'bus_number' in df2_clean.columns:
            st.markdown("### 🚌 노선별 총 이용객수 (상위 10)")
            route_total = df2_clean.groupby('bus_number')['user_count'].sum().sort_values(ascending=False).head(10)
            
            # Plotly를 사용한 인터랙티브 차트
            fig = px.bar(
                x=route_total.index,
                y=route_total.values,
                title="노선별 이용객수",
                labels={'x': '노선번호', 'y': '이용객수'},
                color=route_total.values,
                color_continuous_scale='Blues'
            )
            fig.update_layout(
                showlegend=False,
                height=400,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 🏢 정류장별 평균 일 이용량 (상위 10)")
        station_avg_daily = df5_clean.groupby(['station_id', 'station_name'])['total_user_count'].mean().reset_index()
        station_avg_daily = station_avg_daily.sort_values('total_user_count', ascending=False).head(10)
        
        fig2 = px.bar(
            x=station_avg_daily['station_name'],
            y=station_avg_daily['total_user_count'],
            title="정류장별 평균 일 이용량",
            labels={'x': '정류장명', 'y': '평균 일 이용객수'},
            color=station_avg_daily['total_user_count'],
            color_continuous_scale='Greens'
        )
        fig2.update_layout(
            showlegend=False,
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig2, use_container_width=True)

    # 상세 데이터 테이블
    st.markdown("### 📋 상세 데이터")
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("**노선별 상세 통계**")
        route_stats = df2_clean.groupby('bus_number').agg({
            'user_count': ['sum', 'mean', 'count']
        }).round(2)
        route_stats.columns = ['총 이용객수', '평균 이용객수', '데이터 수']
        route_stats = route_stats.sort_values('총 이용객수', ascending=False).head(10)
        st.dataframe(route_stats, use_container_width=True)
    
    with col4:
        st.markdown("**정류장별 상세 통계**")
        station_stats = df5_clean.groupby(['station_id', 'station_name']).agg({
            'total_user_count': ['sum', 'mean', 'count']
        }).round(2)
        station_stats.columns = ['총 이용객수', '평균 이용객수', '데이터 수']
        station_stats = station_stats.sort_values('총 이용객수', ascending=False).head(10)
        st.dataframe(station_stats, use_container_width=True)

# =====================
# Tab3: 시간대/사용자 유형별 패턴
# =====================
with tab3:
    st.markdown(
        """
        <div class="chart-container">
            <h3>⏰ 시간대별/사용자 유형별 패턴</h3>
            <p>시간대와 사용자 유형에 따른 이용 패턴 분석</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if 'user_type' in df1_clean.columns and 'hour_start' in df1_clean.columns and 'user_count' in df1_clean.columns:
        # 시간대별 패턴
        st.markdown("### 📊 시간대별 이용 패턴")
        
        col1, col2 = st.columns(2)
        
        with col1:
            hourly_pattern = df1_clean.groupby('hour_start')['user_count'].sum().reset_index()
            fig = px.line(
                hourly_pattern,
                x='hour_start',
                y='user_count',
                title="시간대별 총 이용객수",
                labels={'hour_start': '시간대', 'user_count': '이용객수'},
                markers=True
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # 사용자 유형별 시간대 패턴
            user_type_hourly = df1_clean.groupby(['user_type', 'hour_start'])['user_count'].sum().reset_index()
            fig2 = px.line(
                user_type_hourly,
                x='hour_start',
                y='user_count',
                color='user_type',
                title="사용자 유형별 시간대 패턴",
                labels={'hour_start': '시간대', 'user_count': '이용객수', 'user_type': '사용자 유형'}
            )
            fig2.update_layout(height=400)
            st.plotly_chart(fig2, use_container_width=True)

        # 사용자 유형별 통계
        st.markdown("### 👥 사용자 유형별 통계")
        
        col3, col4 = st.columns(2)
        
        with col3:
            user_type_total = df1_clean.groupby('user_type')['user_count'].sum()
            user_type_pct = (user_type_total / user_type_total.sum() * 100).round(1)
            
            fig3 = px.pie(
                values=user_type_total.values,
                names=user_type_total.index,
                title="사용자 유형별 비율",
                hole=0.4
            )
            fig3.update_layout(height=400)
            st.plotly_chart(fig3, use_container_width=True)
        
        with col4:
            st.markdown("**사용자 유형별 상세 통계**")
            user_stats = pd.DataFrame({
                '이용객수': user_type_total,
                '비율(%)': user_type_pct
            }).round(2)
            st.dataframe(user_stats, use_container_width=True)

        # 시간 카테고리별 패턴
        if 'time_category' in df1_clean.columns:
            st.markdown("### 🌅 시간 카테고리별 패턴")
            
            col5, col6 = st.columns(2)
            
            with col5:
                time_category_pattern = df1_clean.groupby('time_category')['user_count'].sum().reset_index()
                fig4 = px.bar(
                    time_category_pattern,
                    x='time_category',
                    y='user_count',
                    title="시간 카테고리별 이용객수",
                    labels={'time_category': '시간대', 'user_count': '이용객수'},
                    color='user_count',
                    color_continuous_scale='Viridis'
                )
                fig4.update_layout(height=400)
                st.plotly_chart(fig4, use_container_width=True)
            
            with col6:
                st.markdown("**시간 카테고리별 상세 통계**")
                time_stats = df1_clean.groupby('time_category').agg({
                    'user_count': ['sum', 'mean', 'count']
                }).round(2)
                time_stats.columns = ['총 이용객수', '평균 이용객수', '데이터 수']
                st.dataframe(time_stats, use_container_width=True)

# =====================
# Tab4: 주말/평일/월별 패턴
# =====================
with tab4:
    st.markdown(
        """
        <div class="chart-container">
            <h3>📅 주말/평일/월별 패턴</h3>
            <p>요일과 월별 이용 패턴 분석</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    
    with col1:
        if 'is_weekend' in df1_clean.columns:
            st.markdown("### 📊 주말 vs 평일 이용 패턴")
            weekend_usage = df1_clean.groupby('is_weekend')['user_count'].sum()
            
            fig = px.bar(
                x=['평일', '주말'],
                y=[weekend_usage.get(False, 0), weekend_usage.get(True, 0)],
                title="주말 vs 평일 이용자 수",
                labels={'x': '요일 구분', 'y': '이용객수'},
                color=['평일', '주말'],
                color_discrete_map={'평일': '#1e3c72', '주말': '#ff6b6b'}
            )
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # 주말/평일 통계
            weekend_stats = pd.DataFrame({
                '구분': ['평일', '주말'],
                '이용객수': [weekend_usage.get(False, 0), weekend_usage.get(True, 0)],
                '비율(%)': [
                    round(weekend_usage.get(False, 0) / weekend_usage.sum() * 100, 1),
                    round(weekend_usage.get(True, 0) / weekend_usage.sum() * 100, 1)
                ]
            })
            st.dataframe(weekend_stats, use_container_width=True)

    with col2:
        if 'year' in df1_clean.columns and 'month' in df1_clean.columns:
            st.markdown("### 📈 월별 이용 추세")
            monthly_trend = df1_clean.groupby(['year', 'month'])['user_count'].sum().reset_index()
            monthly_trend['연월'] = monthly_trend['year'].astype(str) + '-' + monthly_trend['month'].astype(str).str.zfill(2)
            
            fig2 = px.line(
                monthly_trend,
                x='연월',
                y='user_count',
                title="월별 이용 추세",
                labels={'연월': '연월', 'user_count': '이용객수'},
                markers=True
            )
            fig2.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig2, use_container_width=True)
            
            # 월별 통계
            monthly_stats = monthly_trend.copy()
            monthly_stats.columns = ['연도', '월', '이용객수', '연월']
            st.dataframe(monthly_stats[['연월', '이용객수']], use_container_width=True)

    # 요일별 패턴 (추가)
    if 'day_of_week' in df1_clean.columns:
        st.markdown("### 📅 요일별 이용 패턴")
        
        day_order = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
        day_usage = df1_clean.groupby('day_of_week')['user_count'].sum().reindex(day_order, fill_value=0)
        
        fig3 = px.bar(
            x=day_usage.index,
            y=day_usage.values,
            title="요일별 이용객수",
            labels={'x': '요일', 'y': '이용객수'},
            color=day_usage.values,
            color_continuous_scale='Plasma'
        )
        fig3.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)

# 푸터
st.markdown(
    """
    <div class="footer">
        <p><strong>데이터 출처:</strong> 제주데이터허브, 공공데이터포털</p>
        <p>📊 제주도 버스 데이터 대시보드 | 🚌 버스 이용 현황 분석</p>
    </div>
    """,
    unsafe_allow_html=True
)
