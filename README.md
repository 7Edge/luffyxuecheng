# luffyxuecheng
luffyxuecheng项目之后端API

### 初始化项目
#### 修改setting.py配置文件相关
- 设置数据库
  1. 创建scheme,即创建数据库实例
  2. 设置IP，PORT, USER, PASSWORD, NAME
  3. 采用的是mysql作为数据库
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'luffyxuecheng',  # 修改为自己的实例名
        'HOST': '127.0.0.1',  # 修改为自己的mysql的ip
        'PORT': 3306,  # 修改端口
        'USER': 'root', # 用户
        'PASSWORD': '123456', # 密码 
    }
}
```
- 设置CACHE使用Redis
```python
# CACHE
CACHE = {
    'default': {  # 设置默认cache为redis
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379',  # 设置redis-server信息ip:port
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 100  # 连接池最大连接数
            },
            # 'PASSWORD': 'xxx', # 如果有设置了redis-server密码在这里设置
        }
    }
}

```
### 构建运行python环境和依赖库
- python3.7版本
    - window上

