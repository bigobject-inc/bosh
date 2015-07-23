import requests
import json
import sys

def cmd2JSON(cmd):
	return json.dumps({'Stmt':cmd,'Workspace':"",'Opts':{}})

def getData(server,cmdStr):
	r = requests.post(server,data=cmd2JSON(cmdStr) , stream=True)
	#print(r.raw)
	#print("*************************")
	total_row = 0
	for content in json_stream(r.raw):
		total_row += printdata(json.dumps(content))
		#if(total_row > 10000):
		#	resDataSave()
	print("total row : " + str(total_row))	

def json_stream(fp):
	for line in fp:
		#print(line)
		yield json.loads(line)

#def resDataSave()
#	confirmStr= "Size of data exceeded display limit, dump to csv format? (yes/no)"
#        import fileinput
#        print confirmStr
#        while True:
#        	choice=raw_input()
#                if choice=="yes" or choice=="y":
#        	        break
#                elif choice=="no" or choice=="n":
#        		cli.cursor_close(token,exec_ret)
#        		print 'execution time: %ss' %  str(round((end - now),2))
#        		return ""
#        	else:
#        		print confirmStr
#        tools.dump2Csv(result_table,out_command,line_count,status="init")
#        line_count+=len(result_table)
#        result_table=[]
#        isDump=True

def printdata(data_str):
	data = json.loads(data_str)
	#print(data , type(data))
	#print(data['Content'] , type(data['Content']))
	count = 0
	if(type(data['Content']) != dict):
		#print("no return table can be dumpped, admin statement?")
		#print("data:\n" + str(data['Content']))
		#print(str(data['Content']))
		if json.dumps(data['Content']) != "null":
			print(json.dumps(data['Content'], indent=4))
		else:
			print(json.dumps(data['Err'], indent=4))
		return 0	

	if 'content' in data['Content'].keys():
		for row in data['Content']['content']:
			print(row)
			#print(json.dumps(row))
			#output.writerow(row)
			count+=1
	else:
		#print(str(data['Content']))
		print(json.dumps(data['Content'], indent=4))
		#print("no content can be dumpped, admin statement?")
		#print("data:\n" + str(data['Content']))
		
	return count
 
def shell(connargs, shell_name, command):
	bo_url = "http://" + connargs["host"] + ":" + str(connargs["port"]) + "/cmd"
	print("bourl: " + bo_url)
	getData(bo_url, command) 
	
if __name__ == "__main__":
	connargs={}
	connargs["host"] = "http://localhost"
	connargs["port"] = "9090"
	shell(connargs, "*" ,"select * from sales limit 10")

