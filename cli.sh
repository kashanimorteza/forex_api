#!/usr/bin/env bash

#---------------------------------------------------------------------------------Variable
#-----------------------------Color
RED="\033[31m"
GREEN="\033[32m"
YELLOW="\033[33m"
BLUE="\033[34m"
CYAN="\033[36m"
ENDCOLOR="\033[0m"
LINE0="-----"
LINE1="-----------"
LINE2=$LINE1$LINE1
LINE3=$LINE2$LINE2
LINE4=$LINE3$LINE3
header_color=$YELLOW
verbose_color=$BLUE
header_line=$LINE2

#-----------------------------check_jq_yq
check_jq_yq()
{
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
check_jq_yq
#-----------------------------Variable
path="$( cd "$(dirname "$0")" ; pwd -P )"
api_sh=$path/api.sh
config_file=$path/config.yaml
#-----------------------------Config
name=$(yq '.general.name' "$config_file" | tr -d '"')

source /root/forex_api/.env/bin/activate

#---------------------------------------------------------------------------------Menu
#--------------------menu_main
menu_main()
{
    clear
    while true; do
        getHeader
        echo -e  ${YELLOW}"1)  ${GREEN}All"          ${ENDCOLOR}
        echo -e  ${YELLOW}"2)  ${GREEN}Menu Install" ${ENDCOLOR}
        echo -e  ${YELLOW}"3)  ${GREEN}Menu Config"  ${ENDCOLOR}
        echo -e  ${YELLOW}"4)  ${GREEN}Menu Service" ${ENDCOLOR}
        echo -e  ${YELLOW}"5)  ${GREEN}Monitor"      ${ENDCOLOR}
        echo -e "${YELLOW}${LINE2}                   ${ENDCOLOR}"
        echo -e  ${YELLOW}"q)  ${GREEN}Exit"         ${ENDCOLOR}
        read -p "Enter your choice [1-5]: " choice
        case $choice in
            1)  clear && all;;
            2)  clear && menu_install;;
            3)  clear && menu_config;;
            4)  clear && menu_service;;
            5)  clear && monitor;;
            q)  clear && exit;;
            *)  exit;;
        esac
        echo -e "\n"
    done
}

#--------------------menu_install
menu_install()
{
    clear
    while true; do
        getHeader
        echo -e  ${YELLOW}${LINE2}Install        ${ENDCOLOR}
        echo -e  ${YELLOW}"1)  ${GREEN}All"      ${ENDCOLOR}
        echo -e  ${YELLOW}"2)  ${GREEN}Update"   ${ENDCOLOR}
        echo -e  ${YELLOW}"3)  ${GREEN}Upgrade"  ${ENDCOLOR}
        echo -e  ${YELLOW}"4)  ${GREEN}Iptables" ${ENDCOLOR}
        echo -e  ${YELLOW}"5)  ${GREEN}Genaral"  ${ENDCOLOR}
        echo -e  ${YELLOW}"6)  ${GREEN}Nginx"    ${ENDCOLOR}
        echo -e  ${YELLOW}"7)  ${GREEN}Postgres" ${ENDCOLOR}
        echo -e  ${YELLOW}"8)  ${GREEN}Python"   ${ENDCOLOR}
        echo -e "${YELLOW}${LINE2}                   ${ENDCOLOR}"
        echo -e  ${YELLOW}"q)  ${GREEN}Exit"         ${ENDCOLOR}
        read -p "Enter your choice [1-8]: " choice
        case $choice in    
            1)  clear && install_all;;
            2)  clear && install_update;;
            3)  clear && install_upgrade;;
            4)  clear && install_iptables;;
            5)  clear && install_general;;
            6)  clear && install_nginx;;
            7)  clear && install_postgres;;
            8)  clear && install_python;;
            q)  clear && menu_main;;
            *)  menu_main;;
        esac
        echo -e "\n"
    done
}

#--------------------menu_config
menu_config()
{
    clear
    while true; do
        getHeader
        echo -e  ${YELLOW}${LINE2}Config          ${ENDCOLOR}
        echo -e  ${YELLOW}"1)  ${GREEN}All"       ${ENDCOLOR}
        echo -e  ${YELLOW}"2)  ${GREEN}General"   ${ENDCOLOR}
        echo -e  ${YELLOW}"3)  ${GREEN}Network"   ${ENDCOLOR}
        echo -e  ${YELLOW}"4)  ${GREEN}Git"       ${ENDCOLOR}
        echo -e  ${YELLOW}"5)  ${GREEN}Postgres"  ${ENDCOLOR}
        echo -e  ${YELLOW}"6)  ${GREEN}Python"    ${ENDCOLOR}
        echo -e  ${YELLOW}"7)  ${GREEN}Implement" ${ENDCOLOR}
        echo -e "${YELLOW}${LINE2}                   ${ENDCOLOR}"
        echo -e  ${YELLOW}"q)  ${GREEN}Exit"         ${ENDCOLOR}
        read -p "Enter your choice [1-7]: " choice
        case $choice in    
            1)  clear && config_all;;
            2)  clear && config_general;;
            3)  clear && config_network;;
            4)  clear && config_git;;
            5)  clear && config_postgres;;
            6)  clear && config_python;;
            7)  clear && config_implementation;;
            q)  clear && menu_main;;
            *)  menu_main;;
        esac
        echo -e "\n"
    done
}

