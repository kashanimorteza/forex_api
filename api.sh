#!/usr/bin/env bash

#---------------------------------------------------------------------------------Tools
#-----------------------------check_os
check_os() 
{
    #----------Header
    echo -e "${header_color}${header_line}${FUNCNAME[0]}${ENDCOLOR}"
    #----------Action
    if [[ "$OSTYPE" == "darwin"* ]]; then
        check_os_value="mac"
    elif [[ -f /etc/lsb-release ]]; then
        if grep -qi 'ubuntu' /etc/lsb-release; then check_os_value="ubuntu"; else check_os_value="other"; fi
    else
         check_os_value="other"
    fi
    echo $check_os_value
}
#-----------------------------check_jq_yq
check_jq_yq()
{
    #----------Header
    echo -e "${header_color}${header_line}${FUNCNAME[0]}${ENDCOLOR}"
    #----------Action
    # Check jq
    if ! command -v jq >/dev/null 2>&1; then
        echo "jq not found, installing..."
        if [[ "$OSTYPE" == "darwin"* ]]; then
            brew install jq || { echo "Failed to install jq"; return 1; }
        else
            apt update && apt install jq -y || { echo "Failed to install jq"; return 1; }
        fi
    fi
    # Check yq
    if ! command -v yq >/dev/null 2>&1; then
        echo "yq not found, installing..."
        if [[ "$OSTYPE" == "darwin"* ]]; then
            brew install yq || { echo "Failed to install yq"; return 1; }
        else
            apt update && snap install yq || { echo "Failed to install yq"; return 1; }
        fi
    fi
    
    return 0
}
#-----------------------------getHeader
getHeader()
{
    #----------Action
    echo -e "${RED}${LINE4}${name}"
}
#-----------------------------log
log()
{
    #----------Header
    echo -e "${header_color}${header_line}${FUNCNAME[0]}${ENDCOLOR}"
    #----------Action
    datetime=$(date +"%Y-%m-%d %H:%M:%S")
    echo -e "\n${datetime} | ${log_variable}" >> $log_folder/cli.log
}
#-----------------------------monitor
monitor()
{
    #----------Header
    echo -e "${header_color}${header_line}${FUNCNAME[0]}${ENDCOLOR}"
    #----------Data
    webapi_host=$(yq '.webapi.host' "$config_file" | tr -d '"')
    webapi_port=$(yq '.webapi.port' "$config_file" | tr -d '"')
    nginx_api_port=$(yq '.nginx.api.port' "$config_file" | tr -d '"')
    nginx_api_key=$(yq '.nginx.api.key' "$config_file" | tr -d '"')
    nginx_gui_port=$(yq '.nginx.gui.port' "$config_file" | tr -d '"')
    nginx_gui_key=$(yq '.nginx.gui.key' "$config_file" | tr -d '"')
    wifiip=$(ip -4 addr show wlan0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}')
    #----------Action
    echo -e "${BLUE}Webapi${ENDCOLOR}"
    echo -e "${ENDCOLOR}http://${webapi_host}:${webapi_port}${ENDCOLOR}"
    echo -e "${ENDCOLOR}http://${webapi_host}:${webapi_port}/doc1${ENDCOLOR}"
    echo -e "${BLUE}Nginx API${ENDCOLOR}"
    echo -e "${ENDCOLOR}http://${wifiip}:${nginx_api_port}/${nginx_api_key}/doc1${ENDCOLOR}"
    echo -e "${BLUE}Nginx GUI${ENDCOLOR}"
    echo -e "${ENDCOLOR}http://${wifiip}:${nginx_gui_port}/${nginx_gui_key}${ENDCOLOR}"
}
#-----------------------------all
all()
{
    #----------Header
    echo -e "${header_color}${header_line}${FUNCNAME[0]}${ENDCOLOR}"
    #----------Action
    install_all
    config_all
    service_create_all
}

