# -*- coding: utf-8 -*-
"""RL&MC.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mQcKhXN8huCGqucwzLbiNhEA4YGTAau2

**Cadenas de Markov**

Una cadena de Markov (CM) es un tipo particular de proceso estocástico.
Una CM tiene probabilidades de transición estacionarias, es decir, no dependen del tiempo. Las probabilidades del estado siguiente dependen únicamente del estado presente y no de los estados pasados. Esto permite que la CM se pueda representar de manera compacta con un grafo.

![](https://drive.google.com/uc?export=view&id=1K4yyA6Whp88NVc2ocznvcjevvauGCMg5)

Por ejemplo:

En este caso la CM tiene dos estados.
Los parámetros de las aristas son las probabilidades de transición de estado.
Por ejemplo, en esta CM la probabilidad de transitar del estado 1 al estado 2 es de 0.7. 

Esto lo denotamos como $P(s^{t+1}{=}2 \mid s^{t}{=}1) = 0.7$

Las probabilidades de transición de una cadena de Markov se pueden representar de manera matricial.

En este caso la matrix de probabilidades de transición $T$ queda dada por: 

$T = 
\begin{bmatrix}
0.3&0.6 \\
0.7&0.4
\end{bmatrix}
$
"""

import numpy as np #Importación de la librería NumPy, Numerical Python empleado para el manejo de arreglos multidimesionales

T = np.matrix([[0.3,0.6],[0.7,0.4]]) #Creación de la matriz 2x2 T

print(T) #Imprimir T

"""La evolución de la distribución de probabilidad $x$ para los dos estados esta dada por la ecuación:


$
 x = T x
$
 
Por ejemplo, si sabemos con certeza que estamos en el estado 1, se representa como:
 
$
x = 
\begin{bmatrix}
1\\
0
\end{bmatrix}
$
 
Es decir la probabilidad de estar en el estado 1 es 1 y de estar en el estado 2 es 0.
 
Si queremos saber como será la distribución de probabilidad para los estados en el tiempo siguiente hacemos:

$x^{t+1} = 
\begin{bmatrix}
0.3&0.6\\
0.7&0.4
\end{bmatrix}
\begin{bmatrix}
1\\
0
\end{bmatrix}
=
\begin{bmatrix}
0.3\\
0.7
\end{bmatrix}
$
 
Es decir la probabilidad de estar en el estado 1 es 0.3 y de transitar al estado 2 es 0.7. 
Si queremos saber que pasará dos tiempos en el futuro, iteramos la ecuación:

$x^{t+2} = 
\begin{bmatrix}
0.3&0.6\\
0.7&0.4
\end{bmatrix}
\begin{bmatrix}
0.3&0.6\\
0.7&0.4
\end{bmatrix}
\begin{bmatrix}
1\\
0
\end{bmatrix}
=
\begin{bmatrix}
0.3&0.6\\
0.7&0.4
\end{bmatrix}^2
\begin{bmatrix}
1\\
0
\end{bmatrix}
$
 
Con ayuda de NumPy podemos resolver esta multiplicación de matrices:
"""

x = np.matrix([[1],[0]]) #Probabilidades de estados
print('x =\n'+str(x)+'\n')

x_1 = np.matmul(T,x) #Multiplicación de la matriz de estados por la matriz de probabilidades de transición usando la función matmul() de NumPy.
print('x(t+1)=\n'+str(x_1)+'\n')

x_2 = np.matmul(T,x_1) #Multiplicación para calcular la probabilidad de estados a dos pasos de tiempo
print('x(t+2)=\n'+str(x_2)+'\n')

#Comprobar que el resultado anterior es el mismo que elevar la matriz $T$ al cuadrado y multiplicar por $x$ usando la función matrix_power() de NumPy.
x_2= np.matmul(np.linalg.matrix_power(T,2),x)
print('x(t+2)=\n'+str(x_2))

