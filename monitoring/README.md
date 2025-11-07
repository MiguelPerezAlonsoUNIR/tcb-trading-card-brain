# TCB Trading Card Brain - ELK Stack Monitoring

This directory contains the complete monitoring infrastructure for the TCB Trading Card Brain application using the ELK (Elasticsearch, Logstash, Kibana) stack and Elastic Beats.

## Overview

The monitoring stack consists of:

- **Elasticsearch**: Stores and indexes all logs, metrics, and uptime data
- **Logstash**: Processes and transforms log data before indexing
- **Kibana**: Provides visualization and dashboards for monitoring data
- **Filebeat**: Collects and ships application and container logs
- **Metricbeat**: Collects and ships system and Docker metrics
- **Heartbeat**: Monitors application and service uptime

## Architecture

```
┌─────────────────┐
│  TCB Application│
│   (Flask App)   │
└────────┬────────┘
         │ logs
         ▼
┌─────────────────┐       ┌─────────────────┐
│    Filebeat     │──────▶│    Logstash     │
│  (Log Shipper)  │       │  (Log Pipeline) │
└─────────────────┘       └────────┬────────┘
                                   │
┌─────────────────┐                │
│   Metricbeat    │                │
│ (Metric Shipper)│                │
└────────┬────────┘                │
         │                         │
         │                         ▼
         │                 ┌───────────────┐
         └────────────────▶│ Elasticsearch │
         ┌────────────────▶│  (Data Store) │
         │                 └───────┬───────┘
┌────────┴────────┐                │
│   Heartbeat     │                │
│ (Uptime Monitor)│                │
└─────────────────┘                │
                                   ▼
                          ┌────────────────┐
                          │     Kibana     │
                          │ (Visualization)│
                          └────────────────┘
```

## Quick Start

### Prerequisites

- Docker Engine 20.10+
- Docker Compose 1.29+
- At least 4GB of available RAM
- At least 10GB of available disk space

### Starting the Monitoring Stack

1. **Start the ELK stack and beats:**

```bash
cd monitoring
docker-compose -f docker-compose.elk.yml up -d
```

2. **Start the application with monitoring enabled:**

```bash
cd ..
docker network create monitoring_elk 2>/dev/null || true
docker-compose up -d
```

3. **Access Kibana:**

Open your browser and navigate to: `http://localhost:5601`

4. **Verify all services are running:**

```bash
docker-compose -f monitoring/docker-compose.elk.yml ps
```

Expected output:
```
NAME                IMAGE                                          STATUS
tcb-elasticsearch   docker.elastic.co/elasticsearch/...           Up (healthy)
tcb-filebeat        docker.elastic.co/beats/filebeat:...          Up
tcb-heartbeat       docker.elastic.co/beats/heartbeat:...         Up
tcb-kibana          docker.elastic.co/kibana/kibana:...           Up (healthy)
tcb-logstash        docker.elastic.co/logstash/logstash:...       Up (healthy)
tcb-metricbeat      docker.elastic.co/beats/metricbeat:...        Up
```

## Configuration

### Filebeat Configuration

Located at: `filebeat/config/filebeat.yml`

Filebeat collects:
- Docker container logs
- Application logs from `/var/log/tcb/` (if mounted)
- Automatically adds Docker metadata

**Key features:**
- JSON log parsing
- Multiline log support
- Docker metadata enrichment

### Metricbeat Configuration

Located at: `metricbeat/config/metricbeat.yml`

Metricbeat collects:
- System metrics (CPU, memory, disk, network)
- Docker container metrics
- Process information

**Collection interval:** 10 seconds

### Heartbeat Configuration

Located at: `heartbeat/config/heartbeat.yml`

Heartbeat monitors:
- TCB Application (HTTP endpoint)
- Application health endpoint
- Elasticsearch status
- Kibana status
- Logstash status

**Check interval:** 30 seconds

### Logstash Configuration

Located at: `logstash/pipeline/logstash.conf`

Logstash pipeline:
1. **Input**: Receives data from Filebeat on port 5044
2. **Filter**: 
   - Parses JSON logs
   - Parses Flask/Gunicorn logs
   - Parses Nginx access logs
   - Adds service metadata
