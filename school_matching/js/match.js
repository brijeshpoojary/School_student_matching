function replaceAll(txt, replace, with_this) {
  return txt.replace(new RegExp(replace,'g'),with_this);
}


function filter(value){
	
  	var klptable = document.getElementById("ssdata");
	var csvtable = document.getElementById("sedata");
	var school;
	
	
	for(var i=1;i<klptable.rows.length;i++){
		school=klptable.rows[i].innerHTML.replace(/<[^>]+>/g,"|").split("|")[3];
		res=school.toLowerCase().match(value.toLowerCase());
		if(res==value.toLowerCase()){
			klptable.rows[i].style.display='';
		}
		else{
			klptable.rows[i].style.display='none';
		}
	}

	for(var i=1;i<csvtable.rows.length;i++){
		school=csvtable.rows[i].innerHTML.replace(/<[^>]+>/g,"|").split("|")[3];
		res=school.toLowerCase().match(value.toLowerCase());
		if(res==value.toLowerCase()){
			csvtable.rows[i].style.display='';
		}
		else{
			csvtable.rows[i].style.display='none';
		}
	}
}

function clicks(value,type){
	if(type==1){
		var table=document.getElementById('ssdata');
		for(var i=0;i<=table.rows.length-1;i++){
			table.rows[i].bgColor='#FFFFFF';
		}	
	} else {
		table=document.getElementById('sedata');
		for(var i=0;i<=table.rows.length-1;i++){
			table.rows[i].bgColor='#FFFFFF';
		}
	}				
	if(value.bgColor=='#FFD700'){
	 	value.bgColor='#FFFFFF';
		if(type==1){
			var sslc=document.getElementById('db_value');
			sslc.value='';
		
		}
		else{
			var semis=document.getElementById('csv_value');
			semis.value='';
		
		}	
	
	}
	else
	{
	 	value.bgColor='#FFD700';
		if(type==1){
			
			
			var sslc=document.getElementById('db_value');
			value_list= replaceAll(value.innerHTML,"<td>","");
			value_list= replaceAll(value_list,"</td>","|");
			value_list= value_list.substring(0,value_list.length-2);
                        //alert(value_list);
			value_list= value_list.split("|");
			sslc.value=value_list.join("|");
		}
		else{
			var semis=document.getElementById('csv_value');
			value_list= replaceAll(value.innerHTML,"<td>","");
			value_list= replaceAll(value_list,"</td>","|");
			value_list= value_list.substring(0,value_list.length-2);
                        //alert(value_list);
			value_list= value_list.split("|");
			semis.value=value_list.join("|");
		}
	}
}

function myfunction()
{
	var x;
	var r=confirm("Sure you want to continue..??");
	if (r==true)
  	{
		var clst=document.URL.split("/");
		document.getElementById("clst").value=clst[clst.length-2]+"|"+clst[clst.length-1];
		document.forms["form1"].submit();
		
 	 }
	else
	{
		alert('hi');
	}
}
