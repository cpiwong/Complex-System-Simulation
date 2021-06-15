class CircularGrid:

    def __init__(self, NUM_OF_RINGS, CELLS_PER_RING):
        
        self.NUM_OF_RINGS = NUM_OF_RINGS        # total amount of rings in the plot
        self.CELLS_PER_RING = CELLS_PER_RING    # amount of cell for each ring, x cells are added for each ring

        self.rings = []

        # create rings
        for i in range(self.NUM_OF_RINGS):
            new_ring = Ring(i, self)
            self.rings.append(new_ring)

    def get_ring(self, ring_id):
        """ Returns a ring object for a given ring id"""
        return self.rings[ring_id]

    def get_cell(self, ring_id, cell_id):
        """ Returns a cell object for a given ring and cell id"""
        ring = self.rings[ring_id]
        max_value = ring.num_of_children
        return ring.children[cell_id % max_value]

    def get_neighbours(self, cell):
        """ Returns a list of cell objects which are neighbours of the given input cell"""
        # find cell in the ring below with overlapping theta

        neighbours = []

        # find neighbours in lower ring
        if cell.parent.id > 0:
            for i in range(cell.id - self.CELLS_PER_RING, cell.id + 1):
                guess = self.get_cell(cell.parent.id - 1, i)
                if (guess.theta1 <= cell.theta1 and guess.theta2 > cell.theta1) or (guess.theta1 > cell.theta1 and guess.theta1 < cell.theta2):
                    neighbours.append(guess)

        # add left and right neighbour
        neighbours.append(self.get_cell(cell.parent.id, cell.id - 1))
        neighbours.append(self.get_cell(cell.parent.id, cell.id + 1))

        # find neighbours in upper ring
        if cell.parent.id + 1 < self.NUM_OF_RINGS:
            for i in range(cell.id, cell.id + 1 + self.CELLS_PER_RING):
                guess = self.get_cell(cell.parent.id + 1, i)
                if (guess.theta1 <= cell.theta1 and guess.theta2 > cell.theta1) or (guess.theta1 > cell.theta1 and guess.theta1 < cell.theta2):
                    neighbours.append(guess)
        return neighbours

class Ring:

    def __init__(self, ring_id, parent):
        self.id = ring_id
        self.parent = parent
        self.children = []
        self.num_of_children = (ring_id + 1) * self.parent.CELLS_PER_RING
        self.offset = 0

        for i in range(self.num_of_children):
            new_cell = Cell(self, i)
            self.children.append(new_cell)
        
    def __repr__(self):
        return "<Ring id:%s>" % (self.id)

class Cell:

    def __init__(self, parent_ring, cell_id, age=0):

        self.parent = parent_ring
        self.id = cell_id
        self.age = age

        self.level = (self.parent.id + 1)
        delta = 2 * np.pi / (self.level * self.parent.parent.CELLS_PER_RING)
        self.theta1 = self.id * delta
        self.theta2 = self.theta1 + delta
    
    def __repr__(self):
        return "<Cell id:%s parent_ring:%s>" % (self.id, self.parent.id)
