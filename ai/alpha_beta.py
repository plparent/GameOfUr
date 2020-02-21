import random
import numpy as np

########################
# Solution tic-tac-toe #
########################

#####
# joueur_tictactoe : Fonction qui calcule le prochain coup optimal pour gagner la
#                     la partie de Tic-tac-toe à l'aide d'Alpha-Beta Prunning.
#
# etat: Objet de la classe TicTacToeEtat indiquant l'état actuel du jeu.
#
# fct_but: Fonction qui prend en entrée un objet de la classe TicTacToeEtat et
#          qui retourne le score actuel tu plateau. Si le score est positif, les 'X' ont l'avantage
#          si c'est négatif ce sont les 'O' qui ont l'avantage, si c'est 0 la partie est nulle.
#
# fct_transitions: Fonction qui prend en entrée un objet de la classe TicTacToeEtat et
#                   qui retourne une liste de tuples actions-états voisins pour l'état donné.
#
# str_joueur: String indiquant c'est à qui de jouer : les 'X' ou 'O'.
#
# retour: Cette fonction retourne l'action optimal à joeur pour le joueur actuel c.-à-d. 'str_joueur'.
###

def run():
    pass

def transitions(etat):
    pass

def but(etat):
    pass

def joueur_tictactoe(etat,fct_but,fct_transitions,str_joueur):

    if str_joueur == 'X':
        _, action = alphabeta(etat, -np.Inf, np.Inf, True, fct_but, fct_transitions)
    else:
        _, action = alphabeta(etat, -np.Inf, np.Inf, False, fct_but, fct_transitions)
    return action

def alphabeta(n, alpha, beta, isMax, fct_but, fct_transitions):
    utility = fct_but(n)

    if utility is not None:
        return utility, None
    
    action = None
    if isMax:
        value = -np.Inf
        for a, etat in fct_transitions(n).items():
            utility, _ = alphabeta(etat, alpha, beta, False, fct_but, fct_transitions)

            if value < utility:
                value = utility
                action = a

            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value, action
    else:
        value = np.Inf
        for a, etat in fct_transitions(n).items():
            utility, _ = alphabeta(etat, alpha, beta, True, fct_but, fct_transitions)

            if value > utility:
                value = utility
                action = a

            beta = min(beta, value)
            if alpha >= beta:
                break
        return value, action

if __name__ == "__main__":
    run()
