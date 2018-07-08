# 后端文件夹

## 依赖

 - python3
 - pymysql
 - tornado
 - pyyaml
 
## 本地运行后端服务
```
$ python3 app.py
```

访问 http://localhost:8888  
如果接口冲突，则使用：  
```
$ python3 app.py -p 8887
```
更改接口。  

## docker部署
```
$ docker-compose build
$ docker-compose up
```
