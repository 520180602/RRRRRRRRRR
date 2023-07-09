import gdown

zip_url = 'https://drive.google.com/uc?id=1M7GS68vkdn1pIuoj128bF-_rYpGTA9Zw'
output_zip = '/folder_upload.zip'  # Path to save the downloaded zip file
gdown.download(zip_url, output_zip, quiet=False)
