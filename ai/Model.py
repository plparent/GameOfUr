from tensorflow.keras import layers as layer
from tensorflow.keras import Input as Input
from tensorflow.keras import Model as Model
from tensorflow.keras import optimizers as optimizer

def generate_model():
    main_input = Input(shape=(3,8,3))
    x = layer.Conv2D(128,
                     2,
                     kernel_regularizer='l2')(main_input)
    x = layer.BatchNormalization()(x)
    x = layer.ReLU()(x)
    #x = layer.Add()([x, main_input])
    
    head1 = layer.Conv2D(2,
                         1,
                         kernel_regularizer='l2')(x)
    head1 = layer.BatchNormalization()(head1)
    head1 = layer.ReLU()(head1)
    head1 = layer.Flatten()(head1)
    policy_output = layer.Dense(25,
                                activation='softmax',
                                kernel_regularizer='l2',
                                name='policy_output')(head1)
    head2 = layer.Conv2D(1,
                         1,
                         kernel_regularizer='l2')(x)
    head2 = layer.BatchNormalization()(head2)
    head2 = layer.ReLU()(head2)
    head2 = layer.Flatten()(head2)
    head2 = layer.Dense(128,
                        activation='relu',
                        kernel_regularizer='l2')(head2)
    value_output = layer.Dense(1,
                              activation='tanh',
                              kernel_regularizer='l2',
                              name='value_output')(head2)

    model = Model(inputs=main_input, outputs=[policy_output,value_output])

    losses = {
        "policy_output": "categorical_crossentropy",
        "value_output": "mean_squared_error"
        }

    opt = optimizer.SGD(lr=0.001, momentum=0.9)

    model.compile(optimizer=opt, loss=losses, metrics=['accuracy'])

    return model

