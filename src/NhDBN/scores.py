import numpy as np
import matplotlib.pyplot as plt
from systemUtils import clean_figures_folder
from pprint import pprint
from sklearn.metrics import roc_curve, auc
from systemUtils import writeOutputFile

def adjMatrixRoc(adjMatrixProp, trueAdjMatrix, verbose):
  if verbose:
    print('\nThe true adj matrix is: \n') ; writeOutputFile('\nThe true adj matrix is: \n')
    pprint(trueAdjMatrix) ; writeOutputFile(str(trueAdjMatrix))
    print('\nThe proposed adj matrix is: \n') ; writeOutputFile('\nThe proposed adj matrix is: \n')
    pprint(adjMatrixProp) ; writeOutputFile(str(adjMatrixProp))
  # Remove the diagonal that is allways going to be right
  trueAdjMatrixNoDiag = []
  idxToRemove = 0
  for row in trueAdjMatrix:
    row.pop(idxToRemove)
    trueAdjMatrixNoDiag.append(row)
    idxToRemove + 1
  # Now for the inferred matrix  
  adjMatrixPropNoDiag = []
  idxToRemove = 0
  for row in adjMatrixProp:
    row.pop(idxToRemove)
    adjMatrixPropNoDiag.append(row)
    idxToRemove + 1
  # Re-assign them
  trueAdjMatrix = trueAdjMatrixNoDiag
  adjMatrixProp = adjMatrixPropNoDiag

  # Flatten the adj matrix to pass to the RoC
  flattened_true = [item for sublist in trueAdjMatrix for item in sublist]
  flattened_true = [1 if item else 0 for item in flattened_true] # convert to binary response vector
  flattened_scores = [item for sublist in adjMatrixProp for item in sublist]
  
  drawRoc(flattened_scores, flattened_true) # Draw the RoC curve

def drawRoc(inferredScoreEdges, realEdges):
  # Calculate false positive rate and true positive rate
  fpr, tpr, threshold = roc_curve(realEdges, inferredScoreEdges)
  roc_auc = auc(fpr, tpr)
  # Plot the RoC curve
  plt.title('Receiver Operating Characteristic')
  plt.plot(fpr, tpr, marker = 'D', label = 'AUC = %0.2f' % roc_auc)
  plt.legend(loc = 'lower right')
  plt.plot([0, 1], [0, 1],'r--')
  #plt.xlim([0, 1])
  #plt.ylim([0, 1])
  plt.ylabel('True Positive Rate')
  plt.xlabel('False Positive Rate')
  #plt.show() #uncomment to show the figure on finish
  clean_figures_folder('figures/')
  figure_route = 'figures/roc'
  plt.savefig(figure_route, bbox_inches='tight')

def calculateFeatureScores(selectedFeaturesVector, totalDims, currentFeatures, currentResponse):
  adjRow = [0 for x in range(totalDims)]
  
  # Print and write the output
  output_line = (
    '\n>> The current response feature is: X{0}\n'.format(currentResponse + 1)
  )
  print(output_line) ; writeOutputFile(output_line)

  results = {}
  for feat in currentFeatures:
    output_line = (
      '  Edge score for X{0}: '.format(feat + 1)
    )
    print(output_line) ; writeOutputFile(output_line)
    freqSum = 0
    # Calculate the % of apperance
    for currentPi in selectedFeaturesVector:
      if feat in currentPi:
        freqSum = freqSum + 1
    
    # Append to the dictionary of the results
    results['X' + str(feat + 1)] = freqSum / len(selectedFeaturesVector)
    output_line = (
      str(results['X' + str(feat + 1)]) + '\n'
    )
    print(output_line) ; writeOutputFile(output_line)
    # Better return a row on the proposed adj matrix
    adjRow[feat] = freqSum / len(selectedFeaturesVector)

  return adjRow
    
def testFeatureScores():
  dummyData = [
    np.array([1, 3, 6]),
    np.array([1, 3]),
    np.array([8]),
    np.array([9 , 10])
  ]
  
  calculateFeatureScores(dummyData, 10)

def testRocDraw():
  dummyData = {
    'X1': 0.11,
    'X2': 0.99,
    'X3': 0.10,
    'X4': 0.50,
    'X5': 0.99,
    'X6': 0.10
  }

  realEdges = {
    'X1': 0,
    'X2': 1,
    'X3': 0,
    'X4': 0,
    'X5': 1,
    'X6': 0
  }

  y_score = np.array(list(dummyData.values()))
  y_real = np.array(list(realEdges.values()))
  # Test func
  drawRoc(y_score, y_real)

if __name__ == '__main__':
  #testFeatureScores()
  testRocDraw()
  