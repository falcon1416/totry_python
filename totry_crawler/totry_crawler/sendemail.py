import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart

class SendEmail:
  def send(self,title,filepath,filename):

    mail_host = "smtp.163.com"  # 设置服务器
    mail_user = "falcon_13@163.com"  # 用户名
    mail_pass = "ilove911"  # 口令
    sender = 'falcon_13@163.com'
    receivers = "80513548@qq.com"  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    content = "自动发送邮件"

    # 创建一个带附件的实例 
    message = MIMEMultipart() 
    message['From'] =  mail_user
    message['To'] = receivers 
    message['Subject'] = Header(title, 'utf-8')
    # 邮件正文内容 
    message.attach(MIMEText(content, 'plain', 'utf-8')) 

    # 附件
    att = MIMEText(open(filepath, 'rb').read(), 'base64', 'utf-8')
    att['Content-Type'] = 'application/octet-stream'
    att['Content-Disposition'] = 'attachment; filename="'+filename+'.csv"'
    message.attach(att)

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("Error: 无法发送邮件" + e.strerror)


if __name__ == "__main__":
  sm=SendEmail()
  sm.send("测试邮箱","./ccw.json")