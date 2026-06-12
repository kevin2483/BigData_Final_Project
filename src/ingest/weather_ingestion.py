import urllib.request
import json
import csv
import os

api_key = os.environ.get("KMA_API_KEY")
if not api_key:
    raise ValueError("환경변수 KMA_API_KEY가 설정되지 않았습니다.")
    
url = "http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList"
url += "?serviceKey=" + api_key
url += "&pageNo=1&numOfRows=35&dataType=JSON&dataCd=ASOS&dateCd=DAY&startDt=20191001&endDt=20191031&stnIds=108"

print("=== Calling KMA Weather API ===")
try:
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    res_code = response.getcode()

    if res_code == 200:
        res_body = response.read().decode('utf-8')
        data = json.loads(res_body)
        items = data['response']['body']['items']['item']

        csv_file = "/home/maria_dev/real_weather.csv"

        with open(csv_file, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(["date", "avg_temp", "rainfall"])

            for item in items:
                date = item.get("tm", "")
                avg_temp = item.get("avgTa", "0")
                rainfall = item.get("sumRn", "0")

                if not rainfall:
                    rainfall = "0"

                writer.writerow([date, avg_temp, rainfall])

        print("Data successfully saved locally: " + csv_file)

        print("=== Uploading to HDFS ===")
        os.system("hdfs dfs -mkdir -p /user/maria_dev/weather")
        os.system("hdfs dfs -put -f " + csv_file + " /user/maria_dev/weather/")
        os.system("rm -f " + csv_file)

        print("=== Success! Real Weather Data Ingested ===")
    else:
        print("API Error Code: " + str(res_code))
except Exception as e:
    print("Failed to fetch data: " + str(e))
