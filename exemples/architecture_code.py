# -*- coding: utf-8 -*-
import os, sys
codegoogle = os.environ['CODEGOOGLE']
arch_dir = codegoogle+'/f902diagram/trunk/'
#sys.path.append(arch_dir)
#import function
execfile(arch_dir+'/function.py')

import glob


def make_graph(f90files, use_ignoree=[],module_not_printed=[]):
    # Recuperer la dependence entre modules
    module, private  = {}, {}

    for f90 in f90files:
        # Collecter les modules utilisées par un autre
        modname, modused, private_flag = get_mod_and_use(f90, use_ignoree)
        private[modname] = private_flag
        module [modname] = modused

    gtharchi = mygraph('code', rankdir='LR',allnodes=True)


    for mod in module.keys():
        if mod in module_not_printed:
            pass
        else:
            if mod in ['graphics_class','print_class']:
                gtharchi.creer_noeud( mod,fillcolor='green',private = private[mod] )
            else:
                gtharchi.creer_noeud( mod,private = private[mod] )

    # Pourquoi ne pas inclure la boucle suivante dans celle d'au-dessus ?
    # De cette manière je peux facilement identifier les modules externe a
    # f90files appelées et les mettre en jaune par exemple
    for mod in module.keys():
        if mod in module_not_printed:
            pass
        else:
            ##Creer un noeud pour chaque function/subroutine appellees par la subroutine
            for used in module[mod]:
                gtharchi.creer_noeud( used,fillcolor='yellow' ) # Externe a geotherm/src
                gtharchi.lier_noeuds(mod, used )

    return gtharchi

if __name__ == '__main__' :
    execfile(arch_dir+'/gth_graph.py')
    f90files = glob.glob('./geotherm/src/*.f90')
    # Ignorer des modules dans l'arbre d'appel, pour le simplifier par exemple
    use_ignoree = ['storag_class','contxt_class','eos_h2o_ph']
    # ne seront pas affichés
    module_not_printed = ['print_class', 'graphics_class']

    gtharchi = make_graph(f90files, use_ignoree,module_not_printed)
    name = 'architecture_graph'
    gtharchi.write_png(name)

    gtharchi = make_graph(f90files)
    gtharchi.write_png(name+'_complet')

    quit()

    name = 'architecture'+'_graph'
    gtharchi.graph.write_pdf(name+'.pdf')
    gtharchi.graph.write_svg(name+'.svg')
    gtharchi.graph.write(name+'.dot')
    #gtharchi.graph.write_dia(name+'.dia')

