##+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
## Created by: Yaoyao Liu
## NUS School of Computing
## yaoyao.liu@u.nus.edu
## Copyright (c) 2019
##
## This source code is licensed under the MIT-style license found in the
## LICENSE file in the root directory of this source tree
##+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import os

def run_exp(PHASE='META'):
    GPU_ID = 0
    MAX_ITER = 15000
    SHOT_NUM = 1
    PRE_ITER = 10000
    UPDATE_NUM = 20
    META_BATCH_SIZE = 2
    GPU_MODE = 'False'
    WAY_NUM = 5
    LOG_DIR = 'experiment_results'
    PRE_TRA_ITER_MAX = 12000
    PRE_TRA_DROP = 0.9
    SAVE_STEP = 1000
    LR_DROP_STEP = 1000
    PRE_TRA_FLD = './data/pre-train/mini_nh/train'
    PRE_TRA_LAB = 'mini_nh' 

    base_command = 'python main.py --metatrain_iterations=' + str(MAX_ITER) \
        + ' --meta_batch_size=' + str(META_BATCH_SIZE) \
        + ' --shot_num=' + str(SHOT_NUM) \
        + ' --base_lr=0.01' \
        + ' --train_base_epoch_num=' + str(UPDATE_NUM) \
        + ' --way_num=' + str(WAY_NUM) \
        + ' --exp_log_label=' + LOG_DIR \
        + ' --pretrain_dropout=' + str(PRE_TRA_DROP) \
        + ' --activation=leaky_relu' \
        + ' --pre_lr=0.001' \
        + ' --pre_lr_dropstep=5000' \
        + ' --meta_save_step=' + str(SAVE_STEP) \
        + ' --lr_drop_step=' + str(LR_DROP_STEP) \
        + ' --pretrain_folders=' + PRE_TRA_FLD \
        + ' --pretrain_label=' + PRE_TRA_LAB \
        + ' --full_gpu_memory_mode=' + GPU_MODE \
        + ' --device_id=' + str(GPU_ID)

    def process_test_command(TEST_STEP, in_command):
        output_test_command = in_command + ' --phase=meta' + ' --pretrain_iterations=' + str(PRE_ITER) + ' --metatrain=False --test_iter=' + str(TEST_STEP)
        return output_test_command

    def process_test_command_aug(TEST_STEP, in_command):
        output_test_command = in_command + ' --phase=meta' + ' --pretrain_iterations=' + str(PRE_ITER) + ' --metatrain=False --test_iter=' + str(TEST_STEP) + ' --test_base_augmentation=True'
        return output_test_command

    if PHASE=='PRE':
        print('****** Start Pre-training Phase ******')
        pre_command = base_command + ' --phase=pre' + ' --pretrain_iterations=15000'
        os.system(pre_command)

    if PHASE=='META':
        print('****** Start Meta-training Phase ******')
        meta_train_command = base_command + ' --phase=meta' + ' --pretrain_iterations=' + str(PRE_ITER)
        os.system(meta_train_command)

    if PHASE=='META_TE':
        print('****** Start Meta-test Phase ******')

        test_command = process_test_command(0, base_command)
        os.system(test_command)
        for idx in range(MAX_ITER-1):
            if idx!=0 and idx%SAVE_STEP==0:
                test_command = process_test_command(idx, base_command)
                os.system(test_command)
        test_command = process_test_command(MAX_ITER, base_command)
        os.system(test_command)

run_exp(PHASE='PRE')
run_exp(PHASE='META')
run_exp(PHASE='META_TE')
