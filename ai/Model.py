from tensorflow.keras import layers as layer
from tensorflow.keras import Input as Input
from tensorflow.keras import Model as Model
from tensorflow.keras import optimizers as optimizer

def generate_model():
    main_input = Input(26)
    x = layer.layer.Dense(256,
                              activation='relu',
                              kernel_regularizer='l2')(main_input)

    policy_output = layer.Dense(25,
                                activation='softmax',
                                kernel_regularizer='l2',
                                name='policy_output')(x)
    head2 = layer.Dense(64,
                        activation='relu',
                        kernel_regularizer='l2')(x)
    value_output = layer.Dense(1,
                              activation='tanh',
                              kernel_regularizer='l2',
                              name='value_output')(head2)

    model = Model(inputs=main_input, outputs=[policy_output,value_output])

    losses = {
        "policy_output": "categorical_crossentropy",
        "value_output": "mean_squared_error"
        }

    opt = optimizer.SGD(lr=0.01, momentum=0.9)

    model.compile(optimizer=opt, loss=losses, metrics=['accuracy'])

    return model

