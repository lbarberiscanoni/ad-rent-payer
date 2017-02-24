import markovify

# Get raw text as string.
with open("test2.txt") as f:
    text = f.read()
    text = str(text)

# Build the model.
text_model = markovify.Text(text)
print text_model

# Print five randomly-generated sentences
count = 0
listOfSentences = []
while count < 5:
    try:
        sentence = text_model.make_sentence()
    except Exception as e:
        print e
    if sentence != None:
        if sentence not in listOfSentences:
            print sentence
            listOfSentences.append(sentence)
            count += 1
