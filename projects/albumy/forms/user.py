from wtforms import StringField, SubmitField, TextAreaField, HiddenField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Regexp, Optional, ValidationError, EqualTo
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_login import current_user
from albumy.models import User

class EditProfileForm(FlaskForm):
    name = StringField('姓名', validators=[DataRequired(), Length(1, 30)])
    username = StringField('用户名', validators=[DataRequired(), Length(1, 20), Regexp('^[a-zA-Z0-9]*$', message='用户名只能是字母或数字。')])
    website = StringField('个人网站', validators=[Optional(), Length(0, 254)])
    location = StringField('城市', validators=[Optional(), Length(0, 50)])
    bio = TextAreaField('简介', validators=[Optional(), Length(0, 120)])
    submit = SubmitField('确定')

    def validate_username(self, field):
        if field.data != current_user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在！')

class UploadAvatarForm(FlaskForm):
    image = FileField('头像（<= 3M）', validators=[FileRequired(), FileAllowed(['jpg', 'png'], '文件格式必须为 .png 或 .jpg')])
    submit = SubmitField('确定上传')

class CropAvatarForm(FlaskForm):
    x = HiddenField()
    y = HiddenField()
    h = HiddenField()
    w = HiddenField()
    submit = SubmitField('修改头像')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('旧密码', validators=[DataRequired()])
    new_password = PasswordField('新密码', validators=[DataRequired(), Length(8, 128)])
    new_password_confirm = PasswordField('确认新密码', validators=[DataRequired(), Length(8, 128), EqualTo('new_password')])
    submit = SubmitField('确定')

class NotificationSettingForm(FlaskForm):
    receive_comment_notification = BooleanField('新的评论')
    receive_follow_notification = BooleanField('新的关注者')
    receive_collect_notification = BooleanField('新的收藏')
    submit = SubmitField('确定')

class PrivacySettingForm(FlaskForm):
    public_collections = BooleanField('公开收藏')
    submit = SubmitField('确定')

class DeleteAccountForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 20)])
    submit = SubmitField('确定')

    def validate_username(self, field):
        if field != self.username:
            raise ValidationError('用户名不正确！')

class ChangeEmailForm(FlaskForm):
    email = StringField('新的邮箱地址', validators=[DataRequired(), Length(1, 254), Email()])
    submit = SubmitField()
