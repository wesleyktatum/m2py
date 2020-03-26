import torch
import torch.nn as nn
import torch.nn.functional as F

class ThresholdedMSELoss(nn.Module):
    """
    This class contains loss functions that use a mean-squared-error loss for reasonable predictions.
    They inherit from torch.nn.Module just like the custom model. For physically unreasonable conditions,
    prediction loss is more severely calculated. What qualifies as reasonable is based on empirically
    gathered datasets and literature reported boundaries of performance.
    
    For the following predictions that are improbable, the loss is penalized:
    - X < lower
    - X > upper
    """

    def __init__(self, lower, upper):
        super(ThresholdedMSELoss, self).__init__()
        self.lower = lower
        self.upper = upper

    def forward(self, predictions, labels):
#         print (predictions.size())
#         print (labels.size())
        
        result_list = torch.zeros(predictions.size(0))
        element_count = 0
        correct = 0
        
        for x, y in zip(predictions, labels):
#             print (f"{el_count+1}/{result_list.size(0)}")
            
            # if (x >= 0) == 1 (True)
            if torch.le(x, torch.tensor([self.lower])) == torch.tensor([1]):
                #Exponential MSE for x <= 0
#                 print(f"prediction = {x}, lower threshold violated")

                # Need to use only torch.nn.Function() and torch.() functions for autograd to track operations
                error = torch.add(x, torch.neg(y)) #error = x + (-y)
        
                #if precision <= 10%, count as correct
                if torch.le(torch.div(error, y), torch.tensor(0.1)) == torch.tensor([1]):
                    correct += 1
            
                element_result = torch.pow(error, 2)
                element_result = torch.pow(element_result, 1)
            

           # if (x <= 6) == 1 (True)
            elif torch.ge(x, torch.tensor([self.upper])) == torch.tensor([1]):
                #exponential MSE for x >= 6
#                 print(f"prediction = {x}, upper threshold violated")
                error = torch.add(x, torch.neg(y))
            
            #if precision <= 10%, count as correct
                if torch.le(torch.div(error, y), torch.tensor(0.1)) == torch.tensor([1]):
                    correct += 1
            
                element_result = torch.pow(error, 2)
                element_result = torch.pow(element_result, 1)

                # all other values of x
            else:
#                 print(f"prediction = {x}")
                error = torch.add(x, torch.neg(y))
                
                #if precision <= 10%, count as correct
                if torch.le(torch.div(error, y), torch.tensor(0.1)) == torch.tensor([1]):
                    correct += 1
            
                element_result = torch.pow(error, 2)
                
            result_list[el_count] = element_result
            element_count+=1
            
            accuracy = correct/element_count

            result = result_list.mean()

            return result, accuracy

