import yaml

from cvplibrary import CVPGlobalVariables, GlobalVariableNames
hostname = CVPGlobalVariables.getValue(GlobalVariableNames.CVP_SERIAL)



spine_bgp_template = """

ip prefix-list LOOPBACK
 %s

route-map LOOPBACK permit 10
 match ip address prefix-list LOOPBACK

peer-filter LEAF-AS-RANGE
 10 match as-range 65000-65535 result accept
 
router bgp %s
 router-id %s
 no bgp default ipv4-unicast
 maximum-paths 3
 distance bgp 20 200 200
 bgp listen range 192.168.0.0/16 peer-group LEAF_Underlay peer-filter LEAF-AS-RANGE
 neighbor LEAF_Underlay peer group
 neighbor LEAF_Underlay send-community
 neighbor LEAF_Underlay maximum-routes 12000
 redistribute connected route-map LOOPBACK
 address-family ipv4
  neighbor LEAF_Underlay activate
  redistribute connected route-map LOOPBACK
"""

leaf_bgp_template = """

ip prefix-list LOOPBACK
 %s

route-map LOOPBACK permit 10
 match ip address prefix-list LOOPBACK

router bgp %s
 router-id %s
 no bgp default ipv4-unicast
 maximum-paths 3
 distance bgp 20 200 200
 neighbor SPINE_Underlay peer group
 neighbor SPINE_Underlay remote-as %s
 neighbor SPINE_Underlay send-community
 neighbor SPINE_Underlay maximum-routes 12000
%s
 
 neighbor LEAF_Peer peer group
 neighbor LEAF_Peer remote-as %s
 neighbor LEAF_Peer next-hop-self
 neighbor LEAF_Peer maximum-routes 12000

 redistribute connected route-map LOOPBACK
 address-family ipv4
  neighbor SPINE_Underlay activate
  neighbor LEAF_Peer activate
  redistribute connected route-map LOOPBACK
  exit
  
"""

