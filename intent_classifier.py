
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

training_sentences = [
    "how are you","what about you","how r u",
    "play despacito", "play some music", "can you play a song",
    "what time is it", "tell me the current time", "give me the time",
    "what's today date", "tell me today's date", "give me the date",
    "who is albert einstein", "tell me about newton", "who is bill gates",
    "exit", "quit the program", "close yourself",
    "set reminder for 5:00 p.m.", "remind me to call mom", "set a reminder"
]

training_labels = [
    "greet","greet","greet",
    "play_music", "play_music", "play_music",
    "get_time", "get_time", "get_time",
    "get_date", "get_date", "get_date",
    "ask_person", "ask_person", "ask_person",
    "exit", "exit", "exit",
    "set_reminder", "set_reminder", "set_reminder"
]

try:
    with open("new_data.txt", "r") as f:
        for line in f:
            sentence, label = line.strip().split("|||")
            training_sentences.append(sentence)
            training_labels.append(label)
except FileNotFoundError:
    pass
# === Vectorizer + Model ===
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(training_sentences)

model = LogisticRegression()
model.fit(X, training_labels)

# Save model + vectorizer
with open("intent_model.pkl", "wb") as f:
    pickle.dump((vectorizer, model), f)

print("Model trained and saved!")
