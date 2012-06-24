# -*- coding: utf-8 -*-
import pydot

##################################   Adaptation de pydot a mes besoins ##################################
class mygraph(object):
    def __init__(self,name,rankdir=None,allnodes=True):#,shape='box',color='black',fillcolor='green'):
        if rankdir == None:
            self.graph = pydot.Dot(graph_type='digraph')
        else:
            self.graph = pydot.Dot(graph_type='digraph',rankdir=rankdir) # dir de gauche de droite
        self.name      = name
        self.allnodes  = allnodes

    def creer_noeud(self,name,color='black',fillcolor='white',private=False,shape='box'):
        if not hasattr(self,name):
            if private == False:
                label = name
            else:
                shape='record'
                label ='<<table border="0"><tr><td>%s</td></tr><tr><td>private</td></tr></table>>'%name
            setattr(self,name, pydot.Node(name,label=label,shape=shape,color=color,style='filled',fillcolor=fillcolor))
            if self.allnodes == True:
                self.graph.add_node(getattr(self,name))

    def lier_noeud(self, b):
        self.graph.add_edge( pydot.Edge(getattr(self,self.name), getattr(self,b)) )

    def lier_noeuds(self, a, b):
        if hasattr(self,a+b):
            setattr(self,a+b, getattr(self,a+b) + 1) # compteur de lien. pas encore utilise
        else:
            if self.allnodes == False:
                self.graph.add_node(getattr(self,a))
                self.graph.add_node(getattr(self,b))
            self.graph.add_edge( pydot.Edge(getattr(self,a), getattr(self,b)) )
            setattr(self,a+b,1)

    def write_png(self, name):
        self.graph.write_png(name+'.png')

    def write_pdf(self, name):
        #self.graph.write_dia(name)
        self.graph.write_pdf(name+'.pdf')

    def write_svg(self, name):
        self.graph.write_svg(name+'.svg')

    def write_dot(self, name):
        self.graph.write(name+'.dot')


################################## Recuperer les pattern existant et leurs données ##################################
# En mettant pattern = 'function' ou 'subroutine' on obtient toutes les 'pattern' du fichier 'input' et leurs données
def get_pattern_and_datas(pattern, input):
    with open(input,'r') as f90:
        datas, subname, dico = [], [], {}
        insub = 1  # I'm not in a subroutine declaration
        lines = f90.readlines()
        for line in lines:
            l = line.strip()
            if l.startswith('!'):
                pass
            else:
                if insub == 0 :
                    if 'end '+pattern not in line and '::' in line:
                        datas.append(line.strip())
                    elif 'end '+pattern in line:
                        dico[ subname ] = datas
                        datas = []
                        insub = 1
                else:
                    if l.startswith(pattern):
                        worked_line = l.replace(pattern,'')
                        i           = worked_line.index('(')
                        subname     = worked_line[:i]
                        insub = 0
    return dico

################################## Collecter les modules utilisés par un module ##################################
# Collecter les modules utilisés par un module ou un program
# Il est possible d'ignorer certains modules importés par 'input' (le program ou le module)
# il suffit de rentrer la liste des modules a ignorer dans use_ignore
def get_mod_and_use(input,use_ignore=[]):
    with open(input,'r') as f90:
        datas   = []
        private, modflag = False, False
        lines = f90.readlines()
        for line in lines:
            l = line.strip()
            if l.startswith('!') :
                pass

            elif l == 'private':
                private = True

            elif l.startswith('use ') :
                worked_line = l.replace('use ','')
                # supprimons le commentaire de fin de ligne s'il y en a.
                if '!' in worked_line:
                    i           = worked_line.index('!')
                    worked_line = worked_line[:i].strip()
                if not worked_line in use_ignore:
                    datas.append(worked_line.strip())
                    
            elif modflag is False:
                if l.startswith('module ') or  l.startswith('program ') :
                    modflag = True
                    worked_line = l.replace('module ','')
                    modname     = worked_line
                    if '!' in worked_line:
                        i           = worked_line.index('!')
                        modname     = worked_line[:i].strip()

            #elif l.startswith('implicit none') or l.startswith('contains'):
            # private is allways writed after implict none
            elif l.startswith('contains'): # Attention tous les modules n'ont pas necessairement de contains
                break
                
    return modname, datas, private

