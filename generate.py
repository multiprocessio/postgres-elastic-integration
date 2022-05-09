import calendar
import datetime
import dateutil
import json
import random
from urllib.parse import urlencode
from urllib.request import Request, urlopen

CUSTOMERS = 200

MONTHS = 1

AVG_RESPONSE_TIME_S = 5
STDEV_RESPONSE_TIME_S = 50

AVG_REQUEST_PER_DAY = 10
STDEV_REQUEST_PER_DAY = 90


def http(method, url, body):
    data = json.dumps(body).encode() if body else None
    req = Request(url, data=data, method=method)
    req.add_header('Content-Type', 'application/json')
    try:
        rsp = urlopen(req)
        rsp_body = rsp.read().decode()
        return json.loads(rsp_body)
    except Exception as e:
        body = e.read().decode()
        print(json.dumps(json.loads(body), sort_keys=True, indent=2))
        raise
    

random.seed()

start_of_this_month = datetime.datetime.today().replace(day=1)

words = []
with open('/usr/share/dict/words') as f:
    for line in f:
        words.append(line.strip())

for customer in range(CUSTOMERS):
    customer_baseline_req_per_day = max(1, random.gauss(AVG_REQUEST_PER_DAY, STDEV_REQUEST_PER_DAY))
    customer_baseline_response_time_s = max(1, random.gauss(AVG_RESPONSE_TIME_S, STDEV_RESPONSE_TIME_S))

    # Allow these to differ each month
    month_req_per_day = customer_baseline_req_per_day
    month_response_time_s = customer_baseline_response_time_s

    for month in range(MONTHS):
        month_req_per_day = max(1, int(month_req_per_day + random.random() * month_req_per_day - month_req_per_day / 2))
        month_response_time_s = max(1, month_response_time_s + random.random() * month_response_time_s - month_response_time_s / 2)
        
        historic_month = (start_of_this_month.month - month - 1) % 12 + 1
        historic_year = start_of_this_month.year + (start_of_this_month.month - month - 1) // 12
        for day in range(calendar.monthrange(historic_year, historic_month)[1]):
            date = datetime.date(historic_year, historic_month, day+1)
            for req in range(int(month_req_per_day)):
                perturbation = random.random() * month_response_time_s - month_response_time_s / 2
                rsp_time = month_response_time_s + perturbation

                time = datetime.time(int(random.random() * 24), int(random.random() * 60), int(random.random() * 60), int(random.random() * 1000))
                dt = date.isoformat() + "T" + time.isoformat()
                search_term = random.choice(words)
                log = {"url": "/search?q="+search_term, "@timestamp": dt, "response_time": rsp_time, "customer_id": customer}
                index = f'logs-{historic_year}-{historic_month}-{day+1}'
                http('POST', f'http://localhost:9200/{index}/_doc', log)

# TODO: store customer info in postgres
