import numpy as np

class MultiClassPerceptron(object):
	def __init__(self,num_class,feature_dim):
		"""Initialize a multi class perceptron model. 

		This function will initialize a feature_dim weight vector,
		for each class. 

		The LAST index of feature_dim is assumed to be the bias term,
			self.w[:,0] = [w1,w2,w3...,BIAS] 
			where wi corresponds to each feature dimension,
			0 corresponds to class 0.  

		Args:
			num_class(int): number of classes to classify
			feature_dim(int): feature dimension for each example 
		"""

		self.w = np.zeros((feature_dim + 1, num_class)) # 784 * 10

	def train(self,train_set,train_label):
		""" Train perceptron model (self.w) with training dataset. 

		Args:
			train_set(numpy.ndarray): training examples with a dimension of (# of examples, feature_dim)
			train_label(numpy.ndarray): training labels with a dimension of (# of examples, )
		"""
		iteration = 30
		bias = np.hstack((train_set, np.ones((len(train_set), 1))))
		for _ in range(iteration):
			for j in range(len(bias)):
				f =  bias[j]
				predicted_result = np.argmax(np.dot(self.w.transpose(), f))
				if predicted_result != train_label[j]:
					learning_rate = 1 / (j+1)
					self.w[:,train_label[j]] += learning_rate * f
					self.w[:,predicted_result] -= learning_rate * f

	def test(self,test_set,test_label):
		""" Test the trained perceptron model (self.w) using testing dataset. 
			The accuracy is computed as the average of correctness 
			by comparing between predicted label and true label. 
			
		Args:
			test_set(numpy.ndarray): testing examples with a dimension of (# of examples, feature_dim)
			test_label(numpy.ndarray): testing labels with a dimension of (# of examples, )

		Returns:
			accuracy(float): average accuracy value 
			pred_label(numpy.ndarray): predicted labels with a dimension of (# of examples, )
		"""    

		# YOUR CODE HERE
		bias = np.hstack((test_set, np.ones((len(test_set), 1))))
		pred_label = np.argmax(np.matmul(bias, self.w), axis=1)
		accuracy = (len(test_set) - np.count_nonzero(pred_label - test_label)) / len(test_set)
		print("perceptron accuracy:", accuracy)
		return accuracy, pred_label

	def save_model(self, weight_file):
		""" Save the trained model parameters 
		""" 

		np.save(weight_file,self.w)

	def load_model(self, weight_file):
		""" Load the trained model parameters 
		""" 

		self.w = np.load(weight_file)

