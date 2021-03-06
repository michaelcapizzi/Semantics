import numpy as np
import itertools

#class for a logic model
#TODO allow for loading predicates with uncertainty in calculations (i.e., not 1,0 and 0,1 for truth)
#TODO update with outer product (see Grefenstette)

class LogicModel:
    """
    creates a model that utilizes tensor-based application of first-order logic
    :param listOfElements = ["john", "chris", "tom"]
    :param dictionaryOfUnaryPredicates = {"is_mathematician": ["john", "chris"]}
    :param dictionaryOfBinaryPredicates = {"loves": [("john", "john"), ("chris", "john)]}
    """

    def __init__(self, listOfElements, dictionaryOfUnaryPredicates = {}, dictionaryOfBinaryPredicates = {}):
        #domain
        self.elements = listOfElements
        self.elementLookUp = {}
        self.sizeOfDomain = len(self.elements)
        self.domainMatrix = np.zeros((self.sizeOfDomain, self.sizeOfDomain))        #each row is a one-hot
        #unary predicates
        self.unaryPredicateLookUp = dictionaryOfUnaryPredicates
        self.unaryPredicateMatrices = {}
        #binary predicates
        self.binaryPredicateLookUp = dictionaryOfBinaryPredicates
        self.binaryPredicateTensors = {}
        #truth conditions
        self.isTrue = np.array([1., 0.]).reshape((2,1))
        self.isFalse = np.array([0., 1.]).reshape((2,1))
        #connectives
        self.negConnect = np.array([
                                [0.,1.],
                                [1.,0.]
                            ])
        self.orConnect = np.array([                         #first row is first rank from left to right, top to bottom
                                    [1.,1.,0.,0.],
                                    [1.,0.,0.,1.]
                                ]).reshape((2,2,2))
        self.andConnect = np.array([
                                    [1.,0.,0.,1.],              #first row is first rank from left to right, top to bottom
                                    [0.,0.,1.,1.]
                                ]).reshape((2,2,2))
        self.conditionalConnect = np.array([                #first row is first rank from left to right, top to bottom
                                            [1.,0.,0.,1.],
                                            [1.,1.,0.,0.]
                                        ]).reshape((2,2,2))

######################################################

#building the model

    #build entire model
    def buildAll(self):

        self.buildDomain()
        self.buildUnaryPredicates()
        self.buildBinaryPredicates()

    #build domain and lookup dictionary
    def buildDomain(self):
        for elem in range(self.sizeOfDomain):
            #add to lookup dictionary
            self.elementLookUp[self.elements[elem]] = elem
            #build one-hot vector
            # oneHot = np.zeros((self.sizeOfDomain, 1))
            oneHot = np.zeros(self.sizeOfDomain)
            oneHot[elem] = 1
            #add one-hot to domain matrix
            self.domainMatrix[:,elem] = oneHot


    #build unary predicates
    def buildUnaryPredicates(self):
        for pred in self.unaryPredicateLookUp.keys():
            #build predicate matrix
            predMatrix = np.zeros((2, self.sizeOfDomain))
            for elem in self.elements:
                if elem in self.unaryPredicateLookUp[pred]:      #if the predicate applies to the element
                    predMatrix[:,self.elementLookUp[elem]] = self.isTrue.T
                else:                                           #if the predicate does not apply to element
                    predMatrix[:,self.elementLookUp[elem]] = self.isFalse.T
            self.unaryPredicateMatrices[pred] = predMatrix


    def buildBinaryPredicates(self):
        for pred in self.binaryPredicateLookUp.keys():
            #build predicate tensor
            predTensor = np.zeros((2, self.sizeOfDomain, self.sizeOfDomain))
            #get cartesian product
            cartProd = list(itertools.product(*[self.elements for i in [1,2]]))
            for pair in cartProd:
                if pair in self.binaryPredicateLookUp[pred]:    #if the predicate applies to the ordered pair
                    #fill in true side of tensor (dim = 0) with a 1
                        #[0][obj][subj] = 1
                    predTensor[0][self.elementLookUp[pair[1]]][self.elementLookUp[pair[0]]] = 1
                    #false side of tensor (dim =1 ) will remain a 0
                else:                                           #if the predicate doesn't apply to ordered pair
                    #true size of tensor (dim = 0) will remain a 0
                    #fill in false side of tensor (dim = 1) with a 1
                    predTensor[1][self.elementLookUp[pair[1]]][self.elementLookUp[pair[0]]] = 1
            self.binaryPredicateTensors[pred] = predTensor

