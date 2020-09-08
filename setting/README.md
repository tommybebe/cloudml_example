#### 환경 설정용 도커 이미지
- Pycharm IDE + Docker interpreter 세팅을 위한 도커 이미지
- 편의를 위해 다수 패키지 설치된 atlasml/ml-base을 base로 사용
- cloudml runtime에 맞추기 위해 일부 패이지 버전 지정하여 설치 (ex: xgboost)
- google cloud 제품을 위한 python client, bigquery, storage 등 패키지 추가 
- 편의를 위한 몇 가지 패키지 추가

#### build command
```shell script
docker build -t base .
```
