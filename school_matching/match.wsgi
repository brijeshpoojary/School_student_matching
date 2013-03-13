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
	'/go','result',
	'/topframe','topframe',
        '/content/(.*)/(.*)','content'
)

values={"dist":""}
queryvalues={"klpcode":"","klpname":"","schoolcode":"","schoolname":"","district":"","block":"","cluster":""}


class prints:
	def GET(SELF):
		return render.prints()

class index:
	def GET(SELF):
		return render.main()

class topframe:
	def GET(SELF):
		district_query = db2.query('select distinct cast(b3.id as text),b3.name from vw_institution s, vw_boundary b1, vw_boundary b2,vw_boundary b3 where s.boundary_id = b1.id and b1.parent_id=b2.id and b2.parent_id=b3.id and b3.parent_id=1 and b3.boundary_type_id=1')
	
		block_query = db2.query('select distinct cast(b2.id as text),b2.name,b2.parent_id from vw_institution s, vw_boundary b1, vw_boundary b2,vw_boundary b3 where s.boundary_id = b1.id and b1.parent_id=b2.id and b2.parent_id=b3.id and b3.parent_id=1 and b3.boundary_type_id=1')

		cluster_query = db2.query('select distinct cast(b1.id as text),b1.name,b1.parent_id from vw_institution s, vw_boundary b1, vw_boundary b2,vw_boundary b3 where s.boundary_id = b1.id and b1.parent_id=b2.id and b2.parent_id=b3.id and b3.parent_id=1 and b3.boundary_type_id=1')
		fp=csv.reader(open('/home/brijesh/school_student_matching/school_matching/data/sikshanaschools.csv','r'),delimiter='|')
		fp.next()
		district=[]
		block=[]
		cluster=[]
		schools=[row for row in fp]
		for row in schools:
			if row[0] not in district:
				district.append(row[0])
		for row in schools:
			if [row[0],row[1]] not in block:
				block.append([row[0],row[1]])
		for row in schools:
			if [row[1],row[2]] not in cluster:
				cluster.append([row[1],row[2]])

		return render.topframe(district_query,block_query,cluster_query,district,block,cluster)

class content:
	def GET(SELF,dbid,csvid):
		dschools=db2.query('select cast(s.id as text) as school_code,s.name as school_name from vw_institution s, vw_boundary b1, vw_boundary b2,vw_boundary b3 where s.boundary_id = b1.id and b1.parent_id=b2.id and b2.parent_id=b3.id and b3.boundary_type_id=1 and b3.boundary_category_id=9 and s.id not in (select distinct klp_id from school_match_found) and cast(b1.id as text)=''$name'' order by s.name',{"name":dbid})
		fp=csv.reader(open('/home/brijesh/school_student_matching/school_matching/data/sikshanaschools.csv','r'),delimiter='|')
		fp.next()
		school_ids=db2.query('select distinct cast(school_code as text) from school_match_found')
		school_ids=[row.school_code for row in school_ids]
		cschools=[row for row in fp if row[2].strip().upper() == csvid.strip().upper() and row[3].strip() not in school_ids]
		return render.content(dschools,cschools)


"""class index:
	def GET(SELF):
			#dists,blcks,clsts,schls=[],[],[],[]
			fp=csv.reader(open('/home/brijesh/school_student_matching/school_matching/sikshanaschools.csv','r'),delimiter='|')
			fp.next()
			district_query = db2.query('select distinct cast(b3.id as text),b3.name from schools_institution s, schools_boundary b1, schools_boundary b2,schools_boundary b3 where s.boundary_id = b1.id and b1.parent_id=b2.id and b2.parent_id=b3.id and b3.parent_id=1 and b3.boundary_type_id=1')

			block_query = db2.query('select distinct cast(b2.id as text),b2.name,b2.parent_id from schools_institution s, schools_boundary b1, schools_boundary b2,schools_boundary b3 where s.boundary_id = b1.id and b1.parent_id=b2.id and b2.parent_id=b3.id and b3.parent_id=1 and b3.boundary_type_id=1')

                        cluster_query = db2.query('select distinct cast(b1.id as text),b1.name,b1.parent_id from schools_institution s, schools_boundary b1, schools_boundary b2,schools_boundary b3 where s.boundary_id = b1.id and b1.parent_id=b2.id and b2.parent_id=b3.id and b3.parent_id=1 and b3.boundary_type_id=1')

			cluster=[]
			cluster_name=''
			school_ids=db2.query('select distinct cast(school_code as text) from school_match_found')
			school_ids=[row.school_code for row in school_ids]
			
			for row in cluster_query:
				cluster.append([row.id,row.name])
			for row in cluster:
				if row[0]==values['dist']:
					cluster_name=row[1]
			
			schools=[row for row in fp if row[2].strip().upper() == cluster_name.strip().upper() and row[3].strip() not in school_ids]
			klp_schools = db2.query('select cast(s.id as text) as school_code,s.name as school_name,b3.name as district,b2.name as block,b1.name as cluster from schools_institution s, schools_boundary b1, schools_boundary b2,schools_boundary b3 where s.boundary_id = b1.id and b1.parent_id=b2.id and b2.parent_id=b3.id and b3.boundary_type_id=1 and b3.boundary_category_id=9 and s.id not in (select distinct klp_id from school_match_found) and cast(b1.id as text)=''$dist'' order by s.name,b2.name',values)	
			return render.compare(district_query,values,schools,klp_schools,block_query,cluster_query)"""
				

application = web.application(urls,globals()).wsgifunc()


class result:
    def POST(self):
	inputs=web.input()
	global values
	if str(inputs.db_value)!='' and str(inputs.csv_value)!='':
		queryvalues["klpcode"]=str(inputs.db_value).split("|")[0]
		queryvalues["klpname"]=str(inputs.db_value).split("|")[1]
		queryvalues["schoolcode"]=str(inputs.csv_value).split("|")[0]
		queryvalues["schoolname"]=str(inputs.csv_value).split("|")[1]
		
		db2.query('insert into school_match_found values($klpcode,$klpname,$schoolcode,$schoolname)',queryvalues)
	
        raise web.seeother('/content/'+str(inputs.clst).split("|")[0]+'/'+str(inputs.clst).split("|")[1])
