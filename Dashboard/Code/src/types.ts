export interface ModelResult {
  id: string;
  actualLabel: string;
  predictedLabel: string;
  confidence: number;
  timestamp: string;
}

export interface ConfusionMatrixData {
  truePositive: number;
  trueNegative: number;
  falsePositive: number;
  falseNegative: number;
}

export interface ModelStats {
  accuracy: number;
  precision: number;
  recall: number;
  f1Score: number;
}

export interface ShapData {
  name: string;
  value: number;
}

export interface ModelData {
  name: string;
  stats: ModelStats;
  confusionMatrix: ConfusionMatrixData;
  results: ModelResult[];
  shapValues: ShapData[];
  paperUrl?: string;
}