"""Bajo ciertas condiciones, existe una distribución de probabilidad estacionaria sobre los estados.
Esto significa que no importa cual sea la distribución de probabilidad inicial, al iterar la ecuación, la distribución converge a una distribución que no cambia. 

Por ejemplo, definamos un método calcula_dist() para encontrar la distribución de probabilidad al tiempo t ó $n$, dada una condición inicial $x_0$, empleando la misma matriz de probabilidad de transición de estados $T$:
"""

def calcula_dist(T,x_0,n):
    x_n = np.matmul(np.linalg.matrix_power(T,n),x_0)
    print('x(t+'+str(n)+')=\n'+str(x_n))


#Usemos esta función para encontrar la distribución al tiempo 5:
x_10 = calcula_dist(T,x,10)

# Veamos como cambia la distribución con cada una de las iteraciones:
for i in range(10):
    calcula_dist(T,x,i)
    print("\n")

"""Observamos una rápida convergencia a los valores.
¿Qué tanto tenemos que iterar la ecuación para encontrar la distribución?
Esto puede resolverse más fácilmente si observamos que lo que queremos encontrar es $x^{\text{*}}$ tal que:
 
$x^{\text{*}} = T x^{\text{*}}$

Esto es equivalente a resolver el problema de encontrar los vectores característicos de la matriz $T$.

Los vectores característicos de una matriz, también conocidos como eigenvectores,  son aquellos que no cambian de dirección cuando se aplica la transformación lineal $T$ (es decir cuando se multiplica por $T$).

Usando NumPy podemos encontrar el eigenvector de una matriz, usando la función linalg.eig():
"""

#La función linalg.eg() regresa un tupple con un vector y una matriz. El vector corresponde a los eigenevalores y la matriz a los eigenvectores

l,v = np.linalg.eig(T)
print("Eigenvalores de matriz T:\n"+str(l))
print("\n")
print("Eigenvectores de matriz T:\n"+str(v)) #Eigenvectores de matriz T

#Nos interesa el eigenvector que corresponde con el eigenvalor 1, ya que ambos valores del eigenvector (-0.651,-0.759) tienen el mimso signo. 
#En este caso el vector que esta como segunda columna en v. Lo extraemos y normalizamos:
x_s = v[:,1] / sum(v[:,1])
print(x_s)

#La matriz de probabilidad de estados es la misma que la obtenida con la iteración a 10 pasos de la función calcula_dist(T,x_0,n)

"""---

---

**PRÁCTICA Considera la CM representada por el siguiente diagrama:**

![Ejercicio práctico](https://drive.google.com/uc?export=view&id=1rmq02Ip_pJ_vFveXAA4wLOH9pmoGlb50)

**Encuentra la distribución de probabilidad estacionaria.**

---


---

**Procesos de Decisión de Markov (MDPs o PDMs)**

En los Procesos de Decisión de Markov (PDMs) encadenamos la decisiones del agente con un proceso estocástico. 
Nos interesa resolver la ecuación de Bellman para la política del agente.
Recordemos que la política le dice al agente que acción tomar en cada estado posible.

Para encontrar la politica optima $\pi^*$ podemos usar el algoritmo de iteración de políticas.
A continuación te damos una implementación básica del algoritmo:
"""

import numpy as np

#Itertools es una librería con funciones para crear bucles (loops) eficientes. 
#La función product() regresa el producto cartesiano de dos vectores input, equivalente a un bucle anidado (nested for-loop) 
from itertools import product 

#La función choice() de la librería random elige un elemento al azar de una lista input. 
from random import choice 

