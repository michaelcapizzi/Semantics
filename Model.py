import numpy as np

#class for a model
#TODO allow for uncertainty in calculations (i.e., not 1,0 and 0,1 for truth

class Model:

        #listOfElements = ["john", "chris", "tom"]
        #dictionaryOfUnaryPredicates = {"is_mathematician": ["john", "chris"]}
    def __init__(self, listOfElements, dictionaryOfUnaryPredicates = {}):
        #domain
        self.elements = listOfElements
        self.elementLookUp = {}
        self.sizeOfDomain = len(self.elements)
        #unary predicates
        self.unaryPredicateLookUp = dictionaryOfUnaryPredicates
        self.domainMatrix = np.zeros((self.sizeOfDomain, self.sizeOfDomain))        #each row is a one-hot
        #truth conditions
        self.unaryPredicateMatrices = {}
        self.isTrue = np.array([1, 0]).reshape((2,1))
        self.isFalse = np.array([0, 1]).reshape((2,1))
        #connectives
        self.negConnect = np.array([
                                [0,1],
                                [1,0]
                            ])
        self.orConnect = np.array([                         #first row is first rank from left to right, top to bottom
                                    [1,1,0,0],
                                    [1,0,0,1]
                                ]).reshape((2,2,2))
        self.andConnect = np.array([
                                    [1,0,0,1],              #first row is first rank from left to right, top to bottom
                                    [0,0,1,1]
                                ]).reshape((2,2,2))
        self.conditionalConnect = np.array([                #first row is first rank from left to right, top to bottom
                                            [1,0,0,1],
                                            [1,1,0,0]
                                        ]).reshape((2,2,2))

######################################################

#building the model

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


######################################################

#modifying the world

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
                self.addToPredicate(tupleToAdd[0], item)
                self.unaryPredicateLookUp[item].append(tupleToAdd[0])


    #remove from domain
    #TODO build



    #add an element to predicate matrix
    def addToPredicate(self, element, predicate):
        self.unaryPredicateMatrices[predicate][:,self.elementLookUp[element]] = self.isTrue.T


    #remove an element from a predicate matrix
    def removeFromPredicate(self, element, predicate):
        self.unaryPredicateMatrices[predicate][:,self.elementLookUp[element]] = self.isFalse.T

######################################################

#accessing the items in the world

    #get one hot vector
    def getOneHot(self, element):
        return self.domainMatrix[:,self.elementLookUp[element]].reshape(self.sizeOfDomain, 1)


######################################################

#determining truth

    def calculateTruthValue(self, elem1, elem2):
        return np.tensordot(elem1, elem2, axes=1)
        # predicate ==> (self.unaryPredicateMatrices[elem1], self.getOneHot(elem2))
        # negation ==> (self.neg, self.isTrue / self.isFalse)
        #TODO figure out other connectives