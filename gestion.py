# Importation des classes nécessaires
from Mediatheque import Mediatheque
from Media import Book, CD, Vinyles
from Person import Administrator

# Initialisation de la médiathèque
mediateque = Mediatheque()


def display_menu():
    print("\n=== Menu de la Médiathèque ===")
    print("1. Ajouter un utilisateur")
    print("2. Ajouter un média")
    print("3. Emprunter un média")
    print("4. Retourner un média")
    print("5. Vérifier l'historique")
    print("6. Envoyer des avertissements")
    print("7. Quitter")
    return input("Choisissez une option : ")


def ajouter_utilisateur():
    login = input("Entrez le login : ")
    pwd = input("Entrez le mot de passe : ")
    utilisateur = Administrator(login, pwd, "Nom", "Prénom", 1)  # Exemple avec un utilisateur par défaut
    print(mediateque.register_person(utilisateur))


def ajouter_media():
    print("1. Livre")
    print("2. CD")
    print("3. Vinyle")
    choix = input("Choisissez le type de média : ")
    title = input("Entrez le titre du média : ")
    media_id = input("Entrez l'ID du média : ")
    state = input("Entrez l'état du média : ")

    media_classes = {"1": Book, "2": CD, "3": Vinyles}
    if choix in media_classes:
        media = media_classes[choix](title, media_id, state)
        mediateque._Mediatheque__media.append(media)
        print(f"Média '{title}' ajouté avec succès")
    else:
        print("Choix invalide")


def emprunter_media():
    media_title = input("Entrez le titre du média à emprunter : ")
    for media in mediateque._Mediatheque__media:
        if media._Media__title == media_title:
            print(media.borrow())
            return
    print("Média non trouvé")


def retourner_media():
    media_title = input("Entrez le titre du média à retourner : ")
    for borrow in mediateque._Mediatheque__history:
        if borrow._Borrow__media._Media__title == media_title:
            print(mediateque.return_media(borrow))
            return
    print("Aucun emprunt correspondant trouvé")


def verifier_historique():
    historique = mediateque.check_history(None)
    if not historique:
        print("Aucun emprunt trouvé dans l'historique")
    else:
        for borrow in historique:
            print(f"Emprunt : {borrow._Borrow__media._Media__title} par {borrow._Borrow__user._Person__login}")


def envoyer_avertissements():
    avertissements = mediateque.warn_users(None)
    if not avertissements:
        print("Aucun avertissement à envoyer")
    else:
        for avertissement in avertissements:
            print(avertissement)


# Dictionnaire des actions du menu
actions = {
    "1": ajouter_utilisateur,
    "2": ajouter_media,
    "3": emprunter_media,
    "4": retourner_media,
    "5": verifier_historique,
    "6": envoyer_avertissements
}

# Boucle principale de l'interface utilisateur
while True:
    choix = display_menu()
    if choix == "7":
        print("Au revoir !")
        break
    action = actions.get(choix)
    if action:
        action()
    else:
        print("Option invalide, veuillez réessayer.")
