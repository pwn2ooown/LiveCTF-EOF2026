FROM fedora:latest

# Install cronie (cron for Fedora), sqlite and python3
RUN dnf install -y cronie sqlite python3 python3-pip && \
    dnf clean all

# Create application directory
WORKDIR /app

# Copy Flask application
COPY app.py /app/
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Expose internal port  
EXPOSE 5000

# Start via entrypoint
CMD ["/app/start.sh"]