3. **Output**: Sends to Elasticsearch with daily indices

### Kibana Configuration

Located at: `kibana/config/kibana.yml`

Kibana settings:
- Connected to Elasticsearch at `http://elasticsearch:9200`
- Accessible on port 5601
- Monitoring UI enabled

## Using Kibana

### Initial Setup

1. **Access Kibana**: Navigate to `http://localhost:5601`

2. **Create Index Patterns**:
   - Go to Stack Management → Index Patterns
   - Create patterns for:
     - `tcb-logs-*` (Application logs)
     - `metricbeat-tcb-*` (System metrics)
     - `heartbeat-tcb-*` (Uptime data)

3. **Import Dashboards** (optional):
   - Filebeat and Metricbeat come with pre-built dashboards
   - In Kibana, go to Stack Management → Saved Objects → Import

### Viewing Logs

1. Go to **Discover** in Kibana
2. Select the `tcb-logs-*` index pattern
3. Filter logs by:
   - Time range
   - Log level
   - Container name
   - Service name

**Example queries:**
- Find all error logs: `log_level: ERROR`
- Find logs from app container: `container.name: "onepiece-deck-builder"`
- Find Flask logs: `tags: flask_app`

### Viewing Metrics

1. Go to **Discover** or **Dashboard**
2. Select the `metricbeat-tcb-*` index pattern
3. View metrics:
   - CPU usage: `system.cpu.user.pct`
   - Memory usage: `system.memory.actual.used.pct`
   - Docker container stats: `docker.container.*`

### Viewing Uptime

1. Go to **Observability** → **Uptime**
2. View all monitored services
3. Check:
   - Uptime percentage
   - Response times
   - Status history

### Creating Custom Dashboards

1. Go to **Dashboard** → **Create dashboard**
2. Add visualizations:
   - **Line charts**: For time-series metrics
   - **Pie charts**: For log level distribution
   - **Data tables**: For recent logs
   - **Gauges**: For current metrics
3. Save and share your dashboard

## Data Management

### Data Retention

By default, Elasticsearch stores all data. To manage disk space:

1. **Set up Index Lifecycle Management (ILM)**:

```bash
# Example: Delete logs older than 7 days
curl -X PUT "localhost:9200/_ilm/policy/tcb-logs-policy" -H 'Content-Type: application/json' -d'
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {}
      },
      "delete": {
        "min_age": "7d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}'
```

2. **Manual cleanup**:

```bash
# Delete old indices
curl -X DELETE "localhost:9200/tcb-logs-2024.01.*"
```

### Backup Data

```bash
# Backup Elasticsearch data volume
docker run --rm -v monitoring_elasticsearch-data:/data -v $(pwd):/backup ubuntu tar czf /backup/elasticsearch-backup.tar.gz /data

# Restore from backup
docker run --rm -v monitoring_elasticsearch-data:/data -v $(pwd):/backup ubuntu tar xzf /backup/elasticsearch-backup.tar.gz -C /
```

## Performance Tuning

### Memory Configuration

**Elasticsearch**:
- Default: 512MB heap size
- Adjust in `docker-compose.elk.yml`: `ES_JAVA_OPTS=-Xms1g -Xmx1g`
- Recommendation: Set to 50% of available RAM, max 32GB

**Logstash**:
- Default: 256MB heap size
- Adjust in `docker-compose.elk.yml`: `LS_JAVA_OPTS=-Xmx512m -Xms512m`

### Docker Resource Limits

Add resource limits to services:

```yaml
services:
  elasticsearch:
    deploy:
      resources:
        limits:
          memory: 2g
        reservations:
          memory: 1g
```

## Troubleshooting

### Services Not Starting

1. **Check logs**:
```bash
docker-compose -f monitoring/docker-compose.elk.yml logs elasticsearch
docker-compose -f monitoring/docker-compose.elk.yml logs logstash
docker-compose -f monitoring/docker-compose.elk.yml logs kibana
```

