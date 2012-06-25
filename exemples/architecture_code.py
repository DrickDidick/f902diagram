# -*- coding: utf-8 -*-
import os, sys
codegoogle = os.environ['CODEGOOGLE']
arch_dir = codegoogle+'/f902diagram/trunk'
#sys.path.append(arch_dir)
#import function

import glob


execfile(arch_dir+'/f90graph.py')
import os
geotherm_root = os.environ['GEOTHERM_ROOT']
f90files = glob.glob(geotherm_root+'/geotherm/src/*.f90')

# Ignorer des modules dans l'arbre d'appel, pour le simplifier par exemple
ExternalUsed = ['storag_class','contxt_class','eos_h2o_ph']
#use_ignoree = []

# ne seront pas affichés
NotUsed = ['graphics_class','print_class']

gtharchi = make_graph(f90files, use_ignoree=ExternalUsed, module_not_printed=[], highlighted_use=NotUsed)

imgdir = './img/'
name = imgdir+'architecture_graph'
gtharchi.write_png(name)

gtharchi = make_graph(f90files)
gtharchi.write_png(name+'_complet')

quit()

name = 'architecture'+'_graph'
gtharchi.graph.write_pdf(name+'.pdf')
gtharchi.graph.write_svg(name+'.svg')
gtharchi.graph.write(name+'.dot')
# gtharchi.graph.write_dia(name+'.dia')

