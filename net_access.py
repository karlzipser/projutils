## 79 ########################################################################

print(__file__)
from utilz2 import *
import torch


def get_net(
  device='',
  net_class=None,
  weights_file='',
  run_path='',
):
  """
  if using run_path, expect a project having:
      ~/project_<name>/<run name>/<name>/net/code/net.py
          defining net_path=__file__ and class Net()
      ~/project_<name>/<run name>/<name>/net/weights/<weight name>.pth
  Then, run_path should be opjh('project_<name>/<run name>')
  """
  assert device
  net=None
  if net_class:
      net = net_class()
  if weights_file:
    assert not run_path
    assert ope(weights_file)
    assert net
    print('*** Attempting to load from',weights_file+':')
    print('\t',net.load_state_dict(torch.load(weights_file)))
  elif run_path:
    assert ope(run_path)
    assert isNone(net)
    import importlib.util
    name=fname(pname(run_path)).replace('project_','')
    file_path=opj(run_path,name,'net/code/net.py')
    module_name = 'module'
    spec = importlib.util.spec_from_file_location(module_name,file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    w=most_recent_file_in_folder(opj(pname(pname(module.net_path)),'weights'))
    # allow to work if no saved weights
    return get_net(device=device,net_class=module.Net,weights_file=w)
  else:
    print('*** Starting with random weights.')
    assert net
  net.to(device)
  return net


def save_net(net,weights_file):
  print('*** weights_file=',weights_file)
  torch.save(net.state_dict(), weights_file)
    

#EOF
## 79 ########################################################################
