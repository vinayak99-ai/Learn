import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';

// Services
import { WidgetService } from './services/widget.service';

// Components
import { DynamicWidgetComponent } from './components/dynamic-widget/dynamic-widget.component';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { ChartWidgetComponent } from './components/chart-widget/chart-widget.component';
import { TableWidgetComponent } from './components/table-widget/table-widget.component';
import { MetricWidgetComponent } from './components/metric-widget/metric-widget.component';

/**
 * Widgets Module
 * Self-contained module for dynamic widgets system with Python backend integration
 */
@NgModule({
  declarations: [
    DashboardComponent,
    DynamicWidgetComponent,
    ChartWidgetComponent,
    TableWidgetComponent,
    MetricWidgetComponent
  ],
  imports: [
    CommonModule,
    HttpClientModule
  ],
  exports: [
    DashboardComponent,
    DynamicWidgetComponent,
    ChartWidgetComponent,
    TableWidgetComponent,
    MetricWidgetComponent
  ],
  providers: [
    WidgetService
  ]
})
export class WidgetsModule { }
