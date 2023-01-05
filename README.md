# gitlabcicd

Description:

This CICD pipeline demonstrates the power of CICD tools, in this case gitlab, which can help us see the impact of change in network cofiguration in a simulated lab environment prior to applying network configuration on production environment.


base-config.py  - Deploys a lab network below and applies basic network configuration.
pyats-snap - Configure ospf between the network devices and take a snapshot and produces snapshot for ospf neighbors as gitlab artifacts
Gitlab cicd consists of two stages which runs the above scripts as can be seen .gitlab_ci.yml file
Topology Deployed to CML using vril2 client library

![image](https://user-images.githubusercontent.com/94404826/210698295-d54fe79a-6514-4870-b9f8-f1e93353f3b9.png)
