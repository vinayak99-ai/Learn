import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { WidgetConfig, WidgetExecutionRequest, WidgetExecutionResult } from '../models/widget-config.model';

/**
 * Widget Service
 * Handles HTTP communication with the Python backend for widget operations
 */
@Injectable({
  providedIn: 'root'
})
export class WidgetService {
  private apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  /**
   * Fetch all widget configurations from the backend
   */
  getWidgetConfigs(): Observable<WidgetConfig[]> {
    return this.http.get<WidgetConfig[]>(`${this.apiUrl}/widgets`);
  }

  /**
   * Execute widget Python code via the backend
   */
  executeWidget(request: WidgetExecutionRequest): Observable<WidgetExecutionResult> {
    return this.http.post<WidgetExecutionResult>(`${this.apiUrl}/execute-widget`, request);
  }

  /**
   * Get a specific widget configuration by ID
   */
  getWidgetById(id: string): Observable<WidgetConfig> {
    return this.http.get<WidgetConfig>(`${this.apiUrl}/widgets/${id}`);
  }
}
