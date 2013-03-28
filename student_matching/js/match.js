function replaceAll(txt, replace, with_this) {
<<<<<<< HEAD
  return txt.replace(new RegExp(replace,'g'),with_this);
}


function filter(value){
	
  	var klptable = document.getElementById("ssdata");
	var csvtable = document.getElementById("sedata");
	var school;
	
	
	/*for(var i=1;i<klptable.rows.length;i++){
		school=klptable.rows[i].innerHTML.replace(/<[^>]+>/g,"|").split("|")[3];
		res=school.toLowerCase().match(value.toLowerCase());
		if(res==value.toLowerCase()){
			klptable.rows[i].style.display='';
		}
		else{
			klptable.rows[i].style.display='none';
		}
	}*/

	for(var i=1;i<csvtable.rows.length;i++){
		school=csvtable.rows[i].innerHTML.replace(/<[^>]+>/g,"|").split("|")[3];
		res=school.toLowerCase().match(value.toLowerCase());
		if(res==value.toLowerCase()){
			csvtable.rows[i].style.display='';
		}
		else{
			csvtable.rows[i].style.display='none';
=======
  return txt.replace(new RegExp(replace, 'g'),with_this);
}

function filter(value){
	
  	var sslctable = document.getElementById("ssdata");
	var semistable = document.getElementById("sedata");
	var school;
	
	
	for(var i=1;i<sslctable.rows.length;i++){
		school=sslctable.rows[i].innerHTML.replace(/<[^>]+>/g,"|").split("|")[3];
		res=school.toLowerCase().match(value.toLowerCase());
		if(res==value.toLowerCase()){
			sslctable.rows[i].style.display='';
		}
		else{
			sslctable.rows[i].style.display='none';
		}
	}

	for(var i=1;i<semistable.rows.length;i++){
		school=semistable.rows[i].innerHTML.replace(/<[^>]+>/g,"|").split("|")[3];
		res=school.toLowerCase().match(value.toLowerCase());
		if(res==value.toLowerCase()){
			semistable.rows[i].style.display='';
		}
		else{
			semistable.rows[i].style.display='none';
>>>>>>> 9efe44e78bbd31c8f1ca67d77f3ea0bf77c758d9
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
<<<<<<< HEAD
			var sslc=document.getElementById('csv_value');
=======
			var sslc=document.getElementById('sslc');
>>>>>>> 9efe44e78bbd31c8f1ca67d77f3ea0bf77c758d9
			sslc.value='';
		
		}
		else{
<<<<<<< HEAD
			var semis=document.getElementById('db_value');
			semis.value='';
		
		}	
	
=======
			var semis=document.getElementById('semis');
			semis.value='';
		
		}			
>>>>>>> 9efe44e78bbd31c8f1ca67d77f3ea0bf77c758d9
	}
	else
	{
	 	value.bgColor='#FFD700';
		if(type==1){
<<<<<<< HEAD
			
			
			var sslc=document.getElementById('csv_value');
=======
			var sslc=document.getElementById('sslc');
>>>>>>> 9efe44e78bbd31c8f1ca67d77f3ea0bf77c758d9
			value_list= replaceAll(value.innerHTML,"<td>","");
			value_list= replaceAll(value_list,"</td>","|");
			value_list= value_list.substring(0,value_list.length-2);
                        //alert(value_list);
			value_list= value_list.split("|");
<<<<<<< HEAD
			sslc.value=value_list.join("|");
		}
		else{
			var semis=document.getElementById('db_value');
			value_list= replaceAll(value.innerHTML,"<td>","");
			value_list= replaceAll(value_list,"</td>","|");
			value_list= value_list.substring(0,value_list.length-1);
                        //alert(value_list);
			value_list= value_list.split("|");
			semis.value=value_list.join("|");
=======
			sslc.value= value_list.join("|");
			//alert(sslc.value);

		}
		else{
			var semis=document.getElementById('semis');
			value_list= replaceAll(value.innerHTML,"<td>","");
			value_list= replaceAll(value_list,"</td>","|");
			value_list= value_list.substring(0,value_list.length-2);
                        //alert(value_list);
			value_list= value_list.split("|");
			semis.value=value_list.join( "|");
			//alert(semis.value);

>>>>>>> 9efe44e78bbd31c8f1ca67d77f3ea0bf77c758d9
		}
	}
}

function myfunction()
{
	var x;
	var r=confirm("Sure you want to continue..??");
	if (r==true)
  	{
<<<<<<< HEAD
		var data=document.URL.split("/");
		document.getElementById("box").value=data[data.length-3]+"|"+data[data.length-2]+"|"+data[data.length-1];
=======
		
>>>>>>> 9efe44e78bbd31c8f1ca67d77f3ea0bf77c758d9
		document.forms["form1"].submit();
		
 	 }
	else
<<<<<<< HEAD
	{
		alert('hi');
	}
=======
  	{
  		alert('You pressed Cancel!');
  	}
}

function district_change()
{
	document.getElementById('sslc').value='';	
	document.getElementById('semis').value='';
	document.forms["form1"].submit();
>>>>>>> 9efe44e78bbd31c8f1ca67d77f3ea0bf77c758d9
}
