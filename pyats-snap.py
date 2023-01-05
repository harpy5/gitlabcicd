import pyats
from virl2_client import ClientLibrary
from genie.conf import Genie
from genie.utils.diff import Diff
from pprint import pprint
import yaml
import json
client = ClientLibrary("https://10.85.48.20", "admin", "C!sco12345", ssl_verify=False)
testbed = Genie.init("newtest.yml")

R1_config = testbed.devices["R1"]
R2_config = testbed.devices["R2"]
SW1_config =  testbed.devices["dist_sw1"]
SW2_config =  testbed.devices["dist_sw2"]
Access1_config = testbed.devices["access_1"]
Access2_config = testbed.devices['access_2']

R1_config.connect(learn_hostname=True, log_stdout=False)
R2_config.connect(learn_hostname=True, log_stdout=False)
SW1_config.connect(learn_hostname=True, log_stdout=False)
SW2_config.connect(learn_hostname=True, log_stdout=False)
Access1_config.connect(learn_hostname=True, log_stdout=False)
Access2_config.connect(learn_hostname=True, log_stdout=False)
#output = R1_config.parse('show ip ospf neighbor detail')
#print(type(output))
#with open("ospf_pre_neighbor.json", "w") as file:
#	json.dump(output, file, indent=2)
#output = R1_config.learn('ospf')
#interface_snap = R1_config.learn('interface')
#pprint(output.info)
#with open("ospf_pre.json", "w") as file1:
#	json.dump(output.info, file1, indent=2)
    
#with open("interface_pre.json", "w") as file2:
#	json.dump(interface_snap.info, file2, indent=2)

#R1_config.configure('''
#interface GigabitEthernet 0/1
#description shutdown with pyats 
#shutdown
#''')
R2_config.configure('''
      interface GigabitEthernet0/0
       no shut
       ip ospf 10 area 0
       duplex auto
       speed auto
       media-type rj45
      !
      interface GigabitEthernet0/1
       no shut
       ip ospf 10 area 0
       duplex auto
       speed auto
       media-type rj45
      !
      interface GigabitEthernet0/2
       no shut
       ip ospf 10 area 0
       duplex auto
       speed auto
       media-type rj45
      !
      interface GigabitEthernet0/3
       no shut
       duplex auto
       speed auto
       media-type rj45
      !
      router ospf 10
       router-id 10.90.5.10
      !
      ip route 0.0.0.0 0.0.0.0 10.131.10.17
      !
''')

R1_config.configure('''

       interface GigabitEthernet0/0
       no shut
       ip ospf 10 area 0
       duplex auto
       speed auto
       media-type rj45
      !
      interface GigabitEthernet0/1
       no shut
       ip ospf 10 area 0
       duplex auto
       speed auto
       media-type rj45
      !
      interface GigabitEthernet0/2
       no shut
       ip ospf 10 area 0
       duplex auto
       speed auto
       media-type rj45
      !
      interface GigabitEthernet0/3
       no shut
       duplex auto
       speed auto
       media-type rj45
      !
      router ospf 10
       router-id 10.90.5.11
      !
      ip route 0.0.0.0 0.0.0.0 10.131.20.17
      !
''')

SW1_config.configure('''
      feature ospf
      feature interface-vlan
      feature hsrp
      feature lacp
      feature vpc

      ip route 0.0.0.0/0 10.90.1.11
      vlan 1,10,20
      vlan 10
        name datacenter
      
       vrf context management
      

      interface Vlan1

      interface Vlan10
        description **** SVI for Datacenter vlan ****
        no shutdown
        ip router ospf 10 area 0.0.0.0
       

      interface Vlan20
        no shutdown
        ip router ospf 10 area 0.0.0.0
        

     

      interface Ethernet1/1
        no switchport
        ip router ospf 10 area 0.0.0.0
        no shutdown

      interface Ethernet1/2
        no switchport
        ip router ospf 10 area 0.0.0.0
        no shutdown

      router ospf 10
        router-id 10.90.1.10

      no logging console

    
''')

SW2_config.configure('''
      feature ospf
      feature interface-vlan
      feature hsrp
      feature lacp
      feature vpc

       ip route 0.0.0.0/0 10.90.3.11
      ip route 0.0.0.0/0 10.90.4.11
      vlan 1,10,20
      vlan 10
        name datacenter
      vlan 20
        name sales

      vrf context management

      interface Vlan1

      interface Vlan10
        no shutdown
        ip router ospf 10 area 0.0.0.0
        

      interface Vlan20
        no shutdown
        ip router ospf 10 area 0.0.0.0
       

   
      interface Ethernet1/1
        no switchport
        ip router ospf 10 area 0.0.0.0
        no shutdown

      interface Ethernet1/2
        no switchport
        ip router ospf 10 area 0.0.0.0
        no shutdown

       router ospf 10
        router-id 10.90.3.10

       no logging console



''')   

#output = R1_config.parse('show interfaces')
#print(output)
#output = R1_config.learn('ospf')
#interface_snap = R1_config.learn('interface')
#pprint(output.info)
#with open("ospf_after.json", "w") as file3:
#	json.dump(output.info, file3, indent=2)
    
#with open("interface_after.json", "w") as file4:
#	json.dump(interface_snap.info, file4, indent=2)

output = R1_config.parse('show ip ospf neighbor detail')
print(type(output))
with open("ospf_post_neighbor.json", "w") as file:
	json.dump(output, file, indent=2)

#file1 = open('ospf_pre.json')
#file3 = open('ospf_after.json')
#file2 = open('interface_pre.json')
#file4 = open('interface_after.json')
#file5 = open('ospf_pre_neighbor.json')
file6 = open('ospf_post_neighbor.json')

#ospf_pre_snap_dict = json.load(file1)
#ospf_post_snap_dict = json.load(file3)
#interface_pre_snap_dict = json.load(file2)
#interface_post_snap_dict = json.load(file4)
#ospf_neighbor_pre_snap = json.load(file5)
ospf_neighbor_post_snap = json.load(file6)

#dd = Diff(ospf_pre_snap_dict,ospf_post_snap_dict, mode='add')
#dd.findDiff()
#print(dd.findDiff())
#dd = Diff(interface_pre_snap_dict,interface_post_snap_dict, mode='remove')
#dd = Diff(ospf_neighbor_pre_snap,ospf_neighbor_post_snap)
#dd.findDiff()
#print(type(dd))
#with open("ospf_diff.txt", "w") as file:
#	file.write(str(dd))
