import pyats
from virl2_client import ClientLibrary
from genie.conf import Genie
from pprint import pprint
import yaml
client = ClientLibrary("https://10.85.48.20", "admin", "C!sco12345", ssl_verify=False)

"""lab = client.find_labs_by_title("cml-lab")[0]

pyats_testbed = lab.get_pyats_testbed()                             Generate pyats testbed file

with open("labtestbed.yml", "w") as f:
    f.write(pyats_testbed)"""    
print("*********************Creating a lab test network*******************")
lab = client.create_lab(title= "CML Automation Lab using docker" )                                 #Ceate a lab

print("*********************Creating rCore Routers*******************")
R1= lab.create_node("R1", "iosv", 100, 100)
R1.config = "hostname R1"

R2= lab.create_node("R2", "iosv", 300, 100)
R2.config = "hostname R2"
"""
print("*********************Creating rnxos switch*******************")
r2 = lab.create_node("r2", "iosv", 50, 200)
r2.config = "hostname router2"
"""

dist_sw1= lab.create_node("dist_sw1", "nxosv9000", 100, 250)
dist_sw1.config = '''
hostname dist_sw1 
no password strength-check
username admin role network-admin
username admin password cisco role network-admin
username cisco role network-admin
username cisco password cisco role network-admin
'''

dist_sw2= lab.create_node("dist_sw2", "nxosv9000", 300, 250)
dist_sw2.config = '''
hostname dist_sw2 
no password strength-check
username admin role network-admin
username admin password cisco role network-admin
username cisco role network-admin
username cisco password cisco role network-admin
'''

unmanaged_sw=lab.create_node("unmgd_sw", "unmanaged_switch", 400, 400)

access_1 = lab.create_node("access_1", "iosvl2", 300, 500)
access_1.config = "hostname access_1"

access_2 = lab.create_node("access_2", "iosvl2", 100, 500)
access_2.config = "hostname access_2"


print("*********************Creating interfaces on router and nexus Switch*******************")
# create a link between r1 and r2
R1_i1 = R1.create_interface()
R1_i2 = R1.create_interface()
R1_i3 = R1.create_interface()
R1_i4 = R1.create_interface()

R2_i1 = R2.create_interface()
R2_i2 = R2.create_interface()
R2_i3 = R2.create_interface()
R2_i4 = R2.create_interface()

lab.create_link(R1_i1, R2_i1)   # Link between R1 and R2 (G0/0 <-----> G0/0)

dist_sw1_i1 = dist_sw1.create_interface()
dist_sw1_i2 = dist_sw1.create_interface()
dist_sw1_i3 = dist_sw1.create_interface()
dist_sw1_i4 = dist_sw1.create_interface()
dist_sw1_i5 = dist_sw1.create_interface()
dist_sw1_i6 = dist_sw1.create_interface()             # dist_sw1 interfaces
dist_sw1_i7 = dist_sw1.create_interface()
dist_sw1_i8 = dist_sw1.create_interface()



dist_sw2_i1 = dist_sw2.create_interface()
dist_sw2_i2 = dist_sw2.create_interface()
dist_sw2_i3 = dist_sw2.create_interface()
dist_sw2_i4 = dist_sw2.create_interface()
dist_sw2_i5 = dist_sw2.create_interface()
dist_sw2_i6 = dist_sw2.create_interface()            # dist_sw1 interfaces
dist_sw2_i7 = dist_sw2.create_interface()
dist_sw2_i8 = dist_sw2.create_interface()

access_1_i1= access_1.create_interface()
access_1_i2= access_1.create_interface()

access_2_i1= access_2.create_interface()
access_2_i2= access_2.create_interface()


unmgd_sw_i1 = unmanaged_sw.create_interface()       # unmgd_sw interfaces
unmgd_sw_i2 = unmanaged_sw.create_interface()

lab.create_link(dist_sw1_i1, unmgd_sw_i1)
lab.create_link(dist_sw2_i1, unmgd_sw_i2)          # mgmnt0 link to unmgd sw


