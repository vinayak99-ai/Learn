import { Component, Input, OnInit } from '@angular/core';

/**
 * Table Widget Component
 * Displays data in table format
 */
@Component({
  selector: 'app-table-widget',
  template: `
    <div class="table-widget">
      <div *ngIf="!tableData || tableData.length === 0" class="no-data">
        No table data available
      </div>
      
      <div *ngIf="tableData && tableData.length > 0" class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th *ngFor="let column of columns">{{ column }}</th>
            </tr>
          </thead>
          <tbody>
            <tr *ngFor="let row of tableData; let i = index" [class.even-row]="i % 2 === 0">
              <td *ngFor="let column of columns">
                {{ getCellValue(row, column) }}
              </td>
            </tr>
          </tbody>
        </table>
        
        <div class="table-footer" *ngIf="tableData.length > 0">
          <small>Showing {{ tableData.length }} rows</small>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .table-widget {
      padding: 16px;
      overflow: auto;
    }

    .no-data {
      text-align: center;
      padding: 40px;
      color: #999;
      font-style: italic;
    }

    .table-container {
      width: 100%;
      overflow-x: auto;
    }

    .data-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
    }

    .data-table thead {
      background-color: #f5f5f5;
      border-bottom: 2px solid #3498db;
    }

    .data-table th {
      padding: 12px 16px;
      text-align: left;
      font-weight: 600;
      color: #333;
      white-space: nowrap;
    }

    .data-table td {
      padding: 12px 16px;
      border-bottom: 1px solid #e0e0e0;
      color: #555;
    }

    .data-table tbody tr:hover {
      background-color: #f9f9f9;
    }

    .even-row {
      background-color: #fafafa;
    }

    .table-footer {
      margin-top: 12px;
      padding-top: 12px;
      border-top: 1px solid #e0e0e0;
      text-align: right;
      color: #999;
    }
  `]
})
export class TableWidgetComponent implements OnInit {
  @Input() data: any;

  tableData: any[] = [];
  columns: string[] = [];

  ngOnInit(): void {
    this.processData();
  }

  processData(): void {
    if (!this.data) return;

    // Handle different data formats
    if (Array.isArray(this.data)) {
      this.tableData = this.data;
    } else if (this.data.data && Array.isArray(this.data.data)) {
      this.tableData = this.data.data;
      if (this.data.columns) {
        this.columns = this.data.columns;
      }
    }

    // Extract columns from first row if not provided
    if (this.tableData.length > 0 && this.columns.length === 0) {
      const firstRow = this.tableData[0];
      if (typeof firstRow === 'object') {
        this.columns = Object.keys(firstRow);
      }
    }
  }

  getCellValue(row: any, column: string): any {
    if (typeof row === 'object') {
      const value = row[column];
      // Format numbers with comma separators
      if (typeof value === 'number') {
        return value.toLocaleString();
      }
      return value;
    }
    return row;
  }
}
