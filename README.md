# CS50 Ai Course

Welcome to my personal repository for the CS50 AI course! Here, I will maintain all my projects completed during the Harvard course.

This repository contains projects, exercises, and any additional materials related to the CS50 AI course. Feel free to explore the content and follow along with my progress as I work through the course materials.

**This is Project 5 - Traffic**

**Thank you for visiting! 🚀**

*The idea behing this project is to write an AI to identify which traffic sign appears in a photograph*

Example:

    $ python traffic.py gtsrb
    
    Epoch 1/10
    500/500 [==============================] - 5s 9ms/step - loss: 3.7139 - accuracy: 0.1545
    Epoch 2/10
    500/500 [==============================] - 6s 11ms/step - loss: 2.0086 - accuracy: 0.4082
    Epoch 3/10
    500/500 [==============================] - 6s 12ms/step - loss: 1.3055 - accuracy: 0.5917
    Epoch 4/10
    500/500 [==============================] - 5s 11ms/step - loss: 0.9181 - accuracy: 0.7171
    Epoch 5/10
    500/500 [==============================] - 7s 13ms/step - loss: 0.6560 - accuracy: 0.7974
    Epoch 6/10
    500/500 [==============================] - 9s 18ms/step - loss: 0.5078 - accuracy: 0.8470
    Epoch 7/10
    500/500 [==============================] - 9s 18ms/step - loss: 0.4216 - accuracy: 0.8754
    Epoch 8/10
    500/500 [==============================] - 10s 20ms/step - loss: 0.3526 - accuracy: 0.8946
    Epoch 9/10
    500/500 [==============================] - 10s 21ms/step - loss: 0.3016 - accuracy: 0.9086
    Epoch 10/10
    500/500 [==============================] - 10s 20ms/step - loss: 0.2497 - accuracy: 0.9256
    333/333 - 5s - loss: 0.1616 - accuracy: 0.9535

*The images are not uploaded*

*STEPS TAKEN TO ACCOMPLISH THE TASK*

**Step 1**

Here we replicated the implementation seen in the classes (Src code), adapting it to our own circumstance. Initially, we only used one hidden layer and no convolutional layers or pooling layers. The results were really poor, but at least it was working, and we had a baseline to improve from.

        --> Changes from the Src Code:
                We used "softmax" instead of "sigmoid" for the output layer as it suits better for multi-class classification.
                We added a flattening layer to convert the 3D input into a 1D input since the neural network expected 1D input for 
                dense layers.

**Step 2**

Based on the previous code, we added more hidden layers. Despite adding 3 more dense layers, the results were still really poor. This indicated the necessity to change our approach.

        --> Changes from the Previous Code:
                Added more hidden layers to increase model complexity.
                Changed the loss function to categorical_crossentropy as it is more appropriate for multi-class classification.

**Step 3**

As the results were really poor, we decided to switch from using "normal" neural networks to convolutional neural networks (CNNs), as we know CNNs are better suited for image classification tasks. The CNN model was designed with multiple convolutional layers, batch normalization, max-pooling, and dropout layers to enhance performance and prevent overfitting.

        --> Changes from the Previous Code:
            Introduced convolutional layers to extract spatial features.
            Added batch normalization to stabilize and speed up training.
            Added max-pooling layers to reduce the spatial dimensions and computational load.
            Implemented dropout layers to prevent overfitting.


By iteratively refining our approach and incorporating convolutional layers, batch normalization, max-pooling, and dropout layers, we have significantly improved the model's ability to classify traffic signs accurately. This method ensures the model is robust and capable of generalizing well to unseen data.
