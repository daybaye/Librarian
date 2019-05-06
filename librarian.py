# -*- coding: cp1252 -*-
#librarian code created by Deborah Shroder
#Last update: 5/5/2019
#Code takes an input list of faculty and departmental affiliation, an input list of references, and an input list of high impact journals
#Code outputs a list of references with faculty names in bold, a list of the number of papers written per faculty member, a list of all papers published within each department, a list of all papers written in each journal, a list of all papers written in high-impact journals, and a list of all authors appearing in high-impact journals
import codecs
import os

#~~~~~~~~~~~~~~~~~~

##INSTRUCTIONS TO USER
print 'All files must be saved in unicode format'
print 'This code is currently sensitive to diacritical marks (aka Nuñez and Nunez are not the same name)'
print 'All authors should be formatted as: LastName TAB FirstName TAB Division'
print 'All references should be formatted as: Ref#. LastName FirstInitials, LastName FirstInitials, LastName FirstInitials. Title. Journal. Year;Volume(Issue):pages. etc.'
print 'High-impact journal titles should be abbreviated as they appear in the reference list'

##!!!!!!!!!!!!!!!!!!!!!!INPUT FILE NAMES HERE!!!!!!!!!!!!!!!!!!!!!!
##LIST OF ALL REFERNCES TO SEARCH
ref_filename='C:\\Users\\debor\\Downloads\\publications.txt'
##LIST OF ALL FACULTY AUTHORS TO MATCH
author_filename='C:\\Users\\debor\\Downloads\\facultylistaug.txt'

##LIST OF ALL FACULTY IN CROSS-DEPARTMENTAL CENTER
ctsauthor_filename='C:\\Users\\debor\\Downloads\\CTS  faculty list .txt'

##LIST OF ALL HIGH-IMPACT JOURNALS IN FIELD
highimpact_filename='C:\\Users\\debor\\Downloads\\journal title abbreviations2.txt'

##FOLDER FOR OUTPUT RESULTS
folder='C:\\Users\\debor\\Downloads'

##ERROR FILE
errorfile = codecs.open(folder + "\\errors.txt", "w", "utf-16")

while True:
    try:
        data= codecs.open(ref_filename, "r", "utf-16")
        break
    except IOError:
        print 'Reference file does not exist, try again.'
        ref_filename=input('Where is your reference file, and what is it named? Format: "folder\\file.txt" :')
while True:
    try:
        faculty=codecs.open(author_filename, "r", "utf-16")
        break
    except IOError:
        print 'Author file does not exist, try again.'
        author_filename=input('Where is your author list file?: ');
while True:
    try:
        ctsfaculty=codecs.open(ctsauthor_filename, "r", "utf-16")
        break
    except IOError:
        print 'CTS Author file does not exist, try again.'
        ctsauthor_filename=input('Where is your CTS author list file?: ');
while True:
    try:
        highimpact=codecs.open(highimpact_filename, "r", "utf-16")
        break
    except IOError:
        print 'High-impact journal file does not exist, try again.'
        highimpact_filename=input('Where is your high-impact journal abbreviation list?: ');
while True:
    try:
        os.path.isdir(folder)
        break
    except:
        print 'Output folder does not exist, try again.'
        folder=input('What folder should the files output to?')
        
datalines= data.readlines()
facultylines= faculty.readlines()
ctsfacultylines= ctsfaculty.readlines()
highimpactlines= highimpact.readlines()

#~~~~~~~~~~~~~~~~~~

##Empty list creation
authorcounts='';
authorsHI=[];alljournals=[];
alldivisions=[];divisions_count=[];divisions_refs=[];divisions_refsnum=[];divisions_refsct=[];divisions_faculty=[]; divisions_faculty_papercount=[];
journals_refs=[];journals_refsnum=[];journals_refsct=[];


##Adjusting formatting of potentially awkward formatting in input files

for ct in range(len(datalines)):
    datalines[ct]=datalines[ct].replace('? ','?. ')
    datalines[ct]=datalines[ct].replace('! ','!. ')
    datalines[ct]=datalines[ct].replace('; ; ','.')
    datalines[ct]=datalines[ct].replace('[Internet]; ','. [Internet]. ')
    datalines[ct]=datalines[ct].replace(', Jr.',', Jr')
    datalines[ct]=datalines[ct].replace(',Jr.',', Jr')
    if 'et al' in datalines[ct]:
        print '!ET AL ALERT! ' + datalines[ct]
        errorfile.write('!ET AL ALERT! ' + datalines[ct])
for hi in range(len(highimpactlines)):
    highimpactlines[hi]=highimpactlines[hi].replace('\r\n','')
    
##Reading in Faculty Table (Format: LastName TAB FirstName TAB Division)
if 'Last Name' in facultylines[0]:
    start=1
else:
    start=0

for refs in datalines:
    parts = refs.split(".")
    if len(parts)>1:
        if parts[2].count(',')>1 and len(parts)>6:
            print '?EXTRANEOUS PERIOD IN AUTHOR LIST? ' + refs
            errorfile.write('?EXTRANEOUS PERIOD IN AUTHOR LIST? ' + refs)
            names1=parts[1].split(' ')
            names2=parts[2].split(' ')
            print '>>>Two authors, or author + title?: ' + names1[-2] + ' ' + names1[-1] + '. ' + names2[1] + ' ' + names2[2]
            print ' '
            errorfile.write('>>>Two authors, or author + title?: ' + names1[-2] + ' ' + names1[-1] + '. ' + names2[1] + ' ' + names2[2] + '\r\n')
            
        ##Finding location of journal title in reference. Journal title ALWAYS before Year, but extra periods may appear in article title.
        ints='';p=3;n=1;
        while len(ints)<4:
            journal=parts[p]
            try:
                ints=filter(str.isdigit, parts[p+1].encode('ascii','ignore'))
            except IndexError:
                print '!JOURNAL IDENTIFICATION ERROR! ' + refs
                errorfile.write('!JOURNAL IDENTIFICATION ERROR! ' + refs)
                #raise
                journal='Unknown journal'
                break
            p=p+n;
            if p>len(parts)-2:
                n=-1
                
