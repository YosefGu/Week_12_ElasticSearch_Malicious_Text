
docker build -t elasticsearch:1.2 .
docker tag elasticsearch:1.2 yosigu/elasticsearch:1.2
docker push yosigu/elasticsearch:1.2 

docker run -d --name elasticsearch-container `
 -p 8000:8000 `
 -e ES_PATH=http://localhost:9200 `
 -e ES_INDEX=malicious_text `
 -e HOST=127.0.0.1 `
 -e PORT=8000 `
 yosigu/elasticsearch:1.2 