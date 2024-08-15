import sys
import os
import pickle

class Parser:
    def __init__(self, load=False):
        if load:
            self.load()
        else:
            self.weights = {}  # Initialisiere dein Modell hier

    def train(self, train_data, nr_iter=15):
        # Deine Trainingslogik hier
        pass

    def save(self, model_dir):
        with open(os.path.join(model_dir, 'parser_model.pkl'), 'wb') as f:
            pickle.dump(self.weights, f)

    def load(self):
        with open('parser_model.pkl', 'rb') as f:
            self.weights = pickle.load(f)

    def parse(self, sentence):
        # Deine Parsing-Logik hier
        return [], []  # Platzhalter für Tags und Heads

def read_conll(file_path):
    """
    Liest CoNLL-U formatierte Datei und gibt Sätze als Listen von Wörtern, Tags, Kopf-IDs und Labels zurück.
    """
    with open(file_path, encoding="utf-8") as file:
        content = file.read()
    
    for sent_str in content.strip().split('\n\n'):
        lines = [line.split('\t') for line in sent_str.split('\n') if line]
        words = []    # Liste der Wörter
        tags = []     # Liste der POS-Tags
        heads = []    # Liste der Kopf-IDs
        labels = []   # Liste der Abhängigkeitsbeziehungen
        
        for line in lines:
            if len(line) < 10:  # Überprüfen, ob die Zeile genug Spalten hat
                continue
            word = line[1]
            pos = line[3]
            head_str = line[6]
            label = line[7]
            
            words.append(word)
            tags.append(pos)
            
            if head_str == '_':
                head = -1
            else:
                try:
                    head = int(head_str) - 1
                except ValueError:
                    head = -1
            
            heads.append(head)
            labels.append(label)
        
        for i in range(len(heads)):
            if heads[i] == 0:
                heads[i] = -1
        
        yield words, tags, heads, labels

def main_train(model_dir, train_file):
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    
    train_data = read_conll(train_file)
    train_data = list(train_data)
    parser = Parser(load=False)
    parser.train(train_data, nr_iter=15)
    parser.save(model_dir)
    print(f"Model trained and saved to {model_dir}")

def main_test(model_dir, test_file):
    parser = Parser(load=True)
    test_data = read_conll(test_file)
    test_data = list(test_data)
    # Deine Testlogik hier
    print(f"Testing completed with model in {model_dir}")

def main_parse(model_dir):
    parser = Parser(load=True)
    sentence = sys.stdin.read().strip()
    words = sentence.split()
    tags, heads = parser.parse(words)
    print("Tags:", tags)
    print("Heads:", heads)

def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("python3 parser.py train MODEL_DIR TRAIN_DATA")
        print("python3 parser.py test MODEL_DIR TEST_DATA")
        print("python3 parser.py parse MODEL_DIR < tokenized_sentences.txt")
    #    sys.exit(1)

    mode = sys.argv[1]
    
    if mode == 'train':
        if len(sys.argv) != 4:
            print("Usage: python3 parser.py train MODEL_DIR TRAIN_DATA")
            sys.exit(1)
        model_dir = sys.argv[2]
        train_file = sys.argv[3]
        main_train(model_dir, train_file)
        
    elif mode == 'test':
        if len(sys.argv) != 4:
            print("Usage: python3 parser.py test MODEL_DIR TEST_DATA")
            sys.exit(1)
        model_dir = sys.argv[2]
        test_file = sys.argv[3]
        main_test(model_dir, test_file)
        
    elif mode == 'parse':
        if len(sys.argv) != 3:
            print("Usage: python3 parser.py parse MODEL_DIR < tokenized_sentences.txt")
            sys.exit(1)
        model_dir = sys.argv[2]
        main_parse(model_dir)
    
    else:
        print("Invalid mode. Use 'train', 'test', or 'parse'.")
        sys.exit(1)

if __name__ == '__main__':
    main()