2. **Check health status**:
```bash
curl http://localhost:9200/_cluster/health?pretty
curl http://localhost:5601/api/status
```

3. **Common issues**:
   - **Port conflicts**: Ensure ports 9200, 5601, 5044 are available
   - **Insufficient memory**: Increase Docker memory allocation
   - **Permissions**: Ensure proper file permissions on config files

### No Data in Kibana

1. **Verify Filebeat is running**:
```bash
docker logs tcb-filebeat
```

2. **Check Logstash pipeline**:
```bash
docker logs tcb-logstash
```

3. **Verify indices exist**:
```bash
curl http://localhost:9200/_cat/indices?v
```

4. **Check index patterns in Kibana**:
   - Go to Stack Management → Index Patterns
   - Ensure patterns match your indices

### High Disk Usage

1. **Check index sizes**:
```bash
curl http://localhost:9200/_cat/indices?v&s=store.size:desc
```

2. **Enable ILM** (see Data Management section above)

3. **Delete old indices manually**:
```bash
curl -X DELETE "localhost:9200/tcb-logs-2024.01.01"
```

## Monitoring Best Practices

### Log Levels

Configure appropriate log levels in your application:
- **Production**: INFO or WARNING
- **Development**: DEBUG
- **Staging**: INFO

### Metric Collection Intervals

Balance between data granularity and resource usage:
- **Critical metrics**: 10s (default)
- **Non-critical metrics**: 30s or 60s
- **Uptime checks**: 30s to 60s

### Alerts and Notifications

Set up alerts in Kibana for:
- Application errors (log level: ERROR)
- High CPU usage (> 80%)
- High memory usage (> 85%)
- Service downtime (heartbeat)

### Security Considerations

For production deployments:

1. **Enable Elasticsearch security**:
   - Set `xpack.security.enabled=true`
   - Configure authentication
   - Use HTTPS

2. **Secure Kibana**:
   - Enable authentication
   - Use reverse proxy with SSL

3. **Network isolation**:
   - Use private networks
   - Restrict access to monitoring ports

## Integration with Production

### Cloud Deployment

The monitoring stack can be deployed alongside the application in cloud environments:

#### AWS
- Use AWS Elasticsearch Service (Amazon OpenSearch)
- Deploy beats on EC2 instances
- Use CloudWatch for additional monitoring

#### Azure
- Use Azure Elasticsearch Service
- Deploy on Azure VMs
- Integrate with Azure Monitor

#### GCP
- Use Google Cloud Elasticsearch
- Deploy on GCP Compute Engine
- Integrate with Cloud Monitoring

### Scaling

For high-traffic applications:

1. **Elasticsearch cluster**:
   - Add more Elasticsearch nodes
   - Configure sharding and replication

2. **Logstash**:
   - Scale horizontally with multiple Logstash instances
   - Use load balancer

3. **Beats**:
   - Deploy on each application server
   - Configure remote monitoring

## Maintenance

### Regular Tasks

**Daily**:
- Check service health
- Review critical alerts

**Weekly**:
- Review disk usage
- Analyze performance metrics
- Update dashboards

**Monthly**:
- Update ELK stack versions
- Review and optimize ILM policies
- Backup important dashboards and configurations

### Updating the Stack

```bash
# Pull latest images
cd monitoring
docker-compose -f docker-compose.elk.yml pull

# Restart services
docker-compose -f docker-compose.elk.yml up -d
```

## Resources

- [Elasticsearch Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [Logstash Documentation](https://www.elastic.co/guide/en/logstash/current/index.html)
- [Kibana Documentation](https://www.elastic.co/guide/en/kibana/current/index.html)
- [Filebeat Documentation](https://www.elastic.co/guide/en/beats/filebeat/current/index.html)
- [Metricbeat Documentation](https://www.elastic.co/guide/en/beats/metricbeat/current/index.html)
- [Heartbeat Documentation](https://www.elastic.co/guide/en/beats/heartbeat/current/index.html)

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review Docker container logs
3. Consult Elastic documentation
4. Open an issue on the GitHub repository

## License

This monitoring configuration is part of the TCB Trading Card Brain project and follows the same license.
