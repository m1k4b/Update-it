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
    print("\nVos Modpacks :")

    i = 1
    for modpack in data["modpacks"]:
        print(f"{i}. {modpack['name']} | Contient: {', '.join([mod["name"] for mod in modpack['mods']])}")
        i += 1

    if i == 1:
        print("Vos modpacks s'afficheront ici.\n")
    else:
        print()

    choice = int(input("Voulez vous en télécharger un ou en créer un ? 1 pour télécharger, 2 pour créer, 3 pour supprimer, 4 pour arrêter le programme. "))
    if choice == 1:
        modpack_index = int(input("Entrez le numéro du modpack : "))-1
        modpack_to_download = data["modpacks"][modpack_index]
        version = input("Entrez la version : ")
        print("Téléchargement en cours, veuillez patienter...")
        for mod in modpack_to_download["mods"]:
            status_bool,related_data = fast_download_mod(mod["name"],version,"fabric")
            if not status_bool:
                status_to_msg = {
                    "versionNotSupported":f"la version {version} n'est pas supportée.",
                    "loaderNotSupported":f"le loader Fabric n'est pas supporté.",
                    "notFound":f"une erreur inconnue s'est produite. Veuillez réessayer plus tard."
                }
                print(f"Erreur lors du téléchargement de {mod["name"]} : {status_to_msg[related_data]}")
            else:
                print(f"Téléchargement réussi de {mod["name"]} ! Enregistré à la location \"{related_data}\".")

        print("Téléchargement terminé !")
        data["modpacks"][modpack_index]["downloads"]+=1
        save()
    elif choice==2:
        mods = []
        modpack_name = input("Entrez le nom du nouveau modpack : ")
        while True:
            mod_name = input("Entrez le nom d'un mod que vous voulez ajouter (s pour terminer) : ")
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
        modpack_index = int(input("Entrez le numéro du modpack : ")) - 1
        data["modpacks"].pop(modpack_index)
        save()
    elif choice==4:
        sys.exit()