class MDP: #Classes son instancias de Python que actúan como constructores de objetos
    
    def __init__(self,s,r,a,T,gamma): #Cualquier instancia class, inicia con una función __init__() para asignar valores a las propiedades de los objectos.
        """
        Builds the MDP problem
        :param s: states
        :param r: rewards
        :param a: actions
        :param T: dictionary where keys are (s,a) pairs and
        values are probabilities
        :param gamma: the discount factor
        """
        self.s = s
        self.r = r
        self.a = a
        self.T = T
        self.gamma = gamma
        
    def policy_iteration(self,pi=None):
        """
            Policy iteration algorithm
        """
        #initial random policy
        if not pi:
            pi = [choice(self.a) for s in self.s]
        
        print('pi = '+str(pi))
        self.obtainT(pi);
        T = self.obtainT(pi)
        print('T(pi) = \n'+str(T))
        
        V = np.matmul(np.linalg.inv(np.eye(3)-self.gamma*T.T),self.r)
        print('V(s) = '+ str(V))
        
        pi_star = self.find_pi_star(V)
        print("pi*(s) = "+str(pi_star))
        
        if pi_star == pi:
            return pi
        else:
            return self.policy_iteration(pi_star)
        
    def obtainT(self,pi):
        """
        Obtains the transition probability matrix parametrized by the policy pi
        :param pi: the policy
        """
        return           np.matrix([[self.T[(s,t,pi[s])] for s in self.s] for t in self.s])
        
    def find_pi_star(self,V):
        """
        Finds the optimal policy for the given infinite horizon values
        :param V: the infinite horizon expected utility
        """
        
        print("\n".join([str((x,np.matmul(self.obtainT(x).T,np.array(V).T))) for x in product(self.a,self.a,self.a)]))
        
        return list(max(product(self.a,self.a,self.a),            key=lambda x: np.sum(np.matmul(self.obtainT(x).T,np.array(V).T))))

# Para ejecutar el algoritmo primero definimos los estados posibles:
estados = [0,1,2]
print(estados)

# Las acciones posibles:
acciones = [0,1]
print(acciones)

# Ahora las recompensas para cada estado:
recompensas = [0,10,27]
print(recompensas)

# El parámetro gamma es el factor de descuento para la utilidad de valores futuros:
gamma = 0.9
print(gamma)


# Ahora representamos las probabilidaddes condicionales con un diccionario.
# <img src="mdpejemplo2.png" alt="mdp" width="914"/>

# La llave será una tupla con tres elementos, los primeros dos contienen los índices de la transición de estado, el último es la acción que se toma.
 
# El valor del diccionario es la probabilidad asociada al estado, acción correspondiente.

T={
    (0,0,0):0.7,(0,0,1):0.5, (1,0,0):0.4,(1,0,1):0.2, (2,0,0):0.2,(2,0,1):0.1,
    (0,1,0):0.1,(0,1,1):0.3, (1,1,0):0.4,(1,1,1):0.7, (2,1,0):0.2,(2,1,1):0.1,
    (0,2,0):0.2,(0,2,1):0.2, (1,2,0):0.2,(1,2,1):0.1, (2,2,0):0.6,(2,2,1):0.8
}
print(T)


# Vamos a crear una instancia del PDM:
mdp = MDP(estados,recompensas,acciones,T,gamma)


# Comprobamos que obtenemos la misma política que el ejemplo del tren inteligente.
# 
# En el ejemplo $\pi_0 = \begin{bmatrix}0&0&0\end{bmatrix}$.


pi_0 = [0,0,0]
print("T(pi_0) = \n"+str(mdp.obtainT(pi_0)))


# Ahora invocamos el algoritmo de iteración de políticas.
# 
# El algoritmo imprime como cambia la política con las iteraciones.

politica = mdp.policy_iteration(pi_0)

"""---
---

**PRÁCTICA**

**Si cambiamos el valor las recompensas a $[0, 20, 20]$, ¿cambia la politica?**

---
---

**Reinforcement Learning: MDPs and Q-Learning**
"""

"""

@author: stan

"""

import numpy as np
import pylab as pl
from IPython import display
from itertools import product
from math import inf,sqrt
from random import choice,choices