lab.create_link(R1_i2, dist_sw1_i2)   # (G0/1 <--------> Eth1/1)
lab.create_link(R1_i3, dist_sw2_i3)   # (G0/2 <--------> Eth1/2)


lab.create_link(R2_i3, dist_sw1_i3)   # (G0/2 <--------> Eth1/2)
lab.create_link(R2_i2, dist_sw2_i2)   # (G0/2 <--------> Eth1/2)

lab.create_link(dist_sw1_i7, dist_sw2_i7)   # (Eth1/7 <--------> Eth1/7)
lab.create_link(dist_sw1_i8, dist_sw2_i8)   # (Eth1/8 <--------> Eth1/8)

lab.create_link(dist_sw1_i6, access_2_i1)   # (Eth1/5 >--------> G0/0)
lab.create_link(dist_sw1_i5, access_1_i2)   # (Eth1/4 >--------> G0/1)

lab.create_link(dist_sw2_i6, access_2_i2)   # (Eth1/5 >--------> G0/0)
lab.create_link(dist_sw2_i5, access_1_i1)   # (Eth1/5 >--------> G0/0)

lab.start()

lab = client.find_labs_by_title("CML Automation Lab using docker")[0]

pyats_testbed = lab.get_pyats_testbed()                            # Generate pyats testbed file

with open("newlabtestbed.yml", "w") as f:
    f.write(pyats_testbed)

with open('newlabtestbed.yml', 'r') as file:
  read_file = yaml.safe_load(file)
  print(type(read_file))
  #print(read_file)
  read_file['devices']['terminal_server']['credentials']['default']['username'] = 'admin'
  read_file['devices']['terminal_server']['credentials']['default']['password'] = 'C!sco12345'
with open('newtest.yml', 'w') as file:
    yaml.dump(read_file, file)
    

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

R1_config.configure('''
      ! 
      interface GigabitEthernet0/0
       ip address 10.90.5.11 255.255.255.0
       no shutdown
       duplex auto
       speed auto
       media-type rj45
      !
      interface GigabitEthernet0/1
       ip address 10.90.1.11 255.255.255.0
       no shutdown
       duplex auto
       speed auto
       media-type rj45
      !
      interface GigabitEthernet0/2
       ip address 10.90.4.11 255.255.255.0
       no shutdown
       duplex auto
       speed auto
       media-type rj45
      !
      interface GigabitEthernet0/3
       ip address 10.131.20.18 255.255.255.0
       no shutdown
       duplex auto
       speed auto
       media-type rj45
      !
      ip route 0.0.0.0 0.0.0.0 10.131.20.17
      !
     
''')

