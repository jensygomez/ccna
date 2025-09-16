# NetMonDB/core/db_manager/main_db_manager.py

from .db import init_db, insert_or_update_device, get_all_devices

def db_main(device_info, parsed_data=None):
    init_db()
    insert_or_update_device(device_info, parsed_data)

def check_devices_in_db():
    init_db()
    devices = get_all_devices()
    device_list = []
    for d in devices:
        device_list.append({
            "hostname": d[1],
            "ip": d[2],
            "username": d[3],
            "password": d[4],
            "gateway": d[5],
            "interface": d[6],
            "device_type": d[7]
        })
    return device_list
