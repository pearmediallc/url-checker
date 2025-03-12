# URL Checker Deployment Guide

## Prerequisites
- A Linux server with Python 3.8+ installed
- Domain name pointing to your server
- Nginx installed on your server

## Deployment Steps

1. **Upload Files to Server**
   ```bash
   # Create directory on your server
   mkdir -p /var/www/url-checker
   # Copy all files to this directory
   ```

2. **Install Dependencies**
   ```bash
   cd /var/www/url-checker
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Create Systemd Service**
   Create file: `/etc/systemd/system/url-checker.service`
   ```ini
   [Unit]
   Description=URL Checker Gunicorn Service
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/var/www/url-checker
   Environment="PATH=/var/www/url-checker/venv/bin"
   ExecStart=/var/www/url-checker/venv/bin/gunicorn --workers 3 --bind unix:url-checker.sock -m 007 app:app

   [Install]
   WantedBy=multi-user.target
   ```

4. **Create Nginx Configuration**
   Create file: `/etc/nginx/sites-available/url-checker`
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;  # Replace with your domain

       location / {
           proxy_pass http://unix:/var/www/url-checker/url-checker.sock;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

5. **Enable and Start Services**
   ```bash
   # Enable and start the Gunicorn service
   sudo systemctl enable url-checker
   sudo systemctl start url-checker

   # Enable Nginx configuration
   sudo ln -s /etc/nginx/sites-available/url-checker /etc/nginx/sites-enabled/
   sudo systemctl restart nginx
   ```

6. **SSL Setup (Recommended)**
   ```bash
   # Install Certbot
   sudo apt install certbot python3-certbot-nginx

   # Get SSL certificate
   sudo certbot --nginx -d your-domain.com
   ```

## Automatic Startup
The systemd service will automatically start your application when:
- The server boots up
- The application crashes (it will attempt to restart)
- The system resources are available

## Monitoring
Check application status:
```bash
sudo systemctl status url-checker
```

View logs:
```bash
sudo journalctl -u url-checker
```

## Troubleshooting
1. If the service fails to start:
   ```bash
   sudo journalctl -u url-checker -n 50
   ```

2. Check Nginx logs:
   ```bash
   sudo tail -f /var/log/nginx/error.log
   ```

3. Check permissions:
   ```bash
   sudo chown -R www-data:www-data /var/www/url-checker
   sudo chmod -R 755 /var/www/url-checker
   ```
