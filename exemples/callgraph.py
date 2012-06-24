# -*- coding: utf-8 -*-
execfile('../f90graph.py')

f90files = glob.glob('./geotherm/src/*.f90')
f90files = sorted(f90files, key=str.lower)   # Trier la liste. Pas necessaire

# f90files = ['./geotherm/src/MassEquation_class.f90']
# Récupérer toute les fonctions du code
list_of_fct = []
module, tmp, private = {}, {}, {}
# Ignoree des modules dans l'arbre d'appel, pour le simplifier par exemple
use_ignoree = ['storag_class','contxt_class']
for f90 in f90files:
    tmp = get_pattern_and_datas('function ', f90)
    list_of_fct += tmp.keys()
    # Collecter les modules utilsées par un autre
    modname, modused, private_flag = get_mod_and_use(f90, use_ignoree)
    private[modname] = private_flag
    module [modname] = modused
list_of_fct = sorted(list_of_fct)


# call graph pour chaque fichier
for f90 in f90files:
    graf = call_graph(f90, list_of_fct)
    tmp  = graf.keys()
    if not tmp == []:
        f90_basename = os.path.basename(f90[:-4])
        if f90_basename in ['c_interface','divergence','EnerEquation_class','MassEquation_class','method_class'] :
            test = mygraph(f90_basename, rankdir='LR')
        else:
            test = mygraph(f90_basename)
        # Creer et afficher un noeud pour chaque subroutine
        for sub in tmp:
            test.creer_noeud( sub )
            # Creer un noeud pour chaque function/subroutine appellees par la subroutine
            for called in graf[sub]:
                test.creer_noeud( called )
                # Puis lier les subroutines et les functions
                test.lier_noeuds(sub, called )
        test.write_png(f90_basename+'_graph')


###################################################################

test = mygraph('basename')
for f90 in f90files:
    graf = call_graph(f90, list_of_fct)
    tmp  = graf.keys()
    if not tmp == []:
        f90_basename = os.path.basename(f90[:-4])
        # Creer et afficher un noeud pour chaque subroutine
        for sub in tmp:
            test.creer_noeud( sub )
            # Creer un noeud pour chaque function/subroutine appellees par la subroutine
            for called in graf[sub]:
                test.creer_noeud( called )
                # Puis lier les subroutines et les functions
                test.lier_noeuds(sub, called )
test.write_png('OMG_graph')