#--------------------menu_service
menu_service()
{
    clear
    while true; do
        getHeader
        echo -e  ${YELLOW}${LINE2}Services           ${ENDCOLOR}
        echo -e  ${BLUE}"${LINE1}All"                ${ENDCOLOR}
        echo -e  ${YELLOW}"1)  ${GREEN}Create"       ${ENDCOLOR}
        echo -e  ${YELLOW}"2)  ${GREEN}Status"       ${ENDCOLOR}
        echo -e  ${YELLOW}"3)  ${GREEN}Stop"         ${ENDCOLOR}
        echo -e  ${YELLOW}"4)  ${GREEN}Start"        ${ENDCOLOR}
        echo -e  ${YELLOW}"5)  ${GREEN}Restart"      ${ENDCOLOR}
        echo -e  ${YELLOW}"6)  ${GREEN}Enable"       ${ENDCOLOR}
        echo -e  ${YELLOW}"7)  ${GREEN}Disable"      ${ENDCOLOR}
        echo -e  ${BLUE}"${LINE1}webapi"             ${ENDCOLOR}
        echo -e  ${YELLOW}"8)  ${GREEN}Create"       ${ENDCOLOR}
        echo -e  ${YELLOW}"9)  ${GREEN}Status"       ${ENDCOLOR}
        echo -e  ${YELLOW}"10) ${GREEN}Stop"         ${ENDCOLOR}
        echo -e  ${YELLOW}"11) ${GREEN}Start"        ${ENDCOLOR}
        echo -e  ${YELLOW}"12) ${GREEN}Restart"      ${ENDCOLOR}
        echo -e  ${YELLOW}"13) ${GREEN}Enable"       ${ENDCOLOR}
        echo -e  ${YELLOW}"14) ${GREEN}Disable"      ${ENDCOLOR}
        echo -e  ${YELLOW}"15) ${GREEN}Monitor"      ${ENDCOLOR}
        echo -e  ${BLUE}"${LINE1}Nginx"              ${ENDCOLOR}
        echo -e  ${YELLOW}"16) ${GREEN}Create API"   ${ENDCOLOR}
        echo -e  ${YELLOW}"17) ${GREEN}Create GUI"   ${ENDCOLOR}
        echo -e  ${YELLOW}"18) ${GREEN}Status"       ${ENDCOLOR}
        echo -e  ${YELLOW}"19) ${GREEN}Stop"         ${ENDCOLOR}
        echo -e  ${YELLOW}"20) ${GREEN}Start"        ${ENDCOLOR}
        echo -e  ${YELLOW}"21) ${GREEN}Restart"      ${ENDCOLOR}
        echo -e  ${YELLOW}"22) ${GREEN}Enable"       ${ENDCOLOR}
        echo -e  ${YELLOW}"23) ${GREEN}Disable"      ${ENDCOLOR}
        echo -e  ${YELLOW}"24) ${GREEN}Monitor"      ${ENDCOLOR}
        echo -e "${YELLOW}${LINE2}                   ${ENDCOLOR}"
        echo -e  ${YELLOW}"q)  ${GREEN}Exit"         ${ENDCOLOR}
        read -p "Enter your choice [1-24]: " choice
        case $choice in
            #--------------------------All
            1)  clear && service_create_all;;
            2)  clear && service_control_all status;;
            3)  clear && service_control_all stop;;
            4)  clear && service_control_all start;;
            5)  clear && service_control_all restart;;
            6)  clear && service_control_all enable;;
            7)  clear && service_control_all disable;;
            #--------------------------WebApi
            8)  clear && service_create_webapi ;;
            9)  clear && systemctl status $name"_"webapi.service;;
            10) clear && systemctl stop $name"_"webapi.service;;
            11) clear && systemctl start $name"_"webapi.service;;
            12) clear && systemctl restart $name"_"webapi.service;;
            13) clear && systemctl enable $name"_"webapi.service;;
            14) clear && systemctl disable $name"_"webapi.service;;
            15) clear && journalctl -n 100 -u $name"_"webapi.service -f;;
            #--------------------------Nginx
            16) clear && service_create_nginx_create_api;;
            17) clear && service_create_nginx_create_gui;;
            18) clear && systemctl status nginx;;
            19) clear && systemctl stop nginx;;
            20) clear && systemctl start nginx;;
            21) clear && systemctl restart nginx;;
            22) clear && systemctl enable nginx;;
            23) clear && systemctl disable nginx;;
            24) clear && journalctl -n 100 -u nginx -f;;
            q)  clear && menu_main;;
            *)  menu_main ;;
        esac
        echo -e "\n"
    done
}

#---------------------------------------------------------------------------------api_interface
api_interface()
{
    # Call any function from api.sh with all arguments passed through
    if declare -f "$1" > /dev/null 2>&1; then
        "$@"
    else
        echo "Error: Function '$1' not found"
        exit 1
    fi
}

#---------------------------------------------------------------------------------Actions
source $api_sh
cd $path
if [  "$1" == "" ]; then menu_main; fi
if [  "$1" != "" ]; then api_interface $1 $2 $3 $4 $5; fi