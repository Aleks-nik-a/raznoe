#!/bin/bash
#
#


ip_list=("192.168.0.97")

remote_user="root"
local_path="/home/wb/git/test-suite-ng/"


for ip in "${ip_list[@]}"; do
    echo "sync to $ip..."
    rsync -avzhHl "$local_path"  "$remote_user@$ip:/opt/test-suite-ng-Sasha"

    if [ $? -eq 0 ]; then
        echo "Successfully sync $ip"
    else
        echo "Failed to sync to $ip"
    fi
done

# rsync -avzhHl /home/wb/git/test-suite-ng/ root@192.168.0.97:/opt/tsng_Sasha
