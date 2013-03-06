# LICENSE #
GPLv3
AUTHOR: yurenbi

# 用法 #
从 [python official website](http://www.python.org/getit/) 下载 python2.7
新建任意文本文件按照

> OP1<br />
> 微指令1<br />
> 微指令2<br />
> 
> OP2<br />
> 微指令1<br />
> 微指令2<br />


的格式写。(参考s.txt)如OP为3位，共有5个控制信号,可以像这样，

> 100<br />
> 11101<br />
> 11010<br />
> 00101<br />
> 10110<br />
> 
> 000<br />
> 11010<br />
> 10110<br />

注意所有的OP的位数需相同，所有微指令的位数需相同。第一行不能为空，
每个OP后若干行为对应的若干微指令，在下一个OP前必须有且仅能有一个空行。
写完后可以打开 mins2logic.py 把 FILENAME 改成你自己的文本文件(或者直接将你自己的文本
文件存为"s.txt"放在mins2logic.py的同一目录)然后直接执行mins2logic.py即可。
你也可以在命令行下`python mins2logic.py yourfile`
cyn会自动补在OP后作为输入，具体位数取决于微指令最多的那个指令的微指令数。
演示：[http://ascii.io/a/2271](http://ascii.io/a/2271)


对于每一个控制位会输出原始的逻辑式和自动化简后的逻辑式。
总是零的控制位不输出。
