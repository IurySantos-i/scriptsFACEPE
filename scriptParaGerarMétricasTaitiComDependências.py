import json
import requests
import os
import pandas as pd
import re
from datetime import datetime

def difference (lst1, lst2):
    result = []
    for i in range(len(lst1)):
        result.append(len(lst1[i]) - len(lst2[i]))
    return result    

def fill_list(lst, length):
    return [lst[0]] + ['X'] * max(0, length - 1)

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def Union(lst1, lst2):
    final_list = list(set(lst1) | set(lst2))
    return final_list

def Matchmaker(lsttuple, lst):
    final = []
    for str in lst:
        for tuple in lsttuple:
         if str == tuple[0]:
            final.append(tuple[1])
    return list(dict.fromkeys(final))

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def get_commit_date(commit_hash):

    # Get commit details from GitHub API
    url = f'https://api.github.com/repos/{donoDoRepositorio}/{repositorio}/commits/{commit_hash}'
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    commit_data = data['commit']["author"]["date"]

    # Convert commit date string to datetime object
    commit_date = datetime.strptime(commit_data, '%Y-%m-%dT%H:%M:%SZ')
    return commit_date


def get_number_of_files(commit_hash):
    url = f'https://api.github.com/repos/{donoDoRepositorio}/{repositorio}/commits/{commit_hash}'
    #print(url)
    response = requests.get(url, headers=headers)
    #print(response.content)
    tree_url = json.loads(response.content)['commit']['tree']['url']

    # Get the tree for the commit
    response = requests.get(tree_url, headers=headers)
    tree = json.loads(response.content)
    # Get the number of files in the tree
    return len(tree['tree'])



def calculate_days_between_commits(commit_hash1, commit_hash2):
    commit_date1 = get_commit_date(commit_hash1) # Mais antigo
    commit_date2 = get_commit_date(commit_hash2) # Mais Recente

    # Calculate timedelta between commit dates
    delta = commit_date2 - commit_date1
    return delta.days

token = "                   "
headers = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {token}"
}

tasksDoProjeto = pd.read_excel('formalized_tasks_action-center-platform.git.xlsx')
commits = tasksDoProjeto[['Oldest Commit','Most Recent Commit']]

arquivoTaiti = 'https___github.com_EFForg_action-center-platform.csv'
partes = arquivoTaiti.split("_")
donoDoRepositorio = partes[-2]
repositorio = partes[-1].split(".")[0]

degrees = ['dencies.csv','(10%).csv']

path_of_the_directory = r"/home/iury/Documents/Trabalho/TAITIpesq2/Dependencias, gitlogs e Métricas TaitI/action-center-platform.git/"

df = pd.read_csv(arquivoTaiti,engine="python", sep=';')

days = []
numberofchangedfiles = [] #para análise 1
numberoftestifiles = [] #para análise 3
testIwithDeps = []
numberoftestiwithdeps = [] #para análise 5
inclusivedeps = []
deps = []
totalnumberofdeps = []
numberofdeps = [] #para análise 4
precision = []
recall = []
f2= []
precisiondeps = []
recalldeps = []
f2deps= []
prodchangedfiles = []
numberofprodchangedfiles= [] #para análise 2
testIwithFilteredDeps = []
filtereddeps = []
changedprecision = []
changedrecall = []
changedf2= []
changedprecisiondeps = []
changedrecalldeps = []
changedf2deps= []
numberofdepsfortask = []
totalfiles = []
percentofchange = [] #para análise
f2depsMinusf2 = []
filteredF2depsMinusFilteredF2 = []
RecallDepsMinusRecall = []
PrecisionDepsMinusPrecision = []
FilteredRecallDepsMinusFilteredRecall = []
FilteredPrecisionDepsMinusFilteredPrecision = []

index=0

