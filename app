server {
listen 80;
server_name www.erzincankuyumcu.com;

location / {
  include proxy_params;
  proxy_pass http://unix:/home/erzincan_kuyumcular/app.sock;
    }
}             