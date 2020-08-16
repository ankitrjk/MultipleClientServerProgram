import csv

csv_file=open("login_credentials.csv","r").readlines()
header=csv_file.pop(0)
print(header)

filename=1

num_of_lines=len(csv_file)
for i in range(num_of_lines):
    if i%int(num_of_lines/3+1)==0:
        write_file=open(str(filename)+".csv","w+")
        write_file.write(header)
        write_file.writelines(csv_file[i:i+int(num_of_lines/3+1)])
        filename+=1