INACCESIBLE = 0
ACCESIBLE = 1
TERMINAL = 2

class Map:
    
    def __init__(self,types,rewards):
        self.types = np.matrix(types)
        self.rewards = np.matrix(rewards)
        self.rows,self.cols = self.types.shape 
        #padding for plots
        self.e = 0.04
        x = 1/sqrt(2)
        #arrows per action
        self.arrows = {'N':(0,1),
                       'NE':(x,x),
                       'E':(1,0),
                       'SE':(x,-x),
                       'S':(0,-1),
                       'SW':(-x,-x),
                       'W':(-1,0),
                       'NW':(-x,x)}

        self.point = None
        
    def __str__(self):
        return 'types: '+'\n'+str(self.types)+'\n'+\
                'rewards: '+'\n'+str(self.rewards)
        
    def __repr__(self):
        return str(self)
    
    def display_map(self):
        pl.figure()
        ax = pl.gca()
        ax.axis("equal")
        xcoor = [0,0,1,1,0]
        ycoor = [0,1,1,0,0]
        colors = ['black','green','red']
        e = self.e
        for i in range(self.rows):
            r = [x+(i*(e+1)) for x in xcoor]
            for j in range(self.cols):
                c = [y+(j*(e+1)) for y in ycoor]
                pl.fill(c,r,colors[self.types[i,j]])
        #check this on jupyter notebooks
        #display.display(pl.gcf())
        pl.axis('off')
        pl.title('Agent environment')
        
    def display_rewards(self):
        pl.figure()
        cmap = pl.cm.bwr
        cmap.set_bad(color='black')
        r = np.ma.masked_where(self.rewards==0.0,self.rewards)
        pl.imshow(r,cmap=cmap,origin='lower')
        pl.colorbar()
        pl.axis('off')
        pl.title('Reward signal')
        
    def animate_Vs(self,V, error, reset=False, delay=0.5):
        if reset:
            pl.figure()
        else:
            self.cb.remove()
        cmap = pl.cm.bwr
        cmap.set_bad(color='black')
        vs= self.rewards.copy()
        for (x,y),v in V.items():
            vs[y,x]=v
        r = np.ma.masked_where(self.rewards==0.0,vs)
        pl.imshow(r,cmap=cmap,origin='lower')
        pl.axis('off')
        pl.title('Infinite horizon value function. Error = %f'%error)  
        self.cb = pl.colorbar()
        pl.pause(delay)

        
    def display_probs(self,probs):
        pl.figure()
        vbar = np.ones((3,1))
        hbar = np.ones((1,11))
        mat = np.vstack((
                np.hstack((probs['NW'],vbar,probs['N'],vbar,probs['NE'])),
                hbar,
                np.hstack((probs['W'],vbar,np.zeros((3,3)),vbar,probs['E'])),
                hbar,
                np.hstack((probs['SW'],vbar,probs['S'],vbar,probs['SE']))))
        r = np.ma.masked_where(mat==1,mat)
        cmap = pl.cm.jet
        cmap.set_bad(color='white')
        pl.imshow(r,cmap=cmap)
        pl.colorbar()
        pl.axis('off')
        pl.title('Stochastic move probabilities')
    
    def show(self,probs):
        self.display_map()
        self.display_rewards()
        self.display_probs(probs)
        
    def animate_move(self,x_prev,x,reset=False,cumreward=None,delay=1):
        #padding
        e = self.e
        if reset:
            pl.figure()
            self.point = False
            ax = pl.gca()
            ax.axis("equal")
            xcoor = [0,0,1,1,0]
            ycoor = [0,1,1,0,0]
            colors = ['black','green','red']
            for i in range(self.rows):
                r = [x+(i*(e+1)) for x in xcoor]
                for j in range(self.cols):
                    c = [y+(j*(e+1)) for y in ycoor]
                    pl.fill(c,r,colors[self.types[i,j]])
            display.display(pl.gcf())
        x_prev = list(map(lambda c:c+0.5+e*c,x_prev))
        x = list(map(lambda c:c+0.5+e*c,x))
        pl.plot(*zip(x_prev,x),color='white')
        if self.point:
            ax = pl.gca()
            ax.lines[-2].remove()
        else:
            self.point = True
        pl.plot([x[0],x[0]],[x[1],x[1]],marker='.',c='cyan',markersize=40)    
        if cumreward:
            pl.title("Cummulative reward: "+f'{cumreward:06.2f}')
        pl.pause(delay)
        
    def show_policy(self,pi):
        e = 2*self.e
        pl.figure()
        ax = pl.gca()
        ax.axis("equal")
        xcoor = [0,0,1,1,0]
        ycoor = [0,1,1,0,0]
        colors = ['black','green','red']
        for i in range(self.rows):
            r = [x+(i*(2*e+1)) for x in xcoor]
            for j in range(self.cols):
                c = [y+(j*(2*e+1)) for y in ycoor]
                pl.plot(c,r,colors[self.types[i,j]])
                if self.types[(i,j)]== ACCESIBLE:
                    ar
                    row = self.arrows[pi[(j,i)]]
                    ax.quiver(
                            j*(2*e+1)+0.5,
                            i*(2*e+1)+0.5,
                            arrow[0],
                            arrow[1],
                            scale=2,
                            scale_units='x')
        pl.show()
        display.display(pl.gcf())

