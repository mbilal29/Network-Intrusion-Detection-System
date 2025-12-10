# Docker Setup Guide

## 🐳 Overview

The Docker environment simulates a realistic network with three containers:
- **Attacker**: Executes real attack tools (nmap, hping3, arping)
- **IDS**: Analyzes traffic and detects intrusions
- **Victim**: Target system for attacks

## 📋 Prerequisites

- Docker Desktop installed and running
- Python 3.x with scapy, matplotlib, numpy

## 🚀 Quick Start

### 1. Start Docker Containers

```bash
docker-compose up -d
```

**Expected output:**
```
Creating network "ids-net"
Creating ids_container
Creating attacker_container
Creating victim_container
```

### 2. Verify Containers

```bash
docker ps
```

Should show 3 running containers: `ids`, `attacker`, `victim`

### 3. Run Docker Workflow

```bash
cd ids/
python3 run_docker_workflow.py
```

**What happens:**
1. Verifies Docker containers are running
2. Executes real attacks from attacker container
3. Generates PCAPs for IDS analysis
4. Creates visualizations and HTML report
5. Opens report in browser

---

## 🌐 Network Architecture

```
Docker Network: ids-net (10.0.0.0/24)

┌──────────────────────────┐
│   Attacker Container     │
│   IP: 10.0.0.20         │
│   Tools: nmap, hping3    │
│          arping          │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│   IDS Container          │
│   IP: 10.0.0.10         │
│   Python + Scapy        │
│   NET_ADMIN capability   │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│   Victim Container       │
│   IP: 10.0.0.30         │
│   Target: Open ports     │
└──────────────────────────┘
```

---

## 🔧 Docker Compose Configuration

Key settings in `docker-compose.yml`:

```yaml
services:
  ids:
    cap_add:
      - NET_ADMIN  # Enable promiscuous mode
      - NET_RAW    # Enable raw socket access
    networks:
      ids-net:
        ipv4_address: 10.0.0.10
  
  attacker:
    image: kalilinux/kali-rolling
    networks:
      ids-net:
        ipv4_address: 10.0.0.20
  
  victim:
    image: ubuntu:22.04
    networks:
      ids-net:
        ipv4_address: 10.0.0.30

networks:
  ids-net:
    driver: bridge
    ipam:
      config:
        - subnet: 10.0.0.0/24
```

---

## 🎯 Attack Tools

### Port Scan (nmap)
```bash
docker exec attacker nmap -p 1-100 10.0.0.30
```
- Scans ports 1-100 on victim
- Generates PORT_SCAN alerts
- Triggers HIGH_PORT_ENTROPY anomaly detection

### SYN Flood (hping3)
```bash
docker exec attacker hping3 -S -p 80 --flood --rand-source 10.0.0.30
```
- Floods victim port 80 with SYN packets
- Generates SYN_FLOOD alerts
- Shows CRITICAL severity

### ARP Activity (arping)
```bash
docker exec attacker arping -c 10 -I eth0 10.0.0.30
```
- Sends ARP requests to victim
- Generates ARP_SPOOF alerts when MAC changes detected
- Tests baseline anomaly detection

---

## 🔍 Troubleshooting

### Problem: Containers won't start
**Solution:**
```bash
docker-compose down
docker-compose up -d
```

### Problem: "Cannot connect to Docker daemon"
**Solution:** Start Docker Desktop application

### Problem: Network connectivity issues
**Solution:**
```bash
# Verify network exists
docker network ls | grep ids-net

# Inspect network
docker network inspect network-intrusion-detection-system_ids-net
```

### Problem: Attack tools not found
**Solution:**
```bash
# Rebuild attacker container
docker-compose build attacker
docker-compose up -d
```

---

## 📊 Monitoring Docker Containers

### View Container Logs
```bash
# IDS logs
docker logs ids

# Attacker logs
docker logs attacker

# Victim logs
docker logs victim
```

### Check Container Resources
```bash
docker stats
```

### Execute Commands in Containers
```bash
# Access attacker shell
docker exec -it attacker /bin/bash

# Access IDS shell
docker exec -it ids /bin/bash

# Access victim shell
docker exec -it victim /bin/bash
```

---

## 🧹 Cleanup

### Stop Containers
```bash
docker-compose down
```

### Remove Containers and Network
```bash
docker-compose down -v
```

### Remove Images (optional)
```bash
docker rmi network-intrusion-detection-system_ids
docker rmi network-intrusion-detection-system_attacker
docker rmi network-intrusion-detection-system_victim
```

---

## �� Tips

1. **Always start Docker first:** `docker-compose up -d` before running workflow
2. **Check container status:** Use `docker ps` to verify all 3 containers are running
3. **View real-time logs:** `docker logs -f ids` to see IDS output
4. **Network isolation:** Docker network is isolated from host by default
5. **Rebuild after changes:** `docker-compose build` if you modify Dockerfiles