#---------------------------------------------------------------------------------Config
#-----------------------------config_all
config_all()
{
    #----------Header
    echo -e "${header_color}${header_line}${FUNCNAME[0]}${ENDCOLOR}"
    #----------Action
    config_general
    config_network
    config_git
    config_postgres
    config_python
    config_implementation
}
#-----------------------------config_general  : Shell
config_general()
{
    #----------Header
    echo -e "${header_color}${header_line}${FUNCNAME[0]}${ENDCOLOR}"
    #----------Data
    timeZone=$(yq '.general.time_zone' "$config_file" | tr -d '"')
    #----------Verbose
    echo -e "${BLUE}sudo timedatectl set-timezone $timeZone${ENDCOLOR}"
    #----------Action
    sudo timedatectl set-timezone $timeZone
}
#-----------------------------config_network  : Shell
config_network()
{
    #----------Header
    echo -e "${header_color}${header_line}${FUNCNAME[0]}${ENDCOLOR}"
}
#-----------------------------config_git  : Shell
config_git()
{
    #----------Header
    echo -e "${header_color}${header_line}${FUNCNAME[0]}${ENDCOLOR}"
    #----------Data
    git_name=$(yq '.git.name' "$config_file" | tr -d '"')
    git_email=$(yq '.git.email' "$config_file" | tr -d '"')
    #----------Verbose
    echo -e "${verbose_color}git config --global user.email \"${git_email}\"${ENDCOLOR}"
    echo -e "${verbose_color}git config --global user.name \"${git_name}\"${ENDCOLOR}"
    echo -e "${verbose_color}git config --global core.editor \"vim\"${ENDCOLOR}"
    echo -e "${verbose_color}git config user.email \"${git_email}\"${ENDCOLOR}"
    echo -e "${verbose_color}git config user.name \"${git_name}\"${ENDCOLOR}"
    echo -e "${verbose_color}git config core.editor \"vim\"${ENDCOLOR}"
    echo -e "${verbose_color}git config pull.rebase false${ENDCOLOR}"
    #----------Action
    git config --global user.email "${git_email}"
    git config --global user.name "${git_name}"
    git config --global core.editor "vim"
    git config user.email "${git_email}"
    git config user.name "${git_name}"
    git config core.editor "vim"
    git config pull.rebase false
}
#-----------------------------config_postgres
config_postgres()
{
    #----------Header
    echo -e "${header_color}${header_line}${FUNCNAME[0]}${ENDCOLOR}"
    #----------Data
    username=$(yq '.database.data.username' "$config_file" | tr -d '"')
    password=$(yq '.database.data.password' "$config_file" | tr -d '"')
    echo -e "${verbose_color}username: $username${ENDCOLOR}"
    echo -e "${verbose_color}password: $password${ENDCOLOR}"
    #----------Role
    echo -e "${verbose_color}sudo -u postgres psql -c \"CREATE ROLE ${username} WITH LOGIN CREATEDB PASSWORD '${password}';\"${ENDCOLOR}"
    sudo -u postgres psql -c "CREATE ROLE ${username} WITH LOGIN CREATEDB PASSWORD '${password}';"
    #----------Database
    echo -e "${verbose_color}sudo -u postgres psql -c \"CREATE DATABASE forex WITH OWNER=${username};\"${ENDCOLOR}"
    echo -e "${verbose_color}sudo -u postgres psql -c \"CREATE DATABASE management WITH OWNER=${username};\"${ENDCOLOR}"
    echo -e "${verbose_color}sudo -u postgres psql -c \"CREATE DATABASE log WITH OWNER=${username};\"${ENDCOLOR}"
    sudo -u postgres psql -c "CREATE DATABASE forex WITH OWNER=${username};"
    sudo -u postgres psql -c "CREATE DATABASE management WITH OWNER=${username};"
    sudo -u postgres psql -c "CREATE DATABASE log WITH OWNER=${username};"
    #----------Grant privileges for data database
    echo -e "${verbose_color}sudo -u postgres psql -d forex -c \"ALTER ROLE ${username} WITH CONNECTION LIMIT -1;\"${ENDCOLOR}"
    echo -e "${verbose_color}sudo -u postgres psql -d forex -c \"ALTER DATABASE forex OWNER TO ${username};\"${ENDCOLOR}"
    echo -e "${verbose_color}sudo -u postgres psql -d forex -c \"ALTER SCHEMA public OWNER TO ${username};\"${ENDCOLOR}"
    echo -e "${verbose_color}sudo -u postgres psql -d forex -c \"GRANT ALL PRIVILEGES ON SCHEMA public TO ${username};\"${ENDCOLOR}"
    echo -e "${verbose_color}sudo -u postgres psql -d forex -c \"GRANT USAGE ON SCHEMA public TO ${username};\"${ENDCOLOR}"
    echo -e "${verbose_color}sudo -u postgres psql -d forex -c \"GRANT CREATE ON SCHEMA public TO ${username};\"${ENDCOLOR}"
    echo -e "${verbose_color}sudo -u postgres psql -d forex -c \"GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO ${username};\"${ENDCOLOR}"
    echo -e "${verbose_color}sudo -u postgres psql -d forex -c \"GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ${username};\"${ENDCOLOR}"
    echo -e "${verbose_color}sudo -u postgres psql -d forex -c \"GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO ${username};\"${ENDCOLOR}"
    sudo -u postgres psql -d forex -c "ALTER ROLE ${username} WITH CONNECTION LIMIT -1;"
    sudo -u postgres psql -d forex -c "ALTER DATABASE forex OWNER TO ${username};"
    sudo -u postgres psql -d forex -c "ALTER SCHEMA public OWNER TO ${username};"
    sudo -u postgres psql -d forex -c "GRANT ALL PRIVILEGES ON SCHEMA public TO ${username};"
    sudo -u postgres psql -d forex -c "GRANT USAGE ON SCHEMA public TO ${username};"
    sudo -u postgres psql -d forex -c "GRANT CREATE ON SCHEMA public TO ${username};"
    sudo -u postgres psql -d forex -c "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO ${username};"
    sudo -u postgres psql -d forex -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ${username};"
    sudo -u postgres psql -d forex -c "GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO ${username};"
    #----------Grant privileges for management database
    echo -e "${verbose_color}sudo -u postgres psql -d management -c \"ALTER ROLE ${username} WITH CONNECTION LIMIT -1;\"${ENDCOLOR}"
    echo -e "${verbose_color}sudo -u postgres psql -d management -c \"ALTER DATABASE management OWNER TO ${username};\"${ENDCOLOR}"
    echo -e "${verbose_color}sudo -u postgres psql -d management -c \"ALTER SCHEMA public OWNER TO ${username};\"${ENDCOLOR}"
    echo -e "${verbose_color}sudo -u postgres psql -d management -c \"GRANT ALL PRIVILEGES ON SCHEMA public TO ${username};\"${ENDCOLOR}"
    echo -e "${verbose_color}sudo -u postgres psql -d management -c \"GRANT USAGE ON SCHEMA public TO ${username};\"${ENDCOLOR}"
    echo -e "${verbose_color}sudo -u postgres psql -d management -c \"GRANT CREATE ON SCHEMA public TO ${username};\"${ENDCOLOR}"
    echo -e "${verbose_color}sudo -u postgres psql -d management -c \"GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO ${username};\"${ENDCOLOR}"
    echo -e "${verbose_color}sudo -u postgres psql -d management -c \"GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ${username};\"${ENDCOLOR}"
    echo -e "${verbose_color}sudo -u postgres psql -d management -c \"GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO ${username};\"${ENDCOLOR}"
    sudo -u postgres psql -d management -c "ALTER ROLE ${username} WITH CONNECTION LIMIT -1;"
    sudo -u postgres psql -d management -c "ALTER DATABASE management OWNER TO ${username};"
    sudo -u postgres psql -d management -c "ALTER SCHEMA public OWNER TO ${username};"
    sudo -u postgres psql -d management -c "GRANT ALL PRIVILEGES ON SCHEMA public TO ${username};"
    sudo -u postgres psql -d management -c "GRANT USAGE ON SCHEMA public TO ${username};"
    sudo -u postgres psql -d management -c "GRANT CREATE ON SCHEMA public TO ${username};"
    sudo -u postgres psql -d management -c "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO ${username};"
    sudo -u postgres psql -d management -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ${username};"
    sudo -u postgres psql -d management -c "GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO ${username};"
    #----------Grant privileges for log database
    echo -e "${verbose_color}sudo -u postgres psql -d log -c \"ALTER ROLE ${username} WITH CONNECTION LIMIT -1;\"${ENDCOLOR}"
    echo -e "${verbose_color}sudo -u postgres psql -d log -c \"ALTER DATABASE log OWNER TO ${username};\"${ENDCOLOR}"
    echo -e "${verbose_color}sudo -u postgres psql -d log -c \"ALTER SCHEMA public OWNER TO ${username};\"${ENDCOLOR}"
    echo -e "${verbose_color}sudo -u postgres psql -d log -c \"GRANT ALL PRIVILEGES ON SCHEMA public TO ${username};\"${ENDCOLOR}"
    echo -e "${verbose_color}sudo -u postgres psql -d log -c \"GRANT USAGE ON SCHEMA public TO ${username};\"${ENDCOLOR}"
    echo -e "${verbose_color}sudo -u postgres psql -d log -c \"GRANT CREATE ON SCHEMA public TO ${username};\"${ENDCOLOR}"
    echo -e "${verbose_color}sudo -u postgres psql -d log -c \"GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO ${username};\"${ENDCOLOR}"
    echo -e "${verbose_color}sudo -u postgres psql -d log -c \"GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ${username};\"${ENDCOLOR}"
    echo -e "${verbose_color}sudo -u postgres psql -d log -c \"GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO ${username};\"${ENDCOLOR}"
    sudo -u postgres psql -d log -c "ALTER ROLE ${username} WITH CONNECTION LIMIT -1;"
    sudo -u postgres psql -d log -c "ALTER DATABASE log OWNER TO ${username};"
    sudo -u postgres psql -d log -c "ALTER SCHEMA public OWNER TO ${username};"
    sudo -u postgres psql -d log -c "GRANT ALL PRIVILEGES ON SCHEMA public TO ${username};"
    sudo -u postgres psql -d log -c "GRANT USAGE ON SCHEMA public TO ${username};"
    sudo -u postgres psql -d log -c "GRANT CREATE ON SCHEMA public TO ${username};"
    sudo -u postgres psql -d log -c "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO ${username};"
    sudo -u postgres psql -d log -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ${username};"
    sudo -u postgres psql -d log -c "GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO ${username};"
}
#-----------------------------config_python
config_python()
{
    #----------Header
    echo -e "${header_color}${header_line}${FUNCNAME[0]}${ENDCOLOR}"
    #----------Verbose
    echo -e "${verbose_color}pyenv local 3.7${ENDCOLOR}"
    echo -e "${verbose_color}python -m venv .env${ENDCOLOR}"
    echo -e "${verbose_color}.env/bin/python -m pip install --upgrade pip${ENDCOLOR}"
    echo -e "${verbose_color}source .env/bin/activate${ENDCOLOR}"
    echo -e "${verbose_color}pip install -r requirements.txt${ENDCOLOR}"
    echo -e "${verbose_color}pip list${ENDCOLOR}"
    #----------Action
    #pyenv local 3.7
    #python -m venv .env
    .env/bin/python -m pip install --upgrade pip
    . /root/forex_api/.env/bin/activate
    #pip install -r requirements.txt
    #pip list
}
#-----------------------------config_implementation
config_implementation()
{
    #----------Header
    echo -e "${header_color}${header_line}${FUNCNAME[0]}${ENDCOLOR}"
    #----------Verbose
    echo -e "${verbose_color}$path/.env/bin/python  $path/implement.py${ENDCOLOR}"
    #----------Action
    $path/.env/bin/python  $path/implement.py
}

