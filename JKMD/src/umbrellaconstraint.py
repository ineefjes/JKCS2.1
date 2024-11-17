class UmbrellaConstraint:
    """Constrain an atom to move along a given direction only."""
    def __init__(self, a, k, splitpoint, r, adjuststeps = 0):
        self.a = a
        self.k = k*0.043364115308770496
        self.splitpoint = splitpoint
        self.r = r
        self.step = 0
        self.adjusthalf = 0
        self.adjuststeps = adjuststeps
        if self.adjuststeps > 0:
          self.k_to_be = self.k
          self.k = self.k_to_be * self.step / self.adjuststeps
    def adjust_positions(self, atoms, newpositions):
        pass
    def adjust_potential_energy(self, atoms):
        import numpy as np
        CS = atoms.constraints
        #print(CS)
        del atoms.constraints
        vec_COM = atoms[0:self.splitpoint].get_center_of_mass()-atoms[self.splitpoint:].get_center_of_mass()
        norm_vec_COM = vec_COM/np.sqrt(np.sum(vec_COM**2))
        bias_en = 0.5*self.k*(np.sqrt(np.sum(vec_COM**2))-self.r)**2
        #print(bias_en)
        atoms.set_constraint(CS)
        return bias_en
    def adjust_forces(self, atoms, forces):
        import numpy as np
        CS = atoms.constraints
        del atoms.constraints
        vec_COM = atoms[0:self.splitpoint].get_center_of_mass()-atoms[self.splitpoint:].get_center_of_mass()
        norm_vec_COM = vec_COM/np.sqrt(np.sum(vec_COM**2))
        adjustment = self.k*(-self.r*norm_vec_COM+vec_COM)
        #print(adjustment)
        #print(forces[0])
        #TODO make the forces applied as weighted distribution on atoms
        forces[0:self.splitpoint] -= np.array(atoms[0:self.splitpoint].get_masses())[:,np.newaxis]/np.sum(atoms[0:self.splitpoint].get_masses())*adjustment
        forces[self.splitpoint:] += np.array(atoms[self.splitpoint:].get_masses())[:,np.newaxis]/np.sum(atoms[self.splitpoint:].get_masses())*adjustment
        atoms.set_constraint(CS)
        #print(forces[0])
        #print("-----")
        if self.adjuststeps > self.step:
          if self.adjusthalf == 0:
            self.adjusthalf = 1 
          else:
            self.adjusthalf = 0
            self.step += 1
            self.k = self.k_to_be * self.step / self.adjuststeps
    def index_shuffle(self, atoms, ind):
        pass
