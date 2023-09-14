
import os 
import os.path as op
root_dir = r"/gypsum/work1/trahman/zhongyangzha/dvs_hpe/rgb_dataset/human3.6m/videos"
output_root_dir = r"/gypsum/work1/trahman/zhongyangzha/dvs_hpe/rgb_dataset/human3.6m/events_temp/"
extra_output_dir= r"/gypsum/work1/trahman/zhongyangzha/dvs_hpe/rgb_dataset/human3.6m/events/"
threads = 2
base_cmd = r"python v2e.py --dvs346 --dvs_h5=events.h5 --dvs_aedat2=none --no_preview --batch_size 16  --timestamp_resolution 0.00333333333333335 --skip_video_output".split()

def run_cmds(cmds, thread_num=4):
    import subprocess
    import threading
    import time
    import queue
    import sys

    def worker():
        while True:
            cmd = q.get()
            if cmd is None:
                break
            print(" ".join(cmd))
            subprocess.call(cmd)
            q.task_done()

    q = queue.Queue()
    threads = []
    for i in range(thread_num):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)

    for cmd in cmds:
        q.put(cmd)

    # block until all tasks are done
    q.join()

    # stop workers
    for i in range(thread_num):
        q.put(None)
    for t in threads:
        t.join()    


def main():
    import subprocess
    cmds = []
    for sub_dir in os.listdir(root_dir):
        for file in os.listdir(op.join(root_dir,sub_dir,"Videos")):
            input_file = op.join(root_dir,sub_dir,"Videos",file)
            output_dir = op.join(output_root_dir,sub_dir,op.splitext(file)[0])
            if op.exists(output_dir):
                continue
            if op.exists(op.join(extra_output_dir,sub_dir,op.splitext(file)[0])):
                continue
            if not op.exists(op.join(output_root_dir,sub_dir)):
                os.mkdir(op.join(output_root_dir,sub_dir))
            
            cmd = base_cmd + ["-i",input_file, "-o", output_dir]
            subprocess.call(cmd)
            # cmds.append(cmd)

    # run_cmds(cmds, thread_num=threads)

if __name__ == "__main__":
    main()