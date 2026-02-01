import os
import string
import subprocess
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


# ====== config ======
# 跑題目用的執行檔
TARGET = "./pinii_tmp"

# pin & inscount2.so 路徑（記得依照你實際環境改）
PIN = os.path.expanduser("~/pintools/pin")
INSCOUNT_SO = os.path.expanduser(
    "~/pintools/source/tools/ManualExamples/obj-ia32/inscount2.so"
)

# flag 相關設定
FLAG_LEN = 34
FLAG_PREFIX = "FLAG{"
FLAG_SUFFIX = "}"
# \w = [0-9A-Za-z_]
CHARSET = string.ascii_letters + string.digits + "_"

# 一次炸幾個候選字元（thread 數）
MAX_WORKERS = min(32, len(CHARSET))

# 每個執行個體各自寫自己的 inscount 檔，避免 multithread 互相踩檔案
INSCOUNT_DIR = Path("ins_tmp")
INSCOUNT_DIR.mkdir(exist_ok=True)


def run_with_input(s: str) -> int:
    """
    用 pin + inscount2.so 跑一次程式，回傳本次執行的指令數。
    每次呼叫都用 -o 指定一個獨立的輸出檔，避免多執行緒共用同一個 inscount.out。
    """
    out_file = INSCOUNT_DIR / f"inscount_{os.getpid()}_{uuid.uuid4().hex}.out"
    if out_file.exists():
        try:
            out_file.unlink()
        except OSError:
            pass

    cmd = [
        PIN,
        "-t",
        INSCOUNT_SO,
        "-o",
        str(out_file),
        "--",
        TARGET,
    ]

    # NOTE: 題目說「在 stdin 輸入 34 + '\\n'」，這裡直接把猜的 flag 丟進去，
    # 請確保 len(s) == 34，下面主程式會保證。
    # print(cmd)
    proc = subprocess.run(
        cmd,
        input=(s + "\n").encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # 有些題目會在 flag 錯誤時直接 exit(1/非 0)，這裡**不**因為非 0 直接噴錯，
    # 只要有產生對應的 out_file 就繼續用；如果連 out_file 都沒有，再當作真正失敗。
    if not out_file.exists():
        err_out = proc.stderr.decode(errors="ignore")
        out = proc.stdout.decode(errors="ignore")
        raise RuntimeError(
            f"pin/pinii_tmp failed (returncode={proc.returncode}).\n"
            f"stdout:\n{out}\n\nstderr:\n{err_out}"
        )

    data = out_file.read_text().strip().split()
    # 一般 inscount 工具輸出類似: "Count 123456"
    # 取最後一個 token 當作指令數。
    try:
        ooo = int(data[-1])
        print(f"[+] flag: {s} icount: {ooo}")
        return ooo
    except (ValueError, IndexError) as e:
        raise RuntimeError(f"Failed to parse inscount.out: {data}") from e
    finally:
        try:
            out_file.unlink()
        except OSError:
            # 如果檔案正在被其它工具看也沒關係，之後手動清就好
            pass


def brute_force_flag() -> str:
    """
    逐位爆破：
    - 已知格式 FLAG{xxxxxxxx...}
    - 長度 34, 所以未知長度 = 34 - len('FLAG{') - len('}') = 28
    - 每次固定前綴，對當前位枚舉 CHARSET，剩下位置塞 filler，
      利用 inscount 的最大值判斷目前位最可能的字元。
    """
    unknown_len = FLAG_LEN - len(FLAG_PREFIX) - len(FLAG_SUFFIX)
    assert unknown_len > 0

    known = ""  # 已爆破出的 \w* 內容

    for pos in range(unknown_len):
        best_c = None
        best_count = -1
        print(f"[*] brute-forcing pos {pos + 1}/{unknown_len} ...")

        def _test_char(c: str) -> tuple[str, int]:
            # 目前猜測：FLAG{known + c + filler...}
            filler_len = unknown_len - (len(known) + 1)
            filler = "A" * max(filler_len, 0)
            guess = f"{FLAG_PREFIX}{known}{c}{filler}{FLAG_SUFFIX}"

            if len(guess) != FLAG_LEN:
                raise AssertionError(f"Bad guess length: {len(guess)} != {FLAG_LEN}")

            icount = run_with_input(guess)
            return c, icount

        # 這裡一次把當前 byte 的所有候選字元丟進 thread pool「一起炸」
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(_test_char, c) for c in CHARSET]

            for fut in as_completed(futures):
                c, icount = fut.result()
                if icount > best_count:
                    best_count = icount
                    best_c = c

        known += best_c
        print(f"[+] pos {pos + 1}/{unknown_len} fixed char = {best_c!r}")
        print(f"    current flag: {FLAG_PREFIX}{known}{FLAG_SUFFIX}")

    return f"{FLAG_PREFIX}{known}{FLAG_SUFFIX}"


def main() -> None:
    final_flag = brute_force_flag()
    print(f"[+] final flag: {final_flag}")


if __name__ == "__main__":
    main()


