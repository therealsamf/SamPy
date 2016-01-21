

class Render():
    def __init__(self, value):
        self._left = None
        self._right = None
        self._value = value

    @property
    def Left(self):
        return self._left
    @property
    def Right(self):        
        return self._right
    @Left.setter
    def Left(self, value):
        if not isinstance(value, RenderTree) and not value == None:
            raise ValueError
        self._left = value

    @Right.setter
    def Right(self, value):
        if not isinstance(value, RenderTree) and not value == None:
            raise ValueError        
        self._right = value

    @property
    def Value(self):
        return self._value

    def __lt__(self, other):
        return self.Value < other.Value
    def __gt__(self, other):
        return self.Value > other.Value
    def __eq__(self, other):
        if other == None:
            return False
        return self.Value == other.Value
    def __str__(self):
        return "Render[" + str(self.Value) + "]"

class RenderTree():
    def __init__(self, render = None):
        self._node = render
        self._height = 0 #?
        self._balance = 0

    def Insert(self, render):
        if self.Node == None:
            self.Node = render
        elif render < self.Node:
            if self.Node.Left == None:
                self.Node.Left = RenderTree(render)
            else:
                self.Node.Left.Insert(render)

        elif render > self.Node:
            if self.Node.Right == None:
                self.Node.Right = RenderTree(render)
            else:
                self.Node.Right.Insert(render)
        else: #render == self.Node
            """Either we've got a render with exactly the same dimensions
            within the exact same layer and in the exact same spot
            Usually this would be an animation"""
            self.Node = render

        self.Rebalance()
        
    def Rebalance(self):
        self.UpdateHeight(recursive = False)
        self.UpdateBalances(False)

        while self.Balance < -1 or self.Balance > 1:
            #Leftsubtree is larger than right subtree
            if self.Balance > 1:
                if self.Node.Left and self.Node.Left.Balance < 0:
                    self.Node.Left.RotateLeft()
                    self.UpdateHeight()
                    self.UpdateBalances()
                self.RotateRight()
                self.UpdateHeight()
                self.UpdateBalances()
            if self.Balance < -1:
                if self.Node.Right and self.Node.Right.Balance > 0:
                    self.Node.Right.RotateRight()
                    self.UpdateHeight()
                    self.UpdateBalances()
                self.RotateLeft()
                self.UpdateHeight()
                self.UpdateBalances()

    def RotateLeft(self):
        new_root = None
        new_root_sub = None
        if self.Node:
            new_root = self.Node.Right
        if new_root and new_root.Node.Left:
            new_root_sub = new_root.Node.Left
        old_root = self.Node

        self.Node = new_root.Node
        old_root.Right = new_root_sub

        new_root.Node.Left = RenderTree(old_root)
    

    def RotateRight(self):
        """Hopefully this only gets called if there are three nodes to 
be rotated"""
        new_root = None
        new_root_sub = None
        if self.Node:
            new_root = self.Node.Left
        if new_root and new_root.Node.Right:
            new_root_sub = new_root.Node.Right
        old_root = self.Node

        self.Node = new_root.Node
        old_root.Left = new_root_sub
        new_root.Node.Right = RenderTree(old_root)

    def UpdateHeight(self, recursive = True):
        if self.Node != None:
            if recursive:
                if self.Node.Left != None:
                    self.Node.Left.UpdateHeight()
                if self.Node.Right != None:
                    self.Node.Right.UpdateHeight()
            rightHeight = -1
            leftHeight = -1
            if self.Node.Right:
                rightHeight = self.Node.Right.Height
            if self.Node.Left:
                leftHeight = self.Node.Left.Height
            self._height = 1 + max(rightHeight, leftHeight)
        else:
            self._height = -1

    def UpdateBalances(self, recursive = True):
        """
Calculate Tree Balance Factor:

the balance factor is calculated as follows:
balance = height(left subtree) - height(rightsubtree)
"""
        if self.Node:
            if recursive:
                if self.Node.Left:
                    self.Node.Left.UpdateBalances()
                if self.Node.Right:
                    self.Node.Right.UpdateBalances()
            rightHeight = -1
            leftHeight = -1
            if self.Node.Right:
                rightHeight = self.Node.Right.Height
            if self.Node.Left:
                leftHeight = self.Node.Left.Height
            self._balance = leftHeight - rightHeight
        else:
            self._balance = 0
                

    @property
    def Height(self):
        return self._height
    @property
    def Balance(self):
        return self._balance

    @property
    def Node(self):
        return self._node

    @Node.setter
    def Node(self, value):
        if not isinstance(value, Render):
            raise ValueError
        """This method is not to be used outside of the class"""
        self._node = value


    def ToList(self):
        result = []
        if self.Node:
            if self.Node.Left:
                result.extend(self.Node.Left.ToList())
            result.append(self.Node)
            if self.Node.Right:
                result.extend(self.Node.Right.ToList())
        return result
                

                
def main():
    global r
    r = RenderTree()
    r.Insert(Render(1))
    printTree()
    r.Insert(Render(3))
    printTree()
    r.Insert(Render(2))
    printTree()
    r.Insert(Render(4))
    printTree()
    r.Insert(Render(5))
    printTree()
    """
    r.Insert(Render(6))
    printTree()
"""

def printTree():
    print("************************")
    for item in r:
        print(str(item))
    print("&&&&&&&&&&&&&&&&&&&&&&&&")

main()
