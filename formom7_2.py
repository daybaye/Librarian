# -*- coding: cp1252 -*-
#FORMOM code created by Deborah Shroder
#Last update: 7/5/2018
#Code takes an input list of faculty and departmental affiliation, an input list of references, and an input list of high impact journals
#Code outputs a list of references with faculty names in bold, a list of the number of papers written per faculty member, a list of all papers published within each department, a list of all papers written in each journal, a list of all papers written in high-impact journals, and a list of all authors appearing in high-impact journals

##INSTRUCTIONS TO USER
print 'This code is currently sensitive to diacritical marks (aka Nuñez and Nunez are not the same name)'
print 'All authors should be formatted as: LastName TAB FirstName TAB Division'
print 'All references should be formatted as: Ref#. LastName FirstInitials, LastName FirstInitials, LastName FirstInitials. Title. Journal. Year;Volume(Issue):pages. etc.'
print 'High-impact journal titles should be abbreviated as they appear in the reference list'
import sys

##Give user option of messing with actual code, or just clicking 'Run'
easycode=str(raw_input('Do you want to be prompted for filenames? (Yes)...or have you inserted filenames into the code? (No): '))

##Input filenames into command line
if 'Y' in easycode:
    print 'Input files in format: "C:\\USER\\Folder\\file.txt"'
    while True:
        try:    ref_filename=input('Where is your reference file (saved in unicode format), and what is it named? Format: "folder\\file.txt" :');break
        except SyntaxError: print 'Oops! Syntax Error. Try again!'
    while True:
        try:    author_filename=input('Where is your author list file?: ');break
        except SyntaxError: print 'Oops! Syntax Error. Try again!'
    while True:
        try:    highimpact_filename=input('Where is your high-impact journal abbreviation list?: ');break
        except SyntaxError: print 'Oops! Syntax Error. Try again!'
    while True:
        try:    folder=input('What folder should the files output to?');break
        except SyntaxError: print 'Oops! Syntax Error. Try again!'


else:
    ##!!!!!!!!!!!!!!!!!!!!!!INPUT FILE NAMES HERE!!!!!!!!!!!!!!!!!!!!!!
    ref_filename='C:\\Users\\Deborah\\Downloads\\publications2.txt'
    author_filename="C:\\Users\\Deborah\Downloads\\facultylistjul.txt"
    highimpact_filename="C:\\Users\\Deborah\Downloads\\journal title abbreviations1.txt"
    folder="C:\\Users\\Deborah\\Downloads"
    
import codecs
while True:
    try:    data= codecs.open(ref_filename, "r", "utf-16");break
    except IOError: print 'Reference file does not exist, try again.';ref_filename=input('Where is your reference file (saved in unicode format), and what is it named? Format: "folder\\file.txt" :')
while True:
    try:    faculty=codecs.open(author_filename, "r", "utf-16");break
    except IOError: print 'Author file does not exist, try again.';author_filename=input('Where is your author list file?: ');
while True:
    try:    highimpact=codecs.open(highimpact_filename, "r", "utf-16");break
    except IOError: print 'High-impact journal file does not exist, try again.';highimpact_filename=input('Where is your high-impact journal abbreviation list?: ');

datalines= data.readlines()
facultylines= faculty.readlines()
highimpactlines= highimpact.readlines()

authorcount_filename=folder + "\\authorcount.htm"

##Creating output files
while True:
    try:    authorcounttable=codecs.open(authorcount_filename, "w", "utf-16");authorcounttable.write('<table style="width:100%">');break
    except IOError: print 'Output folder does not exist, please create it or re-enter';folder=input('What folder should the files output to?');