for filename in sorted(os.listdir(path_of_the_directory), key = natural_keys):
    if filename.endswith(degrees[0]) and not filename.startswith("http") and (pd.read_csv(filename, sep=";")).values.tolist() == []:

            Taiti= df.at[index,'TestI'][1:-1].split(",")
            Taiti = [x.strip(' ') for x in Taiti]
            tempnumberoftaitifiles = len(Taiti)

            Changed= df.at[index,'Changed files'][1:-1].split(",")
            Changed = [x.strip(' ') for x in Changed]
            tempnumberofchangedfiles = len(Changed)

            precisionTemp = len(intersection(Taiti,Changed))/len(Taiti)
            recallTemp = len(intersection(Taiti,Changed))/len(Changed)
            if (4* precisionTemp + recallTemp == 0):
             f2Temp = 0
            else: f2Temp = (5*precisionTemp*recallTemp)/ (4* precisionTemp + recallTemp)

            numberofchangedfiles.append(tempnumberofchangedfiles)
            testIwithDeps.append(Taiti)
            numberoftestiwithdeps.append(tempnumberoftaitifiles)
            inclusivedeps.append('')
            deps.append("")
            precision.append(precisionTemp)
            recall.append(recallTemp)
            precisiondeps.append(precisionTemp)
            recalldeps.append(recallTemp)
            f2.append(f2Temp)
            f2deps.append(f2Temp)

            # Métricas com filtradas de acordo com a pasta e com a extensão

            filteredChanged =  [s for s in Changed if (s.startswith('app') or s.startswith('lib')) and (s.endswith('.erb') or s.endswith('.rb') or s.endswith('.html') or s.endswith('.haml'))]
            filteredprecisionTemp = len(intersection(Taiti,filteredChanged))/len(Taiti)
            filteredrecallTemp = len(intersection(Taiti,filteredChanged))/len(filteredChanged)
            if (4* filteredprecisionTemp + filteredrecallTemp == 0):
             filteredf2Temp = 0
            else: filteredf2Temp = (5*filteredprecisionTemp*filteredrecallTemp)/ (4* filteredprecisionTemp + filteredrecallTemp)

            tempdays = calculate_days_between_commits(commits.iloc[index][0], commits.iloc[index][1])
            if tempdays == 0:
                tempdays = 1


            tempnumberOfFiles = get_number_of_files(commits.loc[index][1])
            tempchangedpercentage = round(tempnumberofchangedfiles / tempnumberOfFiles , 3)
            if tempchangedpercentage > 1:
                tempchangedpercentage = 1

            days.append(tempdays)
            prodchangedfiles.append(filteredChanged)
            numberofprodchangedfiles.append(len(filteredChanged))
            testIwithFilteredDeps.append(Taiti)
            numberoftestifiles.append(len(Taiti))
            filtereddeps.append('')
            changedprecision.append(filteredprecisionTemp)
            changedrecall.append(filteredrecallTemp)
            changedf2.append(filteredf2Temp)
            changedprecisiondeps.append(filteredprecisionTemp)
            changedrecalldeps.append(filteredrecallTemp)
            changedf2deps.append(filteredf2Temp)
            numberofdepsfortask.append('0')
            totalfiles.append(tempnumberOfFiles)
            percentofchange.append(tempchangedpercentage)
            f2depsMinusf2.append(0)
            filteredF2depsMinusFilteredF2.append(0)
            RecallDepsMinusRecall.append(0)
            PrecisionDepsMinusPrecision.append(0)
            FilteredRecallDepsMinusFilteredRecall.append(0)
            FilteredPrecisionDepsMinusFilteredPrecision.append(0)







            index = index+1
            print(filename)


    elif filename.endswith(degrees[0]) and not filename.startswith("http"):

        df1 = pd.read_csv(filename, engine="python", sep=',')
        weaklogicaldependence = df1['coupled'].tolist()

        stronglogicaldependence=df1['entity'].tolist()

        compare = list(zip(stronglogicaldependence,  weaklogicaldependence))


        Taiti= df.at[index,'TestI'][1:-1].split(",")
        Taiti= [x.strip(' ') for x in Taiti]
        Changed= df.at[index,'Changed files'][1:-1].split(",")
        Changed = [x.strip(' ') for x in Changed]

        Final = Matchmaker(compare,Taiti)

        testIwithDepstemp = Union(Final, Taiti)

        depstemp = [x for x in testIwithDepstemp if x not in Taiti]
        if depstemp == []:
            depstemp = ""

        precisionTemp = len(intersection(Taiti,Changed))/len(Taiti)


        recallTemp = len(intersection(Taiti,Changed))/len(Changed)

        precisiondepsTemp = len(intersection(testIwithDepstemp,Changed))/ len(testIwithDepstemp)


        recalldepsTemp = len(intersection(testIwithDepstemp,Changed))/ len(Changed)



        if (4* precisionTemp + recallTemp == 0):
            f2Temp = 0
        else: f2Temp = (5*precisionTemp*recallTemp)/ (4* precisionTemp + recallTemp)

        if (4* precisiondepsTemp + recalldepsTemp == 0):
            f2depsTemp = 0
        else: f2depsTemp = (5*precisiondepsTemp*recalldepsTemp)/ (4* precisiondepsTemp + recalldepsTemp)

        numberofchangedfiles.append(len(Changed))
        numberoftestifiles.append(len(Taiti))
        testIwithDeps.append(testIwithDepstemp)
        numberoftestiwithdeps.append(len(testIwithDepstemp))
        inclusivedeps.append(Final)
        deps.append(depstemp)
        precision.append(precisionTemp)
        recall.append(recallTemp)
        precisiondeps.append(precisiondepsTemp)
        recalldeps.append(recalldepsTemp)
        f2.append(f2Temp)
        f2deps.append(f2depsTemp)

        # Métricas com filtradas de acordo com a pasta e com a extensão

        filteredChanged =  [s for s in Changed if (s.startswith('app') or s.startswith('lib')) and (s.endswith('.erb') or s.endswith('.rb') or s.endswith('.html') or s.endswith('.haml'))]
        mask = df1.coupled.str.contains(r"^(app|lib).*(\.erb|\.rb|\.html|\.haml)$")
        compare_ = df1[mask]
        weaklogicaldependencetemp=df1['coupled'].tolist()
        stronglogicaldependencetemp=df1['entity'].tolist()

        filteredcompare = list(zip(stronglogicaldependencetemp,  weaklogicaldependencetemp))

        filteredFinal = Matchmaker(filteredcompare,Taiti)

        filteredtestIwithDepstemp = Union(filteredFinal, Taiti)

        filtereddepstemp = [x for x in filteredtestIwithDepstemp if x not in Taiti]
        if filtereddepstemp == []:
            filtereddepstemp = ""

        filteredprecisionTemp = len(intersection(Taiti, filteredChanged))/len(Taiti)


        filteredrecallTemp = len(intersection(Taiti, filteredChanged))/len( filteredChanged)

        filteredprecisiondepsTemp = len(intersection(filteredtestIwithDepstemp, filteredChanged))/ len(filteredtestIwithDepstemp)


        filteredrecalldepsTemp = len(intersection(filteredtestIwithDepstemp, filteredChanged))/ len( filteredChanged)



        if (4* filteredprecisionTemp + filteredrecallTemp == 0):
            filteredf2Temp = 0
        else: filteredf2Temp = (5*filteredprecisionTemp*filteredrecallTemp)/ (4* filteredprecisionTemp + filteredrecallTemp)

        if (4* filteredprecisiondepsTemp + filteredrecalldepsTemp == 0):
            filteredf2depsTemp = 0
        else: filteredf2depsTemp = (5*filteredprecisiondepsTemp*filteredrecalldepsTemp)/ (4* filteredprecisiondepsTemp + filteredrecalldepsTemp)

        tempnumberOfFiles = get_number_of_files(commits.loc[index][1])
        tempchangedpercentage = round (len(Changed) / tempnumberOfFiles ,3)
        if tempchangedpercentage > 1:
            tempchangedpercentage = 1

        prodchangedfiles.append(filteredChanged)
        numberofprodchangedfiles.append(len(filteredChanged))
        testIwithFilteredDeps.append(filteredtestIwithDepstemp)
        filtereddeps.append(filtereddepstemp)
        changedprecision.append(filteredprecisionTemp)
        changedrecall.append(filteredrecallTemp)
        changedf2.append(filteredf2Temp)
        changedprecisiondeps.append(filteredprecisiondepsTemp)
        changedrecalldeps.append(filteredrecalldepsTemp)
        changedf2deps.append(filteredf2depsTemp)
        numberofdepsfortask.append(str(len(weaklogicaldependence)))
        tempdays = calculate_days_between_commits(commits.iloc[index][0], commits.iloc[index][1])
        totalfiles.append(tempnumberOfFiles)
        percentofchange.append(tempchangedpercentage)
        f2depsMinusf2.append(f2depsTemp - f2Temp)
        filteredF2depsMinusFilteredF2.append(filteredf2depsTemp - filteredf2Temp)
        RecallDepsMinusRecall.append(recalldepsTemp- recallTemp)
        PrecisionDepsMinusPrecision.append(precisiondepsTemp - precisionTemp)
        FilteredRecallDepsMinusFilteredRecall.append(filteredrecalldepsTemp - filteredrecallTemp)
        FilteredPrecisionDepsMinusFilteredPrecision.append(filteredprecisiondepsTemp - filteredprecisionTemp)

        if tempdays == 0:
            tempdays = 1
        days.append(tempdays)




        print(filename)
        index = index+1

