import time
import os
import shutil
from pathlib import Path
from ctypes import *


u32 = CDLL("User32.dll")
GetKeyState = u32.GetKeyState
GetKeyState.restype = c_ushort
GetKeyState.argtypes = [c_int]

VK_F5 = 0x74
VK_F7 = 0x76
VK_F12 = 0x7B

def is_key_pressed(key):
    #"if the high-order bit is 1, the key is down; otherwise, it is up."
    return (GetKeyState(key) & (1 << 7)) != 0

def pz_load(selected_slot):
    print("Loading from QuickSlot...")
    shutil.rmtree(selected_slot)
    shutil.copytree(selected_slot+"_BACKUP",selected_slot)
    
def pz_save(selected_slot):
    print("Saving to QuickSlot...")
    shutil.rmtree(selected_slot+"_BACKUP")
    shutil.copytree(selected_slot, selected_slot+"_BACKUP")

def get_save_slot():
    slot = []
    save_root = os.path.join(str(Path.home()),"Zomboid","Saves")
    # Do Apocalypse Files
    apoc_root = os.path.join(save_root,"Apocalypse")
    for item in os.listdir(apoc_root):
        if(item.endswith("_BACKUP")):
            continue
        slot.append(f"Apocalypse\\{item}")
    # Do Survivor Files
    survivor_root = os.path.join(save_root,"Survivor")
    for item in os.listdir(survivor_root):
        if(item.endswith("_BACKUP")):
            continue
        slot.append(f"Survivor\\{item}")
    
    for i in range(0,len(slot)):
        print(f"{i} : {slot[i]}")
    slot_choice = -1
    while slot_choice not in range(0,len(slot)):
        slot_choice = int(input("Select Slot: "))
    return os.path.join(save_root,slot[slot_choice])
    
if __name__=="__main__":
    selected_slot = get_save_slot()
    while not is_key_pressed(VK_F12):
        if(is_key_pressed(VK_F5)):
            pz_save(selected_slot)
        if(is_key_pressed(VK_F7)):
            pz_load(selected_slot)
        time.sleep(0.01)
    print("Exiting - SEE YOU!")

    