divisiontable=codecs.open(folder + "\\divisiontable.htm", "w", "utf-16");divisiontable.write('<table style="width:100%">')
divisioncount=codecs.open(folder + "\\divisioncount.htm", "w", "utf-16");divisioncount.write('<table style="width:100%">')
journaltable=codecs.open(folder + "\\journaltable.htm", "w", "utf-16");journaltable.write('<table style="width:100%">')
journalHItable=codecs.open(folder + "\\journalHItable.htm", "w", "utf-16");journalHItable.write('<table style="width:100%">')
authorHItable=codecs.open(folder + "\\authorHItable.htm", "w", "utf-16");authorHItable.write('<table style="width:100%">')

##Empty list creation
authorsHI=[];alljournals=[];
alldivisions=[];divisions_count=[];divisions_refs=[];divisions_refsnum=[];divisions_refsct=[];divisions_faculty=[]; divisions_faculty_papercount=[];
journals_refs=[];journals_refsnum=[];journals_refsct=[];

##Adjusting formatting of potentially awkward formatting in input files
for ct in range(len(datalines)):
    datalines[ct]=datalines[ct].replace('? ','?. ')
    datalines[ct]=datalines[ct].replace('! ','!. ')
    datalines[ct]=datalines[ct].replace('; ; ','.')
    datalines[ct]=datalines[ct].replace('[Internet]; ','. [Internet]. ')
    if 'et al' in datalines[ct]:
        print '!ET AL ALERT! ' + datalines[ct]
for hi in range(len(highimpactlines)):
    highimpactlines[hi]=highimpactlines[hi].replace('\r\n','')
    highimpactlines[hi]=highimpactlines[hi].replace(' ','')

##Reading in Faculty Table (Format: LastName TAB FirstName TAB Division)
if 'Last Name' in facultylines[0]:
    start=1
else:
    start=0

##Going through each faculty name on list, and searching each reference for that name    

for line in facultylines[start:len(facultylines)]:
    parts = line.split("\t");
    lastname = parts[0];
    firstname = parts[1];
    #education = parts[2];
    #division = parts[3];
    division = parts[2];

    ##Creating unique division lists, and organizing references and faculty according to division
    if division not in alldivisions:
        alldivisions.append(division)
        divisions_count.append(0)
        divisions_refs.append([]);
        divisions_refsnum.append([]);
        divisions_refsct.append([]);
        divisions_faculty.append([]);
        divisions_faculty_papercount.append([])
        
    di=alldivisions.index(division)
    #divisions_faculty[di].append(firstname + ' ' + lastname + ', ' + education)
    divisions_faculty[di].append(firstname + ' ' + lastname)
    divisions_faculty_papercount[di].append(0)

    ##Creating author search term
    searchterm=lastname + ' '+firstname[0]
    count=0
    ct=0
    for refs in datalines:
        parts = refs.split(".")
        if len(parts)>1:
            ##Finding location of journal title in reference. Journal title ALWAYS before Year, but extra periods may appear in article title.
            ints='';p=3;n=1;
            while len(ints)<4:
                journal=parts[p]
                try:
                    ints=filter(str.isdigit, parts[p+1].encode('ascii','ignore'))
                except IndexError:
                    print 'Check formatting of: ' + refs
                    raise
                    
                p=p+n;
                if p>len(parts)-2:
                    n=-1
            ##Creating unique journals list, and organizing references according to journal                    
            if journal not in alljournals:
                alljournals.append(journal)
                journals_refs.append([]);
                journals_refsnum.append([]);
                journals_refsct.append([]);

            ji=alljournals.index(journal)

            ##Searching authors in reference for faculty name
            for authors in parts[1].split(','):
                if len(authors)>2:
                    firstinitial=authors.split()[-1][0]
                    last=''.join(authors.split()[0:-1])
                    if (last.upper()==lastname.upper().replace(' ','') and firstinitial==firstname[0]):
                        count=count+1
                        ##Bolding name of faculty member in reference
                        datalines[ct]=refs.replace(authors, '<b>'+authors+'</b>')
                        ##adding reference to division's list
                        if parts[0] not in divisions_refsnum[di]:
                            divisions_refsnum[di].append(parts[0])
                            divisions_refsct[di].append(ct)
                        ##adding reference to journal's list
                        if parts[0] not in journals_refsnum[ji]:
                            journals_refsnum[ji].append(parts[0])
                            journals_refsct[ji].append(ct)
                        ##adding author to high-impact authors list
                        if journal.replace(' ','') in highimpactlines:
                            name=lastname + ', ' + firstname
                            if name not in authorsHI:
                                authorsHI.append(name)
        ct=ct+1

    fi=divisions_faculty[di].index(divisions_faculty[di][len(divisions_faculty[di])-1])

    if count > 0:
        divisions_faculty_papercount[di][fi]=count
    ##Creating output table of number of papers faculty member has authored
    authorcounttable.write('<tr> <td>' + lastname + '</td><td>' + firstname + '</td><td>' + division + '</td> <td>' + str(count) + '</td> </tr>')
    divisions_count[di]=divisions_count[di]+count
    if len(divisions_refsnum[di])!=len(divisions_refsct[di]):
        print 'Error!' + refs
                        
           
