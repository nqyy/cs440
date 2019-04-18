import numpy as np

"""
    Minigratch Gradient Descent Function to train model
    1. Format the data
    2. call four_nn function to obtain losses
    3. Return all the weights/biases and a list of losses at each epoch
    Args:
        epoch (int) - number of iterations to run through neural net
        w1, w2, w3, w4, b1, b2, b3, b4 (numpy arrays) - starting weights
        x_train (np array) - (n,d) numpy array where d=number of features
        y_train (np array) - (n,) all the labels corresponding to x_train
        num_classes (int) - number of classes (range of y_train)
        shuffle (bool) - shuffle data at each epoch if True. Turn this off for testing.
    Returns:
        w1, w2, w3, w4, b1, b2, b3, b4 (numpy arrays) - resulting weights
        losses (list of ints) - each index should correspond to epoch number
            Note that len(losses) == epoch
    Hints:
        Should work for any number of features and classes
        Good idea to print the epoch number at each iteration for sanity checks!
        (Stdout print will not affect autograder as long as runtime is within limits)
"""
def minibatch_gd(epoch, w1, w2, w3, w4, b1, b2, b3, b4, x_train, y_train, num_classes, shuffle=True):
    # w1: 764*256, w2: 256*256, w3: 256*256, w4: 256*10
    # b1: 256, b2: 256, b3: 256, b4: 10
    # x_train: 50000 * 784, y_train: 50000 (label)
    N = len(x_train) # data size
    n = 200 # batch size
    losses = [None] * epoch
    for e in range(epoch):
        loss = 0
        x_all = x_train.copy()
        y_all = y_train.copy()
        if shuffle:
            indices = np.random.choice(N, N, replace=False)
            x_all = x_train[indices]
            y_all = y_train[indices]
        for i in range(int(N/n)):
            X = x_all[i*n:i*n+n]
            y = y_all[i*n:i*n+n]
            loss += four_nn(w1, w2, w3, w4, b1, b2, b3, b4, X, y, num_classes, False)
        losses[e] = loss
        print("epoch: ", e)
        print("loss: ", loss)
    
    return w1, w2, w3, w4, b1, b2, b3, b4, losses

"""
    Use the trained weights & biases to see how well the nn performs
        on the test data
    Args:
        All the weights/biases from minibatch_gd()
        x_test (np array) - (n', d) numpy array
        y_test (np array) - (n',) all the labels corresponding to x_test
        num_classes (int) - number of classes (range of y_test)
    Returns:
        avg_class_rate (float) - average classification rate
        class_rate_per_class (list of floats) - Classification Rate per class
            (index corresponding to class number)
    Hints:
        Good place to show your confusion matrix as well.
        The confusion matrix won't be autograded but necessary in report.
"""
def test_nn(w1, w2, w3, w4, b1, b2, b3, b4, x_test, y_test, num_classes):
    classifications = four_nn(w1, w2, w3, w4, b1, b2, b3, b4, x_test, y_test, num_classes, test=True)
    avg_class_rate = np.sum(classifications == y_test) / len(x_test)
    class_rate_per_class = [0.0] * num_classes
    for i in range(num_classes):
        class_i = np.argwhere(y_test == i)
        class_rate_per_class[i] = np.sum(classifications[class_i] == i) / len(class_i)

    return avg_class_rate, class_rate_per_class

"""
    4 Layer Neural Network
    Helper function for minibatch_gd
    Up to you on how to implement this, won't be unit tested
    Should call helper functions below
"""
def four_nn(w1, w2, w3, w4, b1, b2, b3, b4, x_test, y_test, num_classes, test):
    z1, acache1 = affine_forward(x_test, w1, b1)
    a1, rcache1 = relu_forward(z1)
    z2, acache2 = affine_forward(a1, w2, b2)
    a2, rcache2 = relu_forward(z2)
    z3, acache3 = affine_forward(a2, w2, b2)
    a3, rcache3 = relu_forward(z3)
    F, acache4 = affine_forward(a3, w4, b4)

    if test == True:
        classifications = np.argmax(F, axis=1)
        return classifications

    loss, dF = cross_entropy(F, y_test)
    dA3, dW4, db4 = affine_backward(dF, acache4)
    dZ3 = relu_backward(dA3, rcache3)
    dA2, dW3, db3 = affine_backward(dZ3, acache3)
    dZ2 = relu_backward(dA2, rcache2)
    dA1, dW2, db2 = affine_backward(dZ2, acache2)
    dZ1 = relu_backward(dA1, rcache1)
    dX, dW1, db1 = affine_backward(dZ1, acache1)
    
    w1 -= 0.1 * dW1
    w2 -= 0.1 * dW2
    w3 -= 0.1 * dW3
    w4 -= 0.1 * dW4
    b1 -= 0.1 * db1
    b2 -= 0.1 * db2
    b3 -= 0.1 * db3
    b4 -= 0.1 * db4

    return loss
"""
    Next five functions will be used in four_nn() as helper functions.
    All these functions will be autograded, and a unit test script is provided as unit_test.py.
    The cache object format is up to you, we will only autograde the computed matrices.

    Args and Return values are specified in the MP docs
    Hint: Utilize numpy as much as possible for max efficiency.
        This is a great time to review on your linear algebra as well.
"""
def affine_forward(A, W, b):
    Z = np.matmul(np.column_stack((A, np.ones(len(A)))), np.vstack((W, b)))
    cache = (A, W, b)
    return Z, cache

def affine_backward(dZ, cache):
    A, W, b = cache
    dA = np.matmul(dZ, W.T)
    dW = np.matmul(A.T, dZ)
    db = np.sum(dZ, axis=0)
    return dA, dW, db

def relu_forward(Z):
    A = Z.copy()
    A[A < 0] = 0
    cache = Z
    return A, cache

def relu_backward(dA, cache):
    Z = cache
    dA = np.where(Z > 0, dA, 0)
    return dA

def cross_entropy(F, y):
    n = len(F)
    Fiyi = F[np.arange(n), y.astype(int)]
    log_stuff = np.log(np.sum(np.exp(F), axis=1))
    loss = (-1 / n) * np.sum(Fiyi - log_stuff)

    first_item = np.zeros(F.shape)
    first_item[np.arange(n), y.astype(int)] = 1
    second_item = np.exp(F) / np.sum(np.exp(F), axis=1).reshape((-1, 1))
    dF = (-1 / n) * (first_item - second_item)

    return loss, dF