#---------------------------------------------------------------------------------Install
#-----------------------------install_all
install_all()
{
    #----------Header
    echo -e "${header_color}${header_line}${FUNCNAME[0]}${ENDCOLOR}"
    #----------Action
    install_update
    #install_upgrade
    install_general
    install_python
    install_nginx
    install_postgres
    install_iptables
}
#-----------------------------install_update
install_update()
{
    #----------Header
    echo -e "${header_color}${header_line}${FUNCNAME[0]}${ENDCOLOR}"
    #----------Verbose
    echo -e "${verbose_color}sudo apt update ${ENDCOLOR}"
    echo -e "${verbose_color}sudo dpkg --configure -a${ENDCOLOR}"
    #----------Action
    apt update -y
    sudo dpkg --configure -a
}
#-----------------------------install_upgrade
install_upgrade()
{
    #----------Header
    echo -e "${header_color}${header_line}${FUNCNAME[0]}${ENDCOLOR}"
    #----------Verbose
    echo -e "${verbose_color}sudo apt upgrade ${ENDCOLOR}"
    #----------Action
    sudo apt upgrade -y
}
#-----------------------------install_general
install_general()
{
    #----------Header
    echo -e "${header_color}${header_line}${FUNCNAME[0]}${ENDCOLOR}"
    #----------Verbose
    echo -e "${verbose_color}apt install -yqq --no-install-recommends ca-certificates${ENDCOLOR}"
    echo -e "${verbose_color}apt install curl git telnet vim telnet${ENDCOLOR}"
    #----------Action
    sudo apt install -yqq --no-install-recommends ca-certificates
    sudo apt install curl git telnet vim telnet -y
}
#-----------------------------install_python
install_python()
{
    #----------Header
    echo -e "${header_color}${header_line}${FUNCNAME[0]}${ENDCOLOR}"
    #----------Verbose
    echo -e "${verbose_color}add-apt-repository ppa:deadsnakes/ppa -y${ENDCOLOR}"
    echo -e "${verbose_color}apt install python3 -y${ENDCOLOR}"
    echo -e "${verbose_color}apt install python3-pip -y${ENDCOLOR}"
    echo -e "${verbose_color}apt install python3-venv -y${ENDCOLOR}"
    #----------Verbose
    echo -e "${verbose_color}apt install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev git${ENDCOLOR}"
    echo -e "${verbose_color}curl https://pyenv.run | bash${ENDCOLOR}"
    echo -e "${verbose_color}export PYENV_ROOT=\"\$HOME/.pyenv\"${ENDCOLOR}"
    echo -e "${verbose_color}export PATH=\"\$PYENV_ROOT/bin:\$PATH\"${ENDCOLOR}"
    echo -e "${verbose_color}eval \"\$(pyenv init -)\"${ENDCOLOR}"
    echo -e "${verbose_color}eval \"\$(pyenv virtualenv-init -)\"${ENDCOLOR}"
    echo -e "${verbose_color}source ~/.bashrc${ENDCOLOR}"
    echo -e "${verbose_color}pyenv install 3.7${ENDCOLOR}"
    echo -e "${verbose_color}pyenv local 3.7${ENDCOLOR}"
    #----------Action
    # Install dependencies
    sudo apt install -y make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev \
    libffi-dev liblzma-dev git
    # Install pyenv
    curl https://pyenv.run | bash
    # Add pyenv to bashrc
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc
    echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
    # Reload bashrc and install Python
    source ~/.bashrc
    pyenv install 3.7
}
#-----------------------------install_nginx
install_nginx()
{
    #----------Header
    echo -e "${header_color}${header_line}${FUNCNAME[0]}${ENDCOLOR}"
    #----------Verbose
    echo -e "${verbose_color}sudo apt install nginx -y${ENDCOLOR}"
    echo -e "${verbose_color}sudo chmod -R 755 /var/www/html${ENDCOLOR}"
    echo -e "${verbose_color}echo \"\" > /etc/nginx/sites-enabled/default${ENDCOLOR}"
    echo -e "${verbose_color}systemctl restart nginx${ENDCOLOR}"
    #----------Action
    sudo apt install nginx -y
    sudo chmod -R 755 /var/www/html
    echo "" > /etc/nginx/sites-enabled/default 
    systemctl restart nginx
}
#-----------------------------install_postgres
install_postgres()
{
    #----------Header
    echo -e "${header_color}${header_line}${FUNCNAME[0]}${ENDCOLOR}"
    #----------Verbose
    echo -e "${verbose_color}sh -c 'echo \"deb http://apt.postgresql.org/pub/repos/apt \$(lsb_release -cs)-pgdg main\" > /etc/apt/sources.list.d/pgdg.list'${ENDCOLOR}"
    echo -e "${verbose_color}wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -${ENDCOLOR}"
    echo -e "${verbose_color}apt update${ENDCOLOR}"
    echo -e "${verbose_color}sudo apt install postgresql-18 -y${ENDCOLOR}"
    echo -e "${verbose_color}psql --version${ENDCOLOR}"
    echo -e "${verbose_color}sed -i \"s/#listen_addresses = 'localhost'/listen_addresses = '0.0.0.0'/\" /etc/postgresql/18/main/postgresql.conf${ENDCOLOR}"
    echo -e "${verbose_color}echo \"host all all 0.0.0.0/0 md5\" >> /etc/postgresql/18/main/pg_hba.conf${ENDCOLOR}"
    echo -e "${verbose_color}sudo systemctl restart postgresql${ENDCOLOR}"
    echo -e "${verbose_color}sudo systemctl status postgresql${ENDCOLOR}"
    echo -e "${verbose_color}systemctl enable postgresql${ENDCOLOR}"
    echo -e "${verbose_color}systemctl start postgresql${ENDCOLOR}"
    echo -e "${verbose_color}systemctl restart postgresql${ENDCOLOR}"
    #----------Action
    sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
    apt update
    sudo apt install postgresql-18 -y
    psql --version
    sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '0.0.0.0'/" /etc/postgresql/18/main/postgresql.conf
    echo "host all all 0.0.0.0/0 md5" >> /etc/postgresql/18/main/pg_hba.conf
    sudo systemctl restart postgresql
    sudo systemctl status postgresql
    systemctl enable postgresql
    systemctl start postgresql
    systemctl restart postgresql
}
#-----------------------------install_iptables
install_iptables()
{
    #----------Header
    echo -e "${header_color}${header_line}${FUNCNAME[0]}${ENDCOLOR}"
    #----------Action
    #---unistall ufw
    echo -e "${BLUE}unistall ufw${ENDCOLOR}"
    apt remove ufw -y
    apt purge ufw  -y
    #---install iptables
    echo -e "${BLUE}install iptables${ENDCOLOR}"
    sudo apt install iptables iptables-persistent -y
    #---configure iptables
    echo -e "${BLUE}configure iptables${ENDCOLOR}"
    sudo iptables -F 
    sudo iptables -X
    sudo iptables -P OUTPUT ACCEPT
    sudo iptables -P FORWARD ACCEPT
    sudo iptables -P INPUT ACCEPT    
    sudo iptables -A INPUT -i lo -j ACCEPT
    sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
    sudo iptables -A OUTPUT -o lo -j ACCEPT
    sudo iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
    sudo iptables -A INPUT -p icmp -j ACCEPT
    sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
    sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
    sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
    sudo iptables -A INPUT -p tcp --dport 11011 -j ACCEPT
    sudo iptables -A INPUT -p tcp --dport 22022 -j ACCEPT
    sudo iptables -A INPUT -p tcp --dport 33033 -j ACCEPT
    sudo iptables -A INPUT -p tcp --dport 44044 -j ACCEPT
    sudo iptables -A INPUT -p tcp --dport 1090 -j ACCEPT
    sudo iptables -A INPUT -p tcp --dport 1091 -j ACCEPT
    sudo iptables -A INPUT -p tcp --dport 1092 -j ACCEPT
    sudo iptables -A INPUT -p tcp --dport 1093 -j ACCEPT
    sudo iptables -A INPUT -p tcp --dport 1094 -j ACCEPT
    sudo iptables -A INPUT -p tcp --dport 1095 -j ACCEPT
    sudo iptables -A INPUT -p tcp --dport 1096 -j ACCEPT
    sudo iptables -A INPUT -p tcp --dport 1097 -j ACCEPT
    sudo iptables -A INPUT -p tcp --dport 1098 -j ACCEPT
    sudo iptables -A INPUT -p tcp --dport 1099 -j ACCEPT
    sudo iptables -A INPUT -p tcp --dport 1100 -j ACCEPT
    sudo iptables -A INPUT -p tcp --dport 1101 -j ACCEPT
    sudo iptables -A INPUT -p tcp --dport 1102 -j ACCEPT
    #---save iptables config
    echo -e "${BLUE}save iptables config${ENDCOLOR}"
    sudo iptables-save | uniq > /etc/iptables/rules.v4
    #---restart iptables
    systemctl restart iptables
    #---crontab
    if ! crontab -l | grep -q "@reboot systemctl restart iptables"; then (crontab -l; echo "@reboot systemctl restart iptables") | crontab -; fi
    #---Log
    log_variable="api.sh | install_iptables"; log
}

