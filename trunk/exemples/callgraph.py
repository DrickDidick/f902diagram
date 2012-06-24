# -*- coding: utf-8 -*-
execfile('../f90graph.py')
imgdir ='./img/'

import os
geotherm_root = os.environ['GEOTHERM_ROOT']
f90files = glob.glob(geotherm_root+'/geotherm/src/*.f90')
f90files = sorted(f90files, key=str.lower)   # Trier la liste. Pas necessaire

# f90files = ['./geotherm/src/MassEquation_class.f90']
#f90files = [geotherm_root+'/geotherm/src/mesh_class.f90']
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
ignore = ['pr_var','pop_contxt','push_contxt']
for f90 in f90files:
    graf = call_graph(f90, list_of_fct, ignore)
    tmp  = graf.keys()
    if not tmp == []:
        f90_basename = os.path.basename(f90[:-4])
        f90called = mygraph(f90_basename, rankdir='LR')
        #f90called = mygraph(f90_basename, rankdir='LR',allnodes=False)
        # if f90_basename in ['tools_class','c_interface','divergence','EnerEquation_class','MassEquation_class','method_class'] :
        #     f90called = mygraph(f90_basename, rankdir='LR')
        # else:
        #     f90called = mygraph(f90_basename)
        # Creer et afficher un noeud pour chaque subroutine
        for sub in tmp:
            f90called.creer_noeud( sub )
            # Creer un noeud pour chaque function/subroutine appellees par la subroutine
            for called in graf[sub]:
                f90called.creer_noeud( called )
                # Puis lier les subroutines et les functions
                f90called.lier_noeuds(sub, called )
        f90called.write_png(imgdir+f90_basename+'_graph')

quit()
###################################################################

total = mygraph('Total', rankdir='LR')
for f90 in f90files:
    graf = call_graph(f90, list_of_fct)
    tmp  = graf.keys()
    if not tmp == []:
        f90_basename = os.path.basename(f90[:-4])
        # Creer et afficher un noeud pour chaque subroutine
        for sub in tmp:
            total.creer_noeud( sub )
            # Creer un noeud pour chaque function/subroutine appellees par la subroutine
            for called in graf[sub]:
                total.creer_noeud( called )
                # Puis lier les subroutines et les functions
                total.lier_noeuds(sub, called )
total.write_png(imgdir+'OMG_graph')


