from itertools import chain
import nltk
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelBinarizer
import sklearn
import pycrfsuite

class crfsute_train():
    def __init__(self):
        self.trainer = pycrfsuite.Trainer(verbose=False)

    def word2features(self, sent, i):
        feature = sent[i][0]
        features = [str(key+'='+feature[key]) for key in feature]
        if i > 0:
            feature1 = sent[i-1][0]
            features.extend([str('-1'+key+'='+feature1[key]) for key in feature1])
        else:
            features.append('BOS')

        if i < len(sent)-1:
            feature1 = sent[i+1][0]
            features.extend([str('+1'+key+'='+feature1[key]) for key in feature1])
        else:
            features.append('EOS')
        return features


    def sent2features(self, sent):
        return [self.word2features(sent, i) for i in range(len(sent))]

    def sent2labels(self, sent):
        return [label for token, label in sent]

    def sent2tokens(self, sent):
        return [token for token, label in sent]

    def train(self, train_data, train_label):
        for xseq, yseq in zip(train_data, train_label):
            self.trainer.append(xseq, yseq)
        self.trainer.set_params({
            'c1': 1.0,   # coefficient for L1 penalty
            'c2': 1e-3,  # coefficient for L2 penalty
            'max_iterations': 50,  # stop earlier

            # include transitions that are possible, but not observed
            'feature.possible_transitions': True
        })
        self.trainer.params()
        self.trainer.train('test.crfsuite')

    def test(self, feature):
        tagger = pycrfsuite.Tagger()
        tagger.open('test.crfsuite')
        return tagger.tag(feature)

    def predict_prob(self, tags):
        tagger = pycrfsuite.Tagger()
        tagger.open('test.crfsuite')
        return tagger.probability(tags)



