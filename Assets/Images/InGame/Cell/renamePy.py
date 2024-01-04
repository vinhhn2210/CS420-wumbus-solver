import os

for i in range(1, 21):
	os.rename(f"Door {i}.png", f"Door-{i}.png", src_dir_fd=None, dst_dir_fd=None)