numberofexclusivedeps = []
for element in deps:
    numberofexclusivedeps.append(len(element))

numberofinclusivedeps = []
for element in inclusivedeps:
    numberofinclusivedeps.append(len(element))

trueFilteredDeps= []
for i in range(0,len(filtereddeps)):
    trueFilteredDeps.append([])
    for j in range(0,len(filtereddeps[i])):
     if (filtereddeps[i][j].startswith('app') or filtereddeps[i][j].startswith('lib')) and (filtereddeps[i][j].endswith('.erb') or filtereddeps[i][j].endswith('.rb') or filtereddeps[i][j].endswith('.html') or filtereddeps[i][j].endswith('.haml')): trueFilteredDeps[i].append(filtereddeps[i][j])

numberoftrueFilteredDeps= []
for element in trueFilteredDeps:
    numberoftrueFilteredDeps.append(len(element))


numberoffiltereddeps = []
for element in filtereddeps:
    numberoffiltereddeps.append(len(element))    

numberoftestiwithfiltereddeps = []
for element in testIwithFilteredDeps:
    numberoftestiwithfiltereddeps.append(len(element))   

definitelypositive = []
for i in range(len(f2)):
    if (max([changedf2[i],changedf2deps[i],f2[i],f2deps[i]]) == f2deps[i]) or (max([changedf2[i],changedf2deps[i],f2[i],f2deps[i]]) == changedf2deps):
        definitelypositive.append("Yes")
    else:            
        definitelypositive.append("No")         

