<!--------------------------------------------------------------------------------- Description --->
# Description
Download live/history price  
Trade  
Auto-trading robots  



<!--------------------------------------------------------------------------------- Resource --->
<br><br>

# Resource
[FXCM : APP](https://tradingstation.fxcm.com/FreeDemo?lc=en_US)  
[FXCM : API](https://www.fxcm.com/markets/algorithmic-trading/api-trading/)  
[fxcodebase](https://fxcodebase.com/)  
[fxcodebase : ForexConnect](https://fxcodebase.com/wiki/index.php/Category:ForexConnect)  
[fxcodebase : ForexConnect : SDK](https://fxcodebase.com/wiki/index.php/Download#Beta_Release_.281.6_Python.29)  
[fxcodebase : ForexConnect : DUC](https://fxcodebase.com/bin/forexconnect/1.6.0/help/Python/web-content.html#index.html)  
[github : ForexConnectAPI](https://github.com/fxcm/ForexConnectAPI)  
[github : gehtsoft](https://github.com/gehtsoft/forex-connect/tree/master/samples/Python)  



<!--------------------------------------------------------------------------------- Install --->
<br><br>

# Install
[Python](https://github.com/kashanimorteza/python_document/blob/main/doc/install.md)  
[Database](https://github.com/kashanimorteza/forex_api/blob/main/database.md)



<!--------------------------------------------------------------------------------- Source --->
<br><br>

# Source
```bash
git clone https://github.com/kashanimorteza/forex_api.git
cd forex_api
```
pyenv
```bash
pyenv local 3.7
python -m venv .env
.env/bin/python -m pip install --upgrade pip
source .env/bin/activate
pip install -r requirements.txt
pip list
```
General
```bash
python3.7 -m venv .env3.7
.env3.7/bin/python -m pip install --upgrade pip
source .env3.7/bin/activate
pip install -r requirements.txt
pip list
```


<!--------------------------------------------------------------------------------- Setup --->
<br><br>

# Setup
<!-------------------------- Config -->
Config
```bash
vim config.yaml
```
<!-------------------------- Implement databases and tables -->
Implement databases and tables
```bash
python implement.py
```



<!--------------------------------------------------------------------------------- Download --->
<br><br>

# Download 
<!-------------------------- Parameters -->
Parameters
```
account        = acc-download | acc-trade
instrument     = all | EUR/USD,EUR/JPY | EUR/USD
timeframe      = all | m1,H1,H2,H3,H4  | W1 | D1 | H8 | H6 | H4 | H3 | H2 | H1 | m30 | m15 | m5 | m1 | t1
mode           = complete | up | down| once
count          = 1 - ~
repeat         = 1 - ~
delay          = 0 - ~
bulk           = true | false
datefrom       = 2001-01-01 00:00:00
dateto         = 2025-01-01 00:00:00
```
<!-------------------------- Parameters -->
Download history
```bash
python download.py account=acc-history1 instrument=all timeframe=W1,D1,H8,H6,H4,H3,H2,H1,m30,m15,m5,m1 mode=down save=True bulk=True dedicate=False clear=False count=100000
```
Update history
```bash
python download.py account=acc-history1 instrument=all timeframe=W1,D1,H8,H6,H4,H3,H2,H1,m30,m15,m5,m1 mode=up save=True bulk=True dedicate=False clear=False count=100000
```
Check history
```bash
python download.py account=acc-history1 instrument=all timeframe=W1,D1,H8,H6,H4,H3,H2,H1,m30,m15,m5,m1 mode=complete save=True bulk=False dedicate=False clear=False count=100000
```

Download tick
```bash
python download.py account=acc-history1 instrument=EUR/USD,XAU/USD,/XAG/USD,USOil,UKOil timeframe=t1 mode=down save=True bulk=True dedicate=False clear=False count=100000 datefrom='2025-01-01 00:00:00'
```
Update tick
```bash
python download.py account=acc-history1 instrument=EUR/USD,XAU/USD,/XAG/USD,USOil,UKOil timeframe=t1 mode=up save=True bulk=True dedicate=False clear=False count=100000
```
Check tick
```bash
python download.py account=acc-history1 instrument=EUR/USD,XAU/USD,/XAG/USD,USOil,UKOil timeframe=t1 mode=complete save=True bulk=False dedicate=False clear=False count=100000 datefrom='2025-12-01 00:00:00'
```

<!-------------------------- Schedule -->
Schedule
```bash
Related to myLib/config.py > class:eSchedule and schedule.py
source .myenv3.7/bin/activate
./schedule.py schedule=MO1
./schedule.py schedule=W1
./schedule.py schedule=D1
./schedule.py schedule=H8
./schedule.py schedule=H6
./schedule.py schedule=H4
./schedule.py schedule=H3
./schedule.py schedule=H2
./schedule.py schedule=H1
./schedule.py schedule=m30
./schedule.py schedule=m15
./schedule.py schedule=m5
./schedule.py schedule=m1
./schedule.py schedule=t1
```
<!-------------------------- Log -->
Log
```bash
tail -f log.txt
```


<!--------------------------------------------------------------------------------- Linux --->
<br><br>

# Linux
<!-------------------------- General -->
General
```bash
sudo apt update
sudo apt upgrade
sudo timedatectl set-timezone UTC
apt install aria2 -y
apt install pigz -y
```
<!-------------------------- Screen -->
Screen
```bash
screen -S forex_api
Ctrl + A  then  D
screen -ls
screen -r forex_api
du -sh History
```
<!-------------------------- Git -->
Git
```bash
sudo apt install git -y
sudo git config --global user.email "kashani.morteza@gmail.com"
sudo git config --global user.name "morteza"
sudo git config --global core.editor vim
```
```bash
git fetch origin
git reset --hard origin/main
```
```bash
git checkout --orphan fresh-start
git add -A
git commit -m "Initial commit (history cleared)"
git branch -D main
git branch -m main
git push -f origin main
```
<!-------------------------- DNS -->
DNS
```bash
echo "" > /etc/resolv.conf
echo "nameserver 185.51.200.2" > /etc/resolv.conf
echo "nameserver 178.22.122.100" >> /etc/resolv.conf
```
<!-------------------------- DNS -->
User
```bash
usermod -aG www-data morteza
chown -R root:www-data /extra
chmod -R 775 /extra
chmod -R 777 /extra
```



<!--------------------------------------------------------------------------------- Linux service --->
<br><br>

# linux service

<!-------------------------- Check -->
Check
```bash
sudo ./linuxService.sh check
```
<!-------------------------- Create / Remove -->
Create / Remove
```bash
sudo ./linuxService.sh create
sudo ./linuxService.sh remove
```
<!-------------------------- Enable / Disable -->
Enable / Disable
```bash
sudo ./linuxService.sh enable
sudo ./linuxService.sh disable
```
<!-------------------------- Start -->
Start
```bash
sudo ./linuxService.sh start
sudo ./linuxService.sh start W1
```
<!-------------------------- Stop -->
Stop
```bash
sudo ./linuxService.sh stop
sudo ./linuxService.sh stop W1
```
<!-------------------------- Restart -->
Restart
```bash
sudo ./linuxService.sh restart
sudo ./linuxService.sh restart W1
```
<!-------------------------- Status -->
Status
```bash
sudo ./linuxService.sh status W1
```
<!-------------------------- monitor -->
Monitor
```bash
sudo ./linuxService.sh monitor
```



<!--------------------------------------------------------------------------------- Shortcut --->
<br><br>

# Shortcut
```bash
vim ~/.bash_aliases
```
```bash
#-------------------------------------------------- [ Forex ]
#---------------- [ General ]
alias f='cd ~/download_forex'
alias fm='~/download_forex/linuxService.sh monitor'
alias fs='~/download_forex/linuxService.sh stop'
#---------------- [ Start Service ]
alias fmo1='~/download_forex/linuxService.sh start MO1'
alias fw1='~/download_forex/linuxService.sh start W1'
alias fd1='~/download_forex/linuxService.sh start D1'
alias fh8='~/download_forex/linuxService.sh start H8'
alias fhu='~/download_forex/linuxService.sh start H6'
alias fh4='~/download_forex/linuxService.sh start H4'
alias fh3='~/download_forex/linuxService.sh start H3'
alias fh2='~/download_forex/linuxService.sh start H2'
alias fh1='~/download_forex/linuxService.sh start H1'
alias fm30='~/download_forex/linuxService.sh start m30'
alias fm15='~/download_forex/linuxService.sh start m15'
alias fm5='~/download_forex/linuxService.sh start m5'
alias fm1='~/download_forex/linuxService.sh start m1'
alias ft1='~/download_forex/linuxService.sh start t1'
#---------------- [ Stop Service ]
alias fmo1s='~/download_forex/linuxService.sh stop MO1'
alias fw1s='~/download_forex/linuxService.sh stop W1'
alias fd1s='~/download_forex/linuxService.sh stop D1'
alias fh8s='~/download_forex/linuxService.sh stop H8'
alias fhus='~/download_forex/linuxService.sh stop H6'
alias fh4s='~/download_forex/linuxService.sh stop H4'
alias fh3s='~/download_forex/linuxService.sh stop H3'
alias fh2s='~/download_forex/linuxService.sh stop H2'
alias fh1s='~/download_forex/linuxService.sh stop H1'
alias fm30s='~/download_forex/linuxService.sh stop m30'
alias fm15s='~/download_forex/linuxService.sh stop m15'
alias fm5s='~/download_forex/linuxService.sh stop m5'
alias fm1s='~/download_forex/linuxService.sh stop m1'
alias ft1s='~/download_forex/linuxService.sh stop t1'
#---------------- [ Screen ]
alias fsm='screen -r forex_monitor'
alias fsmo1='screen -r forex_mo1'
alias fsw1='screen -r forex_w1'
alias fsd1='screen -r forex_d1'
alias fsh8='screen -r forex_h8'
alias fsh6='screen -r forex_h6'
alias fsh4='screen -r forex_h4'
alias fsh3='screen -r forex_h3'
alias fsh2='screen -r forex_h2'
alias fsh1='screen -r forex_h1'
alias fsm30='screen -r forex_m30'
alias fsm15='screen -r forex_m15'
alias fsm5='screen -r forex_m5'
alias fsm1='screen -r forex_m1'
alias fst1='screen -r forex_t1'
```
```bash
source ~/.bash_aliases
```



<!--------------------------------------------------------------------------------- Hard --->
<br><br>

# Hard
<!-------------------------- Hard -->
All drive 
```bash
lsblk -ndo NAME,SIZE,TYPE | grep disk
```
<!-------------------------- Hard -->
All drive with partition
```bash
lsblk -o NAME,SIZE,TYPE,MOUNTPOINT
```
<!-------------------------- Hard -->
Mount address
```bash
df -h | grep dev
df -h /boot
```
<!-------------------------- Hard -->
Create Label
```bash
sudo e2label /dev/sdb1 data1
```
<!-------------------------- Hard -->
Create partition
```bash
sudo fdisk /dev/sdb
g
sudo mkfs.ext4 /dev/sdb1
```
<!-------------------------- Hard -->
mount
```bash
sudo mkdir -p /media/data1
sudo mount /dev/sdb1 /media/data1
```
<!-------------------------- Hard -->
Change Mount address
```bash
sudo umount /media/morteza/2TB
sudo mv /media/morteza/2TB /media/morteza/data1
sudo mount /dev/sdd /data1
```
<!-------------------------- Hard -->
Speed test
```bash
dd if=/dev/zero of=testfile bs=10G count=1 oflag=direct
dd if=testfile of=/dev/null bs=1G count=1 iflag=direct
rm testfile
```
<!-------------------------- Hard -->
Mount
```bash
sudo mkdir -p /media/data1
sudo mkdir -p /media/data2
sudo mkdir -p /media/data3
```
<!-------------------------- Hard -->
```bash
lsblk -f
```
<!-------------------------- Hard -->
vim /etc/fstab
```bash
UUID=425f843e-f102-40cb-9569-d50cebc927a6  /media/data1  ext4  defaults,nofail  0  2
UUID=2bdda109-2171-4ebe-9c09-f0423a1ccec5  /media/data2  ext4  defaults,nofail  0  2
UUID=d7273f09-ca3d-4d88-9cb7-1fa64106aab8  /media/data3  ext4  defaults,nofail  0  2
```



<!--------------------------------------------------------------------------------- Nginx --->
<br><br>

# Nginx
<!-------------------------- Instal -->
Instal
```bash
sudo apt update
sudo apt install nginx -y
sudo chmod -R 755 /var/www/html
```
<!-------------------------- Config -->
Config
```bash
echo "" > /etc/nginx/sites-enabled/default 
sudo vim /etc/nginx/sites-enabled/default
```
```bash
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    root /var/www/html;
    index index.html index.htm;

    location / {
        autoindex on;
        autoindex_exact_size off;
        autoindex_localtime on;
    }
}
```
<!-------------------------- Service -->
Service
```bash
sudo systemctl enable nginx
sudo systemctl restart nginx
sudo systemctl status nginx
```



<!--------------------------------------------------------------------------------- Download --->
<br><br>

# Download History from server
Server 
```bash
cd /root/forex_api
python download.py account=acc-history1 instrument=all timeframe=W1,D1,H8,H6,H4,H3,H2,H1,m30,m15,m5,m1 mode=down save=False bulk=False dedicate=False clear=False count=100000
tar -I pigz -cvf history_2025-11-28.tar.gz History
mv history_2025-11-28.tar.gz /var/www/html/
rm -fr History
```

Client
```bash
cd /root/forex_api
aria2c -x 16 http://91.107.245.66/history_2025-11-28.tar.gz
tar --use-compress-program="pigz -d" -xvf history_2025-11-28.tar.gz -C ./forex_api
python download.py account=acc-history1 instrument=all timeframe=W1,D1,H8,H6,H4,H3,H2,H1 mode=down save=True bulk=True dedicate=False clear=False count=100000
```



<!--------------------------------------------------------------------------------- Structure --->
<br><br>

# Structure
    Instrument
    Account
    Strategy
    Strategy_Item
    Strategy_Item_Trade
    Test_Live



<!--------------------------------------------------------------------------------- Task --->
<br><br>

# Task
    Gui : Execute : Show Detail | Show order | Show graph
    --------------------------------
    Listener close order
    --------------------------------
    Listener price change
    --------------------------------
    Backtest
    --------------------------------
    Readme
    --------------------------------
    Automatic service for download data
    --------------------------------
    Hal kardan moshkel download up
    --------------------------------
    Api Authentication and Encription
    GUi Authentication and Encription
    --------------------------------
    Crreate Dashboard
    --------------------------------
    CHeck Spred betting account
    --------------------------------
