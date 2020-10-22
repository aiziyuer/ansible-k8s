net.bridge.bridge-nf-call-iptables

iptables -A FORWARD -t mangle -d 10.13.32.19 -m physdev --physdev-in eth0 --physdev-out tap142cf4be-bb -j MARK --set-xmark 0x45/0xffffffff

iptables -t mangle -A FORWARD -m physdev --physdev-out veth1edea25 --physdev-is-bridged -j LOG --log-level 1 --log-prefix "(抓取关键字): "

iptables -t mangle -A FORWARD -m physdev --physdev-is-bridged -j LOG --log-level 1 --log-prefix "(抓取关键字): "

iptables -t mangle -A FORWARD -m physdev --physdev-in veth47aa3b1 -j LOG --log-level 1 --log-prefix "(抓取关键字): "

# 应用规则(新建连接还是已建立的连接?)
iptables -I OUTPUT -m state -p tcp --state NEW -j LOG --log-level 1 --log-prefix "(抓取关键字): "
iptables -D OUTPUT -m state -p tcp --state NEW -j LOG --log-level 1 --log-prefix "(抓取关键字): "


iptables -A OUTPUT -m state -p tcp --state NEW -j LOG --log-level 1 --log-prefix "(抓取关键字): "

# 抓取内核回环, 根据规则抓出连接信息
cat /proc/kmsg | grep '(抓取关键字)'
cat /proc/kmsg | grep '3131'
<1>[ 3662.389087] (抓取关键字): IN= OUT=ens192 SRC=10.10.10.105 DST=10.10.10.113 LEN=152 TOS=0x10 PREC=0x00 TTL=64 ID=52113 DF PROTO=TCP SPT=22 DPT=2729 WINDOW=424 RES=0x00 ACK PSH URGP=0 
<1>[ 3851.197960] (抓取关键字): IN= OUT=ens192 SRC=10.10.10.105 DST=10.10.10.106 LEN=60 TOS=0x00 PREC=0x00 TTL=64 ID=28409 DF PROTO=TCP SPT=43886 DPT=22 WINDOW=29200 RES=0x00 SYN URGP=0 
<1>[ 3853.030902] (抓取关键字): IN= OUT=ens192 SRC=10.10.10.105 DST=10.10.10.106 LEN=60 TOS=0x00 PREC=0x00 TTL=64 ID=60613 DF PROTO=TCP SPT=43888 DPT=22 WINDOW=29200 RES=0x00 SYN URGP=0 
<1>[ 3858.389268] (抓取关键字): IN= OUT=ens192 SRC=10.10.10.105 DST=10.10.10.106 LEN=60 TOS=0x00 PREC=0x00 TTL=64 ID=14719 DF PROTO=TCP SPT=43890 DPT=22 WINDOW=29200 RES=0x00 SYN URGP=0 

# 解析IP访问
10.10.10.105:22 => 10.10.10.113:2729
10.10.10.105:43886 => 10.10.10.113:22
10.10.10.105:43888 => 10.10.10.113:22
10.10.10.105:43890 => 10.10.10.113:22

# 只保留源端口为随机端口的访问记录并去重
cat /proc/sys/net/ipv4/ip_local_port_range - cat /proc/sys/net/ipv4/ip_local_reserved_ports
32768   60999                                
10.10.10.105:[随机端口] => 10.10.10.113:22

# 识别IP
本机:[随机端口] => 10.10.10.113:22


#### 特殊的注入过程(istio是sidecar执行了) #####

# 抓取容器id
export container_id=3b464d348311
export pid=$(docker inspect -f '{{.State.Pid}}' ${container_id})
mkdir -p /var/run/netns/
ln -sfT /proc/$pid/ns/net /var/run/netns/$container_id

# 执行iptables的hook
ip netns exec "${container_id}" iptables -A OUTPUT ! -o lo -m state -p tcp --state NEW -j LOG --log-level 1 --log-prefix "(抓取关键字): "


### 基于bcc来抓取流量

```
yum install bcc bcc-tools python3-bcc


```