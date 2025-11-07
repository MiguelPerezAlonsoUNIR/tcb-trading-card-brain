# Kibana Dashboards and Visualizations

This directory contains pre-configured Kibana dashboards for the TCB Trading Card Brain application.

## Available Dashboards

### 1. Application Overview Dashboard
- Real-time application metrics
- Request rate and response times
- Error rate trends
- Active users

### 2. System Metrics Dashboard
- CPU usage over time
- Memory utilization
- Disk I/O
- Network traffic
- Docker container metrics

### 3. Log Analysis Dashboard
- Log levels distribution
- Error logs timeline
- Top error messages
- Log volume by service

### 4. Uptime Monitoring Dashboard
- Service availability
- Response time distribution
- Downtime incidents
- Health check status

## Creating Custom Dashboards

1. **Access Kibana**: Navigate to `http://localhost:5601`

2. **Create Index Pattern** (if not exists):
   - Go to Stack Management → Index Patterns
   - Create pattern: `tcb-logs-*`, `metricbeat-tcb-*`, `heartbeat-tcb-*`

3. **Create Visualizations**:
   - Go to Visualize Library → Create visualization
   - Choose visualization type (Line, Bar, Pie, etc.)
   - Select your data source
   - Configure metrics and buckets

4. **Build Dashboard**:
   - Go to Dashboard → Create dashboard
   - Add your visualizations
   - Arrange and resize as needed
   - Save the dashboard

5. **Export Dashboard**:
   - Go to Stack Management → Saved Objects
   - Select your dashboard
   - Click Export
   - Save to this directory

## Resources

- [Kibana Dashboard Guide](https://www.elastic.co/guide/en/kibana/current/dashboard.html)
- [Creating Visualizations](https://www.elastic.co/guide/en/kibana/current/createvis.html)
