import os

LINUX_ROOT = '/home/jamrot/linux'
TFA_ANALYSER = '/home/jamrot/TFA-project/build/lib/analyzer'
BCLIST_ROOT = '/home/jamrot/TFA-project/bc_list'

def c2ll_dir(dirpath):
    bclist_filepath = f'{BCLIST_ROOT}/bc.list'
    open(bclist_filepath, 'w').close()

    for root, dirs, fs in os.walk(dirpath):
        for f in fs:
            if f.endswith('.c'):
                rel_root = os.path.relpath(root, LINUX_ROOT)
                filepath = os.path.join(rel_root, f)
                filepath_ll = os.path.join(root, f).replace(".c", ".ll")
                filepath_bc = os.path.join(root, f).replace(".c", ".bc")
                os.system(f'cd {LINUX_ROOT} && make LLVM=1 CFLAGS="-O0 -g" {filepath.replace(".c", ".ll")}')
                os.system(f'llvm-as {filepath_ll} -o {filepath_bc}')
                # add .bc path to bc.list
                write2bclist(filepath_bc)
                # break
    
    os.system(f'{TFA_ANALYSER} @{bclist_filepath}')
    os.system('python3 /home/jamrot/TFA-project/my_script/get_call_trace.py')
    os.system('python3 /home/jamrot/TFA-project/my_script/sql_query_all.py')

def write2bclist(filepath):
    with open(f'{BCLIST_ROOT}/bc.list', 'a') as f:
        f.write(filepath + '\n')

c2ll_dir("/home/jamrot/linux/net/ceph")