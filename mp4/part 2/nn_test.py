import unittest
import numpy as np
import numpy.testing as npt
from neural_network import *

class TestNeuralNetwork(unittest.TestCase):

    def parse_row(self, f):
        row = f.readline().strip().split(' ')
        row = [float(x) for x in row]
        return row

    def test_affine(self):
        with open('tests/check_affine.txt', 'r') as f:
            f.readline()
            A = []
            for i in range(10):
                A.append(self.parse_row(f))
            A = np.array(A)

            f.readline()
            f.readline()
            W = []
            for i in range(8):
                W.append(self.parse_row(f))
            W = np.array(W)

            f.readline()
            f.readline()
            b = np.array(self.parse_row(f))

            f.readline()
            f.readline()
            Z = []
            for i in range(10):
                Z.append(self.parse_row(f))
            Z = np.array(Z)

            f.readline()
            f.readline()
            dZ = []
            for i in range(10):
                dZ.append(self.parse_row(f))
            dZ = np.array(dZ)

            f.readline()
            f.readline()
            dA = []
            for i in range(10):
                dA.append(self.parse_row(f))
            dA = np.array(dA)

            f.readline()
            f.readline()
            dW = []
            for i in range(8):
                dW.append(self.parse_row(f))
            dW = np.array(dW)

            f.readline()
            f.readline()
            db = np.array(self.parse_row(f))

            test_Z, cache = affine_forward(A, W, b)
            test_dA, test_dW, test_db = affine_backward(dZ, cache)

            npt.assert_allclose(test_Z, Z)
            npt.assert_allclose(test_dA, dA)
            npt.assert_allclose(test_dW, dW)
            npt.assert_allclose(test_db, db)

    def test_relu(self):
        with open('tests/check_relu.txt', 'r') as f:
            f.readline()
            Z = []
            for i in range(10):
                Z.append(self.parse_row(f))
            Z = np.array(Z)

            f.readline()
            f.readline()
            A = []
            for i in range(10):
                A.append(self.parse_row(f))
            A = np.array(A)

            f.readline()
            f.readline()
            dA = []
            for i in range(10):
                dA.append(self.parse_row(f))
            dA = np.array(dA)

            f.readline()
            f.readline()
            dZ = []
            for i in range(10):
                dZ.append(self.parse_row(f))
            dZ = np.array(dZ)

            test_A, cache = relu_forward(Z)
            test_dZ = relu_backward(dA, cache)

            npt.assert_allclose(A, test_A)
            npt.assert_allclose(dZ, test_dZ)

    def test_crossentropy(self):
        with open('tests/check_cross_entropy.txt', 'r') as f:
            f.readline()
            F = []
            for i in range(10):
                F.append(self.parse_row(f))
            F = np.array(F)

            f.readline()
            f.readline()
            y = np.array(self.parse_row(f))

            f.readline()
            loss = float(f.readline().strip().split(' ')[1])

            f.readline()
            f.readline()
            dF = []
            for i in range(10):
                dF.append(self.parse_row(f))
            dF = np.array(dF)

            test_loss, test_dF = cross_entropy(F, y)
            npt.assert_allclose(test_loss, loss)
            npt.assert_allclose(test_dF, dF)

    def init_weights(self, d, dp):
        return 0.1 * np.random.uniform(0.0, 1.0, (d, dp)), np.zeros(dp)

    def test_minibatch_gradient(self):
        np.random.seed(seed=57)
        w1, b1 = self.init_weights(5, 64)
        w2, b2 = self.init_weights(64, 64)
        w3, b3 = self.init_weights(64, 64)
        w4, b4 = self.init_weights(64, 3)

        with open('tests/expert_policy.txt', 'r') as f:
            data = []
            for line in f:
                row = line.strip().split(' ')
                data.append([float(x) for x in row])

        data = np.array(data)

        x_train = data[:3000, :5]
        y_train = data[:3000, 5]

        w1, w2, w3, w4, b1, b2, b3, b4, losses = minibatch_gd(10, w1, w2, w3, w4, b1, b2, b3, b4, x_train, y_train, 3, False)
        real_losses = [16.47908832639923, 16.47890904710272, 16.478763562070586, 16.47862850676294, 16.47849924186475, 16.478372234884887, 16.478245914771097, 16.478119929957426, 16.477994155766012, 16.477868479188555]
        npt.assert_allclose(losses, real_losses)


if __name__ == '__main__':
    unittest.main()
