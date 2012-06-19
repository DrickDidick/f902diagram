def get_path_and_datas(pattern, input):
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

def get_mod_and_use(input,use_ignoree=[]):
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
                # supprimer commentaire de fin
                if '!' in worked_line:
                    i           = worked_line.index('!')
                    worked_line = worked_line[:i].strip()
                if not worked_line in use_ignoree:
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
            elif l.startswith('contains'):
                break
                
    return modname, datas, private

import re
def call_graph(input, list_of_fct=None):
    with open(input,'r') as f90:
        called, dico = [], {}
        insub, inint = 1, 1  # I'm not in a subroutine or an interface declaration
        lines = f90.readlines()
        for line in lines:
            #print insub, inint
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
                else:
                    # insub = 0
                    if inint == 0:
                        if l.startswith('end interface ') or l.startswith('end interface'):
                            inint = 1
                    else:
                        # inint = 1
                        if l.startswith('interface ') or l.startswith('interface'):
                            inint = 0
                        elif l.startswith('end subroutine '):
                            dico[subname] = called
                            called = []
                            insub  = 1
                        elif l.startswith('call '):
                            worked_line = l.replace('call ','')
                            i           = worked_line.index('(')
                            called.append(worked_line[:i])
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
                                    called.append(worked_line[: iend])
                                    break   # sort de la boucle des qu'une fonction est trouvee dans la ligne
    return dico
