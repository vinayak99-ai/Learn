# Using Plotly.js in Angular: A Detailed Guide

This guide walks you through integrating [Plotly.js](https://plotly.com/javascript/) into an Angular application to create dynamic, data-driven charts. You will learn how to install dependencies, configure Angular modules, create batch charts, fetch data from external APIs, and build a real-world sales-monitoring dashboard.

---

## Table of Contents

1. [Installing Dependencies](#1-installing-dependencies)
2. [Basic Plotly.js Integration with Angular](#2-basic-plotlyjs-integration-with-angular)
3. [Dynamic Batch Chart Creation](#3-dynamic-batch-chart-creation)
4. [Using API Data](#4-using-api-data)
5. [Real-World Example: Sales Dashboard](#5-real-world-example-sales-dashboard)
6. [Additional Enhancements](#6-additional-enhancements)

---

## 1. Installing Dependencies

Install the Angular Plotly wrapper and the full Plotly.js distribution:

```bash
npm install angular-plotly.js plotly.js-dist
```

If your project uses TypeScript, you should also install the community type definitions:

```bash
npm install --save-dev @types/plotly.js
```

---

## 2. Basic Plotly.js Integration with Angular

### 2.1 Import `PlotlyModule` in `AppModule`

Open `src/app/app.module.ts` and add the `PlotlyModule` import:

```typescript
// src/app/app.module.ts
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';

import * as PlotlyJS from 'plotly.js-dist';
import { PlotlyModule } from 'angular-plotly.js';

PlotlyModule.plotlyjs = PlotlyJS;

import { AppComponent } from './app.component';
import { DashboardComponent } from './dashboard/dashboard.component';

@NgModule({
  declarations: [AppComponent, DashboardComponent],
  imports: [
    BrowserModule,
    HttpClientModule,
    PlotlyModule,
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
```

> **Note:** You must assign the `plotly.js-dist` object to `PlotlyModule.plotlyjs` **before** `PlotlyModule` is listed in `imports`. This is required by `angular-plotly.js` v2+.

### 2.2 Render a Single Chart in a Component

```typescript
// src/app/app.component.ts
import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  template: `
    <plotly-plot
      [data]="graph.data"
      [layout]="graph.layout">
    </plotly-plot>
  `,
})
export class AppComponent {
  graph = {
    data: [
      {
        x: ['Jan', 'Feb', 'Mar', 'Apr'],
        y: [10, 15, 13, 17],
        type: 'bar',
        name: 'Monthly Sales',
      },
    ],
    layout: {
      title: 'Monthly Sales',
      xaxis: { title: 'Month' },
      yaxis: { title: 'Sales (USD)' },
    },
  };
}
```

The `<plotly-plot>` component accepts `[data]` and `[layout]` bindings that map directly to the Plotly.js API.

---

## 3. Dynamic Batch Chart Creation

When you need to render multiple charts (a "batch"), store each chart's configuration in an array and iterate over it with `*ngFor`.

### 3.1 Chart Configuration Interface

```typescript
// src/app/models/chart-config.model.ts
export interface ChartConfig {
  id: string;
  title: string;
  data: Partial<Plotly.PlotData>[];
  layout: Partial<Plotly.Layout>;
}
```

### 3.2 Component with Batch Charts

```typescript
// src/app/dashboard/dashboard.component.ts
import { Component, OnInit } from '@angular/core';
import { ChartConfig } from '../models/chart-config.model';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
})
export class DashboardComponent implements OnInit {
  charts: ChartConfig[] = [];

  ngOnInit(): void {
    this.charts = this.buildCharts();
  }

  private buildCharts(): ChartConfig[] {
    return [
      {
        id: 'bar-chart',
        title: 'Sales by Region',
        data: [
          {
            x: ['North', 'South', 'East', 'West'],
            y: [120, 95, 140, 80],
            type: 'bar',
            marker: { color: ['#636EFA', '#EF553B', '#00CC96', '#AB63FA'] },
          },
        ],
        layout: { title: 'Sales by Region', xaxis: { title: 'Region' }, yaxis: { title: 'Revenue ($)' } },
      },
      {
        id: 'pie-chart',
        title: 'Traffic Sources',
        data: [
          {
            labels: ['Organic', 'Paid', 'Social', 'Referral'],
            values: [40, 25, 20, 15],
            type: 'pie',
            hole: 0.3,
          },
        ],
        layout: { title: 'Traffic Sources' },
      },
      {
        id: 'line-chart',
        title: 'Revenue vs Expenses',
        data: [
          {
            x: ['Q1', 'Q2', 'Q3', 'Q4'],
            y: [50000, 65000, 72000, 90000],
            type: 'scatter',
            mode: 'lines+markers',
            name: 'Revenue',
            line: { color: '#00CC96' },
          },
          {
            x: ['Q1', 'Q2', 'Q3', 'Q4'],
            y: [40000, 48000, 55000, 62000],
            type: 'scatter',
            mode: 'lines+markers',
            name: 'Expenses',
            line: { color: '#EF553B' },
          },
        ],
        layout: { title: 'Revenue vs Expenses', xaxis: { title: 'Quarter' }, yaxis: { title: 'Amount ($)' } },
      },
    ];
  }
}
```

### 3.3 Template with `*ngFor`

```html
<!-- src/app/dashboard/dashboard.component.html -->
<section class="dashboard">
  <div class="chart-wrapper" *ngFor="let chart of charts">
    <h2>{{ chart.title }}</h2>
    <plotly-plot
      [data]="chart.data"
      [layout]="chart.layout"
      [config]="{ responsive: true }">
    </plotly-plot>
  </div>
</section>
```

Setting `[config]="{ responsive: true }"` makes every chart resize automatically when the browser window changes size.

---

## 4. Using API Data

### 4.1 Chart Data Service

```typescript
// src/app/services/chart-data.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { ChartConfig } from '../models/chart-config.model';

interface ApiChartResponse {
  id: string;
  title: string;
  type: 'bar' | 'pie' | 'scatter';
  labels?: string[];
  values: number[];
  series?: { name: string; values: number[] }[];
}

@Injectable({ providedIn: 'root' })
export class ChartDataService {
  private readonly apiUrl = 'https://api.example.com/charts';

  constructor(private http: HttpClient) {}

  getCharts(): Observable<ChartConfig[]> {
    return this.http
      .get<ApiChartResponse[]>(this.apiUrl)
      .pipe(map((responses) => responses.map(this.toChartConfig)));
  }

  private toChartConfig(response: ApiChartResponse): ChartConfig {
    const baseLayout: Partial<Plotly.Layout> = { title: response.title };

    switch (response.type) {
      case 'bar':
        return {
          id: response.id,
          title: response.title,
          data: [{ x: response.labels, y: response.values, type: 'bar' }],
          layout: { ...baseLayout, xaxis: { title: 'Category' }, yaxis: { title: 'Value' } },
        };

      case 'pie':
        return {
          id: response.id,
          title: response.title,
          data: [{ labels: response.labels, values: response.values, type: 'pie' }],
          layout: baseLayout,
        };

      case 'scatter':
        return {
          id: response.id,
          title: response.title,
          data: (response.series ?? []).map((s) => ({
            x: response.labels,
            y: s.values,
            type: 'scatter',
            mode: 'lines+markers',
            name: s.name,
          })),
          layout: { ...baseLayout, xaxis: { title: 'Period' }, yaxis: { title: 'Value' } },
        };

      default:
        return { id: response.id, title: response.title, data: [], layout: baseLayout };
    }
  }
}
```

### 4.2 Loading Charts from the API

```typescript
// src/app/dashboard/dashboard.component.ts  (API version)
import { Component, OnInit } from '@angular/core';
import { ChartDataService } from '../services/chart-data.service';
import { ChartConfig } from '../models/chart-config.model';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
})
export class DashboardComponent implements OnInit {
  charts: ChartConfig[] = [];
  loading = true;
  error: string | null = null;

  constructor(private chartDataService: ChartDataService) {}

  ngOnInit(): void {
    this.chartDataService.getCharts().subscribe({
      next: (charts) => {
        this.charts = charts;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load charts. Please try again.';
        this.loading = false;
        console.error(err);
      },
    });
  }
}
```

```html
<!-- src/app/dashboard/dashboard.component.html  (API version) -->
<div *ngIf="loading">Loading charts…</div>
<div *ngIf="error" class="error">{{ error }}</div>

<section class="dashboard" *ngIf="!loading && !error">
  <div class="chart-wrapper" *ngFor="let chart of charts">
    <plotly-plot
      [data]="chart.data"
      [layout]="chart.layout"
      [config]="{ responsive: true }">
    </plotly-plot>
  </div>
</section>
```

---

## 5. Real-World Example: Sales Dashboard

### 5.1 Scenario

A sales manager needs a single-page dashboard showing:

| Chart | Type | Description |
|---|---|---|
| Sales by Region | Bar | Compares total revenue across four geographic regions |
| Traffic Sources | Pie | Shows the percentage breakdown of website traffic origins |
| Revenue vs Expenses | Line | Tracks quarterly revenue and expenses side by side |

### 5.2 Example API Response

```json
[
  {
    "id": "sales-by-region",
    "title": "Sales by Region",
    "type": "bar",
    "labels": ["North", "South", "East", "West"],
    "values": [120000, 95000, 140000, 80000]
  },
  {
    "id": "traffic-sources",
    "title": "Traffic Sources",
    "type": "pie",
    "labels": ["Organic", "Paid", "Social", "Referral"],
    "values": [40, 25, 20, 15]
  },
  {
    "id": "revenue-vs-expenses",
    "title": "Revenue vs Expenses",
    "type": "scatter",
    "labels": ["Q1", "Q2", "Q3", "Q4"],
    "series": [
      { "name": "Revenue",  "values": [50000, 65000, 72000, 90000] },
      { "name": "Expenses", "values": [40000, 48000, 55000, 62000] }
    ]
  }
]
```

### 5.3 Full Dashboard Implementation

#### Sales Dashboard Component

```typescript
// src/app/sales-dashboard/sales-dashboard.component.ts
import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subject, takeUntil } from 'rxjs';
import { ChartDataService } from '../services/chart-data.service';
import { ChartConfig } from '../models/chart-config.model';

@Component({
  selector: 'app-sales-dashboard',
  templateUrl: './sales-dashboard.component.html',
  styleUrls: ['./sales-dashboard.component.scss'],
})
export class SalesDashboardComponent implements OnInit, OnDestroy {
  charts: ChartConfig[] = [];
  loading = true;
  error: string | null = null;

  private destroy$ = new Subject<void>();

  constructor(private chartDataService: ChartDataService) {}

  ngOnInit(): void {
    this.chartDataService
      .getCharts()
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (charts) => {
          this.charts = charts;
          this.loading = false;
        },
        error: (err) => {
          this.error = 'Unable to load dashboard data.';
          this.loading = false;
          console.error(err);
        },
      });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

#### Sales Dashboard Template

```html
<!-- src/app/sales-dashboard/sales-dashboard.component.html -->
<div class="sales-dashboard">
  <header>
    <h1>Sales Performance Dashboard</h1>
  </header>

  <div class="loading-spinner" *ngIf="loading">Loading…</div>
  <div class="error-message" *ngIf="error">{{ error }}</div>

  <div class="charts-grid" *ngIf="!loading && !error">
    <div
      class="chart-card"
      *ngFor="let chart of charts"
      [attr.data-chart-id]="chart.id">
      <plotly-plot
        [data]="chart.data"
        [layout]="chart.layout"
        [config]="{ responsive: true, displayModeBar: true }">
      </plotly-plot>
    </div>
  </div>
</div>
```

#### Sales Dashboard Styles

```scss
/* src/app/sales-dashboard/sales-dashboard.component.scss */
.sales-dashboard {
  padding: 1.5rem;
  font-family: sans-serif;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.chart-card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
  padding: 1rem;
  overflow: hidden;
}

.error-message {
  color: #d32f2f;
  padding: 1rem;
}
```

---

## 6. Additional Enhancements

### 6.1 Real-Time Updates with Observables or WebSockets

Use an interval or a WebSocket to push fresh data into an existing chart without re-mounting the component.

#### Polling with `interval`

```typescript
import { Component, OnInit, OnDestroy } from '@angular/core';
import { interval, Subscription, switchMap } from 'rxjs';
import { ChartDataService } from '../services/chart-data.service';
import { ChartConfig } from '../models/chart-config.model';

@Component({ selector: 'app-realtime-chart', template: `
  <plotly-plot *ngIf="chart" [data]="chart.data" [layout]="chart.layout"></plotly-plot>
` })
export class RealtimeChartComponent implements OnInit, OnDestroy {
  chart: ChartConfig | null = null;
  private subscription!: Subscription;

  constructor(private chartDataService: ChartDataService) {}

  ngOnInit(): void {
    // Poll every 5 seconds
    this.subscription = interval(5000)
      .pipe(switchMap(() => this.chartDataService.getCharts()))
      .subscribe((charts) => (this.chart = charts[0] ?? null));
  }

  ngOnDestroy(): void {
    this.subscription.unsubscribe();
  }
}
```

#### WebSocket Integration

```typescript
import { Injectable, OnDestroy } from '@angular/core';
import { Subject } from 'rxjs';
import { ChartConfig } from '../models/chart-config.model';

@Injectable({ providedIn: 'root' })
export class ChartWebSocketService implements OnDestroy {
  private socket!: WebSocket;
  readonly chartUpdates$ = new Subject<ChartConfig>();

  connect(url: string): void {
    this.socket = new WebSocket(url);

    this.socket.onmessage = (event: MessageEvent) => {
      const payload = JSON.parse(event.data as string) as ChartConfig;
      this.chartUpdates$.next(payload);
    };

    this.socket.onerror = (err) => console.error('WebSocket error', err);
  }

  ngOnDestroy(): void {
    this.socket?.close();
    this.chartUpdates$.complete();
  }
}
```

In your component, subscribe to `chartUpdates$` and reassign the chart data reference to trigger Angular's change detection:

```typescript
this.chartWebSocketService.chartUpdates$
  .pipe(takeUntil(this.destroy$))
  .subscribe((updated) => {
    const idx = this.charts.findIndex((c) => c.id === updated.id);
    if (idx !== -1) {
      // Immutable update triggers OnPush change detection
      this.charts = [
        ...this.charts.slice(0, idx),
        updated,
        ...this.charts.slice(idx + 1),
      ];
    }
  });
```

### 6.2 Handling User-Defined Filters

Allow users to filter chart data by date range, region, or any other dimension without re-fetching from the API.

```typescript
// src/app/dashboard/dashboard.component.ts  (with filter support)
import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { debounceTime, distinctUntilChanged, startWith } from 'rxjs';
import { ChartDataService } from '../services/chart-data.service';
import { ChartConfig } from '../models/chart-config.model';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
})
export class DashboardComponent implements OnInit {
  allCharts: ChartConfig[] = [];
  filteredCharts: ChartConfig[] = [];
  regionFilter = new FormControl<string>('All');

  readonly regions = ['All', 'North', 'South', 'East', 'West'];

  constructor(private chartDataService: ChartDataService) {}

  ngOnInit(): void {
    this.chartDataService.getCharts().subscribe((charts) => {
      this.allCharts = charts;

      this.regionFilter.valueChanges
        .pipe(startWith('All'), debounceTime(200), distinctUntilChanged())
        .subscribe((region) => this.applyFilter(region ?? 'All'));
    });
  }

  private applyFilter(region: string): void {
    if (region === 'All') {
      this.filteredCharts = this.allCharts;
      return;
    }

    this.filteredCharts = this.allCharts.map((chart) => {
      // For bar charts, keep only the selected region's bar
      if (chart.data[0]?.type === 'bar') {
        const trace = chart.data[0] as { x: string[]; y: number[]; type: string };
        const idx = trace.x.indexOf(region);
        return idx === -1
          ? chart
          : {
              ...chart,
              data: [{ ...trace, x: [trace.x[idx]], y: [trace.y[idx]] }],
            };
      }
      return chart;
    });
  }
}
```

```html
<!-- Filter control in the template -->
<label for="region-filter">Region:</label>
<select id="region-filter" [formControl]="regionFilter">
  <option *ngFor="let r of regions" [value]="r">{{ r }}</option>
</select>

<div class="charts-grid">
  <div class="chart-card" *ngFor="let chart of filteredCharts">
    <plotly-plot
      [data]="chart.data"
      [layout]="chart.layout"
      [config]="{ responsive: true }">
    </plotly-plot>
  </div>
</div>
```

---

## Summary

| Topic | Key Points |
|---|---|
| Installation | `npm install angular-plotly.js plotly.js-dist` |
| Module Setup | Assign `PlotlyModule.plotlyjs = PlotlyJS` before importing `PlotlyModule` |
| Batch Charts | Store configs in a `ChartConfig[]` array; iterate with `*ngFor` |
| API Data | Use `HttpClient` + `map` to transform API responses into `ChartConfig` objects |
| Real-Time | Use `interval` + `switchMap` for polling or `WebSocket` for push updates |
| Filters | Use Angular `FormControl` + `debounceTime` to reactively filter data |

By following this guide you can embed Plotly.js efficiently in Angular applications, dynamically generate charts at scale with batch configurations, and integrate external APIs for data-driven visualisations.