######################################################

#modifying the world
#TODO update to handle binary predicates!

    #TODO update to handle added elements in binary predicates
    #add an element to domain and necessary predicates
        #tupleToAdd => (element, [listOfPredicates])
    def addToDomain(self, tupleToAdd):
    #domain
        #add to self.listOfElements
        self.elements.append(tupleToAdd[0])
        #update size of domain
        self.sizeOfDomain += 1
        #add to self.domainDictionary
        self.elementLookUp[tupleToAdd[0]] = self.sizeOfDomain - 1
        #add to self.domainMatrix
        self.domainMatrix = np.insert(self.domainMatrix, self.domainMatrix.shape[1], 0, 1)      #add a column of zeros
        self.domainMatrix = np.insert(self.domainMatrix, self.domainMatrix.shape[0], 0, 0)      #add a row of zeros
        self.domainMatrix[self.domainMatrix.shape[0] - 1][self.domainMatrix.shape[1] - 1] = 1         #update one-hot vector

    #predicates
        #build column in all predicates
        for pred in self.unaryPredicateMatrices.keys():
            self.unaryPredicateMatrices[pred] = np.insert(self.unaryPredicateMatrices[pred], self.unaryPredicateMatrices[pred].shape[1], 0, 1)

        #adds element to appropriate predicates in unaryPredicateMatrices and unaryPredicateLookUp
        if len(tupleToAdd[1]) != 0:
            for item in tupleToAdd[1]:
                self.updateUnaryPredicate(tupleToAdd[0], item)
                self.unaryPredicateLookUp[item].append(tupleToAdd[0])


    #remove from domain
    #TODO build


    #add unary predicate
    def addUnaryPredicate(self, predicate, listOfElements):
        #build predicate matrix
        predMatrix = np.zeros((2, self.sizeOfDomain))
        for elem in listOfElements:
            predMatrix[:,self.elementLookUp[elem]] = self.isTrue.T
        #add matrix
        self.unaryPredicateMatrices[predicate] = predMatrix
        #add to lookup
        self.unaryPredicateLookUp[predicate] = listOfElements


    #add binary predicate
    def addBinaryPredicate(self, predicate, listOfTuples):
        #build predicate tensor
        predTensor = np.zeros((2, self.sizeOfDomain, self.sizeOfDomain))
        #get cartesian product
        cartProd = list(itertools.product(*[self.elements for i in [1,2]]))
        for pair in cartProd:
            if pair in listOfTuples:    #if the predicate applies to the ordered pair
                #fill in true side of tensor (dim = 0) with a 1
                #[0][obj][subj] = 1
                predTensor[0][self.elementLookUp[pair[1]]][self.elementLookUp[pair[0]]] = 1
                #false side of tensor (dim =1 ) will remain a 0
            else:                                           #if the predicate doesn't apply to ordered pair
                #true size of tensor (dim = 0) will remain a 0
                #fill in false side of tensor (dim = 1) with a 1
                predTensor[1][self.elementLookUp[pair[1]]][self.elementLookUp[pair[0]]] = 1
        #add tensor
        self.binaryPredicateTensors[predicate] = predTensor
        #add to lookup
        self.binaryPredicateLookUp[predicate] = listOfTuples


    #add an element to predicate matrix
        #prob = probability that element IS predicate
    def updateUnaryPredicate(self, element, predicate, prob=1):
        if prob == 0:
            self.removeUnaryPredicate(element, predicate)
        else:
            self.unaryPredicateMatrices[predicate][:,self.elementLookUp[element]] = np.array([prob, 1 - prob])


    #add an element to predicate tensor
        #prob = probability that element IS predicate
    def updateBinaryPredicate(self, pair, predicate, prob=1):
        if prob == 0:
            self.removeBinaryPredicate(pair, predicate)
        else:
            self.binaryPredicateTensors[predicate][0][self.elementLookUp[pair[1]]][self.elementLookUp[pair[0]]] = prob
            self.binaryPredicateTensors[predicate][1][self.elementLookUp[pair[1]]][self.elementLookUp[pair[0]]] = 1 - prob



    #remove an element from unary predicate matrix
    def removeUnaryPredicate(self, element, predicate):
        #update in matrix
        self.unaryPredicateMatrices[predicate][:,self.elementLookUp[element]] = self.isFalse.T
        #update in lookup
        # self.unaryPredicateLookUp[predicate] = self.unaryPredicateLookUp[predicate].remove(element)
        self.unaryPredicateLookUp[predicate].remove(element)


    #TODO test removal maintains truth
    def removeBinaryPredicate(self, pair, predicate):
        #build temporary tensor
        updatedTensor = self.binaryPredicateTensors[predicate]

        #update temporary tensor
        updatedTensor[0][self.elementLookUp[pair[1]]][self.elementLookUp[pair[0]]] = 0
        updatedTensor[1][self.elementLookUp[pair[1]]][self.elementLookUp[pair[0]]] = 1

        #reassign as permanent tensor
        self.binaryPredicateTensors[predicate] = updatedTensor

        #update in lookup
        self.binaryPredicateLookUp[predicate].remove(pair)

