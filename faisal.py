

class Kani(object):


    def __init__(self):
        """Initialization."""

        fl = int(input('How many floors are in the frame:(enter a number): '))
        self._floors = fl
        jn = int(input('How many joints per floor?:(enter a number): '))
        self._num_of_joints = jn
        self._beams = int(self._num_of_joints - 1)
        self._columns = self._floors * self._num_of_joints
        self._frame = []
        self._joints = None

        # ALPHABETICAL REPRESENTATIONS OF JOINTS AND BASE FOR
        # EASY IDENTIFICATION
        self._get_joints()
        self._get_base()

        # INITIALIZING FIXED END MOMENTS AND RESTRAINT MOMENTS
        self._fixed_end_moments = {}
        self._restraint_moments = {}

        # CALCULATE VALUES OF FEM
        #self._calculate_FEM(self._joints)
        #self._calculate_RM(self._joints)

        # INITIALIZING BEAM/COLUMN RELATIVE STIFFNESS
        self._beam_relative_stiffness = {}
        self._column_relative_stiffness = {}

        # CALCULATING VALUES OF BEAM/COLUMN RELATIVE STIFFNESS
        self._calculate_beam_relative_stiffness(self._joints)
        self._calculate_column_relative_stiffness(self._frame)

    def _get_joints(self):
        for i in range(self._floors):
            list = []
            for j in range(self._num_of_joints):
                alphabet = 'What value represents the joint {0} of the {1}st floor:'.format(j+1, i+1)
                value = str(input('{}:'.format(alphabet)))
                list.append(value)
            self._frame.append(list)
        self._joints = self._frame[0:2]
        # ---> [[G,H,I], [D,E,F]]

    def _get_base(self):
        list = []
        for base in range(self._num_of_joints):
            alphabet = 'What is the value of the base {}:'.format(base + 1)
            value = str(input('{}:'.format(alphabet)))
            list.append(value)
        self._frame.append(list)
        # ---> [A, B, C]

    def _calculate_FEM(self, joints):
        for i in joints:
            for j in range(len(i)-1):
                name = 'MF_{}{}'.format(i[j], i[j+1])
                load = input('Enter the value of load across member {}{}: '.format(i[j], i[j+1]))
                length = input('Enter the value of length between member {}{}: '.format(i[j], i[j + 1]))
                FEM = (int(load) * (int(length)**2))/12
                self._fixed_end_moments[name] = FEM

    def _calculate_beam_relative_stiffness(self, joints):
        for i in joints:
            for j in range(len(i)-1):
                name = 'K_{}{}'.format(i[j], i[j+1])
                I = float(input('Enter the value of I across member {}{}: '.format(i[j], i[j+1])))
                L = float(input('Enter the value of length between member {}{}: '.format(i[j], i[j + 1])))
                RS = I/L
                value = "{:.3f}".format(RS)
                self._beam_relative_stiffness[name] = float(value)

    def _calculate_column_relative_stiffness(self, frames):
        for i in range(len(frames) - 1):
            for j in range(len(frames[i])):
                name = "K_{}{}".format(frames[i][j], frames[i + 1][j])
                I = float(input('Enter the value of I across member {}{}: '.format(frames[i][j], frames[i + 1][j])))
                L = float(input('Enter the value of length between member {}{}: '.format(frames[i][j], frames[i + 1][j])))
                RS = I/L
                value = "{:.3f}".format(RS)
                self._column_relative_stiffness[name] = float(value)

    def _calculate_RM(self, joints):
        for i in joints:
            for j in range(len(i)-1):
                name1 = 'M_{}'.format(i[j])
                name2 = 'M_{}'.format(i[j+1])
                load = input('Enter the value of load across member {}{}: '.format(i[j], i[j+1]))
                length = input('Enter the value of length between member {}{}: '.format(i[j], i[j + 1]))
                FEM1 = (int(load) * (int(length)**2))/12
                FEM2 = -(FEM1)

                if not name1 in self._restraint_moments.keys():
                    self._restraint_moments[name1] = FEM1
                else:
                    self._restraint_moments[name1] += FEM1

                if not name2 in self._restraint_moments.keys():
                    self._restraint_moments[name2] = FEM2
                else:
                    self._restraint_moments[name2] += FEM2



b = Kani()
# print(b._frame)
print(b._beam_relative_stiffness)
print(b._column_relative_stiffness)
