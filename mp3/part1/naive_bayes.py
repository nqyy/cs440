import numpy as np

class NaiveBayes(object):
	def __init__(self,num_class,feature_dim,num_value):
		"""Initialize a naive bayes model. 

		This function will initialize prior and likelihood, where 
		prior is P(class) with a dimension of (# of class,)
			that estimates the empirical frequencies of different classes in the training set.
		likelihood is P(F_i = f | class) with a dimension of 
			(# of features/pixels per image, # of possible values per pixel, # of class),
			that computes the probability of every pixel location i being value f for every class label.  

		Args:
			num_class(int): number of classes to classify (10)
			feature_dim(int): feature dimension for each example (784)
			num_value(int): number of possible values for each pixel (256)
		"""

		self.num_value = num_value
		self.num_class = num_class
		self.feature_dim = feature_dim

		self.prior = np.zeros((num_class)) # (10)
		self.likelihood = np.zeros((feature_dim,num_value,num_class)) # (784, 256, 10)

	def train(self,train_set,train_label):
		""" Train naive bayes model (self.prior and self.likelihood) with training dataset. 
			self.prior(numpy.ndarray): training set class prior (in log) with a dimension of (# of class,),
			self.likelihood(numpy.ndarray): traing set likelihood (in log) with a dimension of 
				(# of features/pixels per image, # of possible values per pixel, # of class).
			You should apply Laplace smoothing to compute the likelihood. 

		Args:
			train_set(numpy.ndarray): training examples with a dimension of (# of examples, feature_dim) (50000*784)
			train_label(numpy.ndarray): training labels with a dimension of (# of examples, ) (50000)
		"""
		# YOUR CODE HERE
		# prior
		for item in train_label:
			self.prior[item] += 1

		# sorted by class & transposed: 784 * 5000
		train_set_sorted = train_set[np.argsort(train_label), :].transpose()
		counter = 0
		for i in range(self.num_class):
			for pixel in range(self.feature_dim):
				val, count = np.unique(train_set_sorted[pixel][int(counter): int(counter + self.prior[i])], return_counts=True)
				self.likelihood[pixel, val, i] = count
			counter += self.prior[i]

		k = 1
		for i in range(self.num_class):
			self.likelihood[:,:,i] = (self.likelihood[:,:,i] + k) / (self.prior[i] + self.num_value * k)
		
		self.likelihood = np.log(self.likelihood)
		self.prior = np.log(self.prior / len(train_set))

	def test(self,test_set,test_label):
		""" Test the trained naive bayes model (self.prior and self.likelihood) on testing dataset,
			by performing maximum a posteriori (MAP) classification.  
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
		# likelihood: 784 * 256 * 10
		accuracy = 0
		pred_label = np.zeros((len(test_set)))

		for i in range(len(test_set)): # for each test
			posterior_probability = np.zeros((self.num_class)) # 10
			for j in range(self.num_class): # 10
				posterior_probability[j] = self.prior[j]
				selected_list = self.likelihood[np.arange(self.feature_dim), test_set[i], j]
				posterior_probability[j] += np.sum(selected_list)
			pred_label[i] = np.argmax(posterior_probability)

		accuracy = (len(test_set) - np.count_nonzero(pred_label - test_label)) / len(test_set)
		return accuracy, pred_label


	def save_model(self, prior, likelihood):
		""" Save the trained model parameters 
		"""    

		np.save(prior, self.prior)
		np.save(likelihood, self.likelihood)

	def load_model(self, prior, likelihood):
		""" Load the trained model parameters 
		""" 

		self.prior = np.load(prior)
		self.likelihood = np.load(likelihood)

	def intensity_feature_likelihoods(self, likelihood):
		"""
		Get the feature likelihoods for high intensity pixels for each of the classes,
			by sum the probabilities of the top 128 intensities at each pixel location,
			sum k<-128:255 P(F_i = k | c).
			This helps generate visualization of trained likelihood images. 
		
		Args:
			likelihood(numpy.ndarray): likelihood (in log) with a dimension of
				(# of features/pixels per image, # of possible values per pixel, # of class)
		Returns:
			feature_likelihoods(numpy.ndarray): feature likelihoods for each class with a dimension of
				(# of features/pixels per image, # of class)
		"""
		# YOUR CODE HERE
		return np.sum(np.exp(likelihood[:,128:,:]), axis=1)
