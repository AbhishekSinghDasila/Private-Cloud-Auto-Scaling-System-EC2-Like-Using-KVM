# Private-Cloud-Auto-Scaling-System-EC2-Like-Using-KVM
Designed and implemented an Infrastructure-as-a-Service (IaaS) auto-scaling system using KVM and Libvirt.  Developed a Python-based monitoring engine to dynamically provision VMs based on CPU utilization. 

## 📌 EC2-Like VM Auto-Scaling Using KVM (Private Cloud for IoMT Edge)
📖 Overview

This project implements an AWS EC2-like Auto-Scaling Infrastructure in a private cloud environment using Kernel-based Virtual Machine (KVM) and Libvirt.

The system dynamically provisions Virtual Machines (VMs) from a pre-configured Golden Image based on system CPU load — similar to how AWS EC2 Auto Scaling Groups launch instances during high demand.

This implementation simulates real-world Infrastructure-as-a-Service (IaaS) provisioning suitable for:

IoMT Edge Cloud

Federated Learning Clients

Hospital On-Premise Cloud

Intrusion Detection Training Nodes

Distributed Medical AI Workloads

## ⚙️ Technologies Used
```
Tool	                   Purpose
Python	            Monitoring + Automation
KVM	                   Hypervisor
QEMU               	Disk Management
Libvirt	            VM Lifecycle Control
QCOW2	              Backing Image
virbr0	            Virtual Network
SSH	                Remote Access
```

## 🏗️ Architecture
```
              CPU Monitor
                   │
                   ▼
           Python Autoscaler
                   │
         ┌─────────┼─────────┐
         ▼         ▼         ▼
   autoscale1 autoscale2 autoscaleN
         │         │
         └─────Clone─────┐
                         ▼
                   base-vm.qcow2
                         │
                         ▼
                     Libvirt
                         │
                         ▼
                         KVM
                         │
                         ▼
                      Host OS
```

## 🚀 Installation

# Install Virtualization Packages
```
sudo apt update
sudo apt install qemu-kvm libvirt-daemon-system virtinst bridge-utils python3-psutil
```

# Enable services:
```
sudo systemctl enable libvirtd
sudo systemctl start libvirtd
```

## 📦 Create Base Virtual Machine

```
virt-install \
--name base-vm \
--ram 2048 \
--vcpus 2 \
--disk path=base-vm.qcow2,format=qcow2 \
--os-variant ubuntu22.04 \
--network network=default \
--graphics none \
--console pty,target_type=serial \
--cdrom ubuntu-22.04.iso
```

## Install inside VM:
```
sudo apt install openssh-server stress
```

# Shutdown:
```
sudo shutdown now
```

## 🧠 Auto-Scaling Logic

# Run:
```
python3 autoscaler.py
```

System launches new VM when: CPU Usage > 60%

## 📊 Monitor Instances
```
virsh list --all
🧹 Destroy Instances
virsh destroy autoscale-vm1
virsh undefine autoscale-vm1
rm autoscale-vm1.qcow2
```

## 📴 Stop Environment Safely
```
sudo systemctl stop libvirtd.service \
libvirtd.socket \
libvirtd-ro.socket \
libvirtd-admin.socket
```

## ▶️ Restart Later
```
sudo systemctl start libvirtd
sudo virsh net-start default
```

