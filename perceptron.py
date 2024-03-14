import numpy as np

class Perceptron:
    def __init__(self, num_inputs, learning_rate=0.01, epochs=100):
        self.num_inputs = num_inputs
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.weights = np.random.rand(num_inputs + 1)  # Add one for the bias term
       
    def predict(self, inputs):
        summation = np.dot(inputs, self.weights[1:]) + self.weights[0]  # Dot product of inputs and weights + bias
        return 1 if summation > 0 else 0  # Step function
    
    def train(self, training_inputs, labels):
        for _ in range(self.epochs):
            for inputs, label in zip(training_inputs, labels):
                prediction = self.predict(inputs)
                self.weights[1:] += self.learning_rate * (label - prediction) * inputs
                self.weights[0] += self.learning_rate * (label - prediction)  # Update bias term
       
    def print_weights(self):
        print("Weights:", self.weights)


# Example usage
if __name__ == "__main__":
    # Training data (inputs)
    training_inputs = np.array([
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1]
    ])

    # Corresponding labels
    labels = np.array([0, 0, 0, 1])

    # Create a perceptron with 2 inputs
    perceptron = Perceptron(num_inputs=2)

    # Train the perceptron
    perceptron.train(training_inputs, labels)

    # Print the final weights
    perceptron.print_weights()

    # Test the perceptron
    test_inputs = np.array([
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1]
    ])
    for inputs in test_inputs:
        prediction = perceptron.predict(inputs)
        print("Inputs:", inputs, "Prediction:", prediction)
