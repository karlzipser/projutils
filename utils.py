from utilz2 import *


##                                                                          ##
##############################################################################
##                                                                          ##
def show_sample_outputs(inputs,outputs,labels,ig,name,save_path):
    outputs=outputs.detach().cpu().numpy()
    labels=labels.detach().cpu().numpy()
    if False:
        print(outputs)
        print(labels)
        print(shape(outputs))
        print(shape(labels))
    i=0
    o=outputs[i,:,0,0]
    l=0*o
    l[labels[i]]=1
    sh(cuda_to_rgb_image(inputs[i,:]),use_spause=False)
    xs=np.arange(len(o))/len(o)*inputs.size()[2]
    plot(xs,inputs.size()[2]-o/o.max()*inputs.size()[2],'r')
    plot(xs,inputs.size()[2]-l*inputs.size()[2],'b')
    title(d2s(name,ig))
    if save_path:
        plt.savefig(
            opj(save_path,str(ig)+'-'+get_safe_name(name)+'.png'),
            bbox_inches='tight')

def get_second_most_recent_file(folder_path):
    files = sggo(folder_path,'*')
    if len(files) < 2:
        return None
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    return files[1]


def moving_average(data, window_size):
    """ Smooth data using a moving average """
    cumsum = np.cumsum(data)
    cumsum[window_size:] = cumsum[window_size:] - cumsum[:-window_size]
    return cumsum[window_size - 1:] / window_size

##                                                                          ##
##############################################################################
##                                                                          ##
def get_files_sorted_by_mtime(folder_path):
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    files.sort(key=lambda x: os.path.getmtime(x))
    return files
def select_files_to_keep(files, m):
    if m < 2:
        raise ValueError("The number of files to keep must be at least 2.")
    keep_files = [files[0], files[-1]]
    if m > 2:
        step = (len(files) - 1) / (m - 1)
        for i in range(1, m - 1):
            keep_files.append(files[int(round(i * step))])
    return sorted(keep_files, key=lambda x: os.path.getmtime(x))
def cleanup_folder(folder_path, keep_files):
    for f in os.listdir(folder_path):
        file_path = os.path.join(folder_path, f)
        if os.path.isfile(file_path) and file_path not in keep_files:
            os.remove(file_path)
def reduce_file_numbers(folder_path, num_to_keep):
    m=num_to_keep
    files = get_files_sorted_by_mtime(folder_path)
    keep_files = select_files_to_keep(files, m)
    cleanup_folder(folder_path, keep_files)
##                                                                          ##
##############################################################################
##  