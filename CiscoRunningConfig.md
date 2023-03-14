Current configuration : 4827 bytes
!
! Last configuration change at 10:37:37 UTC Tue Mar 14 2023
!
version 15.0
no service pad
service timestamps debug datetime msec
service timestamps log datetime msec
no service password-encryption
service compress-config
!
hostname Switch
!
boot-start-marker
boot-end-marker
!
!
vrf definition Mgmt-vrf
 !
 address-family ipv4
 exit-address-family
 !
 address-family ipv6
 exit-address-family
!
!
no aaa new-model
switch 1 provision ws-c3850-48p
ip routing
!
ip device tracking
!
ip dhcp pool vlan_10
 network 192.168.10.0 255.255.255.0
 default-router 192.168.10.1
 dns-server 8.8.8.8
!
ip dhcp pool vlan_50
 network 192.168.50.0 255.255.255.0
 default-router 192.168.50.1
 dns-server 8.8.8.8
!
!
qos wireless-default-untrust
!
!
!
!
!
!
!
diagnostic bootup level minimal
identity policy webauth-global-inactive
 inactivity-timer 3600
spanning-tree mode pvst
spanning-tree extend system-id
!
redundancy
 mode sso
!
!
!
class-map match-any non-client-nrt-class
  match non-client-nrt
!
policy-map port_child_policy
 class non-client-nrt-class
    bandwidth remaining ratio 10
!
!
!
!
!
!
interface GigabitEthernet0/0
 vrf forwarding Mgmt-vrf
 no ip address
 negotiation auto
!
interface GigabitEthernet1/0/1
 no switchport
 ip address dhcp
!
interface GigabitEthernet1/0/2
 switchport access vlan 20
 switchport mode access
!
interface GigabitEthernet1/0/3
 switchport trunk allowed vlan 30,31
 switchport mode trunk
!
interface GigabitEthernet1/0/4
 switchport access vlan 50
 switchport mode access
!
interface GigabitEthernet1/0/5
 switchport access vlan 10
 switchport mode access
!
interface GigabitEthernet1/0/6
!
interface GigabitEthernet1/0/7
!
interface GigabitEthernet1/0/8
!
interface GigabitEthernet1/0/9
!
interface GigabitEthernet1/0/10
!
interface GigabitEthernet1/0/11
!
interface GigabitEthernet1/0/12
!
interface GigabitEthernet1/0/13
!
interface GigabitEthernet1/0/14
!
interface GigabitEthernet1/0/15
!
interface GigabitEthernet1/0/16
!
interface GigabitEthernet1/0/17
!
interface GigabitEthernet1/0/18
!
interface GigabitEthernet1/0/19
!
interface GigabitEthernet1/0/20
!
interface GigabitEthernet1/0/21
!
interface GigabitEthernet1/0/22
!
interface GigabitEthernet1/0/23
!
interface GigabitEthernet1/0/24
!
interface GigabitEthernet1/0/25
!
interface GigabitEthernet1/0/26
!
interface GigabitEthernet1/0/27
!
interface GigabitEthernet1/0/28
!
interface GigabitEthernet1/0/29
!
interface GigabitEthernet1/0/30
!
interface GigabitEthernet1/0/31
!
interface GigabitEthernet1/0/32
!
interface GigabitEthernet1/0/33
!
interface GigabitEthernet1/0/34
!
interface GigabitEthernet1/0/35
!
interface GigabitEthernet1/0/36
!
interface GigabitEthernet1/0/37
!
interface GigabitEthernet1/0/38
!
interface GigabitEthernet1/0/39
!
interface GigabitEthernet1/0/40
!
interface GigabitEthernet1/0/41
!
interface GigabitEthernet1/0/42
!
interface GigabitEthernet1/0/43
!
interface GigabitEthernet1/0/44
!
interface GigabitEthernet1/0/45
!
interface GigabitEthernet1/0/46
!
interface GigabitEthernet1/0/47
!
interface GigabitEthernet1/0/48
!
interface GigabitEthernet1/1/1
!
interface GigabitEthernet1/1/2
!
interface GigabitEthernet1/1/3
!
interface GigabitEthernet1/1/4
!
interface TenGigabitEthernet1/1/1
!
interface TenGigabitEthernet1/1/2
!
interface TenGigabitEthernet1/1/3
!
interface TenGigabitEthernet1/1/4
!
interface Vlan1
 no ip address
 shutdown
!
interface Vlan10
 ip address 192.168.10.1 255.255.255.0
!
interface Vlan20
 ip address 192.168.20.1 255.255.255.0
!
interface Vlan30
 ip address 192.168.30.1 255.255.255.0
!
interface Vlan31
 ip address 192.168.31.1 255.255.255.0
!
interface Vlan50
 ip address 192.168.50.1 255.255.255.0
!
router ospf 1
 router-id 1.1.1.1
 network 192.168.1.0 0.0.0.255 area 0
!
no ip http server
ip http authentication local
ip http secure-server
ip route 0.0.0.0 0.0.0.0 192.168.1.1
!
!
!
!
!
line con 0
 stopbits 1
line aux 0
 stopbits 1
line vty 0 4
 login
line vty 5 15
 login
!
wsma agent exec
 profile httplistener
 profile httpslistener
wsma agent config
 profile httplistener
 profile httpslistener
wsma agent filesys
 profile httplistener
 profile httpslistener
wsma agent notify
 profile httplistener
 profile httpslistener
!
wsma profile listener httplistener
 transport http
!
wsma profile listener httpslistener
 transport https
ap dot11 24ghz rrm channel dca 1
ap dot11 24ghz rrm channel dca 6
ap dot11 24ghz rrm channel dca 11
ap dot11 5ghz rrm channel dca 36
ap dot11 5ghz rrm channel dca 40
ap dot11 5ghz rrm channel dca 44
ap dot11 5ghz rrm channel dca 48
ap dot11 5ghz rrm channel dca 52
ap dot11 5ghz rrm channel dca 56
ap dot11 5ghz rrm channel dca 60
ap dot11 5ghz rrm channel dca 64
ap dot11 5ghz rrm channel dca 149
ap dot11 5ghz rrm channel dca 153
ap dot11 5ghz rrm channel dca 157
ap dot11 5ghz rrm channel dca 161
ap group default-group
end
