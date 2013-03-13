import socket
import csv
import web
import json

import sys, os,traceback
abspath = os.path.dirname(os.path.abspath(__file__))
#print abspath
if abspath not in sys.path:
	sys.path.append(abspath)
if abspath+'/templates' not in sys.path:
	sys.path.append(abspath+'/templates')

os.chdir(abspath)

render = web.template.render('templates/')

db1=web.database(dbn='postgres',user='klp',pw='hello',db='semis')
db2=web.database(dbn='postgres',user='klp',pw='azsxdcfv',db='sikshana')

urls = (
	'/', 'index',
	'/go','result'
)

values={"dist":""}
queryvalues={"klpcode":"","klpname":"","schoolcode":"","schoolname":"","district":"","block":"","cluster":""}


class prints:
	def GET(SELF):
		return render.prints()

class index:
	def GET(SELF):
			#dists,blcks,clsts,schls=[],[],[],[]
			fp=csv.reader(open('/home/brijesh/school_student_matching/student_matching/sikshanaschools.csv','r'),delimiter='|')
			fp.next()
			district_query = db1.query('select distinct cast(b3.id as text),b3.name from schools_institution s, schools_boundary b1, schools_boundary b2,schools_boundary b3 where s.boundary_id = b1.id and b1.parent_id=b2.id and b2.parent_id=b3.id and b3.parent_id=1 and b3.boundary_type_id=1')
			district=[]
			district_name=''
			school_ids=db2.query('select distinct cast(school_code as text) from school_match_found')
			school_ids=[row.school_code for row in school_ids]
			
			for row in district_query:
				district.append([row.id,row.name])
			for row in district:
				if row[0]==values['dist']:
					district_name=row[1]
			
			schools=[row for row in fp if row[0].strip().upper() == district_name.strip().upper() and row[3].strip() not in school_ids]
			klp_schools = db2.query('select cast(s.id as text) as school_code,s.name as school_name,b3.name as district,b2.name as block,b1.name as cluster from vw_institution s, vw_boundary b1, vw_boundary b2,vw_boundary b3 where s.boundary_id = b1.id and b1.parent_id=b2.id and b2.parent_id=b3.id and b3.boundary_type_id=1 and s.id not in (select distinct klp_id from school_match_found) and cast(b3.id as text)=''$dist'' order by s.name',values)	
			return render.compare(district,values,schools,klp_schools)
				

application = web.application(urls,globals()).wsgifunc()


class result:
    def POST(self):
	inputs=web.input()
	global values
	if str(inputs.sslc)!='' and str(inputs.semis)!='':
		queryvalues["klpcode"]=str(inputs.sslc).split("|")[3]
		queryvalues["klpname"]=str(inputs.sslc).split("|")[4]
		queryvalues["schoolcode"]=str(inputs.semis).split("|")[3]
		queryvalues["schoolname"]=str(inputs.semis).split("|")[4]
		queryvalues["district"]=str(inputs.semis).split("|")[0]
		queryvalues["block"]=str(inputs.semis).split("|")[1]
		queryvalues["cluster"]=str(inputs.semis).split("|")[2]
		db1.query('insert into school_match_found values($klpcode,$klpname,$schoolcode,$schoolname,$district,$block,$cluster)',queryvalues)
		db2.query('insert into school_match_found values($klpcode,$klpname,$schoolcode,$schoolname)',queryvalues)
	values["dist"]=str(inputs.dist)
        raise web.seeother('/')
