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

db1=web.database(dbn='postgres',user='klp',password='chang3d1t',db='semis')
db2=web.database(dbn='postgres',user='klp',password='chang3d1t',db='sikshana')

urls = (
	'/', 'index',
	'/go','result',
	'/topframe','topframe',
    	'/content/(.*)/(.*)/(.*)','content'
)

values={"dist":""}
queryvalues={"klpcode":"","klpname":"","studentcode":"","studentname":"","district":"","block":"","cluster":""}


class prints:
	def GET(SELF):
		return render.prints()

class index:
	def GET(SELF):
		return render.main()

class topframe:
	def GET(SELF):
		district_query = db2.query('select distinct b3.id,b3.name from school_match_found a, vw_institution s, vw_boundary b1, vw_boundary b2,vw_boundary b3 where a.klp_id=s.id and s.boundary_id = b1.id and b1.parent_id=b2.id and b2.parent_id=b3.id and b3.parent_id=1 and b3.boundary_type_id=1 order by b3.name')
	
		block_query = db2.query('select distinct b2.id,b2.name,b2.parent_id from school_match_found a, vw_institution s, vw_boundary b1, vw_boundary b2,vw_boundary b3 where a.klp_id=s.id and s.boundary_id = b1.id and b1.parent_id=b2.id and b2.parent_id=b3.id and b3.parent_id=1 and b3.boundary_type_id=1 order by b2.name')

		cluster_query = db2.query('select distinct b1.id,b1.name,b1.parent_id from school_match_found a, vw_institution s, vw_boundary b1, vw_boundary b2,vw_boundary b3 where a.klp_id=s.id and s.boundary_id = b1.id and b1.parent_id=b2.id and b2.parent_id=b3.id and b3.parent_id=1 and b3.boundary_type_id=1 order by b1.name')
	
        	school_query = db2.query('select distinct a.klp_id as id,a.klp_school_name as name,b1.id as clust_id from school_match_found a, vw_institution s, vw_boundary b1, vw_boundary b2,vw_boundary b3 where a.klp_id=s.id and s.boundary_id = b1.id and s.active=2 and b1.parent_id=b2.id and b2.parent_id=b3.id and b3.parent_id=1 and b3.boundary_type_id=1 order by a.klp_school_name')

		fp=csv.reader(open('/home/brijesh/school_student_matching/student_matching/data/sikshanstudents.csv','r'),delimiter='|')
		fp.next()
		klp_id=[]
		ay_id=[]
		cls=[]
		schools=[row for row in fp]
		for row in schools:
			if row[0] not in klp_id:
				klp_id.append(row[0])
		for row in schools:
			if [row[0],row[1]] not in ay_id:
				ay_id.append([row[0],row[1]])
		for row in schools:
			if [row[0],row[2]] not in cls:
				cls.append([row[0],row[2]])
		
		return render.topframe(district_query,block_query,cluster_query,school_query,klp_id,ay_id,cls)

class content:
	def GET(SELF,sch,cls,ac_id):
		dstudents=db2.query('select s_fewer.student_id,c.first_name,c.middle_name,c.last_name from (select distinct student_id from vw_schools_student_studentgrouprelation where student_group_id in ((select distinct id from vw_schools_studentgroup where institution_id=$name and name =\'7\' and group_type=\'Class\')) and academic_id=$aid) as s_fewer,vw_schools_child c,vw_schools_student s where s_fewer.student_id not in (select distinct klp_id from student_match_found) and s_fewer.student_id = s.id and s.child_id = c.id order by c.first_name',{"name":sch,"class":cls,"aid":ac_id})
		fp1=csv.reader(open('/home/brijesh/school_student_matching/student_matching/data/sikshanstudents.csv','r'),delimiter='|')
		fp1.next()
		fp=sorted(fp1)
		student_ids=db2.query('select distinct student_id from student_match_found')
		stud_ids=[str(row.student_id) for row in student_ids]
		print stud_ids
		cstudents=[row for row in fp if row[0].strip() == sch.strip() and row[4].strip() not in stud_ids]
		return render.display(dstudents,cstudents)


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
		queryvalues["studentcode"]=str(inputs.csv_value).split("|")[0]
		queryvalues["studentname"]=str(inputs.csv_value).split("|")[1]
		
		db2.query('insert into student_match_found values($studentcode,$studentname,$klpcode,$klpname)',queryvalues)
	
        raise web.seeother('/content/'+str(inputs.box).split("|")[0]+'/'+str(inputs.box).split("|")[1]+'/'+str(inputs.box).split("|")[2])
