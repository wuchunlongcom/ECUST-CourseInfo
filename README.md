### 华东理工大学课程信息表 docker部署的远程机器(macOS建立的u20.04.3虚拟机)：wuchunlong@192.168.31.15  密码：83418341

```
快速 进入py375  
$ source  /Users/wuchunlong/local/env375/bin/activate
快速 切换到工程根目录
$ cd /Users/wuchunlong/local/github/u20.04.3-fabric-dbtxt/u1604-fabric-dbtxt/ECUST-CourseInfo-src/src
$ cd /Users/wuchunlong/local/github/u20.04.3-fabric-dbtxt/u1604-fabric-dbtxt/ECUST-CourseInfo-src/src/courseinfo

特点：重新设置了路径 'data/db.sqlite3'

```

# ECUST-CourseInfo

## 本地运行代码

1. 切换到Python3 虚拟环境 virtualenv
	```console
	(env375) wuchunlong@wuchunlong courseinfo$ python --version
		Python 3.7.5
	^C(env375) wuchunlong@wuchunlong courseinfo$ pip --version
		pip 23.1.2 from /Users/wuchunlong/local/env375/lib/python3.7/site-packages/pip (python 3.7)
	```
1. 切换到工程根目录，安装 pip 依赖 
	```
	cd /Users/wuchunlong/local/github/u20.04.3-fabric-dbtxt/u1604-fabric-dbtxt/ECUST-CourseInfo-src/src
	$ ls
		Dockerfile    README.md     ansible-u1804 courseinfo    docker-config  requirements.txt
	$ pip install -r requirements.txt
	```

1. 切换到应用courseinfo目录
	``` 
	$ cd /Users/wuchunlong/local/github/u20.04.3-fabric-dbtxt/u1604-fabric-dbtxt/ECUST-CourseInfo-src/src/courseinfo
	$ ls
		README.md     data          locale        start.sh
		classroom     excel         manage.py     static_common
		courseinfo    initdb.py     myAPI         templates

	```
1. 运行站点
	```
	$ ./start.sh
		...
		System check identified no issues (0 silenced).
		May 26, 2023 - 07:27:01
		Django version 2.2.6, using settings 'courseinfo.settings-debug'
		Starting development server at http://127.0.0.1:8000/
		Quit the server with CONTROL-C.
			
	```
## 制作 Docker 镜像

1. 确认本地 Docker Daemon 运行正常

	```console
	$ docker --version
		Docker version 23.0.5, build bc4487a	
	
	$ docker run hello-world
		Hello from Docker!
		This message shows that your installation appears to be working correctly.
		...
		
	$ docker-compose --version
		Docker Compose version v2.17.3
	```
