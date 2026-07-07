# OpenWA Service — WhatsApp Web Automation
# FIX 7: Session persistence, configurable via env vars

FROM node:20-slim

WORKDIR /app

# Install wget for health checks
RUN apt-get update && apt-get install -y --no-install-recommends wget && \
    rm -rf /var/lib/apt/lists/*

# Copy package files
COPY package*.json ./
RUN npm ci --production

# Copy source
COPY index.js ./

# Session data persisted via Docker volume mount
VOLUME /app/session

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD wget -qO- http://localhost:3000/health || exit 1

CMD ["node", "index.js"]
