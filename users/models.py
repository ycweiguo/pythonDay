import json, time
from datetime import datetime

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .conf import settings
from .managers import UserInheritanceManager, UserManager


#create your models here
def birthday_filter(birthday):
    t = time.time()
    dt = datetime.fromtimestamp(t)
    '''new_minute = str(dt.minute)
    if dt.minute < 10 :
        new_minute = '0' + str(dt.minute)
    :return u'[发布于 %s年%s月%s日 %s：%s]' % （dt.year, dt.month, dt.day, dt.hour, dt.minute）
        '''
    b_year = birthday[:4]
    b_month = birthday[4:6]
    b_day = birthday[6:]

    age = int(dt.year) - int(b_year) - 1

    if int(b_month) > (int(dt.month) - 1):
        if int(b_day) > (int(dt.day) - 1):
            age +=1
    return  age

class AbstractUser(AbstractBaseUser, PermissionsMixin):
    USERS_AUTO_ACTIVATE = not settings.USERS_VERIFY_EMAIL

    email = models.EmailField(
        _('email address'), max_length=255, unique=True, db_index=True)
    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin site.'))

    is_active = models.BooleanField(
        _('active'), default=USERS_AUTO_ACTIVATE,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    user_type = models.ForeignKey(ContentType, null=True, editable=False)

    objects = UserInheritanceManager()
    base_objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        abstract = True

    def get_full_name(self):
        """ Return the email."""
        return self.email

    def get_short_name(self):
        """ Return the email."""
        return self.email

    def email_user(self, subject, message, from_email=None):
        """ Send an email to this User."""
        send_mail(subject, message, from_email, [self.email])

    def activate(self):
        self.is_active = True
        self.save()

    def save(self, *args, **kwargs):
        if not self.user_type_id:
            self.user_type = ContentType.objects.get_for_model(self, for_concrete_model=False)
        super(AbstractUser, self).save(*args, **kwargs)


class User(AbstractUser):

    """
    Concrete class of AbstractUser.
    Use this if you don't need to extend User.
    """
    name = models.CharField(max_length=20,default='第一次登录') #姓名
    sex = models.CharField(max_length=3,default='男')           #性别
    birthday = models.CharField(max_length=20,default='1997-10-31') #8位数字，年月生日计算
    job_number = models.CharField(max_length=10,default='0001') #工作证号

    zhengzhi_mianmao = models.CharField(max_length=10,default='群众') #政治面貌
    zhengzhi_time = models.CharField(max_length=20,default='2010-10-31') #6位数字，入党、团时间

    job = models.CharField(max_length=30,default='工程师') #职称
    job_time = models.CharField(max_length=20,default='2015-10-31') #6位数字，获得职称时间

    job_2 =models.CharField(max_length=30,default='员工') #职务
    id_number = models.CharField(max_length=30,default='11010819901216982') #身份证号
   #本次新增
    xue_li = models.CharField(max_length=30,default='本科') #学历
    school = models.CharField(max_length=30, default='北京化工大学') #学校
    graduate_time = models.CharField(max_length=20,default='2000-10-31') #毕业时间
    job_join_time = models.CharField(max_length=20,default='2000-10-31') #入职时间
    team_belong = models.CharField(max_length=20,default='C640') #部门

    phone = models.CharField(max_length=30,default='18393905493') #手机号

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
    def __str__(self):
        return  self.name

    def age(self):
        return birthday_filter(self.birthday)
