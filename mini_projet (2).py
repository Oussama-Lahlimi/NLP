#----------------------------- PHASE 1----------------------------------------

corpus = [('la', 'DET'), ('belle', 'ADJ'), ('ferme', 'V'),
          ('la', 'DET'), ('porte', 'N'),
          ('.', 'PONCT'), ('la', 'DET'), ('belle', 'ADJ'),
          ('fille', 'N'), ('est', 'COP'),
          ('ferme', 'ADJ'), ('.', 'PONCT'), ('une', 'DET'),
          ('belle', 'N'), ('la', 'PRO'),
          ('porte', 'V'), ('.', 'PONCT'), ('une', 'DET'),
          ('belle', 'ADJ'), ('fille', 'N'),
          ('la', 'PRO'), ('porte', 'V'), ('.', 'PONCT'),
          ('il', 'PRO'), ('la', 'PRO'),
          ('porte', 'V'), ('.', 'PONCT')]



#la premiére etape consiste a creer un dictionnaire d'apres un corpus etiqueté  

#la premiere fonction retoure un dictionnaire nommée lexique qui contient un autre dictionnaire 
def apprendre_Etiquettes(corpus):
    lexique = {}
    for mot, etiquette in corpus:
        if mot not in lexique:
            lexique[mot] = {}
        if etiquette not in lexique[mot]:
            #si le mot n'existe pas on cree un dictionnaire vide a comme clé le mot 
            lexique[mot][etiquette] = 0
        lexique[mot][etiquette] += 1
    return lexique


#la deuxieme question
def Choix_Etiquette(liste_etiquette):
    max_occurrence = 0
    etiquette_plus_frequente = None
    for etiquette, occurrence in liste_etiquette.items():
        if occurrence > max_occurrence:
            max_occurrence = occurrence
            etiquette_plus_frequente = etiquette
    return etiquette_plus_frequente

# la troisiéme Question
def Apprendre_lexique(corpus):
    lexique = apprendre_Etiquettes(corpus)
    lexique_final = {}
    for mot, etiquettes in lexique.items():
        etiquette_plus_frequente = Choix_Etiquette(etiquettes)
        lexique_final[mot] = etiquette_plus_frequente
    return lexique_final

#----------------------------PHASE2-------------------------------------#
#premiere fonction
 
def Reetiqueter_corpus(corpus,lexique):
    nouveau_corpus = []
    for mot,_ in corpus : 
        nouvelle_etiquette = lexique[mot]
        nouveau_corpus.append((mot, nouvelle_etiquette))
    return nouveau_corpus

corpus_test=Reetiqueter_corpus(corpus,Apprendre_lexique(corpus))

# deuxieme fonction calcule le nombre des erreurs 
def Comparer(corpus_reference,corpus_test):
    nb_erreurs = 0
    for i in range(len(corpus_reference)):
        mot_ref, etiquette_ref = corpus_reference[i]
        mot_test, etiquette_test = corpus_test[i]
        if etiquette_ref != etiquette_test:
            nb_erreurs += 1
    return nb_erreurs
         
nb_erreur=Comparer(corpus,corpus_test)
#print(f"le nombre d'erreurs avant appliquer les régles contextuelles ==> {nb_erreur}")

#---------------------------PHASE3----------------------------------------#

# on va écrire une fonction qui applique une regle contextuelle a notre corpus
def Appliquer_regle(corpus_C0,ancienne_etiquette,nouv_etiquette,contex_gauche,contex_droit):
    # C1 est le nouveau corpus aprés appliquer les régles 
    C1=[]
    for i in range(len(corpus)):
        mot,etiquette=corpus[i]
        if i>0 and i< len(corpus)-1:
            etiquette_gauche = corpus[i-1][1]
            etiquette_droit = corpus[i+1][1]
        elif i == 0:
            etiquette_gauche = ''
            etiquette_droit = corpus[i+1][1]
        else:
            etiquette_gauche = corpus[i-1][1]
            etiquette_droit = ''
        if (etiquette == ancienne_etiquette and
        (contex_gauche == '*' or etiquette_gauche == contex_gauche) and
        (contex_droit == '*' or etiquette_droit == contex_droit)):
           C1.append((mot, nouv_etiquette))
        else:
            C1.append((mot, etiquette))
    
    return C1


