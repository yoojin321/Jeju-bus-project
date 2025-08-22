## 제주 버스 데이터 대시보드 (mini-project)

### 개요
이 프로젝트는 제주도의 버스 이용 데이터를 분석하고 시각화하는 Streamlit 대시보드입니다. 대용량 데이터 파일은 용량 제한으로 깃허브에 포함되지 않았으며, 아래 안내에 따라 로컬에서 직접 내려받거나 노트북을 실행해 정제 데이터를 생성하세요.

### 원본 데이터 다운로드 링크
아래 4개의 CSV 파일을 내려받아 `mini-project/origin_data/` 폴더에 저장하세요.

1. 제주데이터허브 – 버스 관련 데이터: <https://www.jejudatahub.net/data/view/data/743>
2. 제주데이터허브 – 버스 관련 데이터: <https://www.jejudatahub.net/data/view/data/512>
3. 공공데이터포털 – 버스 이용 데이터: <https://www.data.go.kr/data/15010850/fileData.do?recommendDataYn=Y>
4. 제주데이터허브 – 버스 관련 데이터: <https://www.jejudatahub.net/data/view/data/561>

권장 저장 경로 및 예시 파일명:
- `mini-project/origin_data/이용자유형별버스정류소이용인원현황.csv`
- `mini-project/origin_data/일별버스승차인원수현황.csv`
- `mini-project/origin_data/일별시간대별버스승차인원수현황.csv`
- `mini-project/origin_data/제주특별자치도_버스정류소현황_20221101.csv`

### 정제 데이터 생성 방법
정제 데이터 파일은 노트북을 실행하여 생성합니다.

1) Jupyter에서 `mini-project/project.ipynb`를 열고 셀을 순서대로 모두 실행합니다.
2) 실행이 완료되면 `mini-project/cleaned_data/` 폴더에 정제된 CSV가 생성됩니다. (예: `df1_clean.csv`, `df2_clean.csv`, `df5_clean.csv`)

참고: 노트북/코드에 정의된 파일명이 환경에 따라 다를 수 있습니다. 생성된 파일명이 대시보드에서 참조하는 파일명과 일치하는지 확인하세요.

### 대용량 파일과 GitHub 업로드
- 대용량 CSV는 깃허브 용량 제한으로 저장소에 포함하지 않았습니다.
- 협업/배포가 필요하다면 Git LFS 사용을 고려하세요.
  - Git LFS 설치 후: `git lfs install` → `git lfs track "*.csv"`
- 또는 위 링크에서 직접 내려받아 `origin_data/`에 배치한 뒤, 노트북을 실행해 `cleaned_data/`를 생성하세요.

### 대시보드 실행 방법
필요 패키지를 설치한 뒤 Streamlit 앱을 실행합니다.

```bash
pip install streamlit pandas folium streamlit-folium matplotlib seaborn

cd mini-project
streamlit run app.py
```

브라우저에서 로컬 주소로 접속하면 대시보드를 확인할 수 있습니다. (예: `http://localhost:8501`)

### 폴더 구조 (요약)
```
mini-project/
  app.py                  # Streamlit 대시보드
  project.ipynb           # 정제 데이터 생성 노트북
  origin_data/            # 원본 CSV (수동 다운로드)
  cleaned_data/           # 정제 CSV (노트북 실행 후 생성)
```


