import shutil
import os
from datetime import datetime

def export_db(db_path, usb_path):
    if not os.path.exists(usb_path):
        print("USB not mounted")
        return

    filename = f"inverter_{datetime.now().date()}.db"
    dest = os.path.join(usb_path, filename)

    shutil.copy(db_path, dest)
    print("Exported to USB:", dest)
