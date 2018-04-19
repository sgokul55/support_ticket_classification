import os
from pandas import DataFrame
import numpy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

import ticket_db

NEWLINE = '\n'
SKIP_FILES = {'cmds'}
classifier_1 = MultinomialNB()
classifier_dt = MultinomialNB()
classifier_rt = MultinomialNB()
classifier_sub_category = MultinomialNB()
count_vectorizer_1 = CountVectorizer(stop_words = 'english')
count_vectorizer_dt = CountVectorizer(stop_words = 'english')
count_vectorizer_rt = CountVectorizer(stop_words = 'english')
count_vectorizer_sub_category = CountVectorizer(stop_words = 'english')

def read_files(path):
    for root, dir_names, file_names in os.walk(path):
        for file_name in file_names:
            if file_name not in SKIP_FILES:
                file_path = os.path.join(root, file_name)
                #print(file_path)
                if os.path.isfile(file_path):
                    lines = []
                    f = open(file_path)
                    for line in f:
                        if line != NEWLINE:
                            lines.append(line)
                    f.close()
                    content = NEWLINE.join(lines)
                    #print(content)
                    yield file_path, content

def build_data_frame(path, classification):
    rows = []
    index = []
    for file_name, text in read_files(path):
        # Remove stop words
        # Apply stemming
        rows.append({'text': text, 'class': classification})
        index.append(file_name)
    data_frame = DataFrame(rows, index=index)
    return data_frame

def add_more_traing_data():
    DT = 'DT'
    RT = 'RT'
    SOURCES = [('data/DT/whaterver.txt', DT),('data/RT/whaterver.txt',RT)]
    data = DataFrame({'text': [], 'class': []})
    for path, classification in SOURCES:
        data = data.append(build_data_frame(path, classification))
    data = data.reindex(numpy.random.permutation(data.index))

def classify_ticket_category(ticket_data, classifier_name):
    #examples = ['Description:FATAL EXCEPTION In ICs without']
    #example_counts = count_vectorizer.transform(examples)
    # Remove stop words
    # Apply stemming
    predictions = []
    if(classifier_name == 'classifier-1'):
        new_ticket_counts = count_vectorizer_1.transform(ticket_data)
        predictions = classifier_1.predict(new_ticket_counts)
    elif(classifier_name == 'classifier-dt'):
        new_ticket_counts = count_vectorizer_dt.transform(ticket_data)
        predictions = classifier_dt.predict(new_ticket_counts)
    elif(classifier_name == 'classifier-rt'):
        new_ticket_counts = count_vectorizer_rt.transform(ticket_data)
        predictions = classifier_rt.predict(new_ticket_counts)
    elif(classifier_name == 'classifier-sc'):
        new_ticket_counts = count_vectorizer_sub_category.transform(ticket_data)
        predictions = classifier_sub_category.predict(new_ticket_counts)
    #print(ticket_data)
    print('My Prediction is: '+predictions[0])
    return predictions[0]

def train_classifier_1():
    print('training classifier-1')
    data_frame_dt = build_data_frame('tickets/training_set/DT', 'DT')
    data_frame_rt = build_data_frame('tickets/training_set/RT', 'RT')
    #print(data_frame_dt)
    #print(data_frame_rt)
    data = DataFrame({'text': [], 'class': []})
    data = data.append(data_frame_dt)
    data = data.append(data_frame_rt)
    #print(data)
    counts = count_vectorizer_1.fit_transform(data['text'].values)
    targets = data['class'].values
    classifier_1.fit(counts, targets)

def train_classifier_dt():
    print('training classifier-2')
    data_frame_dt = build_solution_data_frame('tickets/training_set/DT')
    #print(data_frame_dt)
    data = DataFrame({'text': [], 'class': []})
    data = data.append(data_frame_dt)
    #print(data)
    counts = count_vectorizer_dt.fit_transform(data['text'].values)
    targets = data['class'].values
    classifier_dt.fit(counts, targets)

def train_classifier_rt():
    print('training classifier-3')
    data_frame_rt = build_solution_data_frame('tickets/training_set/RT')
    #print(data_frame_dt)
    data = DataFrame({'text': [], 'class': []})
    data = data.append(data_frame_rt)
    #print(data)
    counts = count_vectorizer_rt.fit_transform(data['text'].values)
    targets = data['class'].values
    classifier_rt.fit(counts, targets)

