import requests
import json

def get_proxmox_ticket(api_url, username, password):
    login_url = f"{api_url}/access/ticket"
    data = {
        'username': root@pam,
        'password': '8cBuZ787'
    }
    response = requests.post(login_url, data=data, verify=False)
    response.raise_for_status()
    return response.json()['data']['ticket'], response.json()['data']['CSRFPreventionToken']

def generate_proxmox_report(node_name, username, password):
    api_url = "https://192.168.20.4:8006/api2/json"
    
    try:
        # Get authentication ticket
        ticket, csrf_token = get_proxmox_ticket(api_url, username, password)
        
        # Set up headers with authentication ticket
        headers = {
            'CSRFPreventionToken': csrf_token,
            'Cookie': f"PVEAuthCookie={ticket}"
        }
        
        # Fetch nodes
        nodes_response = requests.get(f"{api_url}/nodes", headers=headers, verify=False)
        nodes_response.raise_for_status()
        nodes_data = nodes_response.json()
        
        with open("proxmox_report.html", "w") as file:
            file.write("<html><body>")
            file.write("<h1>Proxmox Cluster Report</h1>")
            
            for node in nodes_data['data']:
                node_name = node['node']
                file.write(f"<h2>Node: {node_name}</h2>")
                
                # Fetch VM and LXC details for each node
                vms_response = requests.get(f"{api_url}/nodes/{node_name}/qemu", headers=headers, verify=False)
                vms_response.raise_for_status()
                vms_data = vms_response.json()
                
                file.write("<h3>Virtual Machines:</h3>")
                for vm in vms_data['data']:
                    vm_id = vm['vmid']
                    file.write(f"<h4>VM ID: {vm_id}</h4>")
                    
                    # Fetch snapshot and ISO info
                    snapshot_response = requests.get(f"{api_url}/nodes/{node_name}/qemu/{vm_id}/snapshot", headers=headers, verify=False)
                    snapshot_response.raise_for_status()
                    snapshot_data = snapshot_response.json()
                    
                    if snapshot_data['data']:
                        file.write("<h5>Snapshots:</h5>")
                        for snapshot in snapshot_data['data']:
                            if snapshot['vmstate'] == 0:
                                file.write(f"<p>Snapshot ID: {snapshot['snapname']}, Date: {snapshot['creation']}</p>")
                    
                    # Fetch ISO info
                    vm_config_response = requests.get(f"{api_url}/nodes/{node_name}/qemu/{vm_id}/config", headers=headers, verify=False)
                    vm_config_response.raise_for_status()
                    vm_config_data = vm_config_response.json()
                    
                    for device, value in vm_config_data['data'].items():
                        if device.startswith('ide') and 'iso' in value:
                            file.write(f"<p>Mounted ISO: {value}</p>")
                
                # Fetch LXC details
                lxc_response = requests.get(f"{api_url}/nodes/{node_name}/lxc", headers=headers, verify=False)
                lxc_response.raise_for_status()
                lxc_data = lxc_response.json()
                
                file.write("<h3>Containers:</h3>")
                for lxc in lxc_data['data']:
                    lxc_id = lxc['vmid']
                    file.write(f"<h4>Container ID: {lxc_id}</h4>")
                    
                    # Fetch snapshot info for LXC
                    snapshot_response = requests.get(f"{api_url}/nodes/{node_name}/lxc/{lxc_id}/snapshot", headers=headers, verify=False)
                    snapshot_response.raise_for_status()
                    snapshot_data = snapshot_response.json()
                    
                    if snapshot_data['data']:
                        file.write("<h5>Snapshots:</h5>")
                        for snapshot in snapshot_data['data']:
                            if snapshot['vmstate'] == 0:
                                file.write(f"<p>Snapshot ID: {snapshot['snapname']}, Date: {snapshot['creation']}</p>")
            
            file.write("</body></html>")
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