config = """
spine1-DC1:
  ASN: 65100
  interfaces:
    loopback0:
      ipv4: 192.168.101.101
    ethernet2:
      ipv4: 192.168.103.1
    ethernet3:
      ipv4: 192.168.103.7
    ethernet4:
      ipv4: 192.168.103.13
    ethernet5:
      ipv4: 192.168.103.19
    ethernet6:
      ipv4: 192.168.103.25
    ethernet7:
      ipv4: 192.168.103.31

spine2-DC1:
  ASN: 65100
  interfaces:
    loopback0:
      ipv4: 192.168.101.102
    ethernet2:
      ipv4: 192.168.103.3
    ethernet3:
      ipv4: 192.168.103.9
    ethernet4:
      ipv4: 192.168.103.15
    ethernet5:
      ipv4: 192.168.103.21
    ethernet6:
      ipv4: 192.168.103.27
    ethernet7:
      ipv4: 192.168.103.33

spine3-DC1:
  ASN: 65100
  interfaces:
    loopback0:
      ipv4: 192.168.101.103
    ethernet2:
      ipv4: 192.168.103.5
    ethernet3:
      ipv4: 192.168.103.11
    ethernet4:
      ipv4: 192.168.103.17
    ethernet5:
      ipv4: 192.168.103.23
    ethernet6:
      ipv4: 192.168.103.29
    ethernet7:
      ipv4: 192.168.103.35

leaf1-DC1:
  ASN: 65101
  interfaces:
    loopback0:
      ipv4: 192.168.101.11
    loopback1:
      ipv4: 192.168.102.11     
    ethernet3:
      ipv4: 192.168.103.0
    ethernet4:
      ipv4: 192.168.103.2
    ethernet5:
      ipv4: 192.168.103.4
  spine-peers:
    - 192.168.103.1
    - 192.168.103.3
    - 192.168.103.5

leaf2-DC1:
  ASN: 65101
  interfaces:
    loopback0:
      ipv4: 192.168.101.12
    loopback1:
      ipv4: 192.168.102.11     
    ethernet3:
      ipv4: 192.168.103.6
    ethernet4:
      ipv4: 192.168.103.8
    ethernet5:
      ipv4: 192.168.103.10
  spine-peers:
    - 192.168.103.7
    - 192.168.103.9
    - 192.168.103.11

leaf3-DC1:
  ASN: 65102
  interfaces:
    loopback0:
      ipv4: 192.168.101.13
    loopback1:
      ipv4: 192.168.102.13     
    ethernet3:
      ipv4: 192.168.103.12
    ethernet4:
      ipv4: 192.168.103.14
    ethernet5:
      ipv4: 192.168.103.16
  spine-peers:
    - 192.168.103.13
    - 192.168.103.15
    - 192.168.103.17

leaf4-DC1:
  ASN: 65102
  interfaces:
    loopback0:
      ipv4: 192.168.101.14
    loopback1:
      ipv4: 192.168.102.13     
    ethernet3:
      ipv4: 192.168.103.18
    ethernet4:
      ipv4: 192.168.103.20
    ethernet5:
      ipv4: 192.168.103.22
  spine-peers:
    - 192.168.103.19
    - 192.168.103.21
    - 192.168.103.23

borderleaf1-DC1:
  ASN: 65103
  interfaces:
    loopback0:
      ipv4: 192.168.101.21
    loopback1:
      ipv4: 192.168.102.21     
    ethernet3:
      ipv4: 192.168.103.24
    ethernet4:
      ipv4: 192.168.103.26
    ethernet5:
      ipv4: 192.168.103.28
    ethernet12:
      ipv4: 192.168.254.0
  spine-peers:
    - 192.168.103.25
    - 192.168.103.27
    - 192.168.103.29

borderleaf2-DC1:
  ASN: 65103
  interfaces:
    loopback0:
      ipv4: 192.168.101.22
    loopback1:
      ipv4: 192.168.102.21     
    ethernet3:
      ipv4: 192.168.103.30
    ethernet4:
      ipv4: 192.168.103.32
    ethernet5:
      ipv4: 192.168.103.34
    ethernet12:
      ipv4: 192.168.254.2
  spine-peers:
    - 192.168.103.31
    - 192.168.103.33
    - 192.168.103.35









spine1-DC2:
  ASN: 65200
  interfaces:
    loopback0:
      ipv4: 192.168.201.101
    ethernet2:
      ipv4: 192.168.203.1
    ethernet3:
      ipv4: 192.168.203.7
    ethernet4:
      ipv4: 192.168.203.13
    ethernet5:
      ipv4: 192.168.203.19
    ethernet6:
      ipv4: 192.168.203.25
    ethernet7:
      ipv4: 192.168.203.31

spine2-DC2:
  ASN: 65200
  interfaces:
    loopback0:
      ipv4: 192.168.201.102
    ethernet2:
      ipv4: 192.168.203.3
    ethernet3:
      ipv4: 192.168.203.9
    ethernet4:
      ipv4: 192.168.203.15
    ethernet5:
      ipv4: 192.168.203.21
    ethernet6:
      ipv4: 192.168.203.27
    ethernet7:
      ipv4: 192.168.203.33

spine3-DC2:
  ASN: 65200
  interfaces:
    loopback0:
      ipv4: 192.168.201.103
    ethernet2:
      ipv4: 192.168.203.5
    ethernet3:
      ipv4: 192.168.203.11
    ethernet4:
      ipv4: 192.168.203.17
    ethernet5:
      ipv4: 192.168.203.23
    ethernet6:
      ipv4: 192.168.203.29
    ethernet7:
      ipv4: 192.168.203.35

leaf1-DC2:
  ASN: 65201
  interfaces:
    loopback0:
      ipv4: 192.168.201.11
    loopback1:
      ipv4: 192.168.202.11     
    ethernet3:
      ipv4: 192.168.203.0
    ethernet4:
      ipv4: 192.168.203.2
    ethernet5:
      ipv4: 192.168.203.4
  spine-peers:
    - 192.168.203.1
    - 192.168.203.3
    - 192.168.203.5

leaf2-DC2:
  ASN: 65201
  interfaces:
    loopback0:
      ipv4: 192.168.201.12
    loopback1:
      ipv4: 192.168.202.11     
    ethernet3:
      ipv4: 192.168.203.6
    ethernet4:
      ipv4: 192.168.203.8
    ethernet5:
      ipv4: 192.168.203.10
  spine-peers:
    - 192.168.203.7
    - 192.168.203.9
    - 192.168.203.11

leaf3-DC2:
  ASN: 65202
  interfaces:
    loopback0:
      ipv4: 192.168.201.13
    loopback1:
      ipv4: 192.168.202.13     
    ethernet3:
      ipv4: 192.168.203.12
    ethernet4:
      ipv4: 192.168.203.14
    ethernet5:
      ipv4: 192.168.203.16
  spine-peers:
    - 192.168.203.13
    - 192.168.203.15
    - 192.168.203.17

leaf4-DC2:
  ASN: 65202
  interfaces:
    loopback0:
      ipv4: 192.168.201.14
    loopback1:
      ipv4: 192.168.202.13     
    ethernet3:
      ipv4: 192.168.203.18
    ethernet4:
      ipv4: 192.168.203.20
    ethernet5:
      ipv4: 192.168.203.22
  spine-peers:
    - 192.168.203.19
    - 192.168.203.21
    - 192.168.203.23

borderleaf1-DC2:
  ASN: 65203
  interfaces:
    loopback0:
      ipv4: 192.168.201.21
    loopback1:
      ipv4: 192.168.202.21     
    ethernet3:
      ipv4: 192.168.203.24
    ethernet4:
      ipv4: 192.168.203.26
    ethernet5:
      ipv4: 192.168.203.28
  spine-peers:
    - 192.168.203.25
    - 192.168.203.27
    - 192.168.203.29

borderleaf2-DC2:
  ASN: 65203
  interfaces:
    loopback0:
      ipv4: 192.168.201.22
    loopback1:
      ipv4: 192.168.202.21     
    ethernet3:
      ipv4: 192.168.203.30
    ethernet4:
      ipv4: 192.168.203.32
    ethernet5:
      ipv4: 192.168.203.34
  spine-peers:
    - 192.168.203.31
    - 192.168.203.33
    - 192.168.203.35
"""