######################################################

#accessing the items in the world

    #get one hot vector
    def getOneHot(self, element):
        return self.domainMatrix[:,self.elementLookUp[element]].reshape(self.sizeOfDomain, 1)

    #get a predicate
    def getUnaryPredicate(self, predicate):
        return self.unaryPredicateMatrices[predicate]

    def getBinaryPredicate(self, predicate):
        return self.binaryPredicateTensors[predicate]

######################################################

#determining truth
    def unaryOp(self, predicate, element):
        return np.tensordot (
                                self.getUnaryPredicate(predicate),
                                self.getOneHot(element),
                            axes=1)

    def binaryOp(self, predicate, subjElement, objElement):
        return np.tensordot (
                                np.tensordot    (
                                                    self.getBinaryPredicate(predicate),
                                                    self.getOneHot(subjElement),
                                                axes=1).reshape((2, len(self.elementLookUp.keys()))),      #reshape to 2,sizeOfDomain
                                self.getOneHot(objElement),
                            axes=1)

    def negOp(self, truthValue):
        return np.tensordot (
                                self.negConnect,
                                truthValue,
                            axes=1).reshape((2,1))

    def andOp(self, truthValue1, truthValue2):
        return np.tensordot (
                                np.tensordot    (
                                                    self.andConnect,
                                                    truthValue1,
                                                axes=1).reshape((2,2)).T,
                                truthValue2,
                            axes=1)

    def orOp(self, truthValue1, truthValue2):
        return np.tensordot (
                                np.tensordot    (
                                                    self.orConnect,
                                                    truthValue1,
                                                axes=1).reshape((2,2)).T,
                                truthValue2,
                            axes=1)

    def conditionalOp(self, truthValue1, truthValue2):
        return np.tensordot (
                                np.tensordot    (
                                                    self.conditionalConnect,
                                                    truthValue2,                #the consequent
                                                axes=1).reshape((2,2)).T,
                                truthValue1,                                    #the antecedent
                            axes=1)
