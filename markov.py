import markovify

# Get raw text as string.
with open("test.txt") as f:
    text = f.read()
    text = str(text)

# Build the model.
text_model = markovify.Text(text)
print text_model

# Print five randomly-generated sentences
count = 0
while count < 5:
    try:
        sentence = text_model.make_sentence()
    except Exception as e:
        print e
    if sentence != None:
        print sentence
        count += 1