# Maintenant on doit écrire une fonction qui retourne la régle qui corrige le maximum d'erreurs  

def Choisir_regle(corpus, corpus_test):
    regles = []
    for i in range(len(corpus)):
        mot_ref, etiquette_ref = corpus[i]
        mot_test, etiquette_test = corpus_test[i]
        if etiquette_ref != etiquette_test:
            contexte_gauche = '' if i == 0 else corpus_test[i-1][1]
            contexte_droit = '' if i == len(corpus_test) - 1 else corpus_test[i+1][1]
            regles.append((etiquette_test, etiquette_ref, contexte_gauche, contexte_droit))
    
    regles_occurrences = {}
    for regle in regles:
        if regle not in regles_occurrences:
            regles_occurrences[regle] = 0
        regles_occurrences[regle] += 1
    # nous allons comparer les regles d'apres les valeurs d'occurences
    regle_max_occurrences = max(regles_occurrences, key=regles_occurrences.get)
    contexte_gauche = '*' if regle_max_occurrences[2] == '' else regle_max_occurrences[2]
    contexte_droit = '*' if regle_max_occurrences[3] == '' else regle_max_occurrences[3]
    
    regle_choisie = (regle_max_occurrences[0], regle_max_occurrences[1], contexte_gauche, contexte_droit)
    
    return regle_choisie


regle_choisi=Choisir_regle(corpus, corpus_test)
#print (f"regle({regle_choisi[0]},{regle_choisi[1]},{regle_choisi[2]},{regle_choisi[3]})")
C1=Appliquer_regle(corpus_test,regle_choisi[0],regle_choisi[1],regle_choisi[2],regle_choisi[3])
#print(f"le nouveau corpus etiqueté : \n{C1}")
# maintenant on va revoir le nombre d'erreurs obtenu 
nb_err2=Comparer(corpus,C1)
#print(f"le nombre d'erreur aprés appliquer la regle choisi {nb_err2}" )

#--------------------------PHASE4--------------------------------------------------------------------------------#

# maintenant on va generer plusieurs regles et le nombre d'erreur soit au dessus d'un seuil*
 
def Generer_regles(corpus_reference, corpus_test, seuil):
    regles = []
    nb_erreurs = Comparer(corpus_reference, corpus_test)
    
    while nb_erreurs > seuil:
        regle = Choisir_regle(corpus_reference, corpus_test)
        regles.append(regle)
        corpus_test = Appliquer_regle(corpus_test, regle[0], regle[1], regle[2], regle[3])
        nb_erreurs = Comparer(corpus_reference, corpus_test)
    
    return regles

# On teste la fonction 
Liste_regles=Generer_regles(corpus,corpus_test,0)
#print(f"L'ensemble des regles est : {Liste_regles}")


#-----------------------PHASE 5------------------------------------------------------------------------------------#

# maintenant on va appliquer ces régles au notre corpus de test 

def Etiqueter_corpus(corpus_test, lexique, liste_regles):
    corpus_etiquete=Reetiqueter_corpus(corpus_test,lexique)
    
    for regle in liste_regles:
        ancienne_etiquette, nouvelle_etiquette, contexte_gauche, contexte_droit = regle
        corpus_etiquete = Appliquer_regle(corpus_etiquete, ancienne_etiquette, nouvelle_etiquette, contexte_gauche, contexte_droit)
    
    return corpus_etiquete 
#ca est le nobmre d'erreur avant appliquer les regles
nb_err1=Comparer(corpus_test,corpus)
print(f"le nombre d'erreurs avant appliquer les régles ==> {nb_err1}")
# on fait une comparaison pour assurer que les régles sont appliqué
nb_err2=Comparer(corpus,Etiqueter_corpus(corpus_test,Apprendre_lexique(corpus_test),Liste_regles))
print(f"le nombre d'erreur aprés appliquer les régles ==> {nb_err2}")