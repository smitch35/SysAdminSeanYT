### First we’ll build our global routing for the 3850.
```
Conf t
Ip routing
Router ospf 1
Router-id 1.1.1.1
Network 192.168.1.0 0.0.0.255 area 0
Ip route 0.0.0.0 0.0.0.0 192.168.1.1
```

### Configure port 1 as outbound
```
Conf t
Interface gigabitethernet 1/0/1
No switchport
No shutdown
Ip address dhcp
```

### Configuring VLAN10 End User Vlan (Do this for every vlan you want to setup)
```
Conf t
Vlan 10
Name end_user
Interface vlan 10
Ip address 192.168.10.1 255.255.255.0
Exit
```

### Configure dhcp pools
```
Ip dhcp pool vlan_10
network 192.168.10.0 255.255.255.0
default-router 192.168.10.1
dns-server 8.8.8.8
```

### Configure an Access Port
```
interface [interface-id]
switchport mode access
switchport access vlan 20
No shutdown
```

### Configure a Trunk Port
```
interface [interface-id]
switchport mode trunk
switchport trunk allowed vlan 30,31 
No shutdown
```

### VLAN list
## vlan 10 "End users"
## vlan 20 "HOST MGMT"
## vlan 30 "Vm network 1"
## vlan 31 "vm network 2"
## vlan 50 "out of band host mgmt"


### Configure SSH
```
 ip domain-name your_domain_name
 crypto key generate rsa general-keys modulus 2048
 ip ssh version 2
 username your_username secret your_password
 username your_username privilege 15
 line vty 0 15
 transport input ssh
 write memory
```