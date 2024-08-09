from proxmoxer import ProxmoxAPI
import requests
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from datetime import datetime

# Suppress only the InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)

# Replace with your Proxmox cluster details
proxmox = ProxmoxAPI('192.168.20.4', user='root@pam', password='8cBuZ787', verify_ssl=False)

# Collect data for the HTML file
snapshot_content = ""
tag_content = ""
iso_content = ""
ha_content = ""

def format_datetime(timestamp):
    """ Convert Proxmox timestamp to a readable format """
    try:
        dt = datetime.fromtimestamp(int(timestamp))
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except Exception:
        return "Unknown"

def collect_info(node_name, container_type):
    global snapshot_content, tag_content, iso_content, ha_content
    containers = proxmox.nodes(node_name).__getattr__(container_type).get()

    for container in containers:
        container_id = container['vmid']
        container_name = container['name']

        # Fetch the snapshots for the current container
        try:
            snapshots = proxmox.nodes(node_name).__getattr__(container_type)(container_id).snapshot.get()
            print(f"Snapshots for {container_type} ID {container_id}: {snapshots}")  # Debug statement
        except Exception as e:
            snapshots = []
            snapshot_content += f"<tr><td>{node_name}</td><td>{container_type.upper()} ID: {container_id}</td><td>{container_name}</td><td>Error fetching snapshots: {e}</td></tr>"
            continue

        # Fetch and display tags for the container
        try:
            container_config = proxmox.nodes(node_name).__getattr__(container_type)(container_id).config.get()
            tags = container_config.get('tags') or "No tags assigned"
        except Exception as e:
            tags = "Error fetching tags"
        
        # Check if there are any active snapshots
        active_snapshots = [snapshot for snapshot in snapshots if 'vmstate' in snapshot and snapshot.get('vmstate', 0) == 0]
        print(f"Active snapshots for {container_type} ID {container_id}: {active_snapshots}")  # Debug statement

        # Add to snapshot content
        if active_snapshots:
            for snapshot in active_snapshots:
                snapshot_date = format_datetime(snapshot['snaptime'])
                snapshot_content += f"<tr><td>{node_name}</td><td>{container_type.upper()} ID: {container_id}</td><td>{container_name}</td><td>{snapshot['name']}</td><td>{snapshot_date}</td></tr>"
        else:
            snapshot_content += f"<tr><td>{node_name}</td><td>{container_type.upper()} ID: {container_id}</td><td>{container_name}</td><td>No active snapshots</td><td></td></tr>"

        # Add to tag content
        tag_content += f"<tr><td>{node_name}</td><td>{container_type.upper()} ID: {container_id}</td><td>{container_name}</td><td>{tags}</td></tr>"

        # Check for ISO mounted
        if container_type == 'qemu':  # Only for VMs, not LXCs
            try:
                container_config = proxmox.nodes(node_name).__getattr__(container_type)(container_id).config.get()
                print(f"Container config for VM ID {container_id}: {container_config}")  # Debug statement
                
                # Check for both IDE and SATA with specific names like ide2
                ide_disks = [disk for disk in container_config if disk.startswith('ide')]
                sata_disks = [disk for disk in container_config if disk.startswith('sata')]
                print(f"IDE Disks for VM ID {container_id}: {ide_disks}")  # Debug statement
                print(f"SATA Disks for VM ID {container_id}: {sata_disks}")  # Debug statement
                
                # Combine all disk entries
                disks = ide_disks + sata_disks
                
                # Check for ISO mounts and extract ISO names
                isos = []
                for disk in disks:
                    if 'iso' in container_config[disk]:
                        iso_name = container_config[disk]  # Directly use the string value
                        isos.append(iso_name)
                
                if isos:
                    for iso_name in isos:
                        iso_content += f"<tr><td>{node_name}</td><td>VM ID: {container_id}</td><td>{container_name}</td><td>ISO Mounted: {iso_name}</td></tr>"
                else:
                    iso_content += f"<tr><td>{node_name}</td><td>VM ID: {container_id}</td><td>{container_name}</td><td>No ISO Mounted</td></tr>"
            except Exception as e:
                iso_content += f"<tr><td>{node_name}</td><td>VM ID: {container_id}</td><td>{container_name}</td><td>Error checking ISO: {e}</td></tr>"

        # Check HA status
        try:
            ha_status = proxmox.nodes(node_name).ha.resources(container_id).get()
            ha_status_text = "Enabled" if ha_status else "Disabled"
            ha_content += f"<tr><td>{node_name}</td><td>{container_type.upper()} ID: {container_id}</td><td>{container_name}</td><td>{ha_status_text}</td></tr>"
        except Exception as e:
            ha_content += f"<tr><td>{node_name}</td><td>{container_type.upper()} ID: {container_id}</td><td>{container_name}</td><td>Error fetching HA status: {e}</td></tr>"

# Get list of nodes in the cluster
try:
    nodes = proxmox.nodes.get()
except Exception as e:
    print(f"Error fetching nodes: {e}")
    nodes = []

# Collect information for all nodes
for node in nodes:
    node_name = node['node']
    collect_info(node_name, 'qemu')
    collect_info(node_name, 'lxc')

# Create the HTML body with separate sections for snapshots, tags, ISO status, and HA status
html_content = f"""
<html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                text-align: center;
                background-color: #f4f4f4;
                color: #333;
            }}
            h2, h3 {{
                color: #0056b3;
            }}
            table {{
                margin: 20px auto;
                border-collapse: collapse;
                width: 90%;
                background-color: #ffffff;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }}
            th {{
                background-color: #007bff;
                color: #ffffff;
            }}
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            tr:hover {{
                background-color: #f1f1f1;
            }}
            .section {{
                margin: 20px 0;
            }}
        </style>
    </head>
    <body>
        <h2>Proxmox Cluster Report</h2>
        <div class="section">
            <h3>Snapshots Report</h3>
            <table>
                <tr>
                    <th>Node</th>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Snapshot Name</th>
                    <th>Snapshot Date</th>
                </tr>
                {snapshot_content}
            </table>
        </div>
        <div class="section">
            <h3>Tags Report</h3>
            <table>
                <tr>
                    <th>Node</th>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Tags</th>
                </tr>
                {tag_content}
            </table>
        </div>
        <div class="section">
            <h3>VM ISO Status</h3>
            <table>
                <tr>
                    <th>Node</th>
                    <th>VM ID</th>
                    <th>Name</th>
                    <th>ISO Status</th>
                </tr>
                {iso_content}
            </table>
        </div>
        <div class="section">
            <h3>HA Status</h3>
            <table>
                <tr>
                    <th>Node</th>
                    <th>ID</th>
                    <th>Name</th>
                    <th>HA Status</th>
                </tr>
                {ha_content}
            </table>
        </div>
    </body>
</html>
"""

# Write the HTML content to a file
output_file = 'proxmox_cluster_report.html'
try:
    with open(output_file, 'w') as file:
        file.write(html_content)
    print(f"HTML report successfully created: {output_file}")
except Exception as e:
    print(f"Failed to create HTML file: {e}")
