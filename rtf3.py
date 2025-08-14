import numpy as np

class Rotation(object):
    def __init__(self):
        self.__quaternion = np.array([0.0, 0.0, 0.0, 1.0]) # x, y, z, w order. Ensure unit quaternion.

    @staticmethod
    def from_quaternion(q):
        """
        Create a Rotation3 object from a quaternion.
        :param q: Array-like containing [x, y, z, w].
        :return: Rotation object.
        """
        r = Rotation()
        r.__quaternion = q / np.linalg.norm(q)
        return r

    def to_quaternion(self):
        """
        Convert the Rotation3 object into a quaternion.
        :return: np array containing [x, y, z, w].
        """
        return self.__quaternion.copy()

    @staticmethod
    def from_rotation_matrix(m):
        """
        Create a Rotation3 object from a rotation matrix.
        :param m: 3D rotation matrix.
        :return: Rotation object.
        """
        tr = m[0, 0] + m[1, 1] + m[2, 2]
        if tr > 0:
            s = np.sqrt(tr+1.0) * 2
            qw = 0.25 * s
            qx = (m[2, 1] - m[1, 2]) / s
            qy = (m[0, 2] - m[2, 0]) / s
            qz = (m[1, 0] - m[0, 1]) / s
        elif (m[0, 0] > m[1, 1]) and (m[0, 0] > m[2, 2]):
            s = np.sqrt(1.0 + m[0, 0] - m[1, 1] - m[2, 2]) * 2
            qw = (m[2, 1] - m[1, 2]) / s
            qx = 0.25 * s
            qy = (m[0, 1] + m[1, 0]) / s
            qz = (m[0, 2] + m[2, 0]) / s
        elif m[1, 1] > m[2, 2]:
            s = np.sqrt(1.0 + m[1, 1] - m[0, 0] - m[2, 2]) * 2
            qw = (m[0, 2] - m[2, 0]) / s
            qx = (m[0, 1] + m[1, 0]) / s
            qy = 0.25 * s
            qz = (m[1, 2] + m[2, 1]) / s
        else:
            s = np.sqrt(1.0 + m[2, 2] - m[0, 0] - m[1, 1]) * 2
            qw = (m[1, 0] - m[0, 1]) / s
            qx = (m[0, 2] + m[2, 0]) / s
            qy = (m[1, 2] + m[2, 1]) / s
            qz = 0.25 * s
        q = [qx, qy, qz, qw]

        r = Rotation()
        r.__quaternion = q / np.linalg.norm(q)
        return r

    def to_rotation_matrix(self):
        """
        Convert the Rotation3 object into a rotation matrix.
        :return: 3*3 np array containing 3D rotation matrix.
        """
        m = np.eye(3)
        x = self.__quaternion[0]
        y = self.__quaternion[1]
        z = self.__quaternion[2]
        w = self.__quaternion[3]
        xx = x * x
        xy = x * y
        xz = x * z
        xw = x * w
        yy = y * y
        yz = y * z
        yw = y * w
        zz = z * z
        zw = z * w
        m[0, 0] = 1 - 2 * (yy + zz)
        m[0, 1] = 2 * (xy - zw)
        m[0, 2] = 2 * (xz + yw)
        m[1, 0] = 2 * (xy + zw)
        m[1, 1] = 1 - 2 * (xx + zz)
        m[1, 2] = 2 * (yz - xw)
        m[2, 0] = 2 * (xz - yw)
        m[2, 1] = 2 * (yz + xw)
        m[2, 2] = 1 - 2 * (xx + yy)
        return m

    @staticmethod
    def from_euler_zyx(z, y, x):
        """
        Create a Rotation3 object from a rotation matrix and an euler angles. It's a consecutive Z, Y, Z rotation along the body frame.
        :param z: Z rotation in radians.
        :param y: Y rotation in radians.
        :param x: X rotation in radians.
        :return: Rotation object.
        """
        c1 = np.cos(y / 2)
        s1 = np.sin(y / 2)
        c2 = np.cos(z / 2)
        s2 = np.sin(z / 2)
        c3 = np.cos(x / 2)
        s3 = np.sin(x / 2)
        c1c2 = c1 * c2
        s1s2 = s1 * s2
        qw = c1c2 * c3 - s1s2 * s3
        qx = c1c2 * s3 + s1s2 * c3
        qy = s1 * c2 * c3 + c1 * s2 * s3
        qz = c1 * s2 * c3 - s1 * c2 * s3
        q = [qx, qy, qz, qw]

        r = Rotation()
        r.__quaternion = q / np.linalg.norm(q)
        return r

    @staticmethod
    def from_euler_zyx_deg(z, y, x):
        """
        Create a Rotation3 object from a rotation matrix and an euler angles. It's a consecutive Z, Y, Z rotation along the body frame.
        :param z: Z rotation in degrees.
        :param y: Y rotation in degrees.
        :param x: X rotation in degrees.
        :return: Rotation object.
        """
        return Rotation.from_euler_zyx(np.deg2rad(z), np.deg2rad(y), np.deg2rad(x))

    def draw_pyplot(self, ax, size=1.0):
        """
        Draw a pyplot plot of the Rotation3 object.
        :param ax: Pyplot axes.
        :param size: Axis arrow size.
        """
        m = self.to_rotation_matrix()
        ax.quiver(*np.zeros([3, 3]), *m, length=size, normalize=True, color=['r', 'g', 'b'])

class Transform(object):
    def __init__(self):
        self.r = Rotation()
        self.t = np.ones(3)
