import formencode

class BaseForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    honey = formencode.validators.Empty()

class CommentForm(BaseForm):
	email = formencode.validators.Email(strip=True,not_empty=True)
	user = formencode.validators.UnicodeString(max=30, not_empty=True)
	website = formencode.validators.URL(add_http=True,strip=True)
	content = formencode.validators.UnicodeString(max=1000,strip=True,not_empty=True)

class ArticleForm(BaseForm):
    title = formencode.validators.UnicodeString(max=30, strip=True, not_empty=True)
    content = formencode.validators.UnicodeString(strip=True, not_empty=True)
