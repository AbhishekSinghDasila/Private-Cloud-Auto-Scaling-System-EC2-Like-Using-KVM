import subprocess
import time

THRESHOLD_UP = 60
THRESHOLD_DOWN = 20
MAX_VMS = 3
MIN_VMS = 1
COOLDOWN = 30  # seconds between scaling actions

vm_prefix = "autoscale-vm2"
base_image = "base-vm2.qcow2"

last_scaled_time = 0

def get_running_vms():
    result = subprocess.check_output("virsh list --name", shell=True)
    vms = result.decode().strip().split("\n")
    return [vm for vm in vms if vm.startswith(vm_prefix) and vm != ""]

def get_cpu_time(vm):
    cmd = f"virsh domstats {vm} --vcpu | grep vcpu.0.time"
    result = subprocess.check_output(cmd, shell=True)
    return int(result.decode().split("=")[1])

def get_cpu_usage(vm, interval=2):
    t1 = get_cpu_time(vm)
    time.sleep(interval)
    t2 = get_cpu_time(vm)
    delta = t2 - t1
    return (delta / (interval * 1e9)) * 100

def get_average_cpu(vms):
    total = 0
    for vm in vms:
        total += get_cpu_usage(vm)
    return total / len(vms)

def create_vm(index):
    vm_name = f"{vm_prefix}{index}"
    disk_name = f"{vm_name}.qcow2"

    subprocess.call(
        f"qemu-img create -f qcow2 -b {base_image} -F qcow2 {disk_name}",
        shell=True
    )

    subprocess.call(
        f"virt-install --name {vm_name} "
        f"--ram 1024 --vcpus 1 "
        f"--disk path={disk_name} "
        f"--import --os-variant ubuntu20.04 "
        f"--network network=default "
        f"--graphics none --noautoconsole",
        shell=True
    )

    print(f"[SCALE UP] Created {vm_name}")

def delete_vm(vm):
    subprocess.call(f"virsh destroy {vm}", shell=True)
    subprocess.call(f"virsh undefine {vm}", shell=True)
    subprocess.call(f"rm -f {vm}.qcow2", shell=True)
    print(f"[SCALE DOWN] Deleted {vm}")

def monitor():
    global last_scaled_time

    while True:
        vms = get_running_vms()

        if not vms:
            time.sleep(5)
            continue

        avg_cpu = get_average_cpu(vms)
        print(f"Average CPU Usage: {avg_cpu:.2f}% | Active VMs: {len(vms)}")

        current_time = time.time()

        if current_time - last_scaled_time > COOLDOWN:

            if avg_cpu > THRESHOLD_UP and len(vms) < MAX_VMS:
                create_vm(len(vms) + 1)
                last_scaled_time = current_time

            elif avg_cpu < THRESHOLD_DOWN and len(vms) > MIN_VMS:
                delete_vm(vms[-1])
                last_scaled_time = current_time

        time.sleep(5)

if __name__ == "__main__":
    monitor()
