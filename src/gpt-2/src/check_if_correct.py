from textblob import TextBlob

#it takes a text and returns a list with all the nouns
def extractNouns(text):
  blob = TextBlob(text)
  tags = blob.tags  
  nouns = []
  for i in tags:
    if i[1] == 'NN' or i[1] =='NNP' or i[1] == 'NNS':
      nouns.append(i[0])

  return nouns

#it returns the number of ocurrences of words
def countNouns(nouns, text):
  count = 0
  for i in text:
    if i in nouns:
      count = count+1
  return count      
    
#from an original text and an array of texts we can get the best one by counting the one that has more common names
def compare(text0,textos):
  aux = 0
  max = 0
  #original
  nouns0 = extractNouns(text0)
  for i in textos:
    nouns = extractNouns(i)
    nwords = countNouns(nouns, nouns0)
    if nwords > max :
      max = aux
    aux = aux+1
  return max
  



