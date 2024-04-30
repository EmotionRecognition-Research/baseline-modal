'''
This code is based on https://github.com/okankop/Efficient-3DCNNs
'''
import os
import pandas as pd
import torch
from torch.autograd import Variable
import time
from utils import AverageMeter, calculate_accuracy
from sklearn.metrics import confusion_matrix, precision_score, recall_score
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import ConfusionMatrixDisplay
import gc

file_path = "results.csv"

# Define the expected column names
expected_columns = ['target', 'prediction', 'accent', 'modality']

global df

try:
    # Try reading the CSV file with the expected column names
    df = pd.read_csv(file_path, usecols=expected_columns)
except ValueError:
    # If specified columns are not found, read the CSV file without specifying columns
    df = pd.read_csv(file_path)
    
    # Rename the existing headers to match the expected column names
    df.columns = expected_columns


def val_epoch_multimodal(epoch, data_loader, model, criterion, opt, logger,modality='both',dist=None ):
    #for evaluation with single modality, specify which modality to keep and which distortion to apply for the other modaltiy:
    #'noise', 'addnoise' or 'zeros'. for paper procedure, with 'softhard' mask use 'zeros' for evaluation, with 'noise' use 'noise'
    print('validation at epoch {}'.format(epoch))
    assert modality in ['both', 'audio', 'video']
    gc.collect()
    torch.cuda.empty_cache()    
    model.eval()

    batch_time = AverageMeter()
    data_time = AverageMeter()
    losses = AverageMeter()
    top1 = AverageMeter()
    top5 = AverageMeter()

    end_time = time.time()
    
    all_targets = []
    all_outputs = []
    
    for i, (inputs_audio, inputs_visual, targets) in enumerate(data_loader):
        global df
        data_time.update(time.time() - end_time)
        
        if modality == 'audio':
            print('Skipping video modality')
            if dist == 'noise':
                print('Evaluating with full noise')
                inputs_visual = torch.randn(inputs_visual.size())
            elif dist == 'addnoise': #opt.mask == -4:
                print('Evaluating with noise')
                inputs_visual = inputs_visual + (torch.mean(inputs_visual) + torch.std(inputs_visual)*torch.randn(inputs_visual.size()))
            elif dist == 'zeros':
                inputs_visual = torch.zeros(inputs_visual.size())
            else:
                print('UNKNOWN DIST!')
        elif modality == 'video':
            print('Skipping audio modality')
            if dist == 'noise':
                print('Evaluating with noise')
                inputs_audio = torch.randn(inputs_audio.size())
            elif dist == 'addnoise': #opt.mask == -4:
                print('Evaluating with added noise')
                inputs_audio = inputs_audio + (torch.mean(inputs_audio) + torch.std(inputs_audio)*torch.randn(inputs_audio.size()))

            elif dist == 'zeros':
                inputs_audio = torch.zeros(inputs_audio.size())
        inputs_visual = inputs_visual.permute(0,2,1,3,4)
        inputs_visual = inputs_visual.reshape(inputs_visual.shape[0]*inputs_visual.shape[1], inputs_visual.shape[2], inputs_visual.shape[3], inputs_visual.shape[4])
        
        
        
        targets = targets.to(opt.device)
        # all_targets.extend(targets)
        with torch.no_grad():
            inputs_visual = Variable(inputs_visual)
            inputs_audio = Variable(inputs_audio)
            targets = Variable(targets)
        outputs = model(inputs_audio, inputs_visual)
        # all_outputs.extend(outputs)
        loss = criterion(outputs, targets)
        prec1, prec5 = calculate_accuracy(outputs.data, targets.data, topk=(1,5))
        top1.update(prec1, inputs_audio.size(0))
        top5.update(prec5, inputs_audio.size(0))

        losses.update(loss.data, inputs_audio.size(0))

        batch_time.update(time.time() - end_time)
        end_time = time.time()
        
        # Flatten the tensors
        targets_flat = targets.detach().cpu().numpy().flatten()
        outputs_flat = outputs.argmax(dim=1).detach().cpu().numpy()
        # print(targets_flat, outputs_flat)

        # Create DataFrame
        new_data = pd.DataFrame({'target': targets_flat, 'prediction': outputs_flat, 'accent': [1] * len(targets_flat), 'modality': [1] * len(targets_flat)})
        
        # Append the values to the DataFrame
        df = pd.concat([df, new_data], ignore_index=True)
        del targets
        del outputs

        print('Epoch: [{0}][{1}/{2}]\t'
              'Time {batch_time.val:.5f} ({batch_time.avg:.5f})\t'
              'Data {data_time.val:.5f} ({data_time.avg:.5f})\t'
              'Loss {loss.val:.4f} ({loss.avg:.4f})\t'
              'Prec@1 {top1.val:.5f} ({top1.avg:.5f})\t'
              'Prec@5 {top5.val:.5f} ({top5.avg:.5f})'.format(
                  epoch,
                  i + 1,
                  len(data_loader),
                  batch_time=batch_time,
                  data_time=data_time,
                  loss=losses,
                  top1=top1,
                  top5=top5))

    log = {
            'epoch': epoch,
            'loss': losses.avg.item(),
            'prec1': top1.avg.item(),
            'prec5': top5.avg.item()
        }
    logger.log(log)

    return losses.avg.item(), top1.avg.item(), log, all_targets, all_outputs

def val_epoch(epoch, data_loader, model, criterion, opt, logger, modality='both', dist=None, is_testing=False):
    print('validation at epoch {}'.format(epoch))
    targets = []
    outputs = []
    
    if opt.model == 'multimodalcnn':
        loss, prec1, log, targets, outputs = val_epoch_multimodal(epoch, data_loader, model, criterion, opt, logger, modality, dist=dist)

    df.to_csv(file_path)
    
    if is_testing:
        # Convert targets and outputs to numpy arrays
        targets_np = targets.cpu().numpy()
        outputs_np = outputs.cpu().numpy()

        # Calculate confusion matrix
        conf_mat = confusion_matrix(targets_np, outputs_np)

        # Calculate precision and recall
        precision = precision_score(targets_np, outputs_np, average='macro')
        recall = recall_score(targets_np, outputs_np, average='macro')

        # Add these metrics to the log
        log['confusion_matrix'] = conf_mat
        log['precision'] = precision
        log['recall'] = recall
        
        # Plot confusion matrix
        fig, ax = plt.subplots(figsize=(10, 10))
        disp = ConfusionMatrixDisplay(confusion_matrix=conf_mat)
        disp.plot(cmap=plt.cm.Blues, ax=ax)
        plt.savefig('confusion_matrix.png')

    return loss, prec1, log
