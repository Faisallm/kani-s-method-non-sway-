

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
        self._calculate_FEM(self._joints)
        self._calculate_RM(self._joints)

        # INITIALIZING BEAM/COLUMN RELATIVE STIFFNESS
        self._beam_relative_stiffness = {}
        self._column_relative_stiffness = {}
        self._relative_stiffness = {}

        # CALCULATING VALUES OF BEAM/COLUMN RELATIVE STIFFNESS
        self._calculate_beam_relative_stiffness(self._joints)
        self._calculate_column_relative_stiffness(self._frame)

        # INITIALIZATION OF ROTATION FACTOR DICT
        self._rotation_factor = {}

        # INITIALIZATION OF ROTATION CONTRIBUTIONS DICT
        self._rotation_contrib_alpha = {}
        self._sorted_rotation_contrib_alpha = {}

        # CALCULATING VALUES OF ROTATION FACTORS
        self._calculate_rotation_factor(self._relative_stiffness)

        # INITIALIZING RE-CALCULATED FEM
        self._fem = {}

        # CALCULATING ROTATIONAL CONTRIBUTIONS
        self._calc_rotation_contrib(self._sorted_rotation_contrib_alpha)



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

        # merge the two dictionaries together
        self._beam_relative_stiffness.update(self._column_relative_stiffness)
        self._calc_relative_stiffness(self._beam_relative_stiffness)

    def _calc_relative_stiffness(self, dic):

        for key in dic.keys():
            self._relative_stiffness[key] = dic[key]
            val = list(key[2:5])
            a, b = val
            a, b = b, a
            char = 'K_{}{}'.format(a, b)
            self._relative_stiffness[char] = dic[key]

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

    def _calculate_rotation_factor(self, dic2):

        for i in dic2:
            key = "R_{}".format(i[2:4])
            alpha = i[2]
            similar = [j for j in dic2 if j[2] == alpha]
            val = dic2[i]
            numerator = sum([dic2[i] for i in similar])
            cal = round((-0.5 * val)/numerator, 3)
            self._rotation_factor[key] = cal
        self._calc_rot_contrib_alpha(self._rotation_factor)

    def _calc_rot_contrib_alpha(self, dic):
        for key in dic:
            val = key[2:4]
            char = "M'_{}".format(val)
            char1 = "K_{}".format(val)
            if not self._relative_stiffness[char1] == (-dic[key]):
               self. _rotation_contrib_alpha[char] = 0
        li = []
        for i in self. _rotation_contrib_alpha:
            keys = [j for j in self._rotation_contrib_alpha if i[:4] in j]
            for key in keys:
                if not key in li:
                    li.append(key)
        for i in li:
            self._sorted_rotation_contrib_alpha[i] = 0

    def _calculate_Final_EM(self, li5):
        for i in self._fixed_end_moments:
            self._fem[i] = self._fixed_end_moments[i]
            val = list(i[3:5])
            a, b = val
            a, b = b, a
            char = 'MF_{}{}'.format(a, b)
            self._fem[char] = -self._fixed_end_moments[i]

        for i in li5:
            val = i[2:5]
            char = i[2]
            fm_value = "MF_{}".format(val)
            # print(rm_value)
            r = None
            if fm_value in self._fem:
                r = self._fem[fm_value]
                # print(r)
            else:
                r = 0
            a, b = list(val)
            a, b = b, a
            chars = "M'_{}{}".format(a, b)
            value = None
            if chars in self._sorted_rotation_contrib_alpha:
                value = self._sorted_rotation_contrib_alpha[chars]
            else:
                value = 0
            ad = "M'_{}".format(i[2:4])
            v = None
            if ad in self._sorted_rotation_contrib_alpha:
                v = self._sorted_rotation_contrib_alpha[ad]
            else:
                v = 0

            calc = r + (2 * v) + value
            print('--------------')
            print('M_{}:{} kN m'.format(val, round(calc, 3)))
            print('--------------')


    def _calc_rotation_contrib(self, dic):
        for z in range(4):
            for i in dic:
                key = i[3:5]
                r = None
                r_value = "R_{}".format(key)
                if r_value in self._rotation_factor:
                    r = r_value
                else:
                    x = [a for a in key]
                    a, b = x
                    a, b = b, a
                    c = a + b
                    mr = 'R_{}'.format(c)
                    r = mr

                rs_value = self._rotation_factor[r]

                # value or restraint moment
                key1 = i[3]
                rm_alpha = "M_{}".format(key1)
                rm_value = self._restraint_moments[rm_alpha]
                # value of far end
                key = i[3]

                li = [j for j in dic.keys() if j[4] == key]
                total = []
                for a in li:
                    total.append(dic[a])
                far_end = sum(total)
                rotation_contribution = rs_value * (rm_value + far_end)

                dic[i] = round(rotation_contribution, 2)
        self._calculate_Final_EM(self._rotation_factor)







if __name__ == '__main__':
    f = Kani()