#---------------------------------------------------------------------------------Service
SERVICES=("iptables" "${name}_webapi.service" "nginx")
#-----------------------------service_create_all
service_create_all()
{
    #----------Header
    echo -e "${header_color}${header_line}${FUNCNAME[0]}${ENDCOLOR}"
    #----------Verbose
    echo -e "${verbose_color}service_create_webapi${ENDCOLOR}"
    echo -e "${verbose_color}service_create_nginx_create_api${ENDCOLOR}"
    echo -e "${verbose_color}service_create_nginx_create_gui${ENDCOLOR}"
    #----------Action
    service_create_webapi
    service_create_nginx_create_api
    service_create_nginx_create_gui
}
#-----------------------------service_control_all
service_control_all()
{
    action="$1"
    case "$action" in
        status)
            echo -e "${YELLOW}service_status\n$LINE3${ENDCOLOR}"
            for service in "${SERVICES[@]}"; do
                if systemctl is-active --quiet "$service"; then
                    echo -e "$service : ${GREEN}on${ENDCOLOR}"
                else
                    echo -e "$service : ${RED}off${ENDCOLOR}"
                fi
            done
        ;;
        stop)
            echo -e "${YELLOW}service_stop_all\n$LINE3${ENDCOLOR}"
            for service in "${SERVICES[@]}"; do
                echo -e "${BLUE}$service${ENDCOLOR}"
                systemctl stop $service
            done
        ;;
        restart)
            echo -e "${YELLOW}service_restart_all\n$LINE3${ENDCOLOR}"
            for service in "${SERVICES[@]}"; do
                echo -e "${BLUE}$service${ENDCOLOR}"
                systemctl restart $service
            done
        ;;
        disable)
            echo -e "${YELLOW}service_disable_all\n$LINE3${ENDCOLOR}"
            for service in "${SERVICES[@]}"; do
                echo -e "${BLUE}$service${ENDCOLOR}"
                systemctl disable $service
            done
        ;;
        enable)
            echo -e "${YELLOW}service_enable_all\n$LINE3${ENDCOLOR}"
            for service in "${SERVICES[@]}"; do
                echo -e "${BLUE}$service${ENDCOLOR}"
                systemctl enable $service
            done
        ;;
        *)
            echo -e "Usage: service_control_all {status|remove|stop|restart|disable|enable}"
            return 1
        ;;
    esac
}
#-----------------------------service_create_webapi
service_create_webapi()
{
    #----------Header
    echo -e "${header_color}${header_line}${FUNCNAME[0]}${ENDCOLOR}"
    #----------Data
    webapi_host=$(yq '.webapi.host' "$config_file" | tr -d '"')
    webapi_port=$(yq '.webapi.port' "$config_file" | tr -d '"')
    webapi_workers=$(yq '.webapi.workers' "$config_file" | tr -d '"')
    #----------Verbose
    echo -e "${verbose_color}webapi_host: $webapi_host${ENDCOLOR}"
    echo -e "${verbose_color}webapi_port: $webapi_port${ENDCOLOR}"
    echo -e "${verbose_color}webapi_workers: $webapi_workers${ENDCOLOR}"
    #----------Action
    api_host=$webapi_host
    api_port=$webapi_port
    api_workers=$webapi_workers
    echo -e "${BLUE}$name"_"webapi${ENDCOLOR}"
    echo """[Unit]
    Description=$name"_"webapi

    [Service]
    User=root
    WorkingDirectory=$path/
    ExecStart=$path/.myenv3/bin/uvicorn api:app --host $api_host --port $api_port --workers $api_workers
    SuccessExitStatus=143
    TimeoutStopSec=10
    Restart=on-failure
    RestartSec=65

    [Install]
    WantedBy=multi-user.target""" > /etc/systemd/system/$name"_"webapi.service

    systemctl daemon-reload
    systemctl enable $name"_"webapi
    systemctl restart $name"_"webapi
}
#-----------------------------service_create_nginx_create_api
service_create_nginx_create_api()
{
    #----------Header
    echo -e "${header_color}${header_line}${FUNCNAME[0]}${ENDCOLOR}"
    #----------Data
    webapi_host=$(yq '.webapi.host' "$config_file" | tr -d '"')
    webapi_port=$(yq '.webapi.port' "$config_file" | tr -d '"')
    nginx_api_host=$(yq '.nginx.api.host' "$config_file" | tr -d '"')
    nginx_api_port=$(yq '.nginx.api.port' "$config_file" | tr -d '"')
    nginx_api_key=$(yq '.nginx.api.key' "$config_file" | tr -d '"')
    #----------Verbose
    echo -e "${verbose_color}webapi_host: $webapi_host${ENDCOLOR}"
    echo -e "${verbose_color}webapi_port: $webapi_port${ENDCOLOR}"
    echo -e "${verbose_color}nginx_api_host: $nginx_api_host${ENDCOLOR}"
    echo -e "${verbose_color}nginx_api_port: $nginx_api_port${ENDCOLOR}"
    echo -e "${verbose_color}nginx_api_key: $nginx_api_key${ENDCOLOR}"
    #----------Action
    host=$nginx_api_host
    port=$nginx_api_port
    key=$nginx_api_key
    api_host=$webapi_host
    api_port=$webapi_port
    echo "server {
    listen $port;
    server_name _;

        location /$key {
            proxy_pass http://$api_host:$api_port;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;

            proxy_ssl_verify off;

            proxy_connect_timeout 60s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
            send_timeout 60s;
        }
    }" > /etc/nginx/sites-available/$name"_"api.conf
    
    ln -s /etc/nginx/sites-available/$name"_"api.conf /etc/nginx/sites-enabled/
    nginx -t
    systemctl reload nginx
    systemctl restart nginx
}
#-----------------------------service_create_nginx_create_gui
service_create_nginx_create_gui()
{
    #----------Header
    echo -e "${header_color}${header_line}${FUNCNAME[0]}${ENDCOLOR}"
    #----------Data
    path_gui=$(yq '.general.path_gui' "$config_file" | tr -d '"')
    nginx_gui_host=$(yq '.nginx.gui.host' "$config_file" | tr -d '"')
    nginx_gui_port=$(yq '.nginx.gui.port' "$config_file" | tr -d '"')
    nginx_gui_key=$(yq '.nginx.gui.key' "$config_file" | tr -d '"')
    #----------Verbose
    echo -e "${verbose_color}path_gui: $path_gui${ENDCOLOR}"
    echo -e "${verbose_color}nginx_gui_host: $nginx_gui_host${ENDCOLOR}"
    echo -e "${verbose_color}nginx_gui_port: $nginx_gui_port${ENDCOLOR}"
    echo -e "${verbose_color}nginx_gui_key: $nginx_gui_key${ENDCOLOR}"
    #----------Files
    echo -e "mkdir -p /var/www/$name"_"gui/"
    echo -e "chown -R $USER:$USER /var/www/$name"_"gui/"
    echo -e "chmod -R 755 /var/www/$name"_"gui/"
    echo -e "cp -fr $path_gui/* /var/www/$name"_"gui/"
    mkdir -p /var/www/$name"_"gui/
    chown -R $USER:$USER /var/www/$name"_"gui/
    chmod -R 755 /var/www/$name"_"gui/
    #----------Action
    host=$nginx_gui_host
    port=$nginx_gui_port
    key=$nginx_gui_key
    echo "server {
    listen $port;
    server_name _;
        location /$key {
            alias /var/www/$name"_"gui;
            index index.html;
            try_files \$uri \$uri/ =404;
        }
    }" > /etc/nginx/sites-available/$name"_"gui.conf
    ln -s /etc/nginx/sites-available/$name"_"gui.conf /etc/nginx/sites-enabled/
    nginx -t
    systemctl reload nginx
    systemctl restart nginx
}
#-----------------------------nginx_remove_gui
nginx_remove_gui()
{
    #----------Header
    echo -e "${header_color}${header_line}${FUNCNAME[0]}${ENDCOLOR}"
    #----------Verbose
    echo -e "${verbose_color}rm -fr /etc/nginx/sites-available/$name"_"gui.conf${ENDCOLOR}"
    echo -e "${verbose_color}rm -fr /etc/nginx/sites-enabled/$name"_"gui.conf${ENDCOLOR}"
    echo -e "${verbose_color}systemctl reload nginx${ENDCOLOR}"
    echo -e "${verbose_color}systemctl restart nginx${ENDCOLOR}"
    #----------Action
    rm -fr /etc/nginx/sites-available/$name"_"gui.conf
    rm -fr /etc/nginx/sites-enabled/$name"_"gui.conf
    systemctl reload nginx
    systemctl restart nginx
}
#-----------------------------nginx_remove_api
nginx_remove_api()
{
    #----------Header
    echo -e "${header_color}${header_line}${FUNCNAME[0]}${ENDCOLOR}"
    #----------Verbose
    echo -e "${verbose_color}rm -fr /etc/nginx/sites-available/$name"_"api.conf${ENDCOLOR}"
    echo -e "${verbose_color}rm -fr /etc/nginx/sites-enabled/$name"_"api.conf${ENDCOLOR}"
    echo -e "${verbose_color}systemctl reload nginx${ENDCOLOR}"
    echo -e "${verbose_color}systemctl restart nginx${ENDCOLOR}"
    #----------Action
    rm -fr /etc/nginx/sites-available/$name"_"api.conf
    rm -fr /etc/nginx/sites-enabled/$name"_"api.conf
    systemctl reload nginx
    systemctl restart nginx
}