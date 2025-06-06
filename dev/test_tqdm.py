import tqdm
import sys

print(tqdm.__version__, sys.version, sys.platform, flush=True)

from tqdm import tqdm, trange
from time import sleep


with tqdm(range(1)) as pbar:
    for _ in pbar:
        for i in range(10):
            sleep(0.03)
            pbar.set_postfix(batch=i, refresh=False)
            # pbar.set_postfix_str(s=f"TACT{i}")
            pbar.update(0)

epochs = 1
batches = 10

for b in trange(
    epochs * batches,
    unit_scale=0.1,
    unit=f"epoch",
    bar_format="{l_bar}{bar}|{n:.1f}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]",
) :
    i = b % batches  # batch num
    # epoch = b // batches
    pbar.set_postfix_str(s=f"TACT{i}", refresh=False)
    sleep(0.03)


from tqdm import trange

with trange(1) as pbar:
    for _ in pbar:
        for i in trange(10, desc="batch", leave=False):
            sleep(0.03)
        # pbar.set_postfix(loss=0.99, refresh=False)


from tqdm import tqdm
fis=[k for k in range(100)]
with tqdm(total=len(fis) // 2) as pbar:
    for i in range(0, len(fis) - 1, 2):
        # Giả sử 'fis[i]' là file hiện tại bạn đang xử lý
        pbar.set_postfix(duplicate=f"{i} files")
        # Phần code xử lý
        pbar.update(1)
        sleep(0.3)
