/**
 * Widget Configuration Model
 * Defines the structure for widget configurations including Python code execution
 */

export type WidgetType = 'chart' | 'table' | 'metric' | 'custom';

export interface WidgetConfig {
  id: string;
  name: string;
  type: WidgetType;
  pythonCode: string;
  parameters?: Record<string, any>;
  refreshInterval?: number; // in seconds
  description?: string;
}

export interface WidgetExecutionRequest {
  widgetId: string;
  pythonCode: string;
  parameters?: Record<string, any>;
}

export interface WidgetExecutionResult {
  success: boolean;
  data?: any;
  error?: string;
  executionTime?: number;
}
