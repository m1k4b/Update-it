import sys
from tools import fast_download_mod
import os
import json

def save():
    global data
    with open(os.path.join(app_directory, "data.json"), "w") as f:
        json.dump(data,f,indent=4)

user_directory = os.path.expanduser("~")
app_directory = os.path.join(user_directory, "Update It")

if not os.path.exists(app_directory):
    os.makedirs(app_directory)
    with open(os.path.join(app_directory, "data.json"), "w") as f:
        json.dump({
            "modpacks":[],
        }, f)

with open(os.path.join(app_directory, "data.json"), "r") as f:
    data = json.load(f)

while True:
    print("\nYour Modpacks:")

    i = 1
    for modpack in data["modpacks"]:
        print(f"{i}. {modpack['name']} | Contains: {', '.join([mod['name'] for mod in modpack['mods']])}")
        i += 1

    if i == 1:
        print("Your modpacks will appear here.\n")
    else:
        print()

    choice = int(input("Choose the action you want to perform. 1 to download, 2 to create, 3 to delete, 4 to edit, 5 to exit the program. "))
    if choice == 1:
        modpack_index = int(input("Enter the modpack number: "))-1
        modpack_to_download = data["modpacks"][modpack_index]
        version = input("Enter the version: ")
        location = input("Enter the path to the directory where you want to install the modpack (d for .minecraft/mods): ")
        if location.startswith("\""):
            location = location[1:-1]
        print("Downloading, please wait...")
        for mod in modpack_to_download["mods"]:
            status_bool,related_data = fast_download_mod(mod["name"],version,"fabric",loc=None if location=="d" else location)
            if not status_bool:
                status_to_msg = {
                    "versionNotSupported":f"version {version} is not supported.",
                    "loaderNotSupported":f"the Fabric loader is not supported.",
                    "notFound":f"an unknown error occurred. Please try again later."
                }
                print(f"Error while downloading {mod['name']}: {status_to_msg[related_data]}")
            else:
                print(f"Successfully downloaded {mod['name']}! Saved at \"{related_data}\".")

        print("Download complete!")
        data["modpacks"][modpack_index]["downloads"]+=1
        save()
    elif choice==2:
        mods = []
        modpack_name = input("Enter the name of the new modpack: ")
        while True:
            mod_name = input("Enter the name of a mod you want to add (s to finish): ")
            if mod_name=="s":
                break
            mods.append({
                "name":mod_name
            })
        data["modpacks"].append({
            "name": modpack_name,
            "mods": mods,
            "downloads":0
        })
        save()
    elif choice==3:
        modpack_index = int(input("Enter the modpack number: ")) - 1
        data["modpacks"].pop(modpack_index)
        save()
    elif choice==4:
        modpack_index = int(input("Enter the modpack number: ")) - 1
        edit_choice = int(input("Enter 1 to change the name, 2 to add mods. "))
        if edit_choice==1:
            new_name = input("Enter the new name: ")
            data["modpacks"][modpack_index]["name"] = new_name
            save()
        elif edit_choice==2:
            while True:
                mod_name = input("Enter the name of a mod you want to add (s to finish): ")
                if mod_name == "s":
                    break
                data["modpacks"][modpack_index]["mods"].append({"name":mod_name})
            save()
    elif choice==5:
        save()
        sys.exit()
