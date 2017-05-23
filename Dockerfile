from python:2.7-alpine
VOLUME /usr/src/app
VOLUME /creds
WORKDIR /usr/src/app
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt
COPY *.py .
CMD ["python", "./bw-monitor.py", "--noauth_local_webserver", "--client_secret", "/creds/client_secret.json", "--oauth_json", "/creds/oauth.json"]