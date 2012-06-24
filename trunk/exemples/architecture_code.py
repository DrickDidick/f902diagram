# -*- coding: utf-8 -*-
import os, sys
codegoogle = os.environ['CODEGOOGLE']
arch_dir = codegoogle+'/f902diagram/trunk'
#sys.path.append(arch_dir)
#import function

import glob


execfile(arch_dir+'/f90graph.py')
f90files = glob.glob('./geotherm/src/*.f90')
# Ignorer des modules dans l'arbre d'appel, pour le simplifier par exemple
use_ignoree = ['storag_class','contxt_class','eos_h2o_ph']
# ne seront pas affichés
module_not_printed = ['print_class', 'graphics_class']

gtharchi = make_graph(f90files, use_ignoree,module_not_printed)

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

