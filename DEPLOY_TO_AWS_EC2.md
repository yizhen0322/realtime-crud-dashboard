# ☁️ Deployment Guide: AWS EC2

Deploying to AWS EC2 is very similar to DigitalOcean, but you need to handle **Keys (.pem)** and **Security Groups** (Firewall).

## Phase 1: Launch Instance
1.  Log in to AWS Console -> **EC2**.
2.  Click **Launch Instance**.
3.  **Name**: `internship-backend`.
4.  **OS Image**: Select **Ubuntu** (Ubuntu Server 24.04 LTS).
5.  **Instance Type**: `t2.micro` or `t3.micro` (Free tier eligible).
6.  **Key Pair**:
    -   Click **Create new key pair**.
    -   Name: `my-school-key`.
    -   Type: `RSA`, Format: `.pem`.
    -   **Download the file** and save it to: `C:\Users\yizhen\Desktop\sunway study\alphv_pretask\my-school-key.pem` (Move it there manually).
7.  **Network Settings** (IMPORTANT):
    -   Check **Allow SSH traffic**.
    -   Check **Allow HTTP traffic**.
    -   Click **Edit** (top right of Network settings box).
    -   **Add Security Group Rule**:
        -   Type: `Custom TCP`
        -   Port range: `5173`
        -   Source: `Anywhere (0.0.0.0/0)`
    -   **Add Another Rule**:
        -   Type: `Custom TCP`
        -   Port range: `8000`
        -   Source: `Anywhere (0.0.0.0/0)`
    *This allows you to access the frontend and backend.*
8.  Click **Launch Instance**.
9.  Copy the **Public IPv4 address** (e.g., `54.1.2.3`).

## Phase 2: Copy Files (SCP with Key)
*Do this on your Windows PowerShell.*

1.  Make sure your `.pem` key is in the project folder. (I found `yizhenEC2key.pem`!)
2.  Run this command (Using `ec2-user` for Amazon Linux):
    ```powershell
    cd "C:\Users\yizhen\Desktop\sunway study\alphv_pretask"
    
    # Upload the zip file
    scp -i "yizhenEC2key.pem" submission.zip ec2-user@54.167.59.82:/home/ec2-user/app.zip
    ```

## Phase 3: Run on Server
1.  **SSH into the server**:
    ```powershell
    ssh -i "yizhenEC2key.pem" ec2-user@54.167.59.82
    ```
2.  **Install Docker & Run** (Run these commands inside the AWS server):
    ```bash
    # Update and install unzip/docker
    sudo yum update -y
    sudo yum install -y unzip docker
    
    # Start Docker service
    sudo service docker start
    sudo usermod -a -G docker ec2-user
    # (You might need to exit and reconnect for permissions, but sudo works for now)
    
    # Install Docker Compose Plugin
    sudo mkdir -p /usr/local/lib/docker/cli-plugins/
    sudo curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 -o /usr/local/lib/docker/cli-plugins/docker-compose
    sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
    
    # Unzip app
    unzip app.zip
    
    # Run app
    sudo docker compose up -d --build
    ```

3.  **Access App**:
    -   Frontend: `http://54.160.232.239:5173`
    -   Backend: `http://54.160.232.239:8000`