switches = yaml.load(config)


switches = yaml.load(config)
for iface in switches[hostname]['interfaces']:
#Iterate through all interfaces using iface variable as the incrementing index
    print("interface %s") % iface
#Pull variables into easier to use variables
    ip = switches[hostname]['interfaces'][iface]['ipv4']
    if "ethernet" in iface:
        print " no switchport"
        print " mtu 9214"
        mask = 31
    elif "loopback" in iface:
        mask = 32
    print(" ip address %s/%s") % (ip, mask)
    

asn = switches[hostname]['ASN']
router_id = switches[hostname]['interfaces']['loopback0']['ipv4']

if "DC1" in hostname:
  prefix_list = "permit 192.168.101.0/24 eq 32"
  spine_asn = "65100"
elif "DC2" in hostname:
  prefix_list = "permit 192.168.201.0/24 eq 32"
  spine_asn = "65200"

if "spine" in hostname:
  print spine_bgp_template % (prefix_list, asn, router_id)
  
elif "leaf" in hostname:
    
    neighbors = ""
    for peer in switches[hostname]['spine-peers']:
      neighbors = neighbors + " neighbor " + peer + " peer group SPINE_Underlay\n"
    
    print leaf_bgp_template % (prefix_list, asn, router_id, spine_asn, neighbors, asn)
    
    
    