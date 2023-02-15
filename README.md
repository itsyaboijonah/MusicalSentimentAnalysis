# MusicalSentimentAnalysis

Music emotion classification via lyrical sentiment analysis

The objective of this project is to create a specialized system for lyric-based emotion classification, making use of the expansive body of research available in traditional sentiment analysis.

The first step is to replicate the results of a state-of-the-art sentiment classifier. An interesting starting point would be a CNN, since CNNs are good at extracting local and position-invariant features, like keywords and phrases to detect sentiment, and are straight-forward to use in transfer learning situations, which we will use. Moreover, new and old papers alike cite success at performing sentiment analysis using CNNs, some in a musical context. Features and datasets from these papers would be used as starting points to build our own model.

Once this base CNN model is performing adequately, the next step would be to create a transfer learning model targeted at lyrical content. The MoodyLyrics public dataset will be used for this purpose. It contains 2595 song lyrics annotated using valence and arousal values of words, classified into 4 possible moods. MoodyLyrics is a small dataset, so we would only train the final layers of the model, and keep all the other layers fixed. This way we avoid over-fitting, and preserve all of the high-level features learnt by the base model to classify sentiment in text. We would remove the final layers of the base model and add new layers, which we retrain with the lyric data.

Ideally, this model will benefit from the extra data, specially targeted to the task at hand, and perform with high accuracy. Other papers in sentiment classification transfer learning claim similar successes. Should time permit, ensembling this CNN with an LSTM would also be interesting. Finally, having a working transfer learning classifier, we can obtain a prediction for each line in the song lyrics. Each line would cast a vote, and the category with the most votes would be the final prediction for the song.
