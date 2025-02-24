import pandas as pd
import numpy as np
import os
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM, SpatialDropout1D
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


def fb_sentiment_score():
    current_directory = os.path.dirname(__file__)
    csv_file = 'fb_sentiment.csv'

    # Create the full path to the CSV file
    csv_file_path = os.path.join(current_directory, csv_file)
    fb = pd.read_csv(csv_file_path)
    fb.head()
    fb.columns = map(str.lower, fb.columns)
    fb.shape

    import re
    fb['fbpost'] = fb['fbpost'].apply(lambda x: x.lower())
    fb['fbpost'] = fb['fbpost'].apply(
        lambda x: re.sub(r'[^a-zA-Z0-9\s]', '', x)
    )
    fb = fb[fb.label != "O"]

    max_fatures = 2000
    tokenizer = Tokenizer(num_words=max_fatures, split=' ')
    tokenizer.fit_on_texts(fb['fbpost'].values)
    X = tokenizer.texts_to_sequences(fb['fbpost'].values)
    X = pad_sequences(X)

    fb.label.value_counts()

    Y = pd.get_dummies(fb['label']).values
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.33, random_state=42
    )
    print(X_train.shape, Y_train.shape)
    print(X_test.shape, Y_test.shape)

    embed_dim = 200
    lstm_out = 200

    model = Sequential()
    model.add(Embedding(max_fatures, embed_dim, input_length=X.shape[1]))
    model.add(SpatialDropout1D(0.4))
    model.add(LSTM(lstm_out, dropout=0.2, recurrent_dropout=0.2))
    model.add(Dense(2, activation='softmax'))
    model.compile(
        loss='categorical_crossentropy',
        optimizer='adam',
        metrics=['accuracy']
    )
    print(model.summary())

    batch_size = 32
    hist = model.fit(
        X_train, Y_train, epochs=7, batch_size=batch_size, verbose=2
    )
    model.save('./facebook_sentiment.h5')

    history = pd.DataFrame(hist.history)
    plt.figure(figsize=(7, 7))
    plt.plot(history["loss"])
    plt.plot(history["accuracy"])
    plt.title("Loss and accuracy of model")
    plt.show()

    # Testing the model, and retrieving score and accuracy:
    score, acc = model.evaluate(X_test, Y_test)
    print("score: %.2f" % (score))
    print("accuracy: %.2f" % (acc))

    validation_size = 1500
    X_validate = X_test[-validation_size:]
    Y_validate = Y_test[-validation_size:]
    x_test = X_test[:-validation_size]
    # y_test = Y_test[:-validation_size]

    pos_cnt, neg_cnt, pos_correct, neg_correct = 0, 0, 0, 0
    for x in range(len(X_validate)):
        result = model.predict(
            X_validate[x].reshape(1, x_test.shape[1]),
            verbose=2
        )[0]
        if np.argmax(result) == np.argmax(Y_validate[x]):
            if np.argmax(Y_validate[x]) == 0:
                neg_correct += 1
            else:
                pos_correct += 1
        if np.argmax(Y_validate[x]) == 0:
            neg_cnt += 1
        else:
            pos_cnt += 1

    neg_score = neg_correct / neg_cnt * 100
    pos_score = pos_correct / pos_cnt * 100
    comp_score = neg_score + pos_score
    print("positive_acc", pos_correct / pos_cnt * 100, "%")
    print("negative_acc", neg_correct / neg_cnt * 100, "%")
    sentiment_dict = {
        'neg': neg_score,
        'pos': pos_score,
        "neu": 4.00,
        "compound": comp_score
    }
    return sentiment_dict
