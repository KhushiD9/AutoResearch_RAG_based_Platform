import { Component, OnInit, ViewChild, ElementRef, AfterViewChecked } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService, QueryRequest } from '../../services/api.service';
import { StateService } from '../../services/state.service';

interface Message {
  type: 'user' | 'ai';
  text: string;
  sources?: any[];
}

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.scss']
})
export class ChatComponent implements OnInit, AfterViewChecked {
  @ViewChild('messagesContainer') messagesContainer!: ElementRef;

  collections: string[] = [];
  selectedCollection: string = '';
  currentTopic: string = '';
  question: string = '';
  messages: Message[] = [];
  loading: boolean = false;
  mode: string = 'standard';
  
  modes = [
    { value: 'standard', label: 'Q&A' },
    { value: 'compare', label: 'Compare' },
    { value: 'literature_review', label: 'Review' },
    { value: 'research_gaps', label: 'Gaps' }
  ];

  private shouldScrollToBottom = false;

  constructor(
    private apiService: ApiService,
    private stateService: StateService,
    private router: Router
  ) {}

  ngOnInit() {
    this.loadCollections();
    
    const currentCollection = this.stateService.getCurrentCollection();
    if (currentCollection) {
      this.selectedCollection = currentCollection;
    }

    this.stateService.currentTopic$.subscribe(topic => {
      this.currentTopic = topic;
    });
  }

  ngAfterViewChecked() {
    if (this.shouldScrollToBottom) {
      this.scrollToBottom();
      this.shouldScrollToBottom = false;
    }
  }

  loadCollections() {
    this.apiService.listCollections().subscribe({
      next: (response) => {
        if (response.success) {
          this.collections = response.collections;
        }
      },
      error: (err) => {
        console.error('Error loading collections:', err);
      }
    });
  }

  selectCollection(collection: string) {
    this.selectedCollection = collection;
    this.stateService.setCurrentCollection(collection);
    this.messages = [];
  }

  onAsk() {
    if (!this.question.trim() || !this.selectedCollection || this.loading) {
      return;
    }

    const userMessage: Message = {
      type: 'user',
      text: this.question
    };
    this.messages.push(userMessage);
    this.shouldScrollToBottom = true;

    const request: QueryRequest = {
      collection_name: this.selectedCollection,
      question: this.question,
      n_results: 5,
      mode: this.mode,
      provider: 'gemini'
    };

    const currentQuestion = this.question;
    this.question = '';
    this.loading = true;

    this.apiService.queryPapers(request).subscribe({
      next: (response) => {
        this.loading = false;
        if (response.success) {
          const aiMessage: Message = {
            type: 'ai',
            text: response.answer,
            sources: response.sources
          };
          this.messages.push(aiMessage);
          this.shouldScrollToBottom = true;

          this.saveToHistory(currentQuestion, response.answer);
        } else {
          const errorMessage: Message = {
            type: 'ai',
            text: 'Sorry, I could not find an answer. Please try rephrasing your question.'
          };
          this.messages.push(errorMessage);
          this.shouldScrollToBottom = true;
        }
      },
      error: (err) => {
        this.loading = false;
        const errorMessage: Message = {
          type: 'ai',
          text: 'An error occurred while processing your question. Please try again.'
        };
        this.messages.push(errorMessage);
        this.shouldScrollToBottom = true;
        console.error('Query error:', err);
      }
    });
  }

  saveToHistory(question: string, answer: string) {
    this.apiService.saveHistory({
      collection_name: this.selectedCollection,
      question: question,
      answer: answer,
      mode: this.mode
    }).subscribe({
      error: (err) => console.error('Error saving history:', err)
    });
  }

  scrollToBottom() {
    try {
      this.messagesContainer.nativeElement.scrollTop = 
        this.messagesContainer.nativeElement.scrollHeight;
    } catch (err) {
      console.error('Scroll error:', err);
    }
  }

  navigateToSearch() {
    this.router.navigate(['/search']);
  }
}
