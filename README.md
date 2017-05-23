# bw-monitor
Rasberry pi based bandwidth monitoring

# Building
$ docker build -t bw-monitor .

# Running
$ mkdir creds
Get your google client_secrets.json and place in creds/

$ docker run -it --rm -v <path to creds>:/creds bw-monitor