1. 切换到工程根目录，确认目录中包含 Dockerfile 文件，注意：`chunlongwu/djangodemo:v1.0` 中的 chunlongwu 是申请的 dockerhub 的账户名
	```
	$ ls
		Dockerfile    README.md     ansible-u1804 courseinfo    docker-config  requirements.txt
    #制作Docker镜像 chunlongwu/djangodemo:v1.0 
	(env375) wuchunlong@wuchunlong src$ docker build -t chunlongwu/djangodemo:v1.0 .
		[+] Building 5.3s (18/18) FINISHED                                              
 		=> [internal] load .dockerignore                                          0.0s
 		=> => transferring context: 2B                                            0.0s
 		=> [internal] load build definition from Dockerfile                       0.0s
 		=> => transferring dockerfile: 1.71kB                                     0.0s
 		=> [internal] load metadata for docker.io/maodouzi/django:v2.2.6-oraclec  2.4s
 		=> [auth] maodouzi/django:pull token for registry-1.docker.io             0.0s
 		=> [internal] load build context                                          0.1s
 		=> => transferring context: 1.59MB                                        0.1s
 		=> [ 1/12] FROM docker.io/maodouzi/django:v2.2.6-oracleclient-v19.3@sha2  0.0s
 		=> CACHED [ 2/12] RUN mkdir -p /home/www/ecustCourseInfo/logs     && mkd  0.0s
 		=> CACHED [ 3/12] WORKDIR /home/www/ecustCourseInfo                       0.0s
 		=> [ 4/12] COPY courseinfo /home/www/ecustCourseInfo/src/courseinfo       0.1s
 		=> [ 5/12] COPY requirements.txt /home/www/ecustCourseInfo/src/courseinf  0.0s
 		=> [ 6/12] RUN rm -rf /home/www/ecustCourseInfo/src/courseinfo/initdb.py  1.9s
 		=> [ 7/12] RUN rm /etc/nginx/sites-enabled/default                        0.3s
 		=> [ 8/12] ADD docker-config/nginx.conf /etc/nginx/sites-available/ecust  0.0s 
 		=> [ 9/12] RUN ln -s /etc/nginx/sites-available/ecustCourseInfo.conf /et  0.3s 
 		=> [10/12] ADD docker-config/supervisord.conf /etc/supervisor/supervisor  0.0s 
 		=> [11/12] ADD docker-config/supervisor.conf /etc/supervisor/conf.d/ecus  0.0s 
 		=> [12/12] ADD docker-config/start.sh /tmp/start.sh                       0.0s 
 		=> exporting to image                                                     0.1s
 		=> => exporting layers                                                    0.1s
 		=> => writing image sha256:3517bf12b4081ab2109032ac256af7b6b6c08c95a4c9d  0.0s
 		=> => naming to docker.io/chunlongwu/djangodemo:v1.0                      0.0s
	
	```
	
1. 切换到 courseinfo 目录，在本地测试和运行 Docker 镜像，然后在浏览器上访问: `http://localhost 或 http://127.0.0.1/`

	```
	$ ls
	README.md        courseinfo       excel            locale           myAPI            static
	classroom        data             initdb.py        manage.py        static_common    templates

	$ docker run -d -p 80:80 --mount type=bind,source=$(pwd)/courseinfo/data,target=/home/www/ecustCourseInfo/src/courseinfo/data chunlongwu/djangodemo:v1.0 
		410dc2f7b7222e45a87449d0b9a079eafe9942c70a782256ad7f17a54d490994
		
		
	$ docker ps
		CONTAINER ID   IMAGE                        COMMAND              CREATED              STATUS              PORTS                NAMES
		410dc2f7b722   chunlongwu/djangodemo:v1.0   "sh /tmp/start.sh"   About a minute ago   Up About a minute   0.0.0.0:80->80/tcp   hardcore_spence
	```

1. 停止 Docker 镜像

	```console
	$ docker stop 410dc2f7b722
		410dc2f7b722
	```

1. 镜像上传到 Docker hub

	```bash
	dockerHub       name: chunlongwu      password: 1234567890
	$ docker login
		Authenticating with existing credentials...
		Login Succeeded

		Logging in with your password grants your terminal complete access to your account. 
		For better security, log in with a limited-privilege personal access token. Learn more at https://docs.docker.com/go/access-tokens/
	
	$ docker push chunlongwu/djangodemo:v1.0
		The push refers to repository [docker.io/chunlongwu/djangodemo]
		a1e8003d4cbb: Pushed 
		...
		831b66a484dc: Layer already exists 
		v1.0: digest: sha256:3443356be4c9fa10f3f238dcdc3e8650b904e40a1c1c7f487bebda6e222c23e2 size: 4929
	```
