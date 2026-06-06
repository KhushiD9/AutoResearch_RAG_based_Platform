import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { StateService } from '../../services/state.service';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent implements OnInit {
  topic   = '';
  limit   = 5;
  loading = false;
  error   = '';
  result: any = null;

  currentStep = 0;
  pipelineSteps = [
    'Querying Semantic Scholar & arXiv',
    'Downloading PDFs',
    'Extracting & chunking text',
    'Generating embeddings (all-MiniLM)',
    'Storing in ChromaDB',
  ];
  private stepTimer: any;

  suggestions = [
    'anti-pinch controller',
    'large language models',
    'protein folding',
    'CRISPR delivery',
    'quantum error correction',
  ];

  features = [
    { title: 'Paper Discovery',   desc: 'Searches Semantic Scholar and arXiv simultaneously for open-access papers.' },
    { title: 'RAG Pipeline',      desc: 'Chunks PDFs, embeds with sentence-transformers, stores in ChromaDB.' },
    { title: 'Grounded Answers',  desc: 'Claude retrieves relevant chunks and cites the actual paper content.' },
    { title: 'Literature Review', desc: 'Auto-synthesises multiple papers into a structured review.' },
  ];

  get totalChunks(): number {
    if (!this.result?.processed_papers) return 0;
    return this.result.processed_papers.reduce((s: number, p: any) => s + (p.chunks_count || 0), 0);
  }

  constructor(
    private api: ApiService,
    private state: StateService,
    private router: Router
  ) {}

  ngOnInit(): void {
    const saved = this.state.getLastResult();
    if (saved) { this.result = saved; }
  }

  useSuggestion(s: string): void {
    this.topic = s;
    this.onSearch();
  }

  onSearch(): void {
    if (!this.topic.trim() || this.loading) return;
    this.error   = '';
    this.result  = null;
    this.loading = true;
    this.currentStep = 0;

    // Advance pipeline steps visually while waiting
    this.stepTimer = setInterval(() => {
      if (this.currentStep < this.pipelineSteps.length - 1) this.currentStep++;
    }, 1800);

    this.api.searchPapers({ topic: this.topic.trim(), limit: this.limit, provider: 'anthropic' })
      .subscribe({
        next: (res: any) => {
          clearInterval(this.stepTimer);
          this.loading = false;
          if (res.success) {
            this.result = res;
            this.state.setLastResult(res);
            this.state.setCurrentTopic(this.topic.trim());
            this.state.setCurrentCollection(res.collection_name);
          } else {
            this.error = res.error || 'Search failed. Please try again.';
          }
        },
        error: (err: any) => {
          clearInterval(this.stepTimer);
          this.loading = false;
          this.error = err?.error?.detail || 'Could not reach the backend. Is it running on port 8000?';
        }
      });
  }

  navigateToChat(): void {
    this.router.navigate(['/chat']);
  }

  resetSearch(): void {
    this.result = null;
    this.error  = '';
    this.topic  = '';
    this.state.setLastResult(null);
  }
}
