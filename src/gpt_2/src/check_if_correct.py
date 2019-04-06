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
def countNouns(nouns, textOriginal):
  count = 0
  for i in textOriginal.split(" "):
    for j in nouns:
      if j == i:
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
  

#returns the most important word from a text in order to search later the picture
def getNounImage(text):
  blob = TextBlob(text)
  tags = blob.tags  
  max = 0
  maxP = 0
  word = ""
  personalword = ""
  for i in tags:
    aux = 0
    if i[1] == 'NN' or i[1] == 'NNS':
      for j in text.split(" "):
        if i[0] == j or i[0] == j[:-1]:
          aux = aux+1
      if aux > max :
        max = aux
        word = i[0]
      text.replace(i[1],"")

    elif i[1] =='NNP':
        for j in text.split(" "):
          if i[0] == j or i[0] == j[:-1]:
            aux = aux+1
        if aux > maxP :
          maxP = aux
          personalword = i[0]
        text.replace(i[1],"")

  if personalword == "": return personalword
  else : return personalword


  