def train_classifier_sub_category():
    print('training classifier-4')
    data_frame_sc = build_sc_data_frame('tickets/sample_additional_text')
    #print(data_frame_dt)
    data = DataFrame({'text': [], 'class': []})
    data = data.append(data_frame_sc)
    #print(data)
    counts = count_vectorizer_sub_category.fit_transform(data['text'].values)
    targets = data['class'].values
    classifier_sub_category.fit(counts, targets)

def build_sc_data_frame(path):
    rows = []
    index = []
    count = 1
    for file_name, text in read_files(path):
        rows.append({'text': text, 'class': file_name.split('\\')[-1].split('.txt')[0]})
        index.append(file_name)
        count += 1
    data_frame = DataFrame(rows, index=index)
    return data_frame

def build_solution_data_frame(path):
    rows = []
    index = []
    count = 1
    for file_name, text in read_files(path):
        rows.append({'text': text, 'class': 'SOL' + str(count)})
        index.append(file_name)
        count += 1
    data_frame = DataFrame(rows, index=index)
    return data_frame

def get_prediction(input_data):
    result = {}
    result['classification'] = classify_ticket_category(input_data['incident_description'],'classifier-1')
    if(result['classification'] == 'DT'):
        result['proposed_solution'] = ticket_db.get_proposed_solution('DT',classify_ticket_category(input_data['incident_description'],'classifier-dt'))
    else:
        result['proposed_solution'] = ticket_db.get_proposed_solution('RT',classify_ticket_category(input_data['incident_description'],'classifier-rt'))
    result['sub_category'] = classify_ticket_category(input_data['additional_description'],'classifier-sc')
    return result

if __name__ == '__main__':


    #build_sc_data_frame('tickets/sample_additional_text')
    train_classifier_1()
    train_classifier_dt()
    train_classifier_rt()
    train_classifier_sub_category()
    sample_ticket_test = ['Mandatory SSL CLient PSE missing: SSLC/4384783 Event Name: CLIENT_PSE_MISSING Event Context: SSLC/34ewq Application Component: BC-fdsfadsf-STP']
    sample_ticket_test_sc = ['SAP anonymous client PSE missing']
    if(classify_ticket_category(sample_ticket_test,'classifier-1') == 'DT'):
        print(ticket_db.get_proposed_solution('DT',classify_ticket_category(sample_ticket_test,'classifier-dt')))
    else:
        print(ticket_db.get_proposed_solution('RT',classify_ticket_category(sample_ticket_test,'classifier-rt')))
    classify_ticket_category(sample_ticket_test_sc,'classifier-sc')
    # data_frame_rt = build_routing_ticket_data_frame('tickets/RT')
    # #print(data_frame_dt)
    # #print(data_frame_rt)
    # data = DataFrame({'text': [], 'class': []})
    # #data = data.append(data_frame_dt)
    # data = data.append(data_frame_rt)
    # print(data['text'][1])


    # data_frame_dt = build_data_frame('data/DT', 'DT')
    # data_frame_rt = build_data_frame('data/RT', 'RT')
    # print(data_frame_dt)
    # print(data_frame_rt)
    # data = DataFrame({'text': [], 'class': []})
    # data = data.append(data_frame_dt)
    # data = data.append(data_frame_rt)

    # print(data)

    # import numpy
    # from sklearn.feature_extraction.text import CountVectorizer
    # count_vectorizer = CountVectorizer()
    # counts = count_vectorizer.fit_transform(data['text'].values)

    # from sklearn.naive_bayes import MultinomialNB

    # classifier = MultinomialNB()
    # targets = data['class'].values
    # classifier.fit(counts, targets)

    # examples = ['Summary:Attachments related check - create, read and delete Event Name: ATTACHMENT_API_CHECK']
    # example_counts = count_vectorizer.transform(examples)
    # predictions = classifier.predict(example_counts)
    # #input_type = ['RT','DT']
    # print(examples)
    # print('My Prediction is: '+predictions[0])