import re
def call_graph(input, list_of_fct=[], igcalled = []):
    with open(input,'r') as f90:
        called, dico = [], {}
        insub, inint = 1, 1  # I'm not in a subroutine or an interface declaration
        lines = f90.readlines()
        for line in lines:
            l = line.strip()
            if l.startswith('!') : # ligne de commentaire
                pass
            else:
                if insub == 1 :
                    if l.startswith('subroutine '):
                        worked_line = l.replace('subroutine ','')
                        i           = worked_line.index('(')
                        subname     = worked_line[:i]
                        insub = 0
                    elif l.startswith('function '):
                        worked_line = l.replace('function ','')
                        i           = worked_line.index('(')
                        subname     = worked_line[:i]
                        insub = 0
                else:
                    if inint == 0:
                        if l.startswith('end interface'):
                            inint = 1
                    else:
                        if l.startswith('interface'):
                            inint = 0
                        elif l.startswith('end subroutine') or  l.startswith('end function'):
                            dico[subname] = called
                            called        = []
                            insub         = 1  # sortie de la subroutine
                        elif l.startswith('call '):
                            worked_line = l.replace('call ','')
                            i           = worked_line.index('(')
                            name        = worked_line[:i].strip()
                            if not name in igcalled:
                                called.append(name)
                        else:
                            # Rechercher si j'appelle une de mes fonctions
                            for fct in list_of_fct:
                                # Le modif d'appel est *= mafonction(
                                #pattern = '.*=.*'+fct+'\(.*'
                                pattern = '.*= *'+fct+' *\(.*'
                                match   = re.search(pattern, l)
                                if match :
                                    worked_line = l
                                    ibeg        = worked_line.index('=')
                                    # Supprimer tout ce qu'il y a avt le signe '='
                                    # et enlever espace(s) apres '=' si il y en a
                                    worked_line = worked_line[ibeg+1:].strip()
                                    iend        = worked_line.index('(')
                                    name        = worked_line[:iend].strip()
                                    if not name in igcalled:
                                        called.append(name)
                                    break   # sort de la boucle des qu'une fonction est trouvee dans la ligne
    return dico


def make_graph(f90files, use_ignoree=[], module_not_printed=[]):
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


import glob, os
class souscode(object):
    def __init__(self, dico, input):
        self.subroutines = sorted(dico.keys())
        list_of_fcts = get_pattern_and_datas('function ', input)
        self.functions   = list_of_fcts.keys()
        for sub in self.subroutines:
            setattr(self,sub,sorted(dico[sub]))
        
class code(object):
    def __init__(self):
        self.files = []

    def add_module(self,input,list_of_fcts=[]):
        attr = os.path.basename(input[:-4])
        self.files.append(attr)
        #setattr(self, attr, souscode(get_path_and_datas('subroutine ', input)))
        setattr(self, attr, souscode(call_graph(input, list_of_fcts), input) )


# "state7" [ style = "filled" penwidth = 1 fillcolor = "white" fontname = "Courier New" shape = "Mrecord"
#     label =<<table>
# <tr><td align="center">State #7</td></tr>
# <tr><td align="left" port="r1">Debut : </td></tr>
# <tr><td align="left" port="r3">Fin : </td></tr>
# <tr><td align="left" port="r4">Duree :</td></tr>
# <tr><td align="left" port="r5">&#40;5&#41; r -&gt; &bull;l </td></tr>
#            </table>> ];

# "state7" [ style = "filled" penwidth = 1 fillcolor = "white" fontname = "Courier New" shape = "Mrecord"
#     label =<<table border="0" cellborder="0" cellpadding="3" bgcolor="white">
# <tr><td bgcolor="black" align="center" colspan="2"><font color="white">State #7</font></td></tr>
# <tr><td align="left" port="r1">Debut : </td></tr>
# <tr><td align="left" port="r3">Fin : </td></tr>
# <tr><td align="left" port="r4">Duree :</td></tr>
# <tr><td align="left" port="r5">&#40;5&#41; r -&gt; &bull;l </td></tr>
#            </table>> ];
