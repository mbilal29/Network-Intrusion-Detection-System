# Network-Intrusion-Detection-System

A network based intrusion detection system on a docker-based virtual network

## 📘 Setup & Environment Guide

This project runs on a Docker-based virtual network consisting of three isolated containers:

- **IDS**
- **Attacker**
- **Victim**

All containers communicate on a custom Docker subnet (`ids-net`) to safely simulate and analyze malicious traffic.

## 🛠️ 1. Prerequisites

Install:

- **Docker Desktop** (macOS/Windows/Linux)

## 🌐 2. Create the Docker Network

This network acts like a LAN switch, allowing the IDS to monitor attacker → victim traffic.

```bash
docker network create --subnet=10.0.0.0/24 ids-net
```

## 🧱 3. Build and Launch the Environment

Run from the project root:

```bash
docker-compose up --build
```

This will:

- ✔ Build all 3 Docker images
- ✔ Start attacker, victim, and IDS containers
- ✔ Connect them to the `ids-net` network
- ✔ Assign static IPs:
  - **IDS** → `10.0.0.10`
  - **Attacker** → `10.0.0.20`
  - **Victim** → `10.0.0.30`

If everything builds correctly, you will see:

```
✔ network-intrusion-detection-system-attacker Built
✔ network-intrusion-detection-system-ids Built
✔ network-intrusion-detection-system-victim Built
✔ Container attacker Created
✔ Container ids Created
✔ Container victim Created
```

## 🖥️ 4. Opening Shells Inside Each Container

Open 3 separate terminals for easy testing.

**Attacker**
```bash
docker exec -it attacker bash
```

**Victim**
```bash
docker exec -it victim bash
```

**IDS Node**
```bash
docker exec -it ids bash
```

