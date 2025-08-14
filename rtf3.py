import numpy as np

class Rotation3(object):
    def __init__(self):
        self.__quaternion = np.array([0.0, 0.0, 0.0, 1.0]) # x, y, z, w order. Ensure unit quaternion.

    @staticmethod
    def from_quaternion(q):
        r = Rotation3()
        r.__quaternion = q / np.linalg.norm(q)
        return r

    def to_quaternion(self):
        return self.__quaternion.copy()

    @staticmethod
    def from_rotation_matrix(m):
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

        r = Rotation3()
        r.__quaternion = q / np.linalg.norm(q)
        return r

    def to_rotation_matrix(self):
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

        r = Rotation3()
        r.__quaternion = q / np.linalg.norm(q)
        return r

    @staticmethod
    def from_euler_zyx_deg(z, y, x):
        return Rotation3.from_euler_zyx(z, y, x)

    def draw_pyplot(self, ax, size=1.0):
        m = self.to_rotation_matrix()
        ax.quiver(*np.zeros([3, 3]), *m, length=size, normalize=True, color=['r', 'g', 'b'])



class RTF3(object):
    def __init__(self):
        self.r = Rotation3()
        self.t = np.ones(3)
