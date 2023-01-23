server {
listen 80;
server_name 91.151.89.124;

location / {
  include proxy_params;
  proxy_pass http://unix:/root/erzincan_kuyumcular/app.sock;
    }
}             