circumstantiallypositive = []
for i in range(len(f2)):
    if (       (changedf2[i] < changedf2deps[i] ) and (f2[i]  >= f2deps[i] )   ) or ((changedf2[i]  >= changedf2deps[i] ) and (f2[i]  < f2deps[i])):
        circumstantiallypositive.append("Yes") 
    else:            
        circumstantiallypositive.append("No")


definitelynegative = []
for i in range(len(f2)):
    if (    (changedf2[i]  > changedf2deps[i] ) and (f2[i]  > f2deps[i] )   ):
        definitelynegative.append("Yes")          
    else:            
        definitelynegative.append("No")

noeffectonF2 = []
for i in range(len(f2)):
    if (    (changedf2[i]  == changedf2deps[i] ) and (f2[i]  == f2deps[i])   ):
        noeffectonF2.append("Yes")
    else:            
        noeffectonF2.append("No")



df['DurationOfTask(Days)'] = days
df['#ChangedFiles'] = numberofchangedfiles
df['#TestIFiles'] = numberoftestifiles
df['TestIWithDeps'] = testIwithDeps
df['#TestIWithDeps'] = numberoftestiwithdeps
df['InclusiveDeps'] = inclusivedeps
df['ExclusiveDeps'] = deps
df['#InclusiveDeps'] = numberofinclusivedeps
df['#ExclusiveDeps'] = numberofexclusivedeps
df['Precision'] = precision
df['Recall'] = recall
df['F2'] = f2
df['PrecisionDeps'] = precisiondeps
df['RecallDeps'] = recalldeps
df['F2Deps'] = f2deps
df['ProductionChangedFiles'] = prodchangedfiles
df['#Prod.ChangedFiles'] = numberofprodchangedfiles
df['TestIwithFilteredDeps'] = testIwithFilteredDeps
df['#TestIwithFilteredDeps'] = numberoftestiwithfiltereddeps
df['ProductionDeps'] = trueFilteredDeps
df['#ProductionDeps'] = numberoftrueFilteredDeps
df['FilteredPrecision'] = changedprecision
df['FilteredRecall'] = changedrecall
df['Filteredf2'] = changedf2
df['FilteredPrecisionDeps'] = changedprecisiondeps
df['FilteredRecallDeps'] = changedrecalldeps
df['Filteredf2Deps'] = changedf2deps
df['#DepsForTask'] = numberofdepsfortask
df['TotalFiles'] = totalfiles
df['ProportionOfChange'] = percentofchange
df['F2Deps - F2'] = f2depsMinusf2 
df['FilteredF2Deps - FilteredF2'] = filteredF2depsMinusFilteredF2
df['RecallDeps - Recall'] = RecallDepsMinusRecall
df['PrecisionDeps - Precision'] = PrecisionDepsMinusPrecision
df['FilteredRecallDeps  - FilteredRecall'] = FilteredRecallDepsMinusFilteredRecall 
df['FilteredPrecisionDeps - FilteredPrecision'] = FilteredPrecisionDepsMinusFilteredPrecision
df['#ExclusiveDeps - #FilteredDeps'] = difference(deps,trueFilteredDeps)
df['AverageF2'] = fill_list([sum(f2)/index],index)
df['AverageF2Deps'] = fill_list([sum(f2deps)/index],index)
df['AverageFilteredF2'] = fill_list([sum(changedf2)/index],index )
df['AverageFilteredF2Deps'] = fill_list([sum(changedf2deps)/index],index)
df['DefinitelyPositive'] = definitelypositive
df['CircumstantiallyPositive'] = circumstantiallypositive
df['DefinitelyNegative'] = definitelynegative
df['NoEffectOnF2'] = noeffectonF2



