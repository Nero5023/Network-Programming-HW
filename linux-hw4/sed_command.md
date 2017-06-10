# 把Jennifer的名字改为Jenny
	sed -n 's/Jennifer/Jenny/pg' sed_example.txt 

# 删除第2-5行
	sed '2,5d' sed_example.txt  

# 打印第6-10行
	sed -n '6,10p' sed_example.txt

# 删除所有Karen所在的行
	sed  '/Karen/d' sed_example.txt 

# 在以Lori开头的行末尾加上三个/字符
	sed -n 's/^Lori.*/&\/\/\//p' sed_example.txt

# 所有Tommy所在的行均替换为Tommy Is on Vacation
	sed -n 's/Tommy.*$/Tommy IS on Vacation/pg' sed_example.txt

# 写一个能完成下列任务的sed脚本。 
* a)在第一行前插入标题EMPLOYEES.
* b) 删除以200结尾的工资项。
* c)把名字和姓的内容颠倒
* d)在文件末尾加上FILE END

若完成每一步需要以下命令

	sed '1i\EMPLOYEES' sed_example.txt
	sed  '/200$/d' sed_example.txt
	sed 's/\b\(\w*\)\b \b\(\w*\)\b/\2 \1/' sed_example.txt
	sed '$a\FILE END' sed_example.txt

写成 sed 命令文件 commands.sed

	#!/bin/sed -f
	1i\EMPLOYEES
	/200$/d
	s/\b\(\w*\)\b \b\(\w*\)\b/\2 \1/
	$a\FILE END
	
执行
	
	sed -f commands.sed sed_example.txt