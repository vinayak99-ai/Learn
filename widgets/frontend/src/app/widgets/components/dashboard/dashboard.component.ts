import { Component, OnInit } from '@angular/core';
import { WidgetConfig } from '../../models/widget-config.model';
import { WidgetService } from '../../services/widget.service';

/**
 * Dashboard Component
 * Container that loads and displays multiple widgets in a grid layout
 */
@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  widgets: WidgetConfig[] = [];
  loading = false;
  error: string | null = null;

  constructor(private widgetService: WidgetService) {}

  ngOnInit(): void {
    this.loadWidgets();
  }

  /**
   * Load all widget configurations from the backend
   */
  loadWidgets(): void {
    this.loading = true;
    this.error = null;

    this.widgetService.getWidgetConfigs().subscribe({
      next: (configs) => {
        this.loading = false;
        this.widgets = configs;
      },
      error: (err) => {
        this.loading = false;
        this.error = 'Failed to load widgets: ' + err.message;
      }
    });
  }

  /**
   * Reload all widgets
   */
  refreshDashboard(): void {
    this.loadWidgets();
  }
}
