import { Component, Input, OnInit, OnDestroy } from '@angular/core';
import { WidgetConfig, WidgetExecutionResult } from '../../models/widget-config.model';
import { WidgetService } from '../../services/widget.service';
import { interval, Subscription } from 'rxjs';
import { switchMap } from 'rxjs/operators';

/**
 * Dynamic Widget Component
 * A reusable widget component that executes Python code and displays results
 */
@Component({
  selector: 'app-dynamic-widget',
  templateUrl: './dynamic-widget.component.html',
  styleUrls: ['./dynamic-widget.component.css']
})
export class DynamicWidgetComponent implements OnInit, OnDestroy {
  @Input() config!: WidgetConfig;

  loading = false;
  error: string | null = null;
  result: WidgetExecutionResult | null = null;
  private refreshSubscription?: Subscription;

  constructor(private widgetService: WidgetService) {}

  ngOnInit(): void {
    this.executeWidget();
    
    // Set up auto-refresh if configured
    if (this.config.refreshInterval && this.config.refreshInterval > 0) {
      this.refreshSubscription = interval(this.config.refreshInterval * 1000)
        .pipe(
          switchMap(() => {
            return this.widgetService.executeWidget({
              widgetId: this.config.id,
              pythonCode: this.config.pythonCode,
              parameters: this.config.parameters
            });
          })
        )
        .subscribe({
          next: (result) => {
            this.result = result;
            this.error = result.success ? null : result.error || 'Execution failed';
          },
          error: (err) => {
            this.error = 'Failed to refresh widget: ' + err.message;
          }
        });
    }
  }

  ngOnDestroy(): void {
    if (this.refreshSubscription) {
      this.refreshSubscription.unsubscribe();
    }
  }

  /**
   * Execute the widget's Python code
   */
  executeWidget(): void {
    this.loading = true;
    this.error = null;

    this.widgetService.executeWidget({
      widgetId: this.config.id,
      pythonCode: this.config.pythonCode,
      parameters: this.config.parameters
    }).subscribe({
      next: (result) => {
        this.loading = false;
        this.result = result;
        if (!result.success) {
          this.error = result.error || 'Execution failed';
        }
      },
      error: (err) => {
        this.loading = false;
        this.error = 'Failed to execute widget: ' + err.message;
      }
    });
  }

  /**
   * Manually refresh the widget
   */
  refresh(): void {
    this.executeWidget();
  }
}
