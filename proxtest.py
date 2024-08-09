from proxmoxer import ProxmoxAPI
import urllib3

# Disable SSL warnings (if you're not verifying SSL certificates)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Replace with your Proxmox host details
proxmox = ProxmoxAPI('192.168.20.4', user='root@pam', password='8cBuZ787', verify_ssl=False)

# Define the node name as a variable
node_name = 'TigerHost04'

# Collect data for the HTML file
email_content = ""
cdrom_content = ""
ha_content = ""

def collect_info(container_type):
    global email_content, cdrom_content, ha_content
    containers = proxmox.nodes(node_name).__getattr__(container_type).get()

    for container in containers:
        container_id = container['vmid']
        container_name = container['name']

        # Fetch the snapshots for the current container
        try:
            snapshots = proxmox.nodes(node_name).__getattr__(container_type)(container_id).snapshot.get()
        except Exception as e:
            snapshots = []
            email_content += f"<tr><td>{container_type.upper()} ID: {container_id}</td><td>{container_name}</td><td>Error fetching snapshots: {e}</td><td></td></tr>"
            continue

        # Fetch and display tags for the container
        container_config = proxmox.nodes(node_name).__getattr__(container_type)(container_id).config.get()
        tags = container_config.get('tags') or "No tags assigned"

        # Check if there are any active snapshots
        active_snapshots = [snapshot for snapshot in snapshots if snapshot.get('vmstate', 0) == 1]

        # Add to email content
        if active_snapshots:
            for snapshot in active_snapshots:
                email_content += f"<tr><td>{container_type.upper()} ID: {container_id}</td><td>{container_name}</td><td>{snapshot['name']}, Created On: {snapshot['snaptime']}</td><td>{tags}</td></tr>"
        else:
            email_content += f"<tr><td>{container_type.upper()} ID: {container_id}</td><td>{container_name}</td><td>No active snapshots</td><td>{tags}</td></tr>"

        # Check for CD-ROM mounted
        if container_type == 'qemu':  # Only for VMs, not LXCs
            try:
                disks = container_config.get('ide', [])
                cdroms = [disk for disk in disks if 'cdrom' in disk]
                if cdroms:
                    cdrom_content += f"<tr><td>VM ID: {container_id}</td><td>{container_name}</td><td>CD-ROM Mounted</td></tr>"
                else:
                    cdrom_content += f"<tr><td>VM ID: {container_id}</td><td>{container_name}</td><td>No CD-ROM Mounted</td></tr>"
            except Exception as e:
                cdrom_content += f"<tr><td>VM ID: {container_id}</td><td>{container_name}</td><td>Error checking CD-ROM: {e}</td></tr>"

        # Check HA status
        try:
            ha_status = proxmox.nodes(node_name).ha.resources(container_id).get()
            ha_status_text = "Enabled" if ha_status else "Disabled"
            ha_content += f"<tr><td>{container_type.upper()} ID: {container_id}</td><td>{container_name}</td><td>{ha_status_text}</td></tr>"
        except Exception as e:
            ha_content += f"<tr><td>{container_type.upper()} ID: {container_id}</td><td>{container_name}</td><td>Error fetching HA status: {e}</td></tr>"

# Collect information for both VMs and LXCs
collect_info('qemu')
collect_info('lxc')

# Create the HTML body with the collected information
html_content = f"""
<html>
    <body>
        <h2>Proxmox VM and LXC Report</h2>
        <h3>VMs and LXCs Snapshot and Tag Report</h3>
        <table border="1" cellpadding="5" cellspacing="0">
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Snapshot Info</th>
                <th>Tags</th>
            </tr>
            {email_content}
        </table>
        <h3>VM CD-ROM Status</h3>
        <table border="1" cellpadding="5" cellspacing="0">
            <tr>
                <th>VM ID</th>
                <th>Name</th>
                <th>CD-ROM Status</th>
            </tr>
            {cdrom_content}
        </table>
        <h3>HA Status</h3>
        <table border="1" cellpadding="5" cellspacing="0">
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>HA Status</th>
            </tr>
            {ha_content}
        </table>
    </body>
</html>
"""

# Write the HTML content to a file
output_file = 'proxmox_report.html'
try:
    with open(output_file, 'w') as file:
        file.write(html_content)
    print(f"HTML report successfully created: {output_file}")
except Exception as e:
    print(f"Failed to create HTML file: {e}")
