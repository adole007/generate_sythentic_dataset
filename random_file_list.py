import glob
import os
import random
from collections.abc import Sequence



# iterable random file list
class RandomFileList(Sequence):
    def __init__(self, root_dir, search_pattern, recursive):
        self.file_list = glob.glob(os.path.join(root_dir, search_pattern), recursive=recursive)
        random.shuffle(self.file_list)
        super().__init__()

    def __getitem__(self, i):
        return self.file_list[i]
        

    def __len__(self):
        return len(self.file_list)

    def random_path(self):
        idx = random.randint(1, len(self.file_list)) - 1
        #print(idx)
        #self.file_list[idx]
        #for i in len(idx):
        #resul=[]
        #j=0
         #   resul.append(self.file_list[idx[i]].split('.')[0][-5:])
        #for i in [self.file_list[idx]]:
            #print(i)
            #resul.append(i.split('.')[0][-5:])
            #print(i.split('.')[0][-5:])
            #j = j + 1
        #resul.append([i.split('.')[0][-5:] ])
        #resul=[i.split('.')[0][-5:] for i in [self.file_list[idx]]]
        #resull= "".join(resul[-9:][:-3])
        
        #print(resul)
        #print(*resul, sep = ", ") 
        return self.file_list[idx]
