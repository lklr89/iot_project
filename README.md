# iot_project
School IoT project (RaspberryPi, Azure) 

command to see data in the cloud shell:
az iot hub monitor-events --device-id Group08 --hub-name iotprojecthub

start the websocket daemon to provide data log file:
websocketd --port=8080 --staticdir=static/ tail -f tempdata.log 
