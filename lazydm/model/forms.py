import formencode

class CommentForm(formencode.Schema):
	allow_extra_fields = True
	filter_extra_fields = True
	email = formencode.validators.Email(not_empty=True)
	honey = formencode.validators.Empty()
	user = formencode.validators.UnicodeString(max=30, not_empty=True)
	website = formencode.validators.URL(add_http=True)
	content = formencode.validators.UnicodeString(max=1000,not_empty=True)