df.to_csv('TaitiWithdeps_' + repositorio + '(30%).csv', index=False)


days = []
numberofchangedfiles = [] #para análise 1
numberoftestifiles = [] #para análise 3
testIwithDeps = []
numberoftestiwithdeps = [] #para análise 5
inclusivedeps = []
deps = []
totalnumberofdeps = []
numberofdeps = [] #para análise 4
precision = []
recall = []
f2= []
precisiondeps = []
recalldeps = []
f2deps= []
prodchangedfiles = []
numberofprodchangedfiles= [] #para análise 2
testIwithFilteredDeps = []
filtereddeps = []
changedprecision = []
changedrecall = []
changedf2= []
changedprecisiondeps = []
changedrecalldeps = []
changedf2deps= []
numberofdepsfortask = [] #para análise
totalfiles = []
percentofchange = []
f2depsMinusf2 = []
filteredF2depsMinusFilteredF2 = []
RecallDepsMinusRecall = []
PrecisionDepsMinusPrecision = []
FilteredRecallDepsMinusFilteredRecall = []
FilteredPrecisionDepsMinusFilteredPrecision = []

index=0

for filename in sorted(os.listdir(path_of_the_directory), key = natural_keys):
    if filename.endswith(degrees[1]) and not filename.startswith("http") and (pd.read_csv(filename, sep=";")).values.tolist() == []:

            Taiti= df.at[index,'TestI'][1:-1].split(",")
            Taiti = [x.strip(' ') for x in Taiti]
            tempnumberoftaitifiles = len(Taiti)

            Changed= df.at[index,'Changed files'][1:-1].split(",")
            Changed = [x.strip(' ') for x in Changed]
            tempnumberofchangedfiles = len(Changed)


            precisionTemp = len(intersection(Taiti,Changed))/len(Taiti)
            recallTemp = len(intersection(Taiti,Changed))/len(Changed)
            if (4* precisionTemp + recallTemp == 0):
             f2Temp = 0
            else: f2Temp = (5*precisionTemp*recallTemp)/ (4* precisionTemp + recallTemp)

            testIwithDeps.append(Taiti)
            numberoftestiwithdeps.append(tempnumberoftaitifiles)
            inclusivedeps.append("")
            deps.append("")
            precision.append(precisionTemp)
            recall.append(recallTemp)
            precisiondeps.append(precisionTemp)
            recalldeps.append(recallTemp)
            f2.append(f2Temp)
            f2deps.append(f2Temp)

            # Métricas com filtradas de acordo com a pasta e com a extensão

            filteredChanged =  [s for s in Changed if (s.startswith('app') or s.startswith('lib')) and (s.endswith('.erb') or s.endswith('.rb') or s.endswith('.html') or s.endswith('.haml'))]
            filteredprecisionTemp = len(intersection(Taiti,filteredChanged))/len(Taiti)
            filteredrecallTemp = len(intersection(Taiti,filteredChanged))/len(filteredChanged)
            if (4* filteredprecisionTemp + filteredrecallTemp == 0):
             filteredf2Temp = 0
            else: filteredf2Temp = (5*filteredprecisionTemp*filteredrecallTemp)/ (4* filteredprecisionTemp + filteredrecallTemp)


            tempdays = calculate_days_between_commits(commits.iloc[index][0], commits.iloc[index][1])
            if tempdays == 0:
                tempdays = 1



            tempnumberOfFiles = get_number_of_files(commits.loc[index][1])
            tempchangedpercentage = round(tempnumberofchangedfiles / tempnumberOfFiles , 3)
            if tempchangedpercentage > 1:
                tempchangedpercentage = 1


            days.append(tempdays)
            prodchangedfiles.append(filteredChanged)
            numberofprodchangedfiles.append(len(filteredChanged))
            testIwithFilteredDeps.append(Taiti)
            numberoftestifiles.append(len(Taiti))
            filtereddeps.append('')
            changedprecision.append(filteredprecisionTemp)
            changedrecall.append(filteredrecallTemp)
            changedf2.append(filteredf2Temp)
            changedprecisiondeps.append(filteredprecisionTemp)
            changedrecalldeps.append(filteredrecallTemp)
            changedf2deps.append(filteredf2Temp)
            numberofdepsfortask.append('0')
            totalfiles.append(tempnumberOfFiles)
            percentofchange.append(tempchangedpercentage)
            f2depsMinusf2.append(0)
            filteredF2depsMinusFilteredF2.append(0)
            RecallDepsMinusRecall.append(0)
            PrecisionDepsMinusPrecision.append(0)
            FilteredRecallDepsMinusFilteredRecall.append(0)
            FilteredPrecisionDepsMinusFilteredPrecision.append(0)






            index = index+1
            print(filename)


    elif filename.endswith(degrees[1]) and not filename.startswith("http"):

        df1 = pd.read_csv(filename, engine="python", sep=',')
        print(filename)
        weaklogicaldependence=df1['coupled'].tolist()

        stronglogicaldependence=df1['entity'].tolist()

        compare = list(zip(stronglogicaldependence,  weaklogicaldependence))


        Taiti= df.at[index,'TestI'][1:-1].split(",")
        Taiti= [x.strip(' ') for x in Taiti]
        Changed= df.at[index,'Changed files'][1:-1].split(",")
        Changed = [x.strip(' ') for x in Changed]

        Final = Matchmaker(compare,Taiti)

        testIwithDepstemp = Union(Final, Taiti)

        depstemp = [x for x in testIwithDepstemp if x not in Taiti]
        if depstemp == []:
            depstemp = ""

        precisionTemp = len(intersection(Taiti,Changed))/len(Taiti)


        recallTemp = len(intersection(Taiti,Changed))/len(Changed)

        precisiondepsTemp = len(intersection(testIwithDepstemp,Changed))/ len(testIwithDepstemp)


        recalldepsTemp = len(intersection(testIwithDepstemp,Changed))/ len(Changed)



        if (4* precisionTemp + recallTemp == 0):
            f2Temp = 0
        else: f2Temp = (5*precisionTemp*recallTemp)/ (4* precisionTemp + recallTemp)

        if (4* precisiondepsTemp + recalldepsTemp == 0):
            f2depsTemp = 0
        else: f2depsTemp = (5*precisiondepsTemp*recalldepsTemp)/ (4* precisiondepsTemp + recalldepsTemp)

        numberofchangedfiles.append(len(Changed))
        numberoftestifiles.append(len(Taiti))
        testIwithDeps.append(testIwithDepstemp)
        numberoftestiwithdeps.append(len(testIwithDepstemp))
        inclusivedeps.append(Final)
        deps.append(depstemp)
        precision.append(precisionTemp)
        recall.append(recallTemp)
        precisiondeps.append(precisiondepsTemp)
        recalldeps.append(recalldepsTemp)
        f2.append(f2Temp)
        f2deps.append(f2depsTemp)

        # Métricas com filtradas de acordo com a pasta e com a extensão

        filteredChanged =  [s for s in Changed if (s.startswith('app') or s.startswith('lib')) and (s.endswith('.erb') or s.endswith('.rb') or s.endswith('.html') or s.endswith('.haml'))]
        mask = df1.coupled.str.contains(r"^(app|lib).*(\.erb|\.rb|\.html|\.haml)$")

        compare_ = df1[mask]

        weaklogicaldependencetemp=df1['coupled'].tolist()
        stronglogicaldependencetemp=df1['entity'].tolist()

        filteredcompare = list(zip(stronglogicaldependencetemp,  weaklogicaldependencetemp))

        filteredFinal = Matchmaker(filteredcompare,Taiti)

        filteredtestIwithDepstemp = Union(filteredFinal, Taiti)

        filtereddepstemp = [x for x in filteredtestIwithDepstemp if x not in Taiti]
        if filtereddepstemp == []:
            filtereddepstemp = ""

        filteredprecisionTemp = len(intersection(Taiti, filteredChanged))/len(Taiti)


        filteredrecallTemp = len(intersection(Taiti, filteredChanged))/len( filteredChanged)

        filteredprecisiondepsTemp = len(intersection(filteredtestIwithDepstemp, filteredChanged))/ len(filteredtestIwithDepstemp)


        filteredrecalldepsTemp = len(intersection(filteredtestIwithDepstemp, filteredChanged))/ len( filteredChanged)



        if (4* filteredprecisionTemp + filteredrecallTemp == 0):
            filteredf2Temp = 0
        else: filteredf2Temp = (5*filteredprecisionTemp*filteredrecallTemp)/ (4* filteredprecisionTemp + filteredrecallTemp)

        if (4* filteredprecisiondepsTemp + filteredrecalldepsTemp == 0):
            filteredf2depsTemp = 0
        else: filteredf2depsTemp = (5*filteredprecisiondepsTemp*filteredrecalldepsTemp)/ (4* filteredprecisiondepsTemp + filteredrecalldepsTemp)




        tempnumberOfFiles = get_number_of_files(commits.loc[index][1])
        tempchangedpercentage = round(len(Changed) / tempnumberOfFiles , 3)
        if tempchangedpercentage > 1:
            tempchangedpercentage = 1

        prodchangedfiles.append(filteredChanged)
        numberofprodchangedfiles.append(len(filteredChanged))
        testIwithFilteredDeps.append(filteredtestIwithDepstemp)
        filtereddeps.append(filtereddepstemp)
        changedprecision.append(filteredprecisionTemp)
        changedrecall.append(filteredrecallTemp)
        changedf2.append(filteredf2Temp)
        changedprecisiondeps.append(filteredprecisiondepsTemp)
        changedrecalldeps.append(filteredrecalldepsTemp)
        changedf2deps.append(filteredf2depsTemp)
        numberofdepsfortask.append(str(len(weaklogicaldependence)))
        totalfiles.append(tempnumberOfFiles)
        percentofchange.append(tempchangedpercentage)
        f2depsMinusf2.append(f2depsTemp - f2Temp)
        filteredF2depsMinusFilteredF2.append(filteredf2depsTemp - filteredf2Temp)
        RecallDepsMinusRecall.append(recalldepsTemp- recallTemp)
        PrecisionDepsMinusPrecision.append(precisiondepsTemp - precisionTemp)
        FilteredRecallDepsMinusFilteredRecall.append(filteredrecalldepsTemp - filteredrecallTemp)
        FilteredPrecisionDepsMinusFilteredPrecision.append(filteredprecisiondepsTemp - filteredprecisionTemp)

        tempdays = calculate_days_between_commits(commits.iloc[index][0], commits.iloc[index][1])
        if tempdays == 0:
            tempdays = 1
        days.append(tempdays)




        print(filename)
        index = index+1

