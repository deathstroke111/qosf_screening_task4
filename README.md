# qosf_screening_task4

$$\newcommand{\ket}[1]{\left|{#1}\right\rangle}$$
$$\newcommand{\bra}[1]{\left\langle{#1}\right|}$$

>IN CASE YOU CAN'T RUN THE PACKAGE, PLEASE CHECK THE SAMPLE OUTPUT IN sample_output.ipynb 
>PLEASE OPEN THE FILE QAOA_maxcut.ipynb to render the README instructions properly

>INSTRUCTIONS TO USE THE PACKAGE
>
>- The requirements needed to run this project are given the environment.yml file, It has few commented pip install packages which neds to be run seperately on command line **after installing conda packages** since their are some campatibilty issues.
<br>
>- Go inside the task4 folder
<br>
>- run command for veiwing all addional options ->> python main.py 
<br>
>- The optional parameters to customize :
    - -h, --help               show this help message and exit
    - -s SHOTS, --shots SHOTS  Set the number of shots
    - -d DEPTH, --depth DEPTH  Set the depth of the Quantum circuit
    - -n NUM, --num NUM        Set the number of qubits
    - -i ITER, --iter ITER     Set the number of iterations for optimal gamma and beta
    - -g GRAPH, --graph GRAPH  Select the type of graph


This repository contains the solution of the task4 of QOSF mentorship program.



For this task we had to implement the QAOA algorithm for MaxCut problem the any weighted graph i.e. generalize/extend the idea of unwighted graph to weighted graphs. 
<br> <br>
The real challenge about the MaxCut probelm is that it comes under the class of problem which are of combinational complexity in nature when solved classically by the use of any turing machine.
<br>
Now according to the original paper the objetcive function for this set of classes- defined on bit string of size n- is :

<div align="center">
    $$ C(z) = \sum^m _{\alpha=1} C_{\alpha}(z)$$
</div>

Where $z = z1,z2,z3,..$ is the bit string and $C_{\alpha}(z) = 1$ if z satisfies clause $\alpha$ and $0$ if it doesn't.  
<br>

Since the Qauntum computers operate on a completely different paradigm, they can leverage the nature of physics at the fundamental levels to by pass this combinational limit and could potentially solve the problems under this category more efficiently.Here the authors have tried to demonstrate that very possiblity of solving the MaxCut problem by QAOA algorithm ( <a href="https://arxiv.org/pdf/1411.4028.pdf">original paper link</a> )
<br><br>
The background is to consider the graphs to be weighted and each vertex is a part of connected graph; The aim is to find a optimal cut or rather an arrangement of seperation in which the sum of weights connecting the opposite groups is maximal. Thus transforming the given general clause condition to suite our MaxCut problem, the unitary operator has been defined as 

<div>
    $$U(C,\gamma) = e^{-i \gamma C} = \prod_{\alpha=1}^m e^{-i\gamma C_{\alpha}}$$
</div>

The next operator b has been defined as :

<div>
    $$U(C,\beta) = e^{-i \beta B} =  \prod_{j=1}^m e^{-i\beta \sigma^x_{j}}$$
</div>

The idea behind using this is that, suppose that we use only $U(C,\gamma)$ then we might come across a state which is the eigen state after which we wouldn't be able to cross it, if the maximum state isn't this. Therefore we need a function which can help us gain momentum when trapped in such state (local maxima) if it hadn't been there our momentum would have been reduced to near zero value which would in fact prevent any more change in the value; this is analogous to having genetic mutations in genetic algorithms which is also used for the same purpose.
For this reason we prefer a unitary operator $U_B$ to commute with a $U_C$.
<br><br>

The initial state is usually prefered to be in superposition of all states, therefore the initial state can be given by:

<div>
$$\ket{s} = 1/\sqrt{2^n} \sum_z \ket{z}$$
</div>

We can now notice what we have actually achieved by expressing the MaxCut problem using Qubits. what we have essentialy done is reduce the problem from finding the optimal grapgh arrangement to finding the optimal values of $\beta$ and $\gamma$ which we can easily do using classical techniques such as classical optimizers or even grid search. Below is the same thing written mathematically (here p is the depth of the circuit or rather nmumber totterized states),   

<div>
$$\ket{\gamma,\beta} = U(B,\beta_p) U(C,\gamma_p)...U(B,\beta_1) U(C,\gamma_1) \ket{s}$$
</div>
<br>
Let the expectation value of clause C over $\gamma$ and $\beta$ be defnied by $F_p(\gamma,\beta)$ :

<div>
    $$F_p( \gamma , \beta ) = \bra{ \gamma , \beta }C\ket{ \gamma , \beta }$$
</div>
<br>
Then the maximum of $F_p(\gamma,\beta)$ is $M_p$:
<br>
<div>
   $$ M_p = max_{\gamma,\beta} F_p(\gamma,\beta) $$
</div>
<br>
They also show that the: 

<div>
    $$lim_{p->\infty}M_p = max_z C(z)$$
</div>
<br>

The above equation can be interpreted as if we were to use this approximate technique and do it infinite times then we would eventually reach the maximum state, This can be taken as an omen - We could say that this approximation is good enough for practical purposes. Also One observation to be noted here is that if p doesn't grow with n is then complexity is given by $O(m^2+mn)$ which means the complexity doesn't grow combinationally anymore. A simple grid search on $[0, 2\pi]^p x [0,\pi]^p$ would be enough.
<br>

Finally to extract the result from the obtained optimal $\gamma$ and $\beta$ is easy, we just have to know the corresponding bitstrings with highest probability which we get, it can then be used to get the grouping of vertices and logically the edges connecting opposites groups would be cut.    


<br>
This particular implementation has been adapted from the tutorial of Jack Ceroni on MaxCut for unwieghted graphs. ( <a href ="https://lucaman99.github.io/new_blog/2020/mar16.html">link to the tutorial </a>) 