authorcounttable.write('</table>')
authorcounttable.close()

##Creating output list of high-impact faculty members
for lines in authorsHI:
    authorHItable.write(lines+ '<br>')
authorHItable.close()

##Creating output list of references sorted by division    
for di in range(0,len(alldivisions)):
    if len(divisions_refsct[di]) > 0:
        divisions_refsct[di]=sorted(divisions_refsct[di])
        for ct in divisions_refsct[di]:
            divisions_refs[di].append(datalines[ct])
            dl=divisions_refsct[di].index(ct)
            parts2=datalines[ct].split(".")
            divisions_refs[di][dl]=".".join(parts2[1:len(parts2)]) + '<br>'

##Creating output list of references sorted by journal                
for ji in range(0,len(alljournals)):
    if len(journals_refsct[ji]) > 0:
        journals_refsct[ji]=sorted(journals_refsct[ji])
        for ct in journals_refsct[ji]:
            journals_refs[ji].append(datalines[ct])
            jl=journals_refsct[ji].index(ct)
            parts2=datalines[ct].split(".")
            journals_refs[ji][jl]=".".join(parts2[1:len(parts2)]) + '<br>'

##Writing sorted lists to files    
divisioncount.write('<tr> <td>Division</td> <td>Papers Written in Department</td><td>Faculty Members (Number of Papers)</td> </tr>')

for division in alldivisions:
    di=alldivisions.index(division)

    divisioncount.write('<tr> <td>' + division + '</td> <td>' + str(divisions_count[di]) + '</td><td>')
    for faculty in divisions_faculty[di]:
        fi=divisions_faculty[di].index(faculty)
        divisioncount.write(faculty + ' (' + str(divisions_faculty_papercount[di][fi]) + ') <br>')
    divisioncount.write('</td> </tr>')
    
    divisiontable.write('<tr> <td>' + division + '</td> <td>')
    for lines in divisions_refs[di]:
        li=divisions_refs[di].index(lines)
        divisiontable.write(str(li+1) + '. ' + lines)

    divisiontable.write('</td> </tr>')

divisiontable.close()
divisioncount.close()

for journal in alljournals:
    ji=alljournals.index(journal)
    
    journaltable.write('<tr> <td>' + journal + '</td> <td>')
    for lines in journals_refs[ji]:
        li=journals_refs[ji].index(lines)
        journaltable.write(str(li+1) + '. ' + lines)

    journaltable.write('</td> </tr>')

    if journal.replace(' ','') in highimpactlines:
        journalHItable.write('<tr> <td>' + journal + '</td> <td>')
        for lines in journals_refs[ji]:
            li=journals_refs[ji].index(lines)
            journalHItable.write(str(li+1) + '. ' + lines)

journaltable.close()
journalHItable.close()

filename=folder + '\\formatted_refs.htm'
output=codecs.open(filename, "w", "utf-16")

for refs in datalines:
    output.write('<p>'+refs+'</p>')

output.close()

