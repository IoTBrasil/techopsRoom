### Requests

* Health check:
method: get
route: /health-check - returns 200 if server is up

2. Temperature: post - /temperature - expects parameter temp and save it to database, always return the received temperature

| Request | Route | Method | Parameter | Return |
| - |:--| :-----:| :-----:| -----:|
| Health Check | /health-check | get | - | 200 |
| Temperature | /temperature | post | temp:int | temp value|
