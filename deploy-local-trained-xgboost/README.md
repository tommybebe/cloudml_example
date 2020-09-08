### 기능  
- XGBoost
- local train 
- cloud deploy 
- online predict

### 구조 
```
. .env              : 프로젝트/버킷/인증키 등이 적혀진 설정 파일 
├── data            : 훈련 데이터 다운로드할 장소 
├── src
│   ├── logger.py   : 로깅을 위한 편의 기능
├── trained         : 훈련한 모델 보관할 장소 
│   ├── model.bst   : 훈련한 모델
├── deploy.py       : 배포용 스크립트
├── predict.py      : 예측용 스크립트 
└── trainer.py      : 훈련용 스크립트
```

### 실행 방법
1. .env 파일 설정 
    - PROJECT_ID : GCP 프로젝트 아이디 
    - BUCKET_ID : GCS 버킷 아이디 
    - GOOGLE_APPLICATION_CREDENTIALS : 인증키 json 파일의 경로
    - DEV_MODE : 'dev' or 'prod', 로깅 혹은 폴더/버킷 등의 구분을 위한 설정값
2. py 파일 실행
- trainer.py : 로컬 머신에서 > census 파일 다운로드 > 라벨인코딩 > 훈련 > 모델 파일 저장 > GCS 업로드  
- deploy.py : "test_001" 이름의 모델 생성 > GCS 업로드한 파일로 버전 생성  
- predict.py : 전처리된 예시 데이터로 배포된 버전에 예측 요청 
