import torch
import os
import random
from datetime import datetime
import numpy as np
from Config import Config
from train import Training
import copy
from torch.utils.tensorboard import SummaryWriter

def main():
    # hardware constraint for speed test
    # torch.set_num_threads(1)
    #
    # os.environ['OMP_NUM_THREADS'] = '1'

    # initialization
    config = Config()

    for i in range(len(config.spot_paths)):
        path = './tensorboard_'+ str(i)
        if not os.path.exists(path):
            os.makedirs(path)
        writer = SummaryWriter(path)
        config_used = copy.copy(config)
        # print('config_used.spot_paths first: ', config_used.spot_paths)
        # print('config.spot_paths first : ', config.spot_paths)
        config_used.spot_paths = config.spot_paths[i]
        # print('config_used.spot_paths: ', config_used.spot_paths)
        # print('config.spot_paths first : ', config.spot_paths)
        torch.manual_seed(config_used.seed)
        random.seed(config_used.seed)
        np.random.seed(config_used.seed)
        a = datetime.now()
        print('Start time: ', a.strftime('%H:%M:%S'))

        # stage1 training
        torch.cuda.reset_peak_memory_stats()
        print('Training start ')
        model_train = Training(config_used)
        for epoch in range(config_used.epochs_stage):
            print('Epoch:', epoch)
            model_train.train(epoch)
            # print('loss', model_train.loss),print('loss', type(model_train.loss))
            # print('lr', model_train.actual_lr), print('lr', type(model_train.actual_lr))
            writer.add_scalar('Loss/train', model_train.loss, epoch)
            writer.add_scalar('lr', model_train.actual_lr, epoch)
            # loss = model_train.train(epoch)
            # if epoch > 0 and loss < 0.14:
            #     break

        b = datetime.now()
        print('End time: ', b.strftime('%H:%M:%S'))
        c = b - a
        minutes = divmod(c.seconds, 60)
        print('Time used: ', minutes[0], 'minutes', minutes[1], 'seconds')

        print('Write embeddings')
        model_train.write_embeddings()
        print('Training finished: ', datetime.now().strftime('%H:%M:%S'))
        print("torch.cuda.max_memory_allocated: %fGB" % (torch.cuda.max_memory_allocated(0) / 1024 / 1024 / 1024))

    # torch.manual_seed(config.seed)
    # random.seed(config.seed)
    # np.random.seed(config.seed)
    # a = datetime.now()
    # print('Start time: ', a.strftime('%H:%M:%S'))
    #
    # # stage1 training
    # torch.cuda.reset_peak_memory_stats()
    # print('Training start ')
    # model_train = Training(config)
    # for epoch in range(config.epochs_stage):
    #     print('Epoch:', epoch)
    #     model_train.train(epoch)
    #     # loss = model_train.train(epoch)
    #     # if epoch > 0 and loss < 0.14:
    #     #     break
    #
    # b = datetime.now()
    # print('End time: ', b.strftime('%H:%M:%S'))
    # c = b-a
    # minutes = divmod(c.seconds, 60)
    # print('Time used: ', minutes[0], 'minutes', minutes[1], 'seconds')
    #
    # print('Write embeddings')
    # model_train.write_embeddings()
    # print('Training finished: ', datetime.now().strftime('%H:%M:%S'))
    # print("torch.cuda.max_memory_allocated: %fGB" % (torch.cuda.max_memory_allocated(0) / 1024 / 1024 / 1024))




if __name__ == "__main__":
    main()



