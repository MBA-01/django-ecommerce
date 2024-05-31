import psutil

def check_running_processes(process_name):
    for proc in psutil.process_iter(['pid','name']):
        try:
            if process_name.lower() in proc.info['name'].lower():
                print(f"Process {proc.info['name']} with PID {proc.info['pid']} is running.")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass

# Check for a specific process
check_running_processes('python')


