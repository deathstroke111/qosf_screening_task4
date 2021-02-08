from qiskit import *
from qiskit.tools.visualization import plot_histogram
from matplotlib import pyplot as plt
import networkx as nx
import random
from scipy.optimize import minimize
print("imports successful")

class MaxCut():
    def __init__(self, edge_list, num, shots = 512, depth = 1,):
        self.edge_list = edge_list
        self.num = num
        self.shots = shots
        self.depth = depth
        self.backend = Aer.get_backend('qasm_simulator')
        
    def initialize(self,qc):
        for q in range(qc.num_qubits):
            qc.h(q)
    

    def cost_unitary(self, qc, gamma):
        for i in self.edge_list:
            qc.cu1(-2*gamma*i.weight, i.start_node, i.end_node)
            qc.u1(gamma*i.weight, i.start_node)
            qc.u1(gamma*i.weight, i.end_node)


    def mixer_unitary(self, qc, beta):
        for i in range(qc.num_qubits):
            qc.rx(2*beta, i)

    def create_circuit(self, params):
        #The gamma and beta are designed to support the depth till 4
        gamma = [params[0], params[2], params[4], params[6]]
        beta = [params[1], params[3], params[5], params[7]]
        qc = QuantumCircuit(self.num)
        self.initialize(qc)
        qc.barrier()
        for i in range(0, self.depth):
            self.cost_unitary(qc, gamma[i])
            qc.barrier()
            self.mixer_unitary(qc, beta[i])
        qc.measure_all()
        results = execute(qc,backend=self.backend,shots=self.shots).result()
        return results.get_counts()

    def cost_function(self, params):

        qubit_count = self.create_circuit(params)
        print("qubit count :: ",qubit_count)
        bit_strings = list(qubit_count.keys())
        total_cost = 0
        for bit_string in bit_strings:
            each_bs_cost = 0
            bit_string_encoding = bit_string[::-1]
            for j in self.edge_list:
                #multiplying the whole equation by -1 so that later minize function from scipy can be used to optimize
                each_bs_cost += -1*0.5* j.weight *( 1 -( (1 - 2*int(bit_string_encoding[j.start_node])) * (1 - 2*int(bit_string_encoding[j.end_node])) ))
            #print("bit string freq :: ", qubit_count.get(bit_string))
            total_cost += each_bs_cost*qubit_count.get(bit_string)
        print("Cost: "+str(-1*total_cost/self.shots))
        return total_cost
    
    def visualize(self, f):
        # Creates visualization of the optimal state
        #curently here
        nums = []
        freq = []
        for k,v in f.items():
            number = 0
            #print("key :: ",k, " values :: ",v)
            for j in range(0, len(k)):
                number += 2**(len(k)-j-1)*int(k[j])
            if (number in nums):
                freq[nums.index(number)] = freq[nums.index(number)] + v
            else:
                nums.append(number)
                freq.append(v)
        freq = [s/sum(freq) for s in freq]
        #print(nums)
        #print(freq)
        x = range(0, 2**self.num)
        y = []
        for i in range(0, len(x)):
            if (i in nums):
                y.append(freq[nums.index(i)])
            else:
                y.append(0)
        plt.bar(x, y)
        plt.show()
        
    def do_max_cut(self, max_iter=1000):
        # Defines the optimization method
        init =[float(random.randint(-314, 314))/float(100) for i in range(0, 8)]
        out = minimize(self.cost_function, x0=init, method="COBYLA", options={'maxiter':max_iter})
        print(out)
        optimal_params = out['x']
        f = self.create_circuit(optimal_params)
        #print(f)
        self.visualize(f)
        return