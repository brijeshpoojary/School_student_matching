
function callpage(value){
	var db=document.getElementById("clust");
	var csv=document.getElementById("cclust");

	parent.content.location.href="content/"+trim(db.value)+"/"+trim(csv.value);

}

function change_focus(id,type,flag)
{
	var data='';
	var element=document.getElementById(type);
	if(type=='blk')
		data=block;
	else if(type=='clust')
		data=cluster;
	else if(type=='cblk')
		data=cblk;
	else if(type=='cclust')
		data=cclust;
	element.length=1;
	for(var i=0;i<data.length-1;i++){
		if(trim(data[i][0])==trim(id)){
			if(flag==1)
				element.options[element.length]=new Option(data[i][2],data[i][1]);
			else{
				element.options[element.length]=new Option(data[i][1],data[i][1]);
			}
		}
	}
}

function trim(value){
//	alert(value);
	while(value[value.length-1]==' ')
		value=value.substring(0,value.length-1);
	while(value[0]==' ')
		value=value.substring(1);
//	alert(value);
	return value;
}
