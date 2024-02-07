import os
from subprocess import run
import yaml
import argparse



def get_args():
    parser = argparse.ArgumentParser(
        description="Download from URLs in config yaml file.")
    parser.add_argument("--config", type=str, required=True, 
                        help="path to the config file")
    return parser.parse_args()


def download(url: str, out_path: str) -> None:
    """
    Download file from url to out_path
    url: str
    out_path: str
    """
    if not os.path.exists(out_path):
        print(f"Downloading {url} to {out_path}")

        run(["wget", url, "-O", out_path])

        # check sum
        sha256_path = os.path.join(os.path.dirname(out_path), 'sum',
                                   os.path.basename(out_path) + ".sum.txt")
        os.makedirs(os.path.dirname(sha256_path), exist_ok=True)

        with open(sha256_path, 'a') as f:
            run(["sum", out_path], stdout=f)

    else:
        print(f"{out_path} already exists. Skipping download.")


def main():
    args = get_args()

    with open(args.config, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    for data in config:
        url, out_path = data["url"], data["output"]
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        download(url, out_path)

    print('Done!')


if __name__ == '__main__':
    main()