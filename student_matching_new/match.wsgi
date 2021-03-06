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

urls = (
	'/', 'index',
	'/match','result',
	'/topframe','topframe',
    	'/content/(.*)/(.*)/(.*)','content'
)

klp_students=None

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
                
                ac_year = db2.query('select distinct b.klp_id,a.ayid,c.name from tb_sikshana_student_data a,school_match_found b,tb_academic_year c where a.school_code=cast(b.school_code as text) and a.ayid=c.id') 

		cls = db2.query('select distinct b.klp_id,a.class from tb_sikshana_student_data a,school_match_found b where a.school_code=cast(b.school_code as text)')
		
		return render.topframe(district_query,block_query,cluster_query,school_query,ac_year,cls)

class content:
	def GET(SELF,sch,cls,ac_id):
		klp_students = [] 
		if klp_students is None:
			result=db2.query('select s_fewer.student_id,initcap(c.first_name) as first_name,c.middle_name,initcap(c.last_name) as last_name from (select distinct student_id from vw_schools_student_studentgrouprelation where student_group_id in ((select distinct id from vw_schools_studentgroup where institution_id=$name and name =\'7\' and group_type=\'Class\')) and academic_id=$aid) as s_fewer,vw_schools_child c,vw_schools_student s where s_fewer.student_id not in (select distinct klp_id from student_match_found) and s_fewer.student_id = s.id and s.child_id = c.id order by first_name',{"name":sch,"class":cls,"aid":ac_id})
			klp_students=[[row.student_id,row.first_name,row.middle_name,row.last_name] for row in result]

		sikshana_student=db2.query('select a.student_id,a.student_name,a.ayid,a.class,b.klp_id from tb_sikshana_student_data a,school_match_found b where a.school_code=cast(b.school_code as text) and a.ayid='102' and a.class='7' and a.student_id not in(select distinct student_id from student_match_found) order by a.student_name')
		
		sikshana_students=[[row.student_id,row.student_name] for row in cstudent]

		return render.display(klp_students,sikshana_students)


application = web.application(urls,globals()).wsgifunc()


class result:
    def POST(self):
	inputs=web.input()

	if str(inputs.sikshana_value)!='' and str(inputs.klp_value)!='':
		queryvalues["klpcode"]=str(inputs.klp_value).split("|")[0]
		queryvalues["klpname"]=str(inputs.klp_value).split("|")[1]
		queryvalues["studentcode"]=str(inputs.sikshana_value).split("|")[0]
		queryvalues["studentname"]=str(inputs.sikshana_value).split("|")[1]
		
		db2.query('insert into student_match_found values($studentcode,$studentname,$klpcode,$klpname)',queryvalues)
	
	return render.display()
        #raise web.seeother('/content/'+str(inputs.matched_value).split("|")[0]+'/'+str(inputs.matched_value).split("|")[1]+'/'+str(inputs.matched_value).split("|")[2])


