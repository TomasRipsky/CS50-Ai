-----Steps Taken to Accomplish the Task-----

--Step 1--
Here we replicated the implementation seen in the classes (Src code), adapting it to our own circumstance. Initially, we only used one hidden layer and no convolutional layers or pooling layers. The results were really poor, but at least it was working, and we had a baseline to improve from.

--> Changes from the Src Code:
        We used "softmax" instead of "sigmoid" for the output layer as it suits better for multi-class classification.
        We added a flattening layer to convert the 3D input into a 1D input since the neural network expected 1D input for dense layers.

--Step 2--
Based on the previous code, we added more hidden layers. Despite adding 3 more dense layers, the results were still really poor. This indicated the necessity to change our approach.

--> Changes from the Previous Code:
        Added more hidden layers to increase model complexity.
        Changed the loss function to categorical_crossentropy as it is more appropriate for multi-class classification.

--Step 3--
As the results were really poor, we decided to switch from using "normal" neural networks to convolutional neural networks (CNNs), as we know CNNs are better suited for image classification tasks. The CNN model was designed with multiple convolutional layers, batch normalization, max-pooling, and dropout layers to enhance performance and prevent overfitting.

--> Changes from the Previous Code:
    Introduced convolutional layers to extract spatial features.
    Added batch normalization to stabilize and speed up training.
    Added max-pooling layers to reduce the spatial dimensions and computational load.
    Implemented dropout layers to prevent overfitting.


By iteratively refining our approach and incorporating convolutional layers, batch normalization, max-pooling, and dropout layers, we have significantly improved the model's ability to classify traffic signs accurately. This method ensures the model is robust and capable of generalizing well to unseen data.