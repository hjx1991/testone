from flask_script import Manager
from flask_migrate import MigrateCommand,Migrate
from views import app
from exts import db
from models import *
#初始化Manager
manager = Manager(app)

#使用Migrate绑定app和db模型
migrate = Migrate(app,db)

#在manager添加迁移脚本的命令
#下面'db'为脚本固定参数，可随意取, 如: python manage.py db XXX
manager.add_command('db',MigrateCommand)

if __name__ =='__main__':
    manager.run()
#执行数据库迁移时,检查views文件中是否引导: db.init_app(app)
'''再Cmd执行python manage.py db 
init（创建迁移仓库,就第一次使用） /
 migrade（创建迁移脚本） /
  upgrade（更新）
  '''
#在虚拟环境执行