##Going through each faculty name on list, and searching each reference for that name    

for line in facultylines[start:len(facultylines)]:
    parts = line.split("\t");
    lastname = parts[0];
    firstname = parts[1];
    #education = parts[2];
    #division = parts[3];
    division = parts[2];
    CTSdivision=0;
    for cline in ctsfacultylines:
        if lastname in cline and firstname in cline:
            CTSdivision=1;
    ##Creating unique division lists, and organizing references and faculty according to division
    if division not in alldivisions:
        alldivisions.append(division)
        divisions_count.append(0)
        divisions_refs.append([]);
        divisions_refsnum.append([]);
        divisions_refsct.append([]);
        divisions_faculty.append([]);
        divisions_faculty_papercount.append([])
    if CTSdivision is 1:
        if 'CTS' not in alldivisions:
            alldivisions.append('CTS')
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

    if CTSdivision is 1:
        cdi=alldivisions.index('CTS')
        divisions_faculty[cdi].append(firstname + ' ' + lastname)
        divisions_faculty_papercount[cdi].append(0)

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
                    journal='Unknown journal'
                    break
                    
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
                        if parts[0] not in divisions_refsnum[di]:
                            divisions_refsnum[di].append(parts[0])
                            divisions_refsct[di].append(ct)
                        if CTSdivision is 1:
                            if parts[0] not in divisions_refsnum[cdi]:
                                divisions_refsnum[cdi].append(parts[0])
                                divisions_refsct[cdi].append(ct)
                            if parts[0] not in divisions_refsnum[cdi]:
                                divisions_refsnum[cdi].append(parts[0])
                                divisions_refsct[cdi].append(ct)
                            
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
    if CTSdivision is 1:
        cfi=divisions_faculty[cdi].index(divisions_faculty[cdi][len(divisions_faculty[cdi])-1])

    if count > 0:
        divisions_faculty_papercount[di][fi]=count
    
    ##Creating output table of number of papers faculty member has authored
    if CTSdivision is 0:    
        authorcounts=authorcounts + '<tr> <td>' + lastname + '</td><td>' + firstname + '</td><td>' + division + '</td> <td>' + str(count) + '</td> </tr>'
    if CTSdivision is 1:    
        authorcounts=authorcounts + '<tr> <td>' + lastname + '</td><td>' + firstname + '</td><td>' + division + ', CTS' + '</td> <td>' + str(count) + '</td> </tr>'
        divisions_count[cdi]=divisions_count[cdi]+count

    divisions_count[di]=divisions_count[di]+count
    
    

#~~~~~~~~~~~~~~~~~~

##Creating an output list of number of papers per faculty member
authorcounttable=codecs.open(folder + "\\authorcount.htm", "w", "utf-16")
authorcounttable.write('<table style="width:100%">')
authorcounttable.write(authorcounts)           
authorcounttable.write('</table>')
authorcounttable.close()

#~~~~~~~~~~~~~~~~~~

##Creating output list of high-impact faculty members
authorHItable=codecs.open(folder + "\\authorHItable.htm", "w", "utf-16")
authorHItable.write('<table style="width:100%">')
for lines in authorsHI:
    authorHItable.write(lines+ '<br>')
authorHItable.close()

#~~~~~~~~~~~~~~~~~~

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

#~~~~~~~~~~~~~~~~~~

##Writing sorted lists to files    
divisioncount=codecs.open(folder + "\\divisioncount.htm", "w", "utf-16")
divisioncount.write('<table style="width:100%">')
divisioncount.write('<tr> <td>Division</td> <td>Papers Written in Department</td><td>Faculty Members (Number of Papers)</td> </tr>')

divisiontable=codecs.open(folder + "\\divisiontable.htm", "w", "utf-16")
divisiontable.write('<table style="width:100%">')

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

#~~~~~~~~~~~~~~~~~~

journaltable=codecs.open(folder + "\\journaltable.htm", "w", "utf-16")
journaltable.write('<table style="width:100%">')
journalHItable=codecs.open(folder + "\\journalHItable.htm", "w", "utf-16")
journalHItable.write('<table style="width:100%">')

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

#~~~~~~~~~~~~~~~~~~

formattedrefs=codecs.open(folder + '\\formatted_refs.htm', "w", "utf-16")

for refs in datalines:
    if '<b>' not in refs:
        print '!NO FACULTY FOUND!' + refs
        errorfile.write('!NO FACULTY FOUND!' + refs)
        
    formattedrefs.write('<p>'+refs+'</p>')

formattedrefs.close()

#~~~~~~~~~~~~~~~~~~
print 'THESE FACULTY ON CTS LIST BUT NOT REGULAR LIST'
errorfile.write('THESE FACULTY ON CTS LIST BUT NOT REGULAR LIST')
for cline in ctsfacultylines:
    parts = cline.split("\t");
    if len(parts)>1:
        lastname = parts[0];
        firstname = parts[1];
        firstname=firstname.split(' ')[0]
        firstname=firstname.strip('\r\n')
        found=0
        
        for line in facultylines:
            if lastname in line:
                if firstname in line:
                    found=1;
        
        if found is 0:
            print lastname + ' ' + firstname;
            errorfile.write(lastname + ' ' + firstname)
errorfile.close()