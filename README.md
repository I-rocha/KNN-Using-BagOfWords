# KNN-Using-BagOfWords
This project has the main purpose of processing text and form bag of words(BOW). The application of KNN is used as an example of using the BOW but is not the main purpose here. Besides there is also a list of stop words considered in this application


The flow of processing was  
1. Load data in format of sentences using ',' as a delimiter  
2. Divide sentence into traing and test  
3. Cleaning non textual elements as <new line, tab, dot> and so on. And separating sentence in words  
4. Creating single BOW for test  
5. Remove stop words from training  
6. Creating single BOW for training  
7. Creating Multiple -in my case, 2- Bag of Word (MBOW)  
8. Applying KNN  
Note: There is no need to remove stop words from test, since test can have noise and the AI should 


## Data  
In this case was used 2 bag of words: *alt.altheism.txt* and *talk.politics.misc.txt*. But there is more data that could be added or used instead, these data can be extract from *raw_data/raw_data.rar*  
In code, the 2 variables for training e 2 variables for test representes these two texts


## Output
The folder *output* updates it's 3 files when the application runs:  
1. log.txt  
2. tr_bag01.txt  
3. tr_bag01.txt  

The log archive contains the same information as printed in the shell/command line when running, basically time information of process and accuracy from KNN  
![Log.txt](https://user-images.githubusercontent.com/38757175/193178148-e8adedbe-c712-4e2c-b0af-4fa26f1a798f.png)  
[log.txt]

The last two files are bag of word calculated of each training  
![image](https://user-images.githubusercontent.com/38757175/193178931-d57dcbe1-aeb5-4597-9039-e00089a29401.png)   
[partial tr_bag01.txt]  
First column contains all the words involving text training 1 and 2;  
Second column contains how many times that word was repeated in the specific text (1 or 2)
