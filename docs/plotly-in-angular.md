# Using Plotly.js in Angular: A Detailed Guide

This guide walks you through integrating [Plotly.js](https://plotly.com/javascript/) into an Angular application to create dynamic, data-driven charts. You will learn how to install dependencies, configure Angular modules, create batch charts, fetch data from external APIs, and build a real-world sales-monitoring dashboard.

Each section builds on the previous one: you start with a static component in section 3, add API data loading in section 4, and complete the full-featured Sales Dashboard in section 5.

---

## Prerequisites

- **Angular version:** 14–16 (NgModule-based architecture). All examples use `NgModule` and class-based components.

  > **Angular 17+ note:** Angular 17+ defaults to standalone components. Replace `NgModule` imports with the `imports` array on the `@Component` decorator — e.g., `imports: [PlotlyModule, ReactiveFormsModule, CommonModule]`.

- **Node.js:** 16 or later; npm 8 or later.
- **Existing Angular application** generated with the Angular CLI (`ng new my-app`).

---

## Table of Contents

1. [Installing Dependencies](#1-installing-dependencies)
2. [Basic Plotly.js Integration with Angular](#2-basic-plotlyjs-integration-with-angular)
3. [Dynamic Batch Chart Creation](#3-dynamic-batch-chart-creation)
4. [Loading Charts from an API](#4-loading-charts-from-an-api)
5. [Real-World Example: Sales Dashboard](#5-real-world-example-sales-dashboard)
6. [Additional Enhancements](#6-additional-enhancements)
7. [Unit Testing](#7-unit-testing)

---

## 1. Installing Dependencies

Install the Angular Plotly wrapper and the full Plotly.js distribution:

```bash
npm install angular-plotly.js plotly.js-dist
```

If your project uses TypeScript, install the community type definitions:

```bash
npm install --save-dev @types/plotly.js
```

> **Bundle size:** `plotly.js-dist` is approximately 3.5 MB. If you only need basic chart types (bar, line, scatter, pie), consider a lighter alternative to reduce your bundle:
>
> ```bash
> npm install plotly.js-basic-dist    # ~1.2 MB — covers basic chart types
> # or
> npm install plotly.js-dist-min      # minified full build
> ```
>
> Replace `'plotly.js-dist'` with `'plotly.js-basic-dist'` wherever it appears in the imports below.

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

> **Note:** You must assign `PlotlyModule.plotlyjs = PlotlyJS` **before** `PlotlyModule` is listed in `imports`. This is required by `angular-plotly.js` v2+.

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

### 3.2 `DashboardComponent` — Static Version

This is the starting point. Sections 4 and 5 will progressively add API loading, subscription cleanup, and filter controls to this same component.

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

  /** Used by the template's trackBy to avoid re-rendering unchanged charts. */
  trackByChartId(_: number, chart: ChartConfig): string {
    return chart.id;
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
        layout: {
          title: 'Sales by Region',
          xaxis: { title: 'Region' },
          yaxis: { title: 'Revenue ($)' },
        },
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
        layout: {
          title: 'Revenue vs Expenses',
          xaxis: { title: 'Quarter' },
          yaxis: { title: 'Amount ($)' },
        },
      },
    ];
  }
}
```

### 3.3 Template with `*ngFor` and `trackBy`

```html
<!-- src/app/dashboard/dashboard.component.html -->
<section class="dashboard">
  <div
    class="chart-wrapper"
    *ngFor="let chart of charts; trackBy: trackByChartId"
    [attr.aria-label]="chart.title">
    <h2>{{ chart.title }}</h2>
    <plotly-plot
      [data]="chart.data"
      [layout]="chart.layout"
      [config]="{ responsive: true }">
    </plotly-plot>
  </div>
</section>
```

> **Why `trackBy` matters:** Without `trackBy`, Angular destroys and re-creates every chart DOM node whenever the `charts` array is replaced (for example, during polling or filtering). With `trackByChartId`, Angular reuses DOM nodes for charts whose `id` has not changed — a critical performance optimization.

Setting `[config]="{ responsive: true }"` makes every chart resize automatically when the browser window changes size.

---

## 4. Loading Charts from an API

This section extends `DashboardComponent` to fetch its data from an API instead of using hardcoded values.

### 4.1 Environment Configuration

Store the API base URL in Angular's environment files so it can differ between development and production:

```typescript
// src/environments/environment.ts
export const environment = {
  production: false,
  apiUrl: 'https://api.example.com/charts',
};
```

```typescript
// src/environments/environment.prod.ts
export const environment = {
  production: true,
  apiUrl: 'https://api.example.com/charts',
};
```

### 4.2 `ChartDataService`

```typescript
// src/app/services/chart-data.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { environment } from '../../environments/environment';
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
  private readonly apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  getCharts(): Observable<ChartConfig[]> {
    return this.http
      .get<ApiChartResponse[]>(this.apiUrl)
      .pipe(map((responses) => responses.map((r) => this.toChartConfig(r))));
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

> **`this` context:** `getCharts()` uses `.map((r) => this.toChartConfig(r))` rather than `.map(this.toChartConfig)`. Passing a method reference directly would lose the `this` binding inside `toChartConfig` at runtime, causing errors when it accesses `this`.

### 4.3 Update `DashboardComponent` for API Data

Starting from the static version in section 3.2, apply the following changes (lines marked `+` are additions, lines marked `-` are removals):

```diff
-import { Component, OnInit } from '@angular/core';
-import { ChartConfig } from '../models/chart-config.model';
+import { Component, OnInit } from '@angular/core';
+import { ChartDataService } from '../services/chart-data.service';
+import { ChartConfig } from '../models/chart-config.model';

 @Component({
   selector: 'app-dashboard',
   templateUrl: './dashboard.component.html',
 })
 export class DashboardComponent implements OnInit {
   charts: ChartConfig[] = [];
+  loading = true;
+  error: string | null = null;

-  constructor() {}
+  constructor(private chartDataService: ChartDataService) {}

   ngOnInit(): void {
-    this.charts = this.buildCharts();
+    this.chartDataService.getCharts().subscribe({
+      next: (charts) => {
+        this.charts = charts;
+        this.loading = false;
+      },
+      error: (err) => {
+        this.error = 'Failed to load charts. Please try again.';
+        this.loading = false;
+        console.error(err);
+      },
+    });
   }

   trackByChartId(_: number, chart: ChartConfig): string {
     return chart.id;
   }

-  private buildCharts(): ChartConfig[] { ... }
 }
```

### 4.4 Updated Template

Add loading and error states:

```html
<!-- src/app/dashboard/dashboard.component.html  (after section 4 changes) -->
<div *ngIf="loading">Loading charts…</div>
<div *ngIf="error" class="error" role="alert">{{ error }}</div>

<section class="dashboard" *ngIf="!loading && !error">
  <div
    class="chart-wrapper"
    *ngFor="let chart of charts; trackBy: trackByChartId"
    [attr.aria-label]="chart.title">
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

This section completes `DashboardComponent` by adding subscription cleanup with `takeUntil` and user-controlled region filtering — the features you would need in a real production dashboard.

### 5.1 Scenario

A sales manager needs a single-page dashboard showing:

| Chart | Type | Description |
|---|---|---|
| Sales by Region | Bar | Compares total revenue across four geographic regions |
| Traffic Sources | Pie | Shows the percentage breakdown of website traffic origins |
| Revenue vs Expenses | Line | Tracks quarterly revenue and expenses side by side |

Users can filter bar chart data by selecting a specific region from a dropdown.

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

### 5.3 Add `ReactiveFormsModule` to `AppModule`

The region filter control uses Angular Reactive Forms. Add `ReactiveFormsModule` to `AppModule`:

```typescript
// src/app/app.module.ts
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';   // ← add this

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
    ReactiveFormsModule,              // ← add this
    PlotlyModule,
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
```

### 5.4 Final `DashboardComponent` — Cleanup and Filters

Starting from the API version in section 4.3, apply the following changes:

```diff
-import { Component, OnInit } from '@angular/core';
-import { ChartDataService } from '../services/chart-data.service';
-import { ChartConfig } from '../models/chart-config.model';
+import { Component, OnInit, OnDestroy } from '@angular/core';
+import { FormControl } from '@angular/forms';
+import { combineLatest, Subject } from 'rxjs';
+import { debounceTime, distinctUntilChanged, startWith, takeUntil } from 'rxjs/operators';
+import { ChartDataService } from '../services/chart-data.service';
+import { ChartConfig } from '../models/chart-config.model';

 @Component({
   selector: 'app-dashboard',
   templateUrl: './dashboard.component.html',
+  styleUrls: ['./dashboard.component.scss'],
 })
-export class DashboardComponent implements OnInit {
-  charts: ChartConfig[] = [];
+export class DashboardComponent implements OnInit, OnDestroy {
+  allCharts: ChartConfig[] = [];
+  filteredCharts: ChartConfig[] = [];
   loading = true;
   error: string | null = null;

+  regionFilter = new FormControl<string>('All');
+  readonly regions = ['All', 'North', 'South', 'East', 'West'];
+
+  private destroy$ = new Subject<void>();

   constructor(private chartDataService: ChartDataService) {}

   ngOnInit(): void {
-    this.chartDataService.getCharts().subscribe({
-      next: (charts) => {
-        this.charts = charts;
-        this.loading = false;
-      },
-      error: (err) => {
-        this.error = 'Failed to load charts. Please try again.';
-        this.loading = false;
-        console.error(err);
-      },
-    });
+    combineLatest([
+      this.chartDataService.getCharts(),
+      this.regionFilter.valueChanges.pipe(
+        startWith('All'),
+        debounceTime(200),
+        distinctUntilChanged(),
+      ),
+    ])
+      .pipe(takeUntil(this.destroy$))
+      .subscribe({
+        next: ([charts, region]) => {
+          this.allCharts = charts;
+          this.filteredCharts = this.applyFilter(charts, region ?? 'All');
+          this.loading = false;
+        },
+        error: (err) => {
+          this.error = 'Failed to load charts. Please try again.';
+          this.loading = false;
+          console.error(err);
+        },
+      });
   }

+  ngOnDestroy(): void {
+    this.destroy$.next();
+    this.destroy$.complete();
+  }
+
   trackByChartId(_: number, chart: ChartConfig): string {
     return chart.id;
   }
+
+  trackByRegion(_: number, region: string): string {
+    return region;
+  }
+
+  private applyFilter(charts: ChartConfig[], region: string): ChartConfig[] {
+    if (region === 'All') {
+      return charts;
+    }
+    return charts.map((chart) => {
+      if (chart.data[0]?.type === 'bar') {
+        const trace = chart.data[0] as { x: string[]; y: number[]; type: string };
+        const idx = trace.x.indexOf(region);
+        if (idx === -1) return chart;
+        return { ...chart, data: [{ ...trace, x: [trace.x[idx]], y: [trace.y[idx]] }] };
+      }
+      return chart;
+    });
+  }
 }
```

> **Why `combineLatest` instead of nested subscriptions?** Subscribing to `regionFilter.valueChanges` *inside* the `getCharts()` callback creates a nested subscription that is never unsubscribed — a memory leak. `combineLatest` combines both streams into a single, cleanly-managed subscription that `takeUntil(this.destroy$)` will automatically unsubscribe when the component is destroyed.

The complete final component for copy-paste:

```typescript
// src/app/dashboard/dashboard.component.ts  (final — Sales Dashboard)
import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormControl } from '@angular/forms';
import { combineLatest, Subject } from 'rxjs';
import { debounceTime, distinctUntilChanged, startWith, takeUntil } from 'rxjs/operators';
import { ChartDataService } from '../services/chart-data.service';
import { ChartConfig } from '../models/chart-config.model';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
})
export class DashboardComponent implements OnInit, OnDestroy {
  allCharts: ChartConfig[] = [];
  filteredCharts: ChartConfig[] = [];
  loading = true;
  error: string | null = null;

  regionFilter = new FormControl<string>('All');
  readonly regions = ['All', 'North', 'South', 'East', 'West'];

  private destroy$ = new Subject<void>();

  constructor(private chartDataService: ChartDataService) {}

  ngOnInit(): void {
    combineLatest([
      this.chartDataService.getCharts(),
      this.regionFilter.valueChanges.pipe(
        startWith('All'),
        debounceTime(200),
        distinctUntilChanged(),
      ),
    ])
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: ([charts, region]) => {
          this.allCharts = charts;
          this.filteredCharts = this.applyFilter(charts, region ?? 'All');
          this.loading = false;
        },
        error: (err) => {
          this.error = 'Failed to load charts. Please try again.';
          this.loading = false;
          console.error(err);
        },
      });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  trackByChartId(_: number, chart: ChartConfig): string {
    return chart.id;
  }

  trackByRegion(_: number, region: string): string {
    return region;
  }

  private applyFilter(charts: ChartConfig[], region: string): ChartConfig[] {
    if (region === 'All') {
      return charts;
    }
    return charts.map((chart) => {
      if (chart.data[0]?.type === 'bar') {
        const trace = chart.data[0] as { x: string[]; y: number[]; type: string };
        const idx = trace.x.indexOf(region);
        if (idx === -1) return chart;
        return { ...chart, data: [{ ...trace, x: [trace.x[idx]], y: [trace.y[idx]] }] };
      }
      return chart;
    });
  }
}
```

### 5.5 Final Template

```html
<!-- src/app/dashboard/dashboard.component.html  (final) -->
<div class="sales-dashboard">
  <header>
    <h1>Sales Performance Dashboard</h1>
  </header>

  <div class="filter-bar">
    <label for="region-filter">Filter by region:</label>
    <select id="region-filter" [formControl]="regionFilter">
      <option *ngFor="let r of regions; trackBy: trackByRegion" [value]="r">{{ r }}</option>
    </select>
  </div>

  <div class="loading-spinner" *ngIf="loading">Loading…</div>
  <div class="error-message" *ngIf="error" role="alert">{{ error }}</div>

  <div class="charts-grid" *ngIf="!loading && !error">
    <div
      class="chart-card"
      *ngFor="let chart of filteredCharts; trackBy: trackByChartId"
      [attr.aria-label]="chart.title">
      <plotly-plot
        [data]="chart.data"
        [layout]="chart.layout"
        [config]="{ responsive: true, displayModeBar: true }">
      </plotly-plot>
    </div>
  </div>
</div>
```

### 5.6 Styles

```scss
/* src/app/dashboard/dashboard.component.scss */
.sales-dashboard {
  padding: 1.5rem;
  font-family: sans-serif;
}

.filter-bar {
  margin-bottom: 1rem;

  label {
    margin-right: 0.5rem;
    font-weight: 500;
  }
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

### 6.1 Real-Time Updates with Polling

Use `interval` + `switchMap` to poll the API for fresh data at a regular interval. Note the use of `takeUntil` for cleanup:

```typescript
import { Component, OnInit, OnDestroy } from '@angular/core';
import { interval, Subject } from 'rxjs';
import { switchMap, takeUntil } from 'rxjs/operators';
import { ChartDataService } from '../services/chart-data.service';
import { ChartConfig } from '../models/chart-config.model';

@Component({
  selector: 'app-realtime-chart',
  template: `
    <plotly-plot *ngIf="chart" [data]="chart.data" [layout]="chart.layout"></plotly-plot>
  `,
})
export class RealtimeChartComponent implements OnInit, OnDestroy {
  chart: ChartConfig | null = null;
  private destroy$ = new Subject<void>();

  constructor(private chartDataService: ChartDataService) {}

  ngOnInit(): void {
    interval(5000)
      .pipe(
        switchMap(() => this.chartDataService.getCharts()),
        takeUntil(this.destroy$),
      )
      .subscribe((charts) => (this.chart = charts[0] ?? null));
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

### 6.2 WebSocket Integration

For push-based real-time updates, use a WebSocket service that propagates errors to the component rather than silently logging them:

```typescript
// src/app/services/chart-websocket.service.ts
import { Injectable, OnDestroy } from '@angular/core';
import { Observable, Subject } from 'rxjs';
import { ChartConfig } from '../models/chart-config.model';

@Injectable({ providedIn: 'root' })
export class ChartWebSocketService implements OnDestroy {
  private socket!: WebSocket;
  private readonly chartUpdatesSubject = new Subject<ChartConfig>();
  private readonly errorsSubject = new Subject<string>();

  /** Emits parsed chart updates received from the server. */
  readonly updates$: Observable<ChartConfig> = this.chartUpdatesSubject.asObservable();

  /** Emits a human-readable error message when the WebSocket encounters a problem. */
  readonly errors$: Observable<string> = this.errorsSubject.asObservable();

  connect(url: string): void {
    this.socket = new WebSocket(url);

    this.socket.onmessage = (event: MessageEvent) => {
      try {
        const payload = JSON.parse(event.data as string) as ChartConfig;
        this.chartUpdatesSubject.next(payload);
      } catch {
        this.errorsSubject.next('Received malformed data from the server.');
      }
    };

    this.socket.onerror = () => {
      this.errorsSubject.next('WebSocket connection error. Retrying…');
    };

    this.socket.onclose = (event: CloseEvent) => {
      if (!event.wasClean) {
        this.errorsSubject.next('WebSocket closed unexpectedly. Please refresh the page.');
        // For automatic reconnection, schedule a reconnect here:
        // setTimeout(() => this.connect(url), 5000);
      }
    };
  }

  ngOnDestroy(): void {
    this.socket?.close();
    this.chartUpdatesSubject.complete();
    this.errorsSubject.complete();
  }
}
```

Subscribe to both `updates$` and `errors$` in your component:

```typescript
this.chartWebSocketService.updates$
  .pipe(takeUntil(this.destroy$))
  .subscribe((updated) => {
    const idx = this.allCharts.findIndex((c) => c.id === updated.id);
    if (idx !== -1) {
      // Immutable update triggers OnPush change detection
      this.allCharts = [
        ...this.allCharts.slice(0, idx),
        updated,
        ...this.allCharts.slice(idx + 1),
      ];
      this.filteredCharts = this.applyFilter(
        this.allCharts,
        this.regionFilter.value ?? 'All',
      );
    }
  });

this.chartWebSocketService.errors$
  .pipe(takeUntil(this.destroy$))
  .subscribe((msg) => (this.error = msg));
```

> **Reconnection strategies:** For production use, consider [`RxJS webSocket`](https://rxjs.dev/api/webSocket/webSocket) or [`ngx-socket-io`](https://www.npmjs.com/package/ngx-socket-io), which include built-in reconnection and exponential backoff.

### 6.3 Plotly Chart Events

`angular-plotly.js` exposes Plotly's interaction events as Angular output bindings on `<plotly-plot>`:

```html
<plotly-plot
  [data]="chart.data"
  [layout]="chart.layout"
  (plotlyClick)="onChartClick($event)"
  (plotlyHover)="onChartHover($event)"
  (plotlyUnhover)="onChartUnhover($event)"
  (plotlySelected)="onChartSelected($event)">
</plotly-plot>
```

```typescript
onChartClick(event: { points: Array<{ x: unknown; y: unknown }> }): void {
  const point = event.points[0];
  console.log('Clicked point:', point.x, point.y);
}
```

See the [angular-plotly.js README](https://github.com/plotly/angular-plotly.js#output-events) for the full list of available events.

### 6.4 Accessibility

- **`aria-label` on chart containers:** Add `[attr.aria-label]="chart.title"` to each chart's wrapper `<div>`. This gives screen readers a meaningful description of each chart region (already included in the templates above).
- **`role="alert"` on error messages:** Apply `role="alert"` to your error `<div>` so assistive technologies announce errors immediately (also included in the templates above).
- **Data table fallback:** For critical data, render a visually hidden `<table>` alongside each chart to expose the underlying data to screen readers:

  ```html
  <div class="chart-card" [attr.aria-label]="chart.title">
    <plotly-plot [data]="chart.data" [layout]="chart.layout"></plotly-plot>
    <table class="sr-only" [attr.aria-label]="chart.title + ' data'">
      <!-- render chart.data rows here -->
    </table>
  </div>
  ```

  The `.sr-only` class visually hides the table while keeping it in the accessibility tree:

  ```css
  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
  }
  ```

---

## 7. Unit Testing

### Testing `ChartDataService`

Use Angular's `HttpClientTestingModule` to mock HTTP calls without hitting a real API:

```typescript
// src/app/services/chart-data.service.spec.ts
import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { ChartDataService } from './chart-data.service';
import { environment } from '../../environments/environment';

describe('ChartDataService', () => {
  let service: ChartDataService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [ChartDataService],
    });
    service = TestBed.inject(ChartDataService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => httpMock.verify());

  it('should transform a bar chart API response into a ChartConfig', () => {
    service.getCharts().subscribe((charts) => {
      expect(charts.length).toBe(1);
      expect(charts[0].id).toBe('sales-by-region');
      expect(charts[0].data[0].type).toBe('bar');
    });

    const req = httpMock.expectOne(environment.apiUrl);
    expect(req.request.method).toBe('GET');
    req.flush([
      {
        id: 'sales-by-region',
        title: 'Sales by Region',
        type: 'bar',
        labels: ['North', 'South', 'East', 'West'],
        values: [120000, 95000, 140000, 80000],
      },
    ]);
  });
});
```

---

## Summary

| Topic | Key Points |
|---|---|
| Prerequisites | Angular 14–16, Node 16+, NgModule-based architecture |
| Installation | `npm install angular-plotly.js plotly.js-dist`; use `plotly.js-basic-dist` to reduce bundle by ~2 MB |
| Module Setup | Assign `PlotlyModule.plotlyjs = PlotlyJS` before importing `PlotlyModule`; add `ReactiveFormsModule` when using filters |
| Batch Charts | Store configs in `ChartConfig[]`; iterate with `*ngFor` and `trackBy: trackByChartId` |
| API Data | Use `HttpClient` + `.map((r) => this.toChartConfig(r))` to preserve `this` context; read URL from `environment.apiUrl` |
| Cleanup | Always use `takeUntil(this.destroy$)` and complete `destroy$` in `ngOnDestroy` |
| Filters | Use `combineLatest` + `ReactiveFormsModule` to avoid nested subscriptions |
| Real-Time | Use `interval` + `switchMap` for polling; use a WebSocket service with `updates$` and `errors$` for push updates |
| Events | Use `(plotlyClick)`, `(plotlyHover)`, etc. on `<plotly-plot>` for interaction handling |
| Accessibility | Add `aria-label` to chart containers; `role="alert"` on errors; optionally add a data-table fallback |
| Testing | Use `HttpClientTestingModule` to mock API calls in service tests |

By following this guide you can embed Plotly.js efficiently in Angular applications, dynamically generate charts at scale with batch configurations, and integrate external APIs for data-driven visualisations.
