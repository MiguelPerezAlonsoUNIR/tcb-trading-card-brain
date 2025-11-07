#!/bin/bash

# Validation script for ELK monitoring stack
# This script validates the monitoring setup before deployment

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=========================================="
echo "TCB Monitoring Stack Validation"
echo "=========================================="
echo ""

# Check 1: Docker Compose files syntax
echo "✓ Checking Docker Compose configurations..."
if docker compose -f "$SCRIPT_DIR/docker-compose.elk.yml" config > /dev/null 2>&1; then
    echo -e "${GREEN}✓ docker-compose.elk.yml is valid${NC}"
else
    echo -e "${RED}✗ docker-compose.elk.yml has syntax errors${NC}"
    exit 1
fi

if docker compose -f "$SCRIPT_DIR/../docker-compose.yml" config > /dev/null 2>&1; then
    echo -e "${GREEN}✓ docker-compose.yml is valid${NC}"
else
    echo -e "${RED}✗ docker-compose.yml has syntax errors${NC}"
    exit 1
fi

# Check 2: Configuration files exist
echo ""
echo "✓ Checking configuration files..."
REQUIRED_FILES=(
    "$SCRIPT_DIR/logstash/config/logstash.yml"
    "$SCRIPT_DIR/logstash/pipeline/logstash.conf"
    "$SCRIPT_DIR/kibana/config/kibana.yml"
    "$SCRIPT_DIR/filebeat/config/filebeat.yml"
    "$SCRIPT_DIR/metricbeat/config/metricbeat.yml"
    "$SCRIPT_DIR/heartbeat/config/heartbeat.yml"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓ $(basename $file) exists${NC}"
    else
        echo -e "${RED}✗ $(basename $file) is missing${NC}"
        exit 1
    fi
done

# Check 3: Validate YAML syntax for beat configs
echo ""
echo "✓ Validating YAML syntax..."

# Simple YAML validation for Python-based check
if command -v python3 &> /dev/null; then
    for file in "${REQUIRED_FILES[@]}"; do
        if [[ $file == *.yml ]]; then
            if python3 -c "import yaml; yaml.safe_load(open('$file'))" 2>/dev/null; then
                echo -e "${GREEN}✓ $(basename $file) has valid YAML${NC}"
            else
                echo -e "${RED}✗ $(basename $file) has invalid YAML${NC}"
                exit 1
            fi
        fi
    done
else
    echo -e "${YELLOW}! Python3 not found, skipping YAML validation${NC}"
fi

# Check 4: Management script permissions
echo ""
echo "✓ Checking management script..."
if [ -x "$SCRIPT_DIR/manage-monitoring.sh" ]; then
    echo -e "${GREEN}✓ manage-monitoring.sh is executable${NC}"
else
    echo -e "${YELLOW}! manage-monitoring.sh is not executable${NC}"
    chmod +x "$SCRIPT_DIR/manage-monitoring.sh"
    echo -e "${GREEN}✓ Fixed permissions for manage-monitoring.sh${NC}"
fi

# Check 5: Docker availability
echo ""
echo "✓ Checking Docker..."
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✓ Docker is installed${NC}"
    
    if docker info > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Docker daemon is running${NC}"
    else
        echo -e "${RED}✗ Docker daemon is not running${NC}"
        exit 1
    fi
else
    echo -e "${RED}✗ Docker is not installed${NC}"
    exit 1
fi

# Check 6: Port availability
echo ""
echo "✓ Checking port availability..."
PORTS=(9200 5601 5044 9600)
PORT_NAMES=("Elasticsearch" "Kibana" "Logstash Beats" "Logstash API")

for i in "${!PORTS[@]}"; do
    port=${PORTS[$i]}
    name=${PORT_NAMES[$i]}
    
    # Try multiple methods to check port availability
    port_in_use=false
    
    # Method 1: lsof (if available)
    if command -v lsof &> /dev/null; then
        if lsof -i:$port > /dev/null 2>&1; then
            port_in_use=true
        fi
    # Method 2: netstat (if available)
    elif command -v netstat &> /dev/null; then
        if netstat -tuln 2>/dev/null | grep ":$port " > /dev/null 2>&1; then
            port_in_use=true
        fi
    # Method 3: ss (if available)
    elif command -v ss &> /dev/null; then
        if ss -tuln 2>/dev/null | grep ":$port " > /dev/null 2>&1; then
            port_in_use=true
        fi
    fi
    
    if [ "$port_in_use" = false ]; then
        echo -e "${GREEN}✓ Port $port ($name) is available${NC}"
    else
        echo -e "${YELLOW}! Port $port ($name) is already in use${NC}"
    fi
done

# Check 7: System resources
echo ""
echo "✓ Checking system resources..."

# Check available memory (Linux)
if [[ -f /proc/meminfo ]]; then
    total_mem=$(grep MemTotal /proc/meminfo | awk '{print $2}')
    total_mem_gb=$((total_mem / 1024 / 1024))
    
    if [ $total_mem_gb -ge 4 ]; then
        echo -e "${GREEN}✓ Available RAM: ${total_mem_gb}GB (sufficient)${NC}"
    else
        echo -e "${YELLOW}! Available RAM: ${total_mem_gb}GB (recommended: 4GB+)${NC}"
    fi
fi

# Check available disk space
if command -v df &> /dev/null; then
    # Try with --output for better reliability
    if df --output=avail -BG "$SCRIPT_DIR" &> /dev/null; then
        available_space=$(df --output=avail -BG "$SCRIPT_DIR" | tail -1 | sed 's/G//' | tr -d ' ')
    else
        # Fallback to standard df with error handling
        available_space=$(df -BG "$SCRIPT_DIR" 2>/dev/null | tail -1 | awk '{print $4}' | sed 's/G//')
    fi
    
    # Verify we got a number
    if [[ "$available_space" =~ ^[0-9]+$ ]]; then
        if [ $available_space -ge 10 ]; then
            echo -e "${GREEN}✓ Available disk space: ${available_space}GB (sufficient)${NC}"
        else
            echo -e "${YELLOW}! Available disk space: ${available_space}GB (recommended: 10GB+)${NC}"
        fi
    else
        echo -e "${YELLOW}! Could not determine disk space${NC}"
    fi
fi

# Summary
echo ""
echo "=========================================="
echo -e "${GREEN}✓ Validation completed successfully!${NC}"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Start the monitoring stack: ./manage-monitoring.sh start"
echo "  2. Access Kibana: http://localhost:5601"
echo "  3. View logs: ./manage-monitoring.sh logs"
echo ""
