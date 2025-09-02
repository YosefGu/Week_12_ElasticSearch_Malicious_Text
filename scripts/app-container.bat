
docker build -t app-elastic:1.5 .
docker tag app-elastic:1.5 yosigu/app-elastic:1.5
docker push yosigu/app-elastic:1.5

docker run -d --name app-elastic-container `
--network elastic-net `
-p 8000:8000 `
-e ES_PATH=http://elasticsearch-container:9200 `
-e ES_INDEX=malicious_text `
-e HOST=0.0.0.0 `
yosigu/app-elastic:1.5


-e PORT=8000 `