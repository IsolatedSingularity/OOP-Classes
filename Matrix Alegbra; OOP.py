#%% Importing Modules
from tabulate import tabulate

#Defining matrix algebra
class Matrix():
    
    def __init__(self, matrix: list):
        self.matrix = matrix
        self.num_rows = len(matrix)
        self.num_columns = len(matrix[0])
    
    def __str__(self):
        return tabulate(self.matrix)
    
    #Identity of group
    def create_identity(self):
        
        result =  [[0 for i in range(self.num_rows)] for j in range(self.num_rows)]
        for i in range(0, self.num_rows):
            result[i][i] = 1
        return Matrix(result)  
  
    #Multiplicative action
    def multiplication(self, other):
        
        #Note: the naming convention for the for loop variables are based on the dimensions of the matrices:
        #C = A*B, where dimA = i x k, dimB = k x j, and henceforth dimC = i x j
        newRows=[] #rows of the new matrix C produced by multiplication of A & B
        for i in range(self.num_rows): #iterating through rows of A
            currentRow=[] #rows of currently iterated matrix elements
            for j in range(other.num_columns): #iterating through columns of B
                currentEntry=0 #setting the default entries of C to be zero 
                for k in range(other.num_rows): #iterating through rows of B
                    currentEntry += self.matrix[i][k]*other.matrix[k][j] #matrix product of current column of A (column vector), and current row of B (row vector)
                currentRow.append(currentEntry) #appending the value of the matrix product to the current entry value (default set to 0)
            newRows.append((currentRow)) #appending the entry values to their corresponding rows of C           #REMOVE TUPLE PART????
        return Matrix((newRows)) #returning the matrix C (under the Matrix class)

    #Combining matrices and vectors
    def stacking(self, other):
       
        #C = [A|B], dimA = dimB = i x i, dimC = i x 2i
        newMatrix=[] #rows of the stacked matrix
        for i in range(self.num_rows): #iterating through the rows of matrix A
                newMatrix.append(self.matrix[i]+other.matrix[i]) #appending the concatenated rows of A and B
        return Matrix(newMatrix) #returning the matrix C

    #Splitting matrices and vectors
    def un_stacking(self): #G.un_stacking()
        
        newMatrix=[] #unstacked matrix, this will be the inverted matrix of A in the stacked matrix C = [I|A^{-1}]
        for i in range(self.num_rows): #iterating through rows of A
            currentMatrix=[] #rows of currently iterated matrix elements
            for j in range(int(len(self.matrix[0])/2),len(self.matrix[0])): #selecting the matrix elements of the stacked matrix C, that only correspond to the matrix on the right (A^{-1})
                currentMatrix.append(self.matrix[i][j]) #appending the values to the row list currentMatrix
            newMatrix.append((currentMatrix)) #appending the row segments to the full matrix newMatrix
        return Matrix(newMatrix) #returning the inverse of A, or more generally, the matrix on the right of the stacked matrix C                
    
    #Method of reducing system of equations to identity and solved parameters
    def gauss_jordan(self):
              
        a = [row[:] for row in self.matrix]
        for i in range(self.num_rows):
            if a[i][i] == 0.0:
                sys.exit('Divide by zero detected!')  
            for j in range(self.num_rows):
                if i != j:
                    ratio = a[j][i]/a[i][i]
                    for k in range(self.num_columns):
                        a[j][k] = a[j][k] - ratio * a[i][k] 

        newMatrix=[] #the stacked matrix when fully row reduced (i.e. [A|I] ~ [I|A^{-1}])
        for i in range(self.num_rows): #iterating through rows of A
            currentMatrix=[] #rows of currently iterated matrix elements
            for j in range(self.num_rows): #iterating through rows on the left block matrix of 'a' (the stacked matrix [I|A^{-1}])
                currentMatrix.append(a[i][j]) #appending row values to currentMatrix
            for k in range(self.num_rows,2*self.num_rows): #iterating through rows on the right block matrix of 'a' (the stacked matrix [I|A^{-1}])
                currentMatrix.append(a[i][k]/a[i][i]) #appending row values to currentMatrix [I|A^{-1}]
            newMatrix.append((currentMatrix)) #appending the row segments to the full matrix newMatrix
        return Matrix(newMatrix) #returning the row reduced gauss jordan stacked matrix 
    #Remark: notice how I seperated the appending for the final gauss jordan reduced matrix. This is because
    #as you'll see in the examples below, the left matrix isn't put in a normalized RREF form, but in a
    #similar form to RREF where the rows aren't divided by the coefficients of the leading terms. This 
    #doesn't change our final answer (the inverse), but should be notated as it isn't standard convention
                  
    #Inverse element of group
    def inverse(self):
        '''Returns a Matrix object representing the inverse of self.matrix
        '''
        identityMatrix = self.create_identity() #computing the identity matrix as the same size as the input matrix A
        augmentedMatrix = self.stacking(identityMatrix) #stacking A w/ I, i.e A -> [A|I]
        solvedMatrix = augmentedMatrix.gauss_jordan() #performing gauss jordan reduction to get [I|A^{-1}]
        isolatedInverse = solvedMatrix.un_stacking() #isolating the inverse A^{-1} from the stacked matrix

        return isolatedInverse #returning the inverse of the input matrix A
    
    #System of equations
    def linear_equations(self, X):
        return Matrix(multiplication(inverse(self.Matrix), X)) 

    #Testing code
    def my_test():
        matrix1 = [[12,7,3], [4 ,5,6], [7 ,8,9]] 
        matrix2 = [[5,8,1], [6,7,3], [4,5,9]]
        obj1 = Matrix(matrix1)
        obj2 = Matrix(matrix2)
        print(obj1.multiplication(obj2))
        
