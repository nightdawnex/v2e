import pickle
import os
import subprocess 
import cv2 

v2e_path = r'/workspace/v2e/v2e.py'
# run v2e on specified files
def run_v2e(input,output):
    #create the output directory if not exist
    os.makedirs(output,exist_ok=True)

    with open(input,'rb') as f:
        file = pickle.load(f)
        images = file['images']
        timestamps = file['timestamps']
    # output images to folder
    if not os.path.exists(os.path.join(output,'images')):
        os.mkdir(os.path.join(output,'images'))

    for index,image in enumerate(images):
        cv2.imwrite(os.path.join(output,'images',str(index).zfill(6)+'.png'),image)
    
    #determine the fps
    timestamp_diff = timestamps[1:]-timestamps[:-1]
    fps = 1e6/timestamp_diff.mean()

    cmd = ['python', v2e_path, '--input_frame_rate', str(fps),'-i', os.path.join(output,'images'), '--output_folder', output, '--dvs346', '--skip_video_output', '--overwrite', '--timestamp_resolution', '0.0033333333333', '--dvs_h5', 'events.h5', '--dvs_aedat2', 'None', '--no_preview']
    
    subprocess.run(cmd)

if __name__ == '__main__':
    if not os.path.exists('/tmp/v2e'):
        os.mkdir('/tmp/v2e')
    files = pickle.load(open('/tsukimi/datasets/MVSEC/data_paths.pkl','rb'))['test']
    for file in files:
        run_v2e('/tsukimi/datasets/MVSEC/event_chunks_processed/'+file,'/tmp/v2e/'+file)
