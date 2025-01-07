export interface ModelStats {
  accuracy: number;
  precision: number;
  recall: number;
  f1Score: number;
}

export interface ConfusionMatrix {
  truePositive: number;
  trueNegative: number;
  falsePositive: number;
  falseNegative: number;
}

export interface Result {
  id: string;
  actualLabel: string;
  predictedLabel: string;
  confidence: number;
  timestamp: string;
}

export interface ShapValue {
  name: string;
  value: number;
}

export interface ModelData {
  name: string;
  stats: ModelStats;
  confusionMatrix: ConfusionMatrix;
  results: Result[];
  paperUrl: string;
}
