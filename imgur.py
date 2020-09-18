from imgurpython import ImgurClient
import os
import json

# Note since access tokens expire after an hour, only the refresh token is required (library handles autorefresh)
class Imgur:
	def __init__(self, imgur_credentials):
		self.username = imgur_credentials['username']
		self.client_id = imgur_credentials['client_id']
		self.client_secret = imgur_credentials['client_secret']
		self.access_token = imgur_credentials['access_token']
		self.refresh_token = imgur_credentials['refresh_token']
		self.client = ImgurClient(self.client_id, self.client_secret, self.access_token, self.refresh_token)

	def clean_user_images(self):
		items = self.client.get_account_images(self.username)
		success = True
		for item in items:
			if item.title == 'Instagram_DashBoard' and item.name == 'Instagram_DashBoard':
				res = self.client.delete_image(item.id)
				if not res:
					success = False
		return success

	def upload_image(self,path):

		# Here's the metadata for the upload. All of these are optional, including
		# this config dict itself.
		config = {
			'album': None,
			'name':  'Instagram_DashBoard',
			'title': 'Instagram_DashBoard',
			'description': 'pic'
		}

		print("Uploading image... ")
		image = self.client.upload_from_path(path, config=config, anon=False)
		print("Done")
		print()

		return image
