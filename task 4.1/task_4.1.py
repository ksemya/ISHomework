#Задание 1. Квадраты всех четных чисел
print("Задание 1")
numbersArray=[1,2,3,4,5,6,7,8,9,10]
squaresArray= list(map(lambda x: x**2, list(filter(lambda x : x % 2 == 0, numbersArray))))
print('Квадраты всех четных чисел:'+str(squaresArray))

#Задание 2. Дана входная строка и массив чисел, необходимо вернуть строку с теми буквами, которые стоят на указанных местах
print("Задание 2")
myString='Всем привет'
myArray=[1,3,5]
resultString_1=''
for i in myArray: resultString_1 += myString[i]
print('Строка без list comprehensions: ' + resultString_1)
resultString_2=''.join([myString[x] for x in myArray])
print('Строка c list comprehensions: ' + resultString_2)

#Задание 3. Дан текст (предложения разделены только точками), в котором
#буквы могут находиться в разных регистрах. Необходимо вернуть
#текст, в котором все буквы в нижнем регистре, а первые буквы
#каждого предложения – в верхнем.
print("Задание 3")
myText="ПрИвЕт. Я пРограммирУю на PYTHON. хочУ СтаТЬ ХороШим ПрОгРамМисТоМ"
sentenceArray=myText.split('.')
resultText=''
for sentence in sentenceArray: 
    sentence=sentence.strip()
    resultSentence=sentence[0].upper()+sentence[1:].lower()+'. '
    resultText+=resultSentence
print(resultText)

#Задание 4.functools.reduce
print("Задание 4")
def FunctoolsReduce(function, iterable, initializer = None):
    iterator = iter(iterable)
    if initializer is None:
        initializer = next(iterator)
    accumulation_value = initializer
    
    for x in iterator:
        accumulation_value = function(accumulation_value, x)
    return accumulation_value

result = FunctoolsReduce(lambda x, y: x + y, [1, 2, 3, 4, 5])
print(result)

#Задание 5.Coздайте функцию pipeline_each, в которую вы будете подавать 
#итерируемый объект и список функций, которые последовательно
#надо к нему применить. 
print("Задание 5")
def pipeline_each(obj, funtions):
    for func in myFunctions:
        for i, elem in enumerate(obj):
            obj[i] = func(elem)
    return obj
myIterableObj = [1,2,3,4,5]
myFunctions = [
    lambda x: x*x,
    lambda x: x+x,
    lambda x: x+1]       
print(pipeline_each(myIterableObj, myFunctions))

#Задание 6.Написать генератор, возвращающий по очереди все слова, входящие в предложение.
print("Задание 6")
def wordInSentece(sentence):
    sentenceArray = sentence.split(' ')
    for word in sentenceArray:
        yield word
    
mySentence = 'Этот генератор умеет возвращать по очереди все слова, входящие в предложение'
for word in wordInSentece(mySentence):
    print(word)

#Задание 7.Написать генератор псевдо случайных чисел
print("Задание 7")
def myRandom (seed = 0):
    while True:
        seed = (782+(seed*(seed%4)))%13167
        yield seed
result_1=myRandom(5);

for i in range(10):
    print(next(result_1))

#Задание 8.Написать корутину, которая реализует бесконечную 
#арифметическую прогрессию с возможностью перезапуска с любого места
print("Задание 8")
def infinity_progression():
    n=0
    while True:
        input = yield n
        if (input != None):
            n = input
        n += 1
result=infinity_progression()

print(next(result))
print(next(result))
print(result.send(30))
print(next(result))
print(next(result))
print(result.send(10))
print(next(result))
print(next(result))
