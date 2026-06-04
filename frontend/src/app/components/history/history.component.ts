import { Component, OnInit } from '@angular/core';
import { ApiService, HistoryEntry } from '../../services/api.service';

@Component({
  selector: 'app-history',
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.scss']
})
export class HistoryComponent implements OnInit {
  history: HistoryEntry[] = [];
  loading: boolean = false;
  error: string = '';

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.loadHistory();
  }

  loadHistory() {
    this.loading = true;
    this.error = '';

    this.apiService.getHistory().subscribe({
      next: (response) => {
        this.loading = false;
        if (response.success) {
          this.history = response.entries;
        } else {
          this.error = 'Failed to load history';
        }
      },
      error: (err) => {
        this.loading = false;
        this.error = 'An error occurred while loading history';
        console.error('History error:', err);
      }
    });
  }

  deleteEntry(entryId: string) {
    if (!confirm('Are you sure you want to delete this entry?')) {
      return;
    }

    this.apiService.deleteHistoryEntry(entryId).subscribe({
      next: (response) => {
        if (response.success) {
          this.history = this.history.filter(entry => entry.id !== entryId);
        }
      },
      error: (err) => {
        console.error('Delete error:', err);
        alert('Failed to delete entry');
      }
    });
  }

  clearAll() {
    if (!confirm('Are you sure you want to clear all history? This cannot be undone.')) {
      return;
    }

    this.apiService.clearHistory().subscribe({
      next: (response) => {
        if (response.success) {
          this.history = [];
        }
      },
      error: (err) => {
        console.error('Clear error:', err);
        alert('Failed to clear history');
      }
    });
  }

  formatDate(date: Date | undefined): string {
    if (!date) return '';
    return new Date(date).toLocaleString();
  }

  getModeLabel(mode: string): string {
    const modeLabels: { [key: string]: string } = {
      'standard': 'Q&A',
      'compare': 'Comparison',
      'literature_review': 'Literature Review',
      'research_gaps': 'Research Gaps'
    };
    return modeLabels[mode] || mode;
  }
}
