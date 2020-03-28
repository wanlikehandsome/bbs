# mongo id (数字id不适合分布式)
网站: cnodejs.org
使用类函数注册user
topic.all()  点睛之笔
current_user()
刚开始已经提交的文件没办法忽略
jsbeautiful.org
csrf 跨站脚本攻击的脚本的发起者还是你本人, 只不过是通过你本人触发的别人想要你执行的行为,
而比却没有意识到
<iframe></iframe> 跨域能够发起跨站脚本攻击post请求
xss: 站内脚本攻击, 所有访问到页面的人都会被感染, 拿到cookie还能够登录
flask设置了不能用js访问cookie
一个服务器对应多个二级域名, 从而实现多种不同的功能
代码常常放在 /var/www 里面
不要在服务器上面写配置, 难以维护, 难以修改, 使用软链接到合适的位置, 维护方便
ln -s /var/www/bbs/bbs.conf /etc/supervisor/conf.d/bbs.conf
ll: 查看链接情况
/dev/pydev/bbs/bin/gunicorn
service supervisor restart
nginx 配置文件
/etc/nginx/site-enabled/chat
ln -s /var/www/bbs/bbs.nginx /etc/nginx/sites-enabled/bbs
service nginx restart


# 部署到服务器
gunicorn
nginx
wsgi
supervisor