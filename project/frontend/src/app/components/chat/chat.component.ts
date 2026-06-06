import { Component, OnInit, ViewChild, ElementRef, AfterViewChecked } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { StateService } from '../../services/state.service';

interface ChatMessage {
  type:    'user' | 'ai';
  text:    string;
  mode?:   string;
  sources?: any[];
  time:    string;
}

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.scss']
})
export class ChatComponent implements OnInit, AfterViewChecked {
  @ViewChild('messagesContainer') messagesContainer!: ElementRef;

  collections: string[] = [];
  selectedCollection = '';
  mode = 'standard';
  question = '';
  messages: ChatMessage[] = [];
  loading = false;
  private shouldScroll = false;

  modes = [
    { value: 'standard',          label: 'Q & A',           icon: '?', desc: 'Ask questions grounded in the papers' },
    { value: 'compare',           label: 'Compare',         icon: '=', desc: 'Compare methodologies across papers' },
    { value: 'literature_review', label: 'Lit. Review',     icon: 'L', desc: 'Generate a literature review' },
    { value: 'research_gaps',     label: 'Gaps',            icon: 'G', desc: 'Identify research gaps' },
  ];

  suggestedQuestions = [
    'What are the main findings of these papers?',
    'What methodologies are used?',
    'What are the limitations mentioned?',
    'What future directions do the authors suggest?',
    'What datasets or benchmarks were used?',
  ];

  get activeModeName(): string {
    return this.modes.find(m => m.value === this.mode)?.label || 'Q & A';
  }

  constructor(
    private api: ApiService,
    private state: StateService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadCollections();
    const saved = this.state.getCurrentCollection();
    if (saved) this.selectedCollection = saved;
  }

  ngAfterViewChecked(): void {
    if (this.shouldScroll) {
      this.scrollToBottom();
      this.shouldScroll = false;
    }
  }

  loadCollections(): void {
    this.api.listCollections().subscribe({
      next: (res: any) => {
        if (res.success) this.collections = res.collections;
      },
      error: () => {}
    });
  }

  selectCollection(c: string): void {
    this.selectedCollection = c;
    this.state.setCurrentCollection(c);
  }

  useSuggested(q: string): void {
    this.question = q;
    this.onAsk();
  }

  onKeyDown(event: KeyboardEvent): void {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.onAsk();
    }
  }

  clearMessages(): void { this.messages = []; }

  onAsk(): void {
    if (!this.question.trim() || !this.selectedCollection || this.loading) return;

    const q = this.question.trim();
    this.question = '';
    this.loading  = true;

    this.messages.push({ type: 'user', text: q, time: this.now() });
    this.shouldScroll = true;

    this.api.queryPapers({
      collection_name: this.selectedCollection,
      question: q,
      n_results: 5,
      mode: this.mode,
      provider: 'anthropic',
    }).subscribe({
      next: (res: any) => {
        this.loading = false;
        if (res.success) {
          this.messages.push({
            type:    'ai',
            text:    res.answer,
            mode:    this.mode,
            sources: res.sources,
            time:    this.now(),
          });
          // Save to history
          this.api.saveHistory({
            collection_name: this.selectedCollection,
            question: q,
            answer: res.answer,
            mode: this.mode,
          }).subscribe();
        } else {
          this.messages.push({ type: 'ai', text: res.error || 'No answer returned.', time: this.now() });
        }
        this.shouldScroll = true;
      },
      error: (err: any) => {
        this.loading = false;
        this.messages.push({
          type: 'ai',
          text: err?.error?.detail || 'Request failed. Is the backend running?',
          time: this.now(),
        });
        this.shouldScroll = true;
      }
    });
  }

  navigateToSearch(): void { this.router.navigate(['/search']); }

  private scrollToBottom(): void {
    try {
      const el = this.messagesContainer.nativeElement;
      el.scrollTop = el.scrollHeight;
    } catch {}
  }

  private now(): string {
    return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }
}
