# iftop-python
Minimal iftop in python

```sh
python iftop-stack.py
```

Shows all background newtork connections 
- All IP Connections
- Which programs are making the connections
- Which companies they are connecting

# Output
```sh
(ssm) m@p:~$ python iftop-stack.py
2024-04-30 10:09:30.284819
8.39.36.142 443 RUBIC-7 Handshake firefox-bin
172.64.149.180 443 CLOUD14 Handshake firefox-bin
169.197.150.7 443 g.deepintent.com *.deepintent.com firefox-bin
23.37.223.192 443 a23-37-223-192.deploy.static.akamaitechnologies.com *.rubiconproject.com Magnite, Inc. firefox-bin
209.85.203.94 443 dh-in-f94.1e100.net None firefox-bin
159.127.41.204 443 sjc07-nessy-float2.dotomi.com Handshake firefox-bin
3.163.189.57 443 server-3-163-189-57.sea90.r.cloudfront.net Handshake firefox-bin
52.38.203.118 443 ec2-52-38-203-118.us-west-2.compute.amazonaws.com *.ad-server.k8s.or.ggops.com firefox-bin
```

# Note
## No root required
## Continuously shows new connections
## Restart it, to remove the showing of the old connections

