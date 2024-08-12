from proxmoxer import ProxmoxAPI
import warnings
from datetime import datetime

# Suppress only the InsecureRequestWarning
warnings.simplefilter('ignore', category=UserWarning)

def get_proxmox_api():
	""" Prompt user for Proxmox API Details and return a connection ProxmoxAPI object """
	# Replace input() with a more secure method to handle passwords in production
	host = input("Enter Promox host IP(example https://192.168.20.4): ")
	user = input("Enter Promox user (e.g. , root@pam): ")
	password = input("Enter Proxmox Password: ")

	return ProxmoxAPI(host, user=user, password=password, verify_ssl=False)

proxmox = get_proxmox_api()


# Collect data for the HTML file
node_data = {}

def format_datetime(timestamp):
    """ Convert Proxmox timestamp to a readable format """
    try:
        dt = datetime.fromtimestamp(int(timestamp))
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except Exception:
        return "Unknown"

def collect_info(node_name, container_type):
    containers = proxmox.nodes(node_name).__getattr__(container_type).get()

    if node_name not in node_data:
        node_data[node_name] = {
            'snapshots': '',
            'tags': '',
            'isos': '',
            'ha_status': ''
        }

    for container in containers:
        container_id = container['vmid']
        container_name = container['name']

        # Fetch the snapshots for the current container
        try:
            snapshots = proxmox.nodes(node_name).__getattr__(container_type)(container_id).snapshot.get()
        except Exception as e:
            snapshots = []
            node_data[node_name]['snapshots'] += f"<tr><td>{container_type.upper()} ID: {container_id}</td><td>{container_name}</td><td>Error fetching snapshots: {e}</td></tr>"
            continue

        # Fetch and display tags for the container
        try:
            container_config = proxmox.nodes(node_name).__getattr__(container_type)(container_id).config.get()
            tags = container_config.get('tags') or "No tags assigned"
        except Exception as e:
            tags = "Error fetching tags"

        # Check if there are any active snapshots
        active_snapshots = [snapshot for snapshot in snapshots if 'vmstate' in snapshot and snapshot.get('vmstate', 0) == 0]

        # Add to snapshot content only if there are active snapshots
        if active_snapshots:
            for snapshot in active_snapshots:
                snapshot_date = format_datetime(snapshot['snaptime'])
                node_data[node_name]['snapshots'] += f"<tr><td>{container_type.upper()} ID: {container_id}</td><td>{container_name}</td><td>{snapshot['name']}</td><td>{snapshot_date}</td></tr>"

        # Add to tag content
        node_data[node_name]['tags'] += f"<tr><td>{container_type.upper()} ID: {container_id}</td><td>{container_name}</td><td>{tags}</td></tr>"

        # Check for ISO mounted
        if container_type == 'qemu':  # Only for VMs, not LXCs
            try:
                container_config = proxmox.nodes(node_name).__getattr__(container_type)(container_id).config.get()
                disks = [key for key in container_config if key.startswith(('ide', 'sata'))]
                
                # Check for ISO mounts and extract ISO names
                isos = []
                for disk in disks:
                    if 'iso' in container_config[disk]:
                        iso_name = container_config[disk]  # Directly use the string value
                        isos.append(iso_name)
                
                if isos:
                    for iso_name in isos:
                        node_data[node_name]['isos'] += f"<tr><td>VM ID: {container_id}</td><td>{container_name}</td><td>ISO Mounted: {iso_name}</td></tr>"
            except Exception as e:
                node_data[node_name]['isos'] += f"<tr><td>VM ID: {container_id}</td><td>{container_name}</td><td>Error checking ISO: {e}</td></tr>"

        # Check HA status
        try:
            ha_status = proxmox.nodes(node_name).ha.resources(container_id).get()
            ha_status_text = "Enabled" if ha_status else "Disabled"
            node_data[node_name]['ha_status'] += f"<tr><td>{container_type.upper()} ID: {container_id}</td><td>{container_name}</td><td>{ha_status_text}</td></tr>"
        except Exception as e:
            node_data[node_name]['ha_status'] += f"<tr><td>{container_type.upper()} ID: {container_id}</td><td>{container_name}</td><td>Error fetching HA status: {e}</td></tr>"

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

# Create the HTML body with collapsible sections
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
                text-align: left;
            }}
            .collapsible {{
                background-color: #007bff;
                color: white;
                cursor: pointer;
                padding: 10px;
                width: 100%;
                border: none;
                text-align: left;
                outline: none;
                font-size: 16px;
            }}
            .active, .collapsible:hover {{
                background-color: #0056b3;
            }}
            .content {{
                padding: 0 18px;
                display: none;
                overflow: hidden;
                background-color: #f9f9f9;
            }}
        </style>
    </head>
    <body>
        <h2>Proxmox Cluster Report</h2>
"""

for node_name, data in node_data.items():
    node_section = f"""
        <div class="section">
            <button class="collapsible">{node_name}</button>
            <div class="content">
    """

    if data['snapshots']:
        node_section += f"""
            <h3>Snapshots Report</h3>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Snapshot Name</th>
                    <th>Snapshot Date</th>
                </tr>
                {data['snapshots']}
            </table>
        """

    node_section += f"""
            <h3>Tags Report</h3>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Tags</th>
                </tr>
                {data['tags']}
            </table>
    """

    if data['isos']:
        node_section += f"""
            <h3>VM ISO Status</h3>
            <table>
                <tr>
                    <th>VM ID</th>
                    <th>Name</th>
                    <th>ISO Status</th>
                </tr>
                {data['isos']}
            </table>
        """

    node_section += f"""
            <h3>HA Status</h3>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>HA Status</th>
                </tr>
                {data['ha_status']}
            </table>
            </div>
        </div>
    """

    html_content += node_section

html_content += """
        <script>
            var coll = document.getElementsByClassName("collapsible");
            var i;

            for (i = 0; i < coll.length; i++) {
                coll[i].addEventListener("click", function() {
                    this.classList.toggle("active");
                    var content = this.nextElementSibling;
                    if (content.style.display === "block") {
                        content.style.display = "none";
                    } else {
                        content.style.display = "block";
                    }
                });
            }
        </script>
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