numberofexclusivedeps = []
for element in deps:
    numberofexclusivedeps.append(len(element))

numberofinclusivedeps = []
for element in inclusivedeps:
    numberofinclusivedeps.append(len(element))

trueFilteredDeps= []
for i in range(0,len(filtereddeps)):
    trueFilteredDeps.append([])
    for j in range(0,len(filtereddeps[i])):
     if (filtereddeps[i][j].startswith('app') or filtereddeps[i][j].startswith('lib')) and (filtereddeps[i][j].endswith('.erb') or filtereddeps[i][j].endswith('.rb') or filtereddeps[i][j].endswith('.html') or filtereddeps[i][j].endswith('.haml')): trueFilteredDeps[i].append(filtereddeps[i][j])

numberoftrueFilteredDeps= []
for element in trueFilteredDeps:
    numberoftrueFilteredDeps.append(len(element))


numberoffiltereddeps = []
for element in filtereddeps:
    numberoffiltereddeps.append(len(element))    

numberoftestiwithfiltereddeps = []
for element in testIwithFilteredDeps:
    numberoftestiwithfiltereddeps.append(len(element))    


definitelypositive = []
for i in range(len(f2)):
    if (max([changedf2[i],changedf2deps[i],f2[i],f2deps[i]]) == f2deps[i]) or (max([changedf2[i],changedf2deps[i],f2[i],f2deps[i]]) == changedf2deps):
        definitelypositive.append("Yes")
    else:            
        definitelypositive.append("No")         

