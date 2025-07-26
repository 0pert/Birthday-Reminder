# Birthday Reminder
- Flask
- Jinja2
- Waitress
- Poetry (valfritt)

Applikationen är konfigurerad för att ligga bakom en reverse proxy med URI-prefix `/bday`.


Jag har satt upp det med nginx och följande konf:


`/etc/nginx/sites-available/bday`
```
server {
    listen 80;
    server_name 192.168.0.200;  # ändra till din domän eller IP

    location /bday/ {
        proxy_pass http://127.0.0.1:8080/; 
        #(porten ska matcha waitress / flask)
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Prefix /bday;
    }
}
```
#### Skapa en länk från den nya konfigurationen till sites-enabled:
```
sudo ln -s /etc/nginx/sites-available/bday /etc/nginx/sites-enabled/
```
#### Testa konfig:
```
sudo nginx -t
```
#### Ladda om konfigen:
```
sudo nginx -s reload
```

## Kör appen som en systemd-tjänst (Daemon)
Detta gör att applikationen körs i bakgrunden och startas automatiskt när servern / Raspberryn startas om.
#### Skapa en tjänst-fil:
```
sudo nano /etc/systemd/system/bday.service
```
#### Innehåll:
```
[Unit]
Description=Flask app for bday using Waitress
After=network.target

[Service]
User=it
WorkingDirectory=/var/www/bday
ExecStart=/var/www/bday/.venv/bin/python /var/www/bday/app.py
Environment="PATH=/var/www/bday/.venv/bin"
Restart=always

[Install]
WantedBy=multi-user.target
```

#### Kör dessa kommandon:
```
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl start bday
sudo systemctl enable bday
sudo systemctl status bday
```