class MDPWorld:
    
    def __init__(self,filename):

        self.types = {INACCESIBLE:'Inaccesible',
                      ACCESIBLE:'Accesible',
                      TERMINAL:'Terminal'}
        self.actions = ['N','NE','E','SE','S','SW','W','NW']
        self.n_actions = len(self.actions)
        self.read(filename)
        
    def read(self,filename):
        self.filename = filename
        with open(filename) as f:
            lines = [l.strip() for l in f.readlines()]
        rows,cols = map(int,lines[0].split())
        map_info = [l.split() for l in lines[1:rows+1]]
        types = [list(map(int,row[0::2])) for row in map_info]
        rewards = [list(map(float,row[1::2])) for row in map_info]
        self.probs = {}
        for i in range(0,self.n_actions):
            probs_info = [l.split() for l in lines[rows+3*i+1:rows+3*(i+1)+1]]
            self.probs[self.actions[i]]=np.matrix(
                    [list(map(float,row)) for row in probs_info])
        self.map = Map(types,rewards)
        
    def attempt_location(self,x_prev, x_new):
        # returns the new location if it is an allowed move and
        # the previous otherwise
        return \
            x_new if 0<=x_new[0]<self.map.cols and 0<=x_new[1]<self.map.rows\
            and self.map.types[(x_new[1],x_new[0])] != INACCESIBLE else x_prev

    
    def reachable_state_probability_pairs(self,s,action):
        probs = self.probs[action]
        #state probability pairs
        sp = {}
        for x in product([-1,0,1],[-1,0,1]):
            pos = self.attempt_location(s,(x[0]+s[0],x[1]+s[1]))
            prob = probs[::-1,:][(x[1]+1,x[0]+1)]
            if prob > 0:
                sp[pos] = sp[pos] + prob if pos in sp else prob
        return sp
    
    def move(self,s,action):
        #thresholds for stochastic simulation
        ths = np.cumsum(self.probs[action][::-1,:]).reshape(3,3)
        r = np.random.uniform()
        m = np.where(r<=ths)
        pos = min(zip(m[0],m[1]))
        #changed index order
        s_p = self.attempt_location(
            s,(s[0]+int(pos[1])-1,s[1]+int(pos[0])-1))
        return (s_p,self.reward_of_cell(s_p))
        
    def simulate(self,pi,n,x=(0,0)):
        self.map.animate_move(x,x,reset=True)
        #rows and columns are swaped in the matrix
        cumreward = self.reward_of_cell(x)
        for i in range(n):
            x_prev = x
            x,reward = self.move(x,pi[x])
            cumreward += reward
            self.map.animate_move(x_prev,x,cumreward=cumreward)
            if self.terminal_cell(x):
                break
        return cumreward
            
    def random_pi(self):
        pi = {p:a for p,a in \
              zip(product(range(self.map.cols),range(self.map.rows)),
              np.random.choice(self.actions,self.map.rows*self.map.cols))}
        return pi
    
    def expected_reward(self,cell, action,V):
        return sum(map(lambda i:V[i[0]]*i[1],
            self.reachable_state_probability_pairs(cell,action).items()))
        
    def accesible_cell(self, cell):
        return self.map.types [(cell[1],cell[0])] == ACCESIBLE
    
    def terminal_cell(self,cell):
        return self.map.types [(cell[1],cell[0])] == TERMINAL
    
    def reward_of_cell(self,cell):
        return self.map.rewards[(cell[1],cell[0])]
    
    def compute_v(self,gamma,animate=False,epsilon=1.e-9):
        error = inf
            
        V = {cell:0.0 \
             if not self.terminal_cell(cell) else self.reward_of_cell(cell) \
             for cell in product(range(self.map.cols),range(self.map.rows))}
        if animate == True:
            self.map.animate_Vs(V,error,reset=True)
        while error > epsilon*(1-gamma)/gamma:
            V_prev = V.copy()
            for cell in filter(lambda x:self.accesible_cell(x),V.keys()):
                V[cell] = self.reward_of_cell(cell)+ \
                gamma*max([self.expected_reward(cell,action,V) \
                     for action in self.actions])
            error = max([abs(V[k]-V_prev[k]) for k in V.keys()])
            if animate:
                self.map.animate_Vs(V,error)
        return V
                
    def compute_optimal_pi(self,gamma,epsilon=1.e-9):
        Vs = self.compute_v(gamma,animate=False,epsilon=epsilon)
        pi = {}
        for cell,v in Vs.items():
                pi[cell] = max([(action,self.expected_reward(cell,action,Vs))\
                     for action in self.actions],key=lambda c:c[1])[0]       
        return pi     
    
    def best_action_Q(self,Q,s):
        return max([(a,Q[(s,a)]) for a in self.actions ],
                    key=lambda x:x[1])[0]
        
    def q_learn(self,alpha,gamma,episodes,steps):
        n,m = self.map.cols,self.map.rows
        cells = [x for x in product(range(n),range(m))\
                 if self.accesible_cell(x) or self.terminal_cell(x)]
        #initialize with instantaneous reward
        self.Q = {(s,a):self.reward_of_cell(s) \
                  for s,a in product(cells,self.actions)}
        for episode,s in enumerate(choices(cells,k=episodes),1):
            # instantaneous reward
            r = self.reward_of_cell(s)
            for step in range(steps):
                # explore action
                a = choice(self.actions)
                # attempt to move
                s_p, r_p = self.move(s,a)
                self.Q[(s,a)] = (1-alpha)*self.Q[(s,a)]+\
                alpha*(r+gamma*max([self.Q[(s_p,a)] for a in self.actions]))
                s,r = s_p,r_p
                if self.terminal_cell(s):
                    # early termination
                    break
        return {s:self.best_action_Q(self.Q,s) for s in cells}

#Visualizar los datos en el documento problem-1.mdp exportando de URL-GitHub
import pandas as pd
url = "https://raw.githubusercontent.com/riiaa/MDP_and_RL/master/problem-2.mdp"
m = pd.read_csv(url)
m

#Cargar los datos con la función MDFWorld que nos permite separar el espacio en "tipos" y "recompensas"
m = MDPWorld('problem-2.mdp')

m.map.show()

v= m.compute_v(1.animate=TRUE, epsilon=1.e-6)

pi=m.random_pi()
m.simulate()
