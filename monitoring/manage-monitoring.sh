#!/bin/bash

# TCB Trading Card Brain - Monitoring Stack Management Script
# This script helps manage the ELK stack and beats monitoring infrastructure

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Function to print colored messages
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    print_info "Docker is running"
}

# Function to check system resources
check_resources() {
    print_info "Checking system resources..."
    
    # Check available memory (Linux)
    if [[ -f /proc/meminfo ]]; then
        total_mem=$(grep MemTotal /proc/meminfo | awk '{print $2}')
        total_mem_gb=$((total_mem / 1024 / 1024))
        
        if [ $total_mem_gb -lt 4 ]; then
            print_warning "System has less than 4GB RAM. Monitoring stack may run slowly."
        else
            print_info "Available RAM: ${total_mem_gb}GB"
        fi
    fi
}

# Function to create necessary network
create_network() {
    print_info "Creating Docker network for monitoring..."
    if docker network inspect monitoring_elk > /dev/null 2>&1; then
        print_info "Network 'monitoring_elk' already exists"
    else
        docker network create monitoring_elk
        print_info "Network 'monitoring_elk' created"
    fi
}

# Function to start monitoring stack
start_monitoring() {
    print_info "Starting ELK stack and beats..."
    cd "$SCRIPT_DIR"
    
    # Create network first
    create_network
    
    # Start the monitoring stack
    docker-compose -f docker-compose.elk.yml up -d
    
    print_info "Waiting for services to be healthy..."
    sleep 10
    
    # Wait for Elasticsearch
    print_info "Waiting for Elasticsearch..."
    for i in {1..30}; do
        if curl -s http://localhost:9200/_cluster/health > /dev/null 2>&1; then
            print_info "Elasticsearch is ready"
            break
        fi
        echo -n "."
        sleep 2
    done
    echo ""
    
    # Wait for Kibana
    print_info "Waiting for Kibana..."
    for i in {1..30}; do
        if curl -s http://localhost:5601/api/status > /dev/null 2>&1; then
            print_info "Kibana is ready"
            break
        fi
        echo -n "."
        sleep 2
    done
    echo ""
    
    print_info "Monitoring stack started successfully!"
    print_info "Access Kibana at: http://localhost:5601"
    print_info "Elasticsearch API at: http://localhost:9200"
}

# Function to stop monitoring stack
stop_monitoring() {
    print_info "Stopping ELK stack and beats..."
    cd "$SCRIPT_DIR"
    docker-compose -f docker-compose.elk.yml down
    print_info "Monitoring stack stopped"
}

# Function to restart monitoring stack
restart_monitoring() {
    print_info "Restarting monitoring stack..."
    stop_monitoring
    sleep 2
    start_monitoring
}

# Function to view logs
view_logs() {
    cd "$SCRIPT_DIR"
    if [ -z "$1" ]; then
        print_info "Showing logs for all services..."
        docker-compose -f docker-compose.elk.yml logs -f
    else
        print_info "Showing logs for $1..."
        docker-compose -f docker-compose.elk.yml logs -f "$1"
    fi
}

# Function to check status
check_status() {
    print_info "Checking monitoring stack status..."
    cd "$SCRIPT_DIR"
    
    echo ""
    print_info "=== Docker Containers ==="
    docker-compose -f docker-compose.elk.yml ps
    
    echo ""
    print_info "=== Elasticsearch Health ==="
    if curl -s http://localhost:9200/_cluster/health?pretty 2>/dev/null; then
        echo ""
    else
        print_error "Elasticsearch is not responding"
    fi
    
    echo ""
    print_info "=== Elasticsearch Indices ==="
    if curl -s http://localhost:9200/_cat/indices?v 2>/dev/null; then
        echo ""
    else
        print_error "Cannot retrieve indices"
    fi
    
    echo ""
    print_info "=== Service URLs ==="
    echo "Kibana:         http://localhost:5601"
    echo "Elasticsearch:  http://localhost:9200"
    echo "Logstash:       http://localhost:9600"
}

# Function to cleanup old data
cleanup_data() {
    print_warning "This will delete old monitoring data. Are you sure? (y/N)"
    read -r response
    
    if [[ "$response" =~ ^[Yy]$ ]]; then
        print_info "Cleaning up old indices..."
        
        # Delete indices older than 7 days
        # Get current date minus 7 days
        if date -v-7d &>/dev/null; then
            # BSD date (macOS)
            cutoff_date=$(date -v-7d +%Y.%m.%d)
        else
            # GNU date (Linux)
            cutoff_date=$(date -d '7 days ago' +%Y.%m.%d)
        fi
        
        print_info "Deleting indices older than $cutoff_date..."
        
        # Get list of indices and delete old ones
        curl -s "localhost:9200/_cat/indices/tcb-logs-*?h=index" | while read index; do
            index_date=$(echo "$index" | grep -oE '[0-9]{4}\.[0-9]{2}\.[0-9]{2}' || echo "")
            if [ ! -z "$index_date" ] && [ "$index_date" \< "$cutoff_date" ]; then
                print_info "Deleting index: $index"
                curl -X DELETE "localhost:9200/$index"
            fi
        done
        
        print_info "Cleanup complete"
    else
        print_info "Cleanup cancelled"
    fi
}

# Function to backup data
backup_data() {
    print_info "Backing up Elasticsearch data..."
    
    BACKUP_DIR="$PROJECT_ROOT/backups"
    mkdir -p "$BACKUP_DIR"
    
    BACKUP_FILE="$BACKUP_DIR/elasticsearch-backup-$(date +%Y%m%d-%H%M%S).tar.gz"
    
    # Get the actual volume name from docker-compose
    cd "$SCRIPT_DIR"
    VOLUME_NAME=$(docker-compose -f docker-compose.elk.yml config --volumes | grep elasticsearch-data | head -1)
    
    if [ -z "$VOLUME_NAME" ]; then
        print_warning "Could not determine volume name, using default"
        VOLUME_NAME="monitoring_elasticsearch-data"
    fi
    
    print_info "Using volume: $VOLUME_NAME"
    
    docker run --rm \
        -v "${VOLUME_NAME}:/data" \
        -v "$BACKUP_DIR:/backup" \
        ubuntu tar czf "/backup/$(basename $BACKUP_FILE)" /data
    
    print_info "Backup saved to: $BACKUP_FILE"
}

# Function to show help
show_help() {
    cat << EOF
TCB Trading Card Brain - Monitoring Stack Management

Usage: $0 [COMMAND]

Commands:
    start       Start the monitoring stack (ELK + Beats)
    stop        Stop the monitoring stack
    restart     Restart the monitoring stack
    status      Show status of all monitoring services
    logs        Show logs (optional: specify service name)
    cleanup     Clean up old monitoring data
    backup      Backup Elasticsearch data
    help        Show this help message

Examples:
    $0 start                # Start monitoring stack
    $0 logs                 # Show all logs
    $0 logs elasticsearch   # Show Elasticsearch logs only
    $0 status               # Check status of all services
    $0 cleanup              # Clean up old data

Service names:
    elasticsearch, logstash, kibana, filebeat, metricbeat, heartbeat

EOF
}

# Main script logic
main() {
    case "${1:-help}" in
        start)
            check_docker
            check_resources
            start_monitoring
            ;;
        stop)
            stop_monitoring
            ;;
        restart)
            check_docker
            restart_monitoring
            ;;
        status)
            check_status
            ;;
        logs)
            view_logs "$2"
            ;;
        cleanup)
            cleanup_data
            ;;
        backup)
            backup_data
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Unknown command: $1"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
