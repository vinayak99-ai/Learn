import { Component, Input, OnInit } from '@angular/core';

/**
 * Chart Widget Component
 * Displays data in chart format
 */
@Component({
  selector: 'app-chart-widget',
  template: `
    <div class="chart-widget">
      <div *ngIf="!chartData || chartData.length === 0" class="no-data">
        No chart data available
      </div>
      
      <div *ngIf="chartData && chartData.length > 0" class="chart-container">
        <!-- Simple bar chart visualization -->
        <div class="chart-bars">
          <div class="chart-bar" *ngFor="let item of chartData">
            <div class="bar-label">{{ item.label || item.name }}</div>
            <div class="bar-wrapper">
              <div class="bar-fill" 
                   [style.width.%]="getBarWidth(item.value)"
                   [title]="item.value">
              </div>
              <span class="bar-value">{{ item.value }}</span>
            </div>
          </div>
        </div>
        
        <!-- Chart metadata -->
        <div class="chart-metadata" *ngIf="metadata">
          <div *ngIf="metadata.title" class="chart-title">{{ metadata.title }}</div>
          <div *ngIf="metadata.subtitle" class="chart-subtitle">{{ metadata.subtitle }}</div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .chart-widget {
      padding: 16px;
    }

    .no-data {
      text-align: center;
      padding: 40px;
      color: #999;
      font-style: italic;
    }

    .chart-container {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .chart-bars {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .chart-bar {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .bar-label {
      min-width: 120px;
      font-size: 14px;
      font-weight: 500;
      color: #333;
    }

    .bar-wrapper {
      flex: 1;
      display: flex;
      align-items: center;
      gap: 8px;
      position: relative;
    }

    .bar-fill {
      height: 30px;
      background: linear-gradient(90deg, #3498db, #2980b9);
      border-radius: 4px;
      transition: width 0.3s ease;
      min-width: 2px;
    }

    .bar-value {
      font-size: 14px;
      font-weight: 600;
      color: #333;
      min-width: 60px;
    }

    .chart-metadata {
      margin-top: 16px;
      padding-top: 16px;
      border-top: 1px solid #e0e0e0;
    }

    .chart-title {
      font-size: 16px;
      font-weight: 600;
      color: #333;
      margin-bottom: 4px;
    }

    .chart-subtitle {
      font-size: 14px;
      color: #666;
    }
  `]
})
export class ChartWidgetComponent implements OnInit {
  @Input() data: any;

  chartData: any[] = [];
  metadata: any = null;
  maxValue = 0;

  ngOnInit(): void {
    this.processData();
  }

  processData(): void {
    if (!this.data) return;

    // Handle different data formats
    if (Array.isArray(this.data)) {
      this.chartData = this.data;
    } else if (this.data.data && Array.isArray(this.data.data)) {
      this.chartData = this.data.data;
      this.metadata = this.data.metadata;
    } else if (typeof this.data === 'object') {
      // Convert object to array format
      this.chartData = Object.keys(this.data).map(key => ({
        label: key,
        value: this.data[key]
      }));
    }

    // Calculate max value for bar width calculation
    this.maxValue = Math.max(...this.chartData.map(item => 
      typeof item.value === 'number' ? item.value : 0
    ));
  }

  getBarWidth(value: number): number {
    if (this.maxValue === 0) return 0;
    return (value / this.maxValue) * 100;
  }
}
