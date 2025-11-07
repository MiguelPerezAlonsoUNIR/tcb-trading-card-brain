# TCB Monitoring - Quick Reference

## Quick Commands

### Starting Services
```bash
# Start monitoring stack only
cd monitoring && ./manage-monitoring.sh start

# Start application with monitoring
docker network create monitoring_elk
docker-compose up -d
cd monitoring && ./manage-monitoring.sh start
```

### Accessing Services
- **Kibana**: http://localhost:5601
- **Elasticsearch**: http://localhost:9200
- **Logstash**: http://localhost:9600

### Status & Logs
```bash
# Check status
./manage-monitoring.sh status

# View all logs
./manage-monitoring.sh logs

# View specific service logs
./manage-monitoring.sh logs elasticsearch
./manage-monitoring.sh logs kibana
```

### Stopping Services
```bash
# Stop monitoring stack
./manage-monitoring.sh stop

# Stop application
docker-compose down
```

## Common Tasks

### View Application Logs in Kibana
1. Open http://localhost:5601
2. Go to **Discover**
3. Create index pattern: `tcb-logs-*`
4. Filter by: `service: tcb-trading-card-brain`

### Monitor System Metrics
1. Open http://localhost:5601
2. Create index pattern: `metricbeat-tcb-*`
3. View CPU: `system.cpu.user.pct`
4. View Memory: `system.memory.actual.used.pct`

### Check Service Uptime
1. Open http://localhost:5601
2. Go to **Observability** → **Uptime**
3. View all monitored endpoints

### Search Logs
```bash
# Using Elasticsearch API
curl "http://localhost:9200/tcb-logs-*/_search?q=ERROR"

# View all indices
curl http://localhost:9200/_cat/indices?v

# Get cluster health
curl http://localhost:9200/_cluster/health?pretty
```

## Troubleshooting

### Services Not Starting
```bash
# Check Docker
docker ps -a

# Check logs
./manage-monitoring.sh logs elasticsearch

# Restart
./manage-monitoring.sh restart
```

### No Data in Kibana
1. Verify Filebeat is running: `docker ps | grep filebeat`
2. Check Logstash pipeline: `./manage-monitoring.sh logs logstash`
3. Verify indices: `curl http://localhost:9200/_cat/indices?v`

### High Disk Usage
```bash
# Check index sizes
curl http://localhost:9200/_cat/indices?v&s=store.size:desc

# Delete old indices
curl -X DELETE "http://localhost:9200/tcb-logs-2024.01.*"

# Or use cleanup
./manage-monitoring.sh cleanup
```

## Index Patterns to Create

| Pattern | Purpose |
|---------|---------|
| `tcb-logs-*` | Application and container logs |
| `metricbeat-tcb-*` | System and Docker metrics |
| `heartbeat-tcb-*` | Uptime monitoring data |

## Useful Kibana Queries

### Application Logs
- All errors: `log_level: ERROR`
- Flask logs: `tags: flask_app`
- From app container: `container.name: "onepiece-deck-builder"`
- Last hour errors: `@timestamp:[now-1h TO now] AND log_level:ERROR`

### System Metrics
- High CPU: `system.cpu.user.pct > 80`
- High memory: `system.memory.actual.used.pct > 85`
- Docker containers: `docker.container.name: *`

### Uptime
- Service down: `monitor.status: down`
- Slow responses: `monitor.duration.us > 1000000`

## Data Retention

Default retention periods:
- Logs: 7 days
- Metrics: 30 days
- Uptime: 30 days

To change, edit `.env` or set up ILM policies.

## Backup & Restore

### Backup
```bash
./manage-monitoring.sh backup
```

### Restore
```bash
docker run --rm \
  -v monitoring_elasticsearch-data:/data \
  -v $(pwd)/backups:/backup \
  ubuntu tar xzf /backup/elasticsearch-backup-TIMESTAMP.tar.gz -C /
```

## Resource Usage

Typical resource consumption:
- **Elasticsearch**: 512MB-1GB RAM, 5-10GB disk
- **Logstash**: 256-512MB RAM
- **Kibana**: 256-512MB RAM
- **Beats**: 50-100MB RAM each

Total: ~2-3GB RAM minimum

## Security Notes

For production:
1. Enable Elasticsearch security (`xpack.security.enabled=true`)
2. Set strong passwords
3. Use HTTPS
4. Restrict network access
5. Configure authentication

See `monitoring/README.md` for details.
