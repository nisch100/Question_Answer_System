
# coding: utf-8

# In[1]:


import spacy
import nltk
import random
import operator
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

with open('Questions.txt') as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
questions = [x.strip() for x in content] 

with open('Answers.txt') as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
answers = [x.strip() for x in content if x != ''] 

ct = 1
answer_store = {}
for i in answers:
    answer_store[ct] = i
    ct +=1

#randques = random.choice(questions)
pick_question = input("Please pick me number between 0 and " + str(len(questions)-1)+'(inclusive): ')
randques = questions[int(pick_question)]
print("The question you want answered is %r" %(randques))

cumilative_list = []
quantity = ['How much']
time = ['When']
place = ['Where is']
task = ['How to','How do', 'How can']
definition = ['What']
person = ['Who']
cumilative_list.extend(quantity+time+place+task+definition+person)
nlp = spacy.load("en_core_web_sm")
doc = nlp(randques)

def helper(answers,types,found):
    for i in answers:
            if found == 'yes':
                break
            doc = nlp(i)
            for ent in doc.ents:
                if ent.label_ == types:
                    print("Answer Found: ",i)
                    found = 'yes'
                    break
    if found == 'no':
        return 'no'
    else:
        return 'yes'
prev = ""
found = 'no'
lt = randques.split()
for token in lt:
    #print(doc)
    #print(token)
    if found == 'yes':
        #print("Entered")
        break
    bigram =  str(prev + ' ' + token)
   # print(bigram.strip())
    if token.strip() in person or bigram.strip() in person :
        found = helper(answers,'PERSON',found)
        print("The value of found is ", found)
    elif token.strip() in time or bigram.strip() in time:
        found = helper(answers,'DATE',found)
    elif token.strip() in definition or bigram.strip() in definition:
        found = helper(answers,'PRODUCT',found)
    elif token.strip() in place or bigram.strip() in place:
        found = helper(answers,'GPE',found)
   # print("Quantity is ", quantity[0])
   # print('Bigram is ', bigram)
    elif token.strip() in quantity or bigram.strip() in quantity :
        print("Got in buddy")
        found = helper(answers,'MONEY',found)
    
    prev = token
    if found == 'yes':
        break

if found == 'no':
        print("Answer Not found using spacy approach")
        x = input("Would you like to try the dictionary approach? ")
        if x.lower() == 'yes':
            stop_words = set(stopwords.words('english')) 
            word_tokens = word_tokenize(randques) 
  
            filtered_sentence = [w.strip().lower() for w in word_tokens if w not in stop_words and w not in cumilative_list] 
            found = 'no'
            dicti = {}
            ct = 1
            for x in answers:
                dicti[ct] = 0
                sent = x.split()
                for i in sent:
                    if i.strip().lower() in filtered_sentence:
                        dicti[ct] += 1
                ct = ct+1
            answer_key = max(dicti.items(), key=operator.itemgetter(1))[0]
            print("'Answer Found is' \n", answer_store[answer_key])
        else:
            print("Sorry we were unable to help. Have a nice day")
