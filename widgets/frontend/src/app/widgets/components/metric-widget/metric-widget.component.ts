import { Component, Input, OnInit } from '@angular/core';

/**
 * Metric Widget Component
 * Displays key metrics/KPIs
 */
@Component({
  selector: 'app-metric-widget',
  template: `
    <div class="metric-widget">
      <div *ngIf="!metrics || metrics.length === 0" class="no-data">
        No metrics available
      </div>
      
      <div *ngIf="metrics && metrics.length > 0" class="metrics-container">
        <div class="metric-card" *ngFor="let metric of metrics">
          <div class="metric-icon" *ngIf="metric.icon">{{ metric.icon }}</div>
          <div class="metric-content">
            <div class="metric-label">{{ metric.label || metric.name }}</div>
            <div class="metric-value" [class]="getMetricClass(metric)">
              {{ formatValue(metric.value) }}
            </div>
            <div class="metric-change" *ngIf="metric.change !== undefined">
              <span [class.positive]="metric.change > 0" 
                    [class.negative]="metric.change < 0">
                {{ metric.change > 0 ? '↑' : '↓' }} {{ Math.abs(metric.change) }}%
              </span>
            </div>
            <div class="metric-description" *ngIf="metric.description">
              <small>{{ metric.description }}</small>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .metric-widget {
      padding: 16px;
    }

    .no-data {
      text-align: center;
      padding: 40px;
      color: #999;
      font-style: italic;
    }

    .metrics-container {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
    }

    .metric-card {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      border-radius: 8px;
      padding: 20px;
      color: white;
      display: flex;
      flex-direction: column;
      gap: 8px;
      transition: transform 0.2s;
    }

    .metric-card:hover {
      transform: translateY(-2px);
    }

    .metric-card:nth-child(2) {
      background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }

    .metric-card:nth-child(3) {
      background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }

    .metric-card:nth-child(4) {
      background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
    }

    .metric-icon {
      font-size: 32px;
      margin-bottom: 8px;
    }

    .metric-content {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .metric-label {
      font-size: 14px;
      opacity: 0.9;
      font-weight: 500;
    }

    .metric-value {
      font-size: 28px;
      font-weight: 700;
      margin: 8px 0;
    }

    .metric-value.large {
      font-size: 32px;
    }

    .metric-change {
      font-size: 14px;
      font-weight: 600;
    }

    .metric-change .positive {
      color: #4caf50;
    }

    .metric-change .negative {
      color: #f44336;
    }

    .metric-description {
      font-size: 12px;
      opacity: 0.8;
      margin-top: 4px;
    }
  `]
})
export class MetricWidgetComponent implements OnInit {
  @Input() data: any;

  metrics: any[] = [];
  Math = Math;

  ngOnInit(): void {
    this.processData();
  }

  processData(): void {
    if (!this.data) return;

    // Handle different data formats
    if (Array.isArray(this.data)) {
      this.metrics = this.data;
    } else if (this.data.metrics && Array.isArray(this.data.metrics)) {
      this.metrics = this.data.metrics;
    } else if (typeof this.data === 'object') {
      // Convert single metric object or key-value pairs
      if (this.data.label && this.data.value !== undefined) {
        this.metrics = [this.data];
      } else {
        this.metrics = Object.keys(this.data).map(key => ({
          label: key,
          value: this.data[key]
        }));
      }
    }
  }

  formatValue(value: any): string {
    if (typeof value === 'number') {
      // Format large numbers with K, M, B suffixes
      if (value >= 1000000000) {
        return (value / 1000000000).toFixed(1) + 'B';
      } else if (value >= 1000000) {
        return (value / 1000000).toFixed(1) + 'M';
      } else if (value >= 1000) {
        return (value / 1000).toFixed(1) + 'K';
      }
      return value.toLocaleString();
    }
    return String(value);
  }

  getMetricClass(metric: any): string {
    if (typeof metric.value === 'number' && metric.value >= 1000000) {
      return 'large';
    }
    return '';
  }
}
