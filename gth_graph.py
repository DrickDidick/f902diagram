import pydot

class mygraph(object):
    def __init__(self,name,rankdir=None,allnodes=False):#,shape='box',color='black',fillcolor='green'):
        if rankdir == None:
            self.graph = pydot.Dot(graph_type='digraph')
        else:
            self.graph = pydot.Dot(graph_type='digraph',rankdir=rankdir) # dir de gauche de droite
        #setattr(self,name, pydot.Node(name))
        #self.graph.add_node(getattr(self,name))
        self.name      = name
        self.allnodes  = allnodes
        #self.shape     = shape
        #self.color     = color
        #self.fillcolor = fillcolor

    def creer_noeud(self,name,color='black',fillcolor='white',private=False,shape='box'):
        try:
            # tester si le noeud existe deja. Si oui ne rien faire
            getattr(self,name)
        except:
            #setattr(self,name, pydot.Node(name,shape='box',color=color))
            if private == False:
                label = name
            else:
                shape='record'
                #label ="<f0> %s|private"%name

                label ='<<table border="0"> \
<tr><td>%s</td></tr>\
<tr><td>private </td></tr> \
</table>>'%name
# #<tr><td align="left" port="r1">private </td></tr> \
# #'<<table border="0" cellborder="0" cellpadding="3" bgcolor="white"> \

            setattr(self,name, pydot.Node(name,label=label,shape=shape,color=color,style='filled',fillcolor=fillcolor))
            # if fillcolor == None:
            #     setattr(self,name, pydot.Node(name,shape='box',ratio='auto',label=label))
            # else:
            #     setattr(self,name, pydot.Node(name,shape='box',style='filled',fillcolor=fillcolor))
            if self.allnodes == True:
                self.graph.add_node(getattr(self,name))

    def lier_noeud(self, b):
        self.graph.add_edge( pydot.Edge(getattr(self,self.name), getattr(self,b)) )

    def lier_noeuds(self, a, b):
        try:
            getattr(self,a+b) # test si un lien existe
            setattr(self,a+b, getattr(self,a+b) + 1) # compteur de lien
            #print getattr(self,a+b)
        except:
            if self.allnodes == False:
                self.graph.add_node(getattr(self,a))
                self.graph.add_node(getattr(self,b))
            self.graph.add_edge( pydot.Edge(getattr(self,a), getattr(self,b)) )
            setattr(self,a+b,1)

    def write_png(self, name):
        self.graph.write_png(name+'.png')
        #self.graph.write_dia(name)
        #self.graph.write_pdf(name)
        #self.graph.write_svg(name)
        #self.graph.write(name+'.tex')




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
