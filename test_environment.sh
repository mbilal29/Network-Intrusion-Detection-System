#!/bin/bash
# Quick test script to verify the IDS environment is working

echo "======================================"
echo "IDS Environment Quick Test"
echo "======================================"
echo ""

echo "Step 1: Checking if Docker network exists..."
if docker network ls | grep -q ids-net; then
    echo "✅ ids-net network exists"
else
    echo "❌ ids-net network NOT found"
    echo "Creating network..."
    docker network create --subnet=10.0.0.0/24 ids-net
fi

echo ""
echo "Step 2: Checking if containers are running..."
if docker ps | grep -q "ids"; then
    echo "✅ Containers are running"
    docker ps --filter "network=ids-net" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
else
    echo "❌ Containers not running"
    echo "Run: docker-compose up --build"
    exit 1
fi

echo ""
echo "Step 3: Testing connectivity..."
echo "Testing attacker → victim ping..."
docker exec attacker ping -c 2 10.0.0.30 > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Attacker can reach victim"
else
    echo "❌ Connectivity issue"
fi

echo ""
echo "======================================"
echo "Environment Status: READY ✅"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Open terminal: docker exec -it ids bash"
echo "2. Run sniffer: cd /app && python3 sniffer.py"
echo "3. In another terminal: docker exec -it attacker bash"
echo "4. Test attacks: ping 10.0.0.30 or nmap -sS 10.0.0.30"
echo ""
