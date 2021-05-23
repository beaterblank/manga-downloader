import urllib
import shutil
import requests
import os
import tqdm

def send_request_image(url: str) -> requests.Response:
	domain = urllib.parse.urlparse(url).netloc
	header = {
		'Accept': 'image/png,image/svg+xml,image/*;q=0.8,video/*;q=0.8,*/*;q=0.5',
		'Accept-Encoding': 'gzip, deflate, br',
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15',
		'Host': domain, 'Accept-Language': 'en-ca', 'Referer': 'https://manganelo.com/',
		'Connection': 'keep-alive'
	}
	r = requests.get(url, stream=True, timeout=5, headers=header)
	return r


def download_images(image_urls, save_dir: str):
	image_paths = []
	length = len(image_urls)
	pbar = tqdm.tqdm(total=length)
	for i, url in enumerate(image_urls):
		pbar.update(1)
		image = send_request_image(url)
		image_ext = url.split(".")[-1]
		image_dst_path = os.path.join(save_dir, f"{i}.{image_ext}")
		if image is not None:
			with open(image_dst_path, "wb") as fh:
				image.raw.decode_content = True
				try:
					shutil.copyfileobj(image.raw, fh)
				except Exception:
					pass
				else:
					image_paths.append(image_dst_path)
	return image_paths