R2_config.configure('''
       interface GigabitEthernet0/0
       ip address 10.90.5.10 255.255.255.0
       duplex auto
       speed auto
       media-type rj45
      !
      interface GigabitEthernet0/1
       ip address 10.90.3.11 255.255.255.0
       duplex auto
       speed auto
       media-type rj45
      !
      interface GigabitEthernet0/2
       ip address 10.90.2.11 255.255.255.0
       duplex auto
       speed auto
       media-type rj45
      !
      interface GigabitEthernet0/3
       ip address 10.131.10.18 255.255.255.0
       duplex auto
       speed auto
       media-type rj45
      !
      ip route 0.0.0.0 0.0.0.0 10.131.10.17
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
      vpc domain 10
        role priority 10
        peer-keepalive destination 10.85.1.11 source 10.85.1.10

      interface Vlan1

      interface Vlan10
        description **** SVI for Datacenter vlan ****
        no shutdown
        ip address 10.90.6.1/24
        hsrp 2
          authentication md5 key-string cisco
          ip 10.90.6.3

      interface Vlan20
        no shutdown
        ip address 10.90.7.2/24
        hsrp 3
          authentication md5 key-string cisco
          ip 10.90.7.3

      interface port-channel15
        description ** vPC Peer-Link *****
        switchport mode trunk
        spanning-tree port type network
        vpc peer-link

      interface port-channel20
        switchport mode trunk
        vpc 20

      interface port-channel30
        switchport mode trunk
        vpc 30

      interface port-channel40
        switchport mode trunk
        vpc 40

      interface Ethernet1/1
        no switchport
        ip address 10.90.1.10/24
        no shutdown

      interface Ethernet1/2
        no switchport
        ip address 10.90.2.10/24
        no shutdown

      interface Ethernet1/3

      interface Ethernet1/4
        description *** vpc link to access2 ***
        switchport mode trunk
        channel-group 40 mode active

      interface Ethernet1/5
        description *** vpc link to access 1 ***
        switchport mode trunk
        channel-group 30 mode active

      interface Ethernet1/6
        switchport mode trunk
        channel-group 20 mode active

      interface Ethernet1/7
        description **** vPC Peer-Link ****
        switchport mode trunk
        channel-group 15 mode passive

      interface Ethernet1/8
        description **** vPC Peer-Link ****
        switchport mode trunk
        channel-group 15 mode passive

      interface mgmt0
        vrf member management
        ip address 10.85.1.10/24

        
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
      vpc domain 10
        role priority 20
        peer-keepalive destination 10.85.1.10 source 10.85.1.11

      interface Vlan1

      interface Vlan10
        no shutdown
        ip address 10.90.6.2/24
        hsrp 2
          authentication md5 key-string cisco
          ip 10.90.6.3

      interface Vlan20
        no shutdown
        ip address 10.90.7.1/24
        hsrp 3
          authentication md5 key-string cisco
          ip 10.90.7.3

      interface port-channel15
        description *** vPC Peer-Link ***
        switchport mode trunk
        spanning-tree port type network
        vpc peer-link

      interface port-channel20
        switchport mode trunk
        vpc 20

      interface port-channel30
        switchport mode trunk
        vpc 30

      interface port-channel40
        switchport mode trunk
        vpc 40

      interface Ethernet1/1
        no switchport
        ip address 10.90.3.10/24
       
        no shutdown

      interface Ethernet1/2
        no switchport
        ip address 10.90.4.10/24
        no shutdown

      interface Ethernet1/3

      interface Ethernet1/4
        description *** vpc link to access2
        switchport mode trunk
        channel-group 40 mode active

      interface Ethernet1/5
        description *** vPC Link to access 1 ***
        switchport mode trunk
        channel-group 30 mode active

      interface Ethernet1/6
        switchport mode trunk
        channel-group 20 mode active

      interface Ethernet1/7
        description **** vPC Peer-Link ****
        switchport mode trunk
        channel-group 15 mode active

      interface Ethernet1/8
        description **** vPC Peer-Link ****
        switchport mode trunk
        channel-group 15 mode active

       interface mgmt0
        vrf member management
        ip address 10.85.1.11/24

      

       no logging console



''')
Access1_config.configure('''
    
      interface GigabitEthernet0/0
       switchport trunk encapsulation dot1q
       switchport mode trunk
       negotiation auto
       channel-group 30 mode active
      !
      interface GigabitEthernet0/1
       switchport trunk encapsulation dot1q
       switchport mode trunk
       negotiation auto
       channel-group 30 mode active
      !
      interface Port-channel30
       switchport trunk encapsulation dot1q
       switchport mode trunk
      !
''')

Access2_config.configure('''
   
      interface GigabitEthernet0/0
       switchport trunk encapsulation dot1q
       switchport mode trunk
       negotiation auto
       channel-group 40 mode active
      !
      interface GigabitEthernet0/1
       switchport trunk encapsulation dot1q
       switchport mode trunk
       negotiation auto
       channel-group 40 mode active
       no shut
      !
      interface Port-channel40
       switchport trunk encapsulation dot1q
       switchport mode trunk
       no shut
      !
''')
#Output = R1_config.learn('ospf')

#pprint(Output)

R1_config.disconnect()
R2_config.disconnect()
SW1_config.disconnect()
SW2_config.disconnect()
Access1_config.disconnect()
Access2_config.disconnect()
