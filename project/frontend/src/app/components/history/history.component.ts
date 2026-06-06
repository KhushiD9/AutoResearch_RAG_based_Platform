import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';

@Component({ selector: 'app-history', templateUrl: './history.component.html', styleUrls: ['./history.component.scss'] })
export class HistoryComponent implements OnInit {
  entries: any[] = [];
  loading = false;

  constructor(private api: ApiService) {}
  ngOnInit() { this.load(); }

  load() {
    this.loading = true;
    this.api.getHistory().subscribe({ next: (r: any) => { this.loading = false; if (r.success) this.entries = r.entries; }, error: () => { this.loading = false; } });
  }

  deleteEntry(id: string) {
    this.api.deleteHistoryEntry(id).subscribe({ next: () => { this.entries = this.entries.filter(e => e.id !== id); } });
  }

  clearAll() {
    this.api.clearHistory().subscribe({ next: () => { this.entries = []; } });
  }
}