circumstantiallypositive = []
for i in range(len(f2)):
    if (       (changedf2[i] < changedf2deps[i] ) and (f2[i]  >= f2deps[i] )   ) or ((changedf2[i]  >= changedf2deps[i] ) and (f2[i]  < f2deps[i])):
        circumstantiallypositive.append("Yes") 
    else:            
        circumstantiallypositive.append("No")


definitelynegative = []
for i in range(len(f2)):
    if (    (changedf2[i]  > changedf2deps[i] ) and (f2[i]  > f2deps[i] )   ):
        definitelynegative.append("Yes")          
    else:            
        definitelynegative.append("No")

noeffectonF2 = []
for i in range(len(f2)):
    if (    (changedf2[i]  == changedf2deps[i] ) and (f2[i]  == f2deps[i])   ):
        noeffectonF2.append("Yes")
    else:            
        noeffectonF2.append("No")    

df['DurationOfTask(Days)'] = days
df['#ChangedFiles'] = numberofchangedfiles
df['#TestIFiles'] = numberoftestifiles
df['TestIWithDeps'] = testIwithDeps
df['#TestIWithDeps'] = numberoftestiwithdeps
df['InclusiveDeps'] = inclusivedeps
df['ExclusiveDeps'] = deps
df['#InclusiveDeps'] = numberofinclusivedeps
df['#ExclusiveDeps'] = numberofexclusivedeps
df['Precision'] = precision
df['Recall'] = recall
df['F2'] = f2
df['PrecisionDeps'] = precisiondeps
df['RecallDeps'] = recalldeps
df['F2Deps'] = f2deps
df['ProductionChangedFiles'] = prodchangedfiles
df['#Prod.ChangedFiles'] = numberofprodchangedfiles
df['TestIwithFilteredDeps'] = testIwithFilteredDeps
df['#TestIwithFilteredDeps'] = numberoftestiwithfiltereddeps
df['ProductionDeps'] = trueFilteredDeps
df['#ProductionDeps'] = numberoftrueFilteredDeps
df['FilteredPrecision'] = changedprecision
df['FilteredRecall'] = changedrecall
df['Filteredf2'] = changedf2
df['FilteredPrecisionDeps'] = changedprecisiondeps
df['FilteredRecallDeps'] = changedrecalldeps
df['Filteredf2Deps'] = changedf2deps
df['#DepsForTask'] = numberofdepsfortask
df['TotalFiles'] = totalfiles
df['ProportionOfChange'] = percentofchange
df['F2Deps - F2'] = f2depsMinusf2 
df['FilteredF2Deps - FilteredF2'] = filteredF2depsMinusFilteredF2
df['RecallDeps - Recall'] = RecallDepsMinusRecall
df['PrecisionDeps - Precision'] = PrecisionDepsMinusPrecision
df['FilteredRecallDeps  - FilteredRecall'] = FilteredRecallDepsMinusFilteredRecall 
df['FilteredPrecisionDeps - FilteredPrecision'] = FilteredPrecisionDepsMinusFilteredPrecision
df['#ExclusiveDeps - #FilteredDeps'] = difference(deps,trueFilteredDeps)
df['AverageF2'] = fill_list([sum(f2)/index],index)
df['AverageF2Deps'] = fill_list([sum(f2deps)/index],index)
df['AverageFilteredF2'] = fill_list([sum(changedf2)/index],index )
df['AverageFilteredF2Deps'] = fill_list([sum(changedf2deps)/index],index)
df['DefinitelyPositive'] = definitelypositive
df['CircumstantiallyPositive'] = circumstantiallypositive
df['DefinitelyNegative'] = definitelynegative
df['NoEffectOnF2'] = noeffectonF2

df.to_csv('TaitiWithdeps_' + repositorio + '( 10% ).csv', index=False)