## 部署到远端站点
1. 配置 ~/.ssh/config 文件，HostName 可以直接写 IP 地址，IdentityFile 是密钥文件，可以用 ssh-keygen 生成，然后通过 ssh-copy-id 拷贝到远端机器。
    远端机器：ssh  wuchunlong@192.168.31.15
	```
	$ sudo vim ~/.ssh/config

		Host course
		HostName        192.168.31.15
		User            wuchunlong
		IdentityFile    ~/.ssh/id_rsa
	```

	```
	$ ssh-keygen
	Generating public/private rsa key pair.
	Enter file in which to save the key (/Users/wuchunlong/.ssh/id_rsa): 
	/Users/wuchunlong/.ssh/id_rsa already exists.
	Overwrite (y/n)? y
	Enter passphrase (empty for no passphrase): 
	Enter same passphrase again: 
	Your identification has been saved in /Users/wuchunlong/.ssh/id_rsa.
	Your public key has been saved in /Users/wuchunlong/.ssh/id_rsa.pub.
	The key fingerprint is:
	SHA256:FY3WcT+NxFX5eRU2Eiv+2rswRZiZwWbXcRopZme/V4c wuchunlong@wuchunlong.local
	The key's randomart image is:
	+---[RSA 3072]----+
	|          o=.=*BO|
	|          o=%+OB=|
	|         .+O.*o+*|
	|         .. o E.B|
	|        S  . .  =|
	|            o  ..|
	|           o .  .|
	|            =    |
	|           . +o  |
	+----[SHA256]-----+


	$ ssh-copy-id wuchunlong@192.168.31.15 -i ~/.ssh/id_rsa.pub
		wuchunlong@192.168.31.15's password: 83418341
	#确认.  不用用户名密码，可以直接访问远端机器
	$ ssh course
		Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.15.0-72-generic x86_64)

 		* Documentation:  https://help.ubuntu.com
 		* Management:     https://landscape.canonical.com
 		* Support:        https://ubuntu.com/advantage

		131 updates can be applied immediately.
		To see these additional updates run: apt list --upgradable

		New release '22.04.2 LTS' available.
		Run 'do-release-upgrade' to upgrade to it.

		Your Hardware Enablement Stack (HWE) is supported until April 2025.
		Last login: Fri May 26 03:41:03 2023 from 192.168.31.14
		wuchunlong@ubuntu:~$

	```
1. 切换到 ansible-u1804目录，修改 inventory/inventory.ini.example, 复制 `inventory/inventory.ini.example`

	```console
	$ ls
	README.md inventory playbooks

	$ sudo vim inventory/inventory.ini.example
	[all:vars]
	image_name="chunlongwu/djangodemo"
	image_version="v1.0"
	data_external_dir="/Users/wuchunlong/local/github/u20.04.3-fabric-dbtxt/u1604-fabric-dbtxt/ECUST-CourseInfo-src/src/courseinfo/data/"
	data_hostpath="/root/data/"
	data_containerpath="/home/www/ecustCourseInfo/src/courseinfo/data/"

	bastion_data_device="/dev/vdb"

	[webserver]
	course
	
	$ cp inventory/inventory.ini.example inventory/inventory.ini

	```

1. 执行部署() 

	```console
	$ ansible-playbook -i inventory/inventory.ini playbooks/deploy.yml

	PLAY [webserver] *****************************************************************************************************************

	TASK [Gathering Facts] ***********************************************************************************************************
	ok: [course]

	TASK [init02_config_webserver : Container present] *****************************
	changed: [course]

	PLAY RECAP *********************************************************************
	course                     : ok=19   changed=6    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
	```
1. 执行完毕后，可以通过浏览器访问远程机器
	```
	http://192.168.31.15/    远程机器，通过浏览器访问正常！
	```
1. 查看远程机器的工作状态
	```
	(env375) wuchunlong@wuchunlong ansible-u1804$ ssh wuchunlong@192.168.31.15
	查看使用的容器
	wuchunlong@ubuntu:~$ sudo docker ps
		CONTAINER ID   IMAGE                        COMMAND              CREATED       STATUS       PORTS                NAMES
		fa19b6bb377c   chunlongwu/djangodemo:v1.0   "sh /tmp/start.sh"   3 hours ago   Up 3 hours   0.0.0.0:80->80/tcp   49d94d26619fcae7589b5dd97376dbfd714662f043dfc3774c0a1de7721673dd	
	
	停止使用的容器
	wuchunlong@ubuntu:~$ sudo docker stop fa19b6bb377c
		fa19b6bb377c
	wuchunlong@ubuntu:~$ sudo docker ps
		CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
	
	http://192.168.31.15/    远程机器连接失败！
	```
## 更新时间